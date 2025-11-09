#!/usr/bin/env python3
"""
Database migration: Unify session fields after removing Claude Code SDK
- Remove active_claude_session_id column
- Rename active_agent_session_id to active_session_id
- Migrate 'claude' cli_type values to 'agent'
"""
import sqlite3
import sys
from pathlib import Path

def migrate():
    # Get database path
    db_path = Path(__file__).parent.parent.parent / "data" / "cc.db"

    if not db_path.exists():
        print(f"❌ Database file not found: {db_path}")
        sys.exit(1)

    print(f"📦 Migrating database: {db_path}")

    try:
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check current columns
        cursor.execute("PRAGMA table_info(projects)")
        columns = {row[1] for row in cursor.fetchall()}

        # Step 1: Create new active_session_id column if it doesn't exist
        if "active_session_id" not in columns:
            print("🔧 Creating new active_session_id column...")
            cursor.execute("""
                ALTER TABLE projects
                ADD COLUMN active_session_id VARCHAR(128)
            """)

            # Copy data from active_agent_session_id to active_session_id
            if "active_agent_session_id" in columns:
                print("📋 Copying data from active_agent_session_id to active_session_id...")
                cursor.execute("""
                    UPDATE projects
                    SET active_session_id = active_agent_session_id
                    WHERE active_agent_session_id IS NOT NULL
                """)
            # If active_agent_session_id doesn't exist but active_claude_session_id does, use that
            elif "active_claude_session_id" in columns:
                print("📋 Copying data from active_claude_session_id to active_session_id...")
                cursor.execute("""
                    UPDATE projects
                    SET active_session_id = active_claude_session_id
                    WHERE active_claude_session_id IS NOT NULL
                """)
        else:
            print("✅ Column 'active_session_id' already exists")

        # Step 2: Update preferred_cli values from 'claude' to 'agent'
        print("🔧 Updating preferred_cli values from 'claude' to 'agent'...")
        cursor.execute("""
            UPDATE projects
            SET preferred_cli = 'agent'
            WHERE preferred_cli = 'claude'
        """)
        rows_updated = cursor.rowcount
        print(f"   Updated {rows_updated} project(s)")

        # Step 3: Update cli_type in sessions table
        # Check if sessions table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'")
        if cursor.fetchone():
            print("🔧 Updating cli_type in sessions table from 'claude' to 'agent'...")
            cursor.execute("""
                UPDATE sessions
                SET cli_type = 'agent'
                WHERE cli_type = 'claude'
            """)
            rows_updated = cursor.rowcount
            print(f"   Updated {rows_updated} session(s)")

        # Step 4: Update cli_source in messages table
        # Check if messages table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        if cursor.fetchone():
            print("🔧 Updating cli_source in messages table from 'claude' to 'agent'...")
            cursor.execute("""
                UPDATE messages
                SET cli_source = 'agent'
                WHERE cli_source = 'claude'
            """)
            rows_updated = cursor.rowcount
            print(f"   Updated {rows_updated} message(s)")

        # Note: SQLite doesn't support dropping columns directly
        # The old columns (active_claude_session_id, active_agent_session_id) will remain
        # but won't be used by the application
        print("\n⚠️  Note: SQLite doesn't support dropping columns.")
        print("   Old columns (active_claude_session_id, active_agent_session_id) remain in the table")
        print("   but are no longer used by the application.")

        conn.commit()
        print("\n✅ Migration completed successfully!")

        # Verify the migration
        cursor.execute("PRAGMA table_info(projects)")
        columns = [row[1] for row in cursor.fetchall()]

        if "active_session_id" in columns:
            print("✅ Verified: Column 'active_session_id' exists in projects table")

            # Check data migration
            cursor.execute("SELECT COUNT(*) FROM projects WHERE active_session_id IS NOT NULL")
            count = cursor.fetchone()[0]
            print(f"   {count} project(s) have active sessions")

            # Check preferred_cli values
            cursor.execute("SELECT COUNT(*) FROM projects WHERE preferred_cli = 'claude'")
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"⚠️  Warning: {count} project(s) still have preferred_cli = 'claude'")
            else:
                print("✅ No projects with preferred_cli = 'claude'")
        else:
            print("❌ Warning: Column verification failed")

        conn.close()

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()