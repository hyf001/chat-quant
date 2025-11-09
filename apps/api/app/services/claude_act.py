"""
System prompt loading utilities for Claude-based agents.

This module provides functions to load and manage system prompts
used by various Claude adapters (claude_agent.py, etc.)
"""
from pathlib import Path

from app.common.types import AgentType
from app.prompt import prompt_util


def find_prompt_file() -> Path:
    """
    Find the system-prompt.md file in app/prompt/ directory.
    """
    current_path = Path(__file__).resolve()

    # Get the app directory (current file is in app/services/)
    app_dir = current_path.parent.parent  # app/
    prompt_file = app_dir / 'prompt' / 'system-prompt.md'

    if prompt_file.exists():
        return prompt_file

    # Fallback: look for system-prompt.md in various locations
    fallback_locations = [
        current_path.parent.parent / 'prompt' / 'system-prompt.md',  # app/prompt/
        current_path.parent.parent.parent.parent / 'docs' / 'system-prompt.md',  # project-root/docs/
        current_path.parent.parent.parent.parent / 'system-prompt.md',  # project-root/
    ]

    for location in fallback_locations:
        if location.exists():
            return location

    # Return expected location even if it doesn't exist
    return prompt_file


def load_system_prompt(force_reload: bool = False,agent_type:AgentType = AgentType.ANALYIS) -> str:
    """
    Load system prompt from app/prompt/system-prompt.md file.
    Falls back to basic prompt if file not found.

    Args:
        force_reload: If True, ignores cache and reloads from file
    """
    # Simple caching mechanism
    if not force_reload and hasattr(load_system_prompt, '_cached_prompt'):
        return load_system_prompt._cached_prompt

    try:
        prompt_content = prompt_util.getPrompt(agent_type)
        # Cache the loaded prompt
        load_system_prompt._cached_prompt = prompt_content
        return prompt_content

    except Exception as e:
        print(f"❌ Error loading system prompt: {e}")
        import traceback
        traceback.print_exc()

    # Fallback to basic prompt
    fallback_prompt = (
        "You are Claude Code, an advanced AI coding assistant specialized in building modern fullstack web applications.\n"
        "You assist users by chatting with them and making changes to their code in real-time.\n\n"
        "Constraints:\n"
        "- Do not delete files entirely; prefer edits.\n"
        "- Keep changes minimal and focused.\n"
        "- Use UTF-8 encoding.\n"
        "- Follow modern development best practices.\n"
    )

    print(f"🔄 Using fallback system prompt ({len(fallback_prompt)} chars)")
    load_system_prompt._cached_prompt = fallback_prompt
    return fallback_prompt


def get_system_prompt(agent_type: AgentType) -> str:
    """Get the current system prompt (uses cached version)"""
    return load_system_prompt(False,agent_type)


def get_initial_system_prompt(agent_type: AgentType) -> str:
    """Get the initial system prompt for project creation (uses cached version)"""
    return load_system_prompt(False,agent_type)