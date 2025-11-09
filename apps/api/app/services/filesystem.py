import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def init_git_repo(repo_path: str) -> None:
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)


def scaffold_nextjs_minimal(repo_path: str) -> None:
    """Create Next.js project using official create-next-app"""
    import subprocess
    import tempfile
    import shutil
    
    # Get parent directory to create project in
    parent_dir = Path(repo_path).parent
    project_name = Path(repo_path).name
    
    try:
        # Create Next.js app with TypeScript and Tailwind CSS
        cmd = [
            "npx", 
            "create-next-app@latest", 
            project_name,
            "--typescript",
            "--tailwind", 
            "--eslint",
            "--app",
            "--import-alias", "@/*",
            "--use-npm",
            "--skip-install",  # We'll install dependencies later (handled by backend)
            "--yes"            # Auto-accept all prompts
        ]
        
        # Set environment for non-interactive mode
        env = os.environ.copy()
        env["CI"] = "true"  # Force non-interactive mode
        
        from app.core.terminal_ui import ui
        ui.info(f"Running create-next-app with command: {' '.join(cmd)}", "Filesystem")
        
        # Run create-next-app in the parent directory with timeout
        result = subprocess.run(
            cmd, 
            cwd=parent_dir, 
            check=True, 
            capture_output=True, 
            text=True,
            env=env,
            timeout=300  # 5 minute timeout
        )
        
        ui.success(f"Created Next.js app: {result.stdout}", "Filesystem")
        
        # Skip npm install for faster project creation
        # Users can run 'npm install' manually when needed
        ui.info("Skipped dependency installation for faster setup", "Filesystem")
        
    except subprocess.TimeoutExpired as e:
        ui.error("create-next-app timed out after 5 minutes", "Filesystem")
        raise Exception(f"Project creation timed out. This might be due to slow network or hung process.")
    except subprocess.CalledProcessError as e:
        ui.error(f"Error creating Next.js app: {e}", "Filesystem")
        ui.debug(f"Command: {' '.join(cmd)}", "Filesystem")
        ui.debug(f"stdout: {e.stdout}", "Filesystem")
        ui.debug(f"stderr: {e.stderr}", "Filesystem")
        
        # Provide more specific error messages
        if "EACCES" in str(e.stderr):
            error_msg = "Permission denied. Please check directory permissions."
        elif "ENOENT" in str(e.stderr):
            error_msg = "Command not found. Please ensure Node.js and npm are installed."
        elif "network" in str(e.stderr).lower():
            error_msg = "Network error. Please check your internet connection."
        else:
            error_msg = f"Failed to create Next.js project: {e.stderr or e.stdout or str(e)}"
        
        raise Exception(error_msg)


def write_env_file(project_dir: str, content: str) -> None:
    (Path(project_dir) / ".env").write_text(content)


def scaffold_analysis_workspace(repo_path: str) -> None:
    """Create analysis workspace structure for data analysis projects"""
    from app.core.terminal_ui import ui

    try:
        repo_dir = Path(repo_path)

        # Create only .claude directory and .env file in repo/
        claude_dir = repo_dir / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)

        # Create .env file
        env_file = repo_dir / ".env"
        env_file.write_text("# Analysis project environment variables\n")

        ui.success(f"Created minimal repo structure at {repo_path}", "Filesystem")

    except Exception as e:
        ui.error(f"Error creating analysis workspace: {e}", "Filesystem")
        raise Exception(f"Failed to create analysis workspace: {str(e)}")


