"""
Project Initializer Service
Handles project initialization, scaffolding, and setup
"""
import os
import json
import shutil
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.common.types import AgentType
from app.services.filesystem import (
    ensure_dir,
    scaffold_nextjs_minimal,
    scaffold_analysis_workspace,
    copy_export_cache_to_project,
    copy_fin_analysis_cache_to_project,
    init_git_repo,
    write_env_file
)


async def initialize_nextjs_project(project_id: str, name: str, project_path: str) -> None:
    """
    Initialize a Next.js project

    Args:
        project_id: Project identifier
        name: Project name
        project_path: Path to the project repo directory
    """
    # Scaffold NextJS project using create-next-app (includes automatic git init)
    scaffold_nextjs_minimal(project_path)

    # CRITICAL: Force create independent git repository for each project
    # create-next-app inherits parent .git when run inside existing repo
    # This ensures each project has its own isolated git history
    # init_git_repo(project_path)

    # Create initial .env file
    env_content = f"NEXT_PUBLIC_PROJECT_ID={project_id}\nNEXT_PUBLIC_PROJECT_NAME={name}\n"
    write_env_file(project_path, env_content)

    # Create metadata directory and initial metadata file
    create_project_metadata(project_id, name)

    # Setup Claude Code configuration
    setup_claude_config(project_path)


async def initialize_analysis_project(project_id: str, name: str) -> None:
    """
    Initialize a data analysis project

    Args:
        project_id: Project identifier
        name: Project name
    """
    from app.core.terminal_ui import ui

    # Determine project path
    project_path = os.path.join(settings.projects_root, project_id)

    # Create minimal repo structure (only .claude and .env)
    scaffold_analysis_workspace(project_path)

    # Define template source path
    project_template_path = os.path.join(settings.claudable_project_root, "project_template")

    # Recursively copy template directory to project path
    if os.path.exists(project_template_path) and os.path.isdir(project_template_path):
        ui.info(f"Copying project template from {project_template_path} to {project_path}...", "Analysis Init") 
        try:
            # Use shutil.copytree to recursively copy the entire template directory
            shutil.copytree(project_template_path, project_path, dirs_exist_ok=True)
            ui.success(f"Template files copied successfully to {project_path}", "Analysis Init")
        except Exception as e:
            ui.error(f"Failed to copy template files: {e}", "Analysis Init")
            raise
    else:
        ui.warning(f"Template directory not found at {project_template_path}", "Analysis Init")
        raise Exception(f"Template directory not found at {project_template_path}")

    ui.success(f"Analysis project initialized at {project_path}", "Analysis Init")


async def initialize_project(
    project_id: str,
    name: str,
    agent_type: Optional[str] = None
) -> str:
    """
    Initialize a new project with directory structure and scaffolding

    Args:
        project_id: Unique project identifier
        name: Human-readable project name
        agent_type: Agent type string (e.g., "next-js", "analysis"). Defaults to NEXT_JS if not provided.

    Returns:
        str: Path to the created project directory
    """

    # Parse agent type, default to NEXT_JS if not provided or invalid
    parsed_agent_type = AgentType.NEXT_JS
    if agent_type:
        try:
            parsed_agent_type = AgentType(agent_type)
        except ValueError:
            # Invalid agent type, use default
            from app.core.terminal_ui import ui
            ui.warning(f"Invalid agent type '{agent_type}', using default NEXT_JS", "Initializer")

    # Create project directory
    if parsed_agent_type == AgentType.NEXT_JS:
        project_path = os.path.join(settings.projects_root, project_id, "repo")
    else:
        project_path = os.path.join(settings.projects_root, project_id)
    ensure_dir(project_path)

    # Create assets directory
    assets_path = os.path.join(settings.projects_root, project_id, "assets")
    ensure_dir(assets_path)

    try:
        # Branch based on agent type
        if parsed_agent_type == AgentType.ANALYIS:
            # Initialize data analysis project
            await initialize_analysis_project(project_id, name)
        else:
            # Initialize Next.js project (default)
            await initialize_nextjs_project(project_id, name, project_path)

        return project_path

    except Exception as e:
        # Clean up failed project directory
        import shutil
        project_root = os.path.join(settings.projects_root, project_id)
        if os.path.exists(project_root):
            shutil.rmtree(project_root)

        # Re-raise with user-friendly message
        raise Exception(f"Failed to initialize project: {str(e)}")


