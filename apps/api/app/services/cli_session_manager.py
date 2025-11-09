"""
CLI Session Manager for Multi-CLI Support
Handles session persistence and continuity across different CLI agents
"""
from typing import Dict, Optional, Any
from sqlalchemy.orm import Session
from app.models.projects import Project
from apps.api.app.common.types import AgentType


class CLISessionManager:
    """Manages CLI sessions across different AI agents"""

    def __init__(self, db: Session):
        self.db = db
        self._session_cache: Dict[str, str] = {}  # project_id -> session_id

    def get_session_id(self, project_id: str, cli_type: AgentType = None) -> Optional[str]:
        """Get existing session ID for a project

        Note: cli_type parameter is kept for backward compatibility but ignored
        since we now have a unified session field.
        """
        # Check cache first
        if project_id in self._session_cache:
            return self._session_cache[project_id]

        # Get from database
        project = self.db.get(Project, project_id)
        if not project:
            return None

        session_id = project.active_session_id

        # Update cache
        if session_id:
            self._session_cache[project_id] = session_id

        return session_id
    
    def set_session_id(self, project_id: str, cli_type: AgentType, session_id: str) -> bool:
        """Set session ID for a project

        Note: cli_type parameter is kept for backward compatibility but ignored
        since we now have a unified session field.
        """
        project = self.db.get(Project, project_id)
        if not project:
            return False

        # Update project record with unified session field
        project.active_session_id = session_id

        self.db.commit()

        # Update cache
        self._session_cache[project_id] = session_id

        from app.core.terminal_ui import ui
        ui.success(f"Set session ID for project {project_id}: {session_id}", "Session")
        return True
    
    def get_all_sessions(self, project_id: str) -> Dict[str, Optional[str]]:
        """Get all CLI session IDs for a project"""
        project = self.db.get(Project, project_id)
        if not project:
            return {}

        return {
            "agent": project.active_session_id,
        }
    
    def clear_session_id(self, project_id: str, cli_type: AgentType) -> bool:
        """Clear session ID for a project and CLI type"""
        return self.set_session_id(project_id, cli_type, None)
    
    def clear_all_sessions(self, project_id: str) -> bool:
        """Clear all CLI session IDs for a project"""
        project = self.db.get(Project, project_id)
        if not project:
            return False

        project.active_session_id = None

        self.db.commit()

        # Clear cache
        if project_id in self._session_cache:
            del self._session_cache[project_id]

        from app.core.terminal_ui import ui
        ui.info(f"Cleared all CLI sessions for project {project_id}", "Session")
        return True
    
    def get_session_stats(self, project_id: str) -> Dict[str, Any]:
        """Get session statistics for a project"""
        from app.models.sessions import Session as ChatSession
        from sqlalchemy import func
        
        # Get session counts by CLI type
        session_stats = self.db.query(
            ChatSession.cli_type,
            func.count(ChatSession.id).label('count'),
            func.avg(ChatSession.duration_ms).label('avg_duration_ms'),
            func.sum(ChatSession.total_messages).label('total_messages'),
            func.max(ChatSession.started_at).label('last_used')
        ).filter(
            ChatSession.project_id == project_id
        ).group_by(ChatSession.cli_type).all()
        
        stats = {}
        for stat in session_stats:
            stats[stat.cli_type] = {
                "session_count": stat.count,
                "avg_duration_ms": int(stat.avg_duration_ms) if stat.avg_duration_ms else 0,
                "total_messages": stat.total_messages or 0,
                "last_used": stat.last_used.isoformat() if stat.last_used else None,
                "active_session_id": self.get_session_id(project_id, AgentType(stat.cli_type))
            }
        
        return stats
    
    def get_preferred_cli(self, project_id: str) -> Optional[AgentType]:
        """Get preferred CLI for a project"""
        project = self.db.get(Project, project_id)
        if not project:
            return None

        try:
            return AgentType(project.preferred_cli)
        except ValueError:
            return AgentType.NEXT_JS  # Default fallback
    
    def set_preferred_cli(self, project_id: str, cli_type: AgentType, fallback_enabled: bool = True) -> bool:
        """Set preferred CLI for a project"""
        project = self.db.get(Project, project_id)
        if not project:
            return False
        
        project.preferred_cli = cli_type.value
        project.fallback_enabled = fallback_enabled
        self.db.commit()
        
        print(f"✅ [Session] Set preferred CLI for project {project_id}: {cli_type.value} (fallback: {fallback_enabled})")
        return True
    
    def is_fallback_enabled(self, project_id: str) -> bool:
        """Check if fallback is enabled for a project"""
        project = self.db.get(Project, project_id)
        if not project:
            return True  # Default to enabled
        
        return project.fallback_enabled
    
    
    def cleanup_stale_sessions(self, project_id: str, days_threshold: int = 30) -> int:
        """Clean up old/stale CLI session IDs"""
        from datetime import datetime, timedelta
        from app.models.sessions import Session as ChatSession
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_threshold)
        
        # Find sessions that haven't been used recently
        stale_sessions = self.db.query(ChatSession).filter(
            ChatSession.project_id == project_id,
            ChatSession.started_at < cutoff_date,
            ChatSession.status.in_(["completed", "failed"])
        ).all()
        
        # Clear session IDs for stale sessions
        cleared_count = 0
        for session in stale_sessions:
            if session.cli_type:
                try:
                    cli_type = AgentType(session.cli_type)
                    current_session_id = self.get_session_id(project_id, cli_type)
                    
                    # Only clear if it matches the stale session's claude_session_id
                    if current_session_id == session.claude_session_id:
                        self.clear_session_id(project_id, cli_type)
                        cleared_count += 1
                        
                except ValueError:
                    continue
        
        from app.core.terminal_ui import ui
        ui.info(f"Project {project_id}: Cleared {cleared_count} stale session IDs", "Cleanup")
        return cleared_count