def copy_export_cache_to_project(source_cache_dir: str, target_repo_dir: str) -> None:
    """
    Copy exported cache data to project repository

    Note: The cache data may be obtained from various sources (MCP services,
    HTTPS APIs, etc.), but this function is source-agnostic and simply copies
    the exported cache to the project.

    Args:
        source_cache_dir: Source export cache directory (e.g., {EXPORT_CACHE_ROOT}/data_analysis)
        target_repo_dir: Target project repository directory (e.g., {project_id}/repo)

    Raises:
        Exception: If copy operation fails
    """
    from app.core.terminal_ui import ui
    import shutil

    try:
        source_path = Path(source_cache_dir)
        target_path = Path(target_repo_dir)

        # Check if source directory exists
        if not source_path.exists():
            ui.warning(f"Export cache directory not found: {source_cache_dir}", "Filesystem")
            ui.info("Skipping cache copy - project will start with empty cache", "Filesystem")
            return

        # Check if source directory is empty
        subdirs = [d for d in source_path.iterdir() if d.is_dir()]
        if not subdirs:
            ui.info(f"Export cache directory is empty: {source_cache_dir}", "Filesystem")
            ui.info("Skipping cache copy - no data to copy", "Filesystem")
            return

        # Copy all subdirectories from source to target
        copied_count = 0
        skipped_count = 0
        for subdir in subdirs:
            target_subdir = target_path / subdir.name

            # Skip if target already exists
            if target_subdir.exists():
                ui.debug(f"Skipping existing directory: {subdir.name}", "Filesystem")
                skipped_count += 1
                continue

            # Copy directory with filtering (exclude temporary directories)
            def ignore_temp_dirs(directory, contents):
                """Ignore function for shutil.copytree to skip temporary directories"""
                ignored = []
                for name in contents:
                    full_path = Path(directory) / name
                    # Skip directories ending with _temp (e.g., data_table_temp, bi_report_temp)
                    if full_path.is_dir() and name.endswith('_temp'):
                        ignored.append(name)
                        ui.debug(f"Skipping temporary directory during copy: {name}", "Filesystem")
                return ignored

            shutil.copytree(subdir, target_subdir, ignore=ignore_temp_dirs)
            copied_count += 1
            ui.debug(f"Copied cache directory: {subdir.name}", "Filesystem")

        if copied_count > 0:
            ui.success(
                f"Copied {copied_count} cache directories from {source_cache_dir} to {target_repo_dir}",
                "Filesystem"
            )
        else:
            ui.info("No new cache directories to copy", "Filesystem")

    except Exception as e:
        ui.error(f"Error copying export cache: {e}", "Filesystem")
        raise Exception(f"Failed to copy export cache: {str(e)}")


def copy_fin_cache_to_project(source_cache_dir: str, target_base_dir: str) -> None:
    """
    Copy financial view table cache to project repository with special structure

    This function copies fin_data_analysis cache directories to a specialized structure:
    Source: data/projects/cache/fin_data_analysis/{domain}/*.yaml
    Target: data/projects/{project_id}/repo/fin/view_table/{domain}/*.yaml

    Args:
        source_cache_dir: Source fin_data_analysis cache directory
        target_base_dir: Target base directory (e.g., {project_id}/repo/fin/view_table)

    Raises:
        Exception: If copy operation fails
    """
    from app.core.terminal_ui import ui
    import shutil

    try:
        source_path = Path(source_cache_dir)
        target_base_path = Path(target_base_dir)

        # Check if source directory exists
        if not source_path.exists():
            ui.debug(f"Financial view cache directory not found: {source_cache_dir}", "Filesystem")
            return

        # Get all domain subdirectories (stock, fund, macro, etc.)
        domain_dirs = [d for d in source_path.iterdir() if d.is_dir() and not d.name.endswith('_temp')]

        if not domain_dirs:
            ui.debug(f"Financial view cache directory is empty: {source_cache_dir}", "Filesystem")
            return

        # Copy each domain directory to target structure
        copied_count = 0
        skipped_count = 0

        for domain_dir in domain_dirs:
            # Skip temporary directories
            if domain_dir.name.endswith('_temp'):
                continue

            # Target path: fin/view_table/{domain}/
            target_domain_dir = target_base_path / domain_dir.name

            # Skip if target already exists
            if target_domain_dir.exists():
                ui.debug(f"Skipping existing financial view domain: {domain_dir.name}", "Filesystem")
                skipped_count += 1
                continue

            # Create parent directories if needed
            target_domain_dir.parent.mkdir(parents=True, exist_ok=True)

            # Copy domain directory (all yaml files)
            shutil.copytree(domain_dir, target_domain_dir)
            copied_count += 1
            ui.debug(f"Copied financial view domain: {domain_dir.name}", "Filesystem")

        if copied_count > 0:
            ui.success(
                f"Copied {copied_count} financial view domains to {target_base_dir}",
                "Filesystem"
            )
        else:
            ui.debug("No new financial view domains to copy", "Filesystem")

    except Exception as e:
        ui.error(f"Error copying financial view cache: {e}", "Filesystem")
        raise Exception(f"Failed to copy financial view cache: {str(e)}")