async def cleanup_project(project_id: str) -> bool:
    """
    Clean up project files and directories. Be robust against running preview
    processes, transient filesystem locks, and read-only files.

    Args:
        project_id: Project identifier to clean up

    Returns:
        bool: True if cleanup was successful
    """

    project_root = os.path.join(settings.projects_root, project_id)

    # Nothing to do
    if not os.path.exists(project_root):
        return False

    # 1) Ensure any running preview processes for this project are terminated
    try:
        from app.services.local_runtime import cleanup_project_resources
        cleanup_project_resources(project_id)
    except Exception as e:
        # Do not fail cleanup because of process stop errors
        print(f"[cleanup] Warning: failed stopping preview process for {project_id}: {e}")

    # 2) Robust recursive deletion with retries
    import time
    import errno
    import stat
    import shutil

    def _onerror(func, path, exc_info):
        # Try to chmod and retry if permission error
        try:
            if not os.path.exists(path):
                return
            os.chmod(path, stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)
            func(path)
        except Exception:
            pass

    attempts = 0
    max_attempts = 5
    last_err = None
    while attempts < max_attempts:
        try:
            shutil.rmtree(project_root, onerror=_onerror)
            return True
        except OSError as e:
            last_err = e
            # On macOS, ENOTEMPTY (66) or EBUSY can happen if watchers are active
            if e.errno in (errno.ENOTEMPTY, errno.EBUSY, 66):
                time.sleep(0.25 * (attempts + 1))
                attempts += 1
                continue
            else:
                print(f"Error cleaning up project {project_id}: {e}")
                return False
        except Exception as e:
            last_err = e
            print(f"Error cleaning up project {project_id}: {e}")
            return False

    # Final attempt to handle lingering dotfiles
    try:
        # Remove remaining leaf entries then rmdir tree if any
        for root, dirs, files in os.walk(project_root, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception:
                    pass
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception:
                    pass
        os.rmdir(project_root)
        return True
    except Exception as e:
        print(f"Error cleaning up project {project_id}: {e if e else last_err}")
        return False


async def get_project_path(project_id: str) -> Optional[str]:
    """
    Get the filesystem path for a project
    
    Args:
        project_id: Project identifier
    
    Returns:
        Optional[str]: Path to project directory if it exists
    """
    
    project_path = os.path.join(settings.projects_root, project_id, "repo")
    
    if os.path.exists(project_path):
        return project_path
    
    return None


async def project_exists(project_id: str) -> bool:
    """
    Check if a project exists on the filesystem
    
    Args:
        project_id: Project identifier
    
    Returns:
        bool: True if project exists
    """
    
    project_path = os.path.join(settings.projects_root, project_id)
    return os.path.exists(project_path)


def create_project_metadata(project_id: str, name: str):
    """
    Create initial metadata file with placeholder content
    This will be filled by CLI Agent based on the user's initial prompt
    
    Args:
        project_id: Project identifier
        name: Project name
    """
    
    # Create data directory structure
    data_dir = os.path.join(settings.projects_root, project_id, "data")
    metadata_dir = os.path.join(data_dir, "metadata")
    ensure_dir(metadata_dir)
    
    metadata_data = {
        "name": name,
        "description": "Project created with AI assistance"
    }
    
    metadata_path = os.path.join(metadata_dir, f"{project_id}.json")
    
    try:
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_data, f, indent=2, ensure_ascii=False)
        from app.core.terminal_ui import ui
        ui.success(f"Created initial metadata at {metadata_path}", "Project")
    except Exception as e:
        ui.error(f"Failed to create metadata: {e}", "Project")
        raise







def setup_claude_config(project_path: str):
    """
    Setup Claude Code configuration for the project

    Args:
        project_path: Path to the project repository directory
    """
    try:
        from app.core.terminal_ui import ui

        # Create .claude directory structure
        claude_dir = os.path.join(project_path, ".claude")
        claude_hooks_dir = os.path.join(claude_dir, "hooks")
        claude_skills_dir = os.path.join(claude_dir, "skills")
        ensure_dir(claude_dir)
        ensure_dir(claude_hooks_dir)
        ensure_dir(claude_skills_dir)

        # Get paths to source files in project root
        # Current file: apps/api/app/services/project/initializer.py
        # Go up to project root: ../../../../..
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_file_dir, "..", "..", "..", "..", "..")
        project_root = os.path.abspath(project_root)
        scripts_dir = os.path.join(project_root, "scripts")
        settings_src = os.path.join(scripts_dir, "settings.json")
        type_check_src = os.path.join(scripts_dir, "type_check.sh")
        skills_src_dir = os.path.join(project_root, ".claude", "skills")

        # Copy settings.json
        settings_dst = os.path.join(claude_dir, "settings.json")
        if os.path.exists(settings_src):
            shutil.copy2(settings_src, settings_dst)
            ui.success(f"Copied settings.json to {settings_dst}", "Claude Config")
        else:
            ui.warning(f"Source file not found: {settings_src}", "Claude Config")

        # Copy type_check.sh
        type_check_dst = os.path.join(claude_hooks_dir, "type_check.sh")
        if os.path.exists(type_check_src):
            shutil.copy2(type_check_src, type_check_dst)
            # Make the script executable
            os.chmod(type_check_dst, 0o755)
            ui.success(f"Copied type_check.sh to {type_check_dst}", "Claude Config")
        else:
            ui.warning(f"Source file not found: {type_check_src}", "Claude Config")

        # Copy .claude/skills directory
        if os.path.exists(skills_src_dir) and os.path.isdir(skills_src_dir):
            # Copy all files from skills source directory to skills destination
            copied_count = 0
            for item in os.listdir(skills_src_dir):
                src_item = os.path.join(skills_src_dir, item)
                dst_item = os.path.join(claude_skills_dir, item)

                if os.path.isfile(src_item):
                    shutil.copy2(src_item, dst_item)
                    copied_count += 1
                elif os.path.isdir(src_item):
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
                    copied_count += 1

            if copied_count > 0:
                ui.success(f"Copied {copied_count} items from skills directory to {claude_skills_dir}", "Claude Config")
            else:
                ui.info("Skills directory is empty, no files copied", "Claude Config")
        else:
            ui.warning(f"Skills source directory not found: {skills_src_dir}", "Claude Config")

        ui.success("Claude Code configuration setup complete", "Claude Config")

    except Exception as e:
        ui.error(f"Failed to setup Claude configuration: {e}", "Claude Config")
        # Don't fail the whole project creation for this
        pass
