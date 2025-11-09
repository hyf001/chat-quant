#!/usr/bin/env python3
"""
Database migration: Add active_agent_session_id column to projects table
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

        # Check if column already exists
        cursor.execute("PRAGMA table_info(projects)")
        columns = [row[1] for row in cursor.fetchall()]

        if "active_agent_session_id" in columns:
            print("✅ Column 'active_agent_session_id' already exists. No migration needed.")
            conn.close()
            return

        # Add the new column
        print("🔧 Adding column 'active_agent_session_id' to projects table...")
        cursor.execute("""
            ALTER TABLE projects
            ADD COLUMN active_agent_session_id VARCHAR(128)
        """)

        conn.commit()
        print("✅ Migration completed successfully!")

        # Verify the column was added
        cursor.execute("PRAGMA table_info(projects)")
        columns = [row[1] for row in cursor.fetchall()]

        if "active_agent_session_id" in columns:
            print("✅ Verified: Column 'active_agent_session_id' exists in projects table")
        else:
            print("❌ Warning: Column verification failed")

        conn.close()

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