def copy_fin_analysis_cache_to_project(source_cache_dir: str, target_repo_dir: str) -> None:
    """
    Copy financial analysis cache directly to project repository without additional nesting

    This function copies fin_data_analysis cache directories directly to repo root:
    Source: data/projects/cache/fin_data_analysis/{domain}/*.yaml
    Target: data/projects/{project_id}/repo/{domain}/*.yaml (e.g., repo/stock/, repo/fund/, repo/usstock/)

    Args:
        source_cache_dir: Source fin_data_analysis cache directory
        target_repo_dir: Target project repository directory (e.g., {project_id}/repo)

    Raises:
        Exception: If copy operation fails
    """
    from app.core.terminal_ui import ui
    import shutil

    try:
        source_path = Path(source_cache_dir)
        target_path = Path(target_repo_dir)

        # Check if source directory exists
        if not source_path.exists():
            ui.warning(f"Financial analysis cache directory not found: {source_cache_dir}", "Filesystem")
            ui.info("Skipping cache copy - project will start with empty cache", "Filesystem")
            return

        # Get all domain subdirectories (stock, fund, usstock, etc.)
        domain_dirs = [d for d in source_path.iterdir() if d.is_dir() and not d.name.endswith('_temp')]

        if not domain_dirs:
            ui.info(f"Financial analysis cache directory is empty: {source_cache_dir}", "Filesystem")
            ui.info("Skipping cache copy - no data to copy", "Filesystem")
            return

        # Copy each domain directory directly to target repo
        copied_count = 0
        skipped_count = 0

        for domain_dir in domain_dirs:
            # Skip temporary directories
            if domain_dir.name.endswith('_temp'):
                ui.debug(f"Skipping temporary directory: {domain_dir.name}", "Filesystem")
                continue

            # Target path: repo/{domain}/ (no additional nesting)
            target_domain_dir = target_path / domain_dir.name

            # Skip if target already exists
            if target_domain_dir.exists():
                ui.debug(f"Skipping existing domain directory: {domain_dir.name}", "Filesystem")
                skipped_count += 1
                continue

            # Copy domain directory with filtering (exclude temporary subdirectories)
            def ignore_temp_dirs(directory, contents):
                """Ignore function for shutil.copytree to skip temporary directories"""
                ignored = []
                for name in contents:
                    full_path = Path(directory) / name
                    # Skip directories ending with _temp
                    if full_path.is_dir() and name.endswith('_temp'):
                        ignored.append(name)
                        ui.debug(f"Skipping temporary subdirectory during copy: {name}", "Filesystem")
                return ignored

            shutil.copytree(domain_dir, target_domain_dir, ignore=ignore_temp_dirs)
            copied_count += 1
            ui.debug(f"Copied financial analysis domain: {domain_dir.name}", "Filesystem")

        if copied_count > 0:
            ui.success(
                f"Copied {copied_count} financial analysis domains from {source_cache_dir} to {target_repo_dir}",
                "Filesystem"
            )
        else:
            ui.info("No new financial analysis domains to copy", "Filesystem")

    except Exception as e:
        ui.error(f"Error copying financial analysis cache: {e}", "Filesystem")
        raise Exception(f"Failed to copy financial analysis cache: {str(e)}")
