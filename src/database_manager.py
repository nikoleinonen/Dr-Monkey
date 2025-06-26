from datetime import datetime, timedelta, timezone
import sqlite3
import os
import logging
from src.logging_config import get_logger

logger = get_logger("DB_Manager")

# This will be set by main.py
_internal_db_file_path: str | None = None

def configure_database_path(path: str):
    """Sets the database file path for the module to use."""
    global _internal_db_file_path
    _internal_db_file_path = path
    logger.info(f"Database path has been configured internally to: {_internal_db_file_path}")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    if _internal_db_file_path is None:
        logger.critical("Database path not configured. Call configure_database_path() first.")
        return None
    try:
        conn = sqlite3.connect(_internal_db_file_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error for path '{_internal_db_file_path}': {e}", exc_info=True)
        return None

def begin_transaction(conn: sqlite3.Connection):
    """Begins a new database transaction."""
    try:
        conn.execute("BEGIN TRANSACTION")
        logger.debug("Transaction started.")
    except sqlite3.Error as e:
        logger.error(f"Error beginning transaction: {e}", exc_info=True)
        raise # Re-raise to ensure calling code handles it

def commit_transaction(conn: sqlite3.Connection):
    """Commits the current database transaction."""
    try:
        conn.commit()
        logger.debug("Transaction committed.")
    except sqlite3.Error as e:
        logger.error(f"Error committing transaction: {e}", exc_info=True)
        raise # Re-raise

def rollback_transaction(conn: sqlite3.Connection):
    """Rolls back the current database transaction."""
    try:
        conn.rollback()
        logger.debug("Transaction rolled back.")
    except sqlite3.Error as e:
        logger.error(f"Error rolling back transaction: {e}", exc_info=True)
        # No re-raise here, as rollback is often a last resort in error handling

def initialize_database():
    """Creates the necessary tables if they don't exist."""
    if _internal_db_file_path is None:
        logger.critical("Database path not configured for initialization. Call configure_database_path() first.")
        return

    if _internal_db_file_path:
        db_dir = os.path.dirname(_internal_db_file_path)
        if db_dir: 
            logger.info(f"Ensuring database directory exists for configured path: {db_dir}")
            os.makedirs(db_dir, exist_ok=True)

    conn = get_db_connection()
    if conn is None:
        logger.critical("Failed to get database connection for initialization.")
        return

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                username TEXT,
                last_iq_score INTEGER DEFAULT NULL,
                last_monkey_percentage INTEGER DEFAULT NULL,
                analysis_tests_taken INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)

        cursor.execute("PRAGMA table_info(user_profiles)")
        columns = [column['name'] for column in cursor.fetchall()]
        if 'username' not in columns:
            try:
                cursor.execute("ALTER TABLE user_profiles ADD COLUMN username TEXT")
                logger.info("Added 'username' column to 'user_profiles' table.")
            except sqlite3.Error as e:
                logger.error(f"Failed to add 'username' column: {e}", exc_info=True)

        if 'last_iq_score' not in columns:
            try:
                cursor.execute("ALTER TABLE user_profiles ADD COLUMN last_iq_score INTEGER DEFAULT NULL")
                logger.info("Added 'last_iq_score' column to 'user_profiles' table.")
            except sqlite3.Error as e:
                logger.error(f"Failed to add 'last_iq_score' column: {e}", exc_info=True)
        if 'last_monkey_percentage' not in columns:
            try:
                cursor.execute("ALTER TABLE user_profiles ADD COLUMN last_monkey_percentage INTEGER DEFAULT NULL")
                logger.info("Added 'last_monkey_percentage' column to 'user_profiles' table.")
            except sqlite3.Error as e:
                logger.error(f"Failed to add 'last_monkey_percentage' column: {e}", exc_info=True)
        if 'analysis_tests_taken' not in columns:
            try:
                cursor.execute("ALTER TABLE user_profiles ADD COLUMN analysis_tests_taken INTEGER NOT NULL DEFAULT 0")
                logger.info("Added 'analysis_tests_taken' column to 'user_profiles' table.")
            except sqlite3.Error as e:
                logger.error(f"Failed to add 'analysis_tests_taken' column: {e}", exc_info=True)

        # New table to store historical analysis results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                iq_score INTEGER NOT NULL,
                monkey_percentage INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id, guild_id) REFERENCES user_profiles(user_id, guild_id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_analysis_history_user_guild ON user_analysis_history (user_id, guild_id)")

        logger.info("Checked/created 'user_profiles' table.")
        logger.info("Checked/created 'user_analysis_history' table and index.")

        conn.commit()
        logger.info("Database tables checked/created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()

def ensure_user_exists(user_id: int, guild_id: int, username: str | None = None):
    """
    Ensures a user profile and related stats rows (gambling) exist for a given user and guild.
    Inserts new records with default values if they are not present.
    If a username is provided, it updates the username in the user_profiles table.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    
    current_username = username if username is not None else "UnknownUser"

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO user_profiles (user_id, guild_id, username, last_iq_score, last_monkey_percentage, analysis_tests_taken) 
            VALUES (?, ?, ?, NULL, NULL, 0)
        """, (user_id, guild_id, current_username)) 

        if username is not None: 
            cursor.execute("""
                UPDATE user_profiles 
                SET username = ?
                WHERE user_id = ? AND guild_id = ?
            """, (username, user_id, guild_id))
        conn.commit()
        return True

    except sqlite3.Error as e:
        logger.error(f"Error ensuring user profile exists for user {user_id} in guild {guild_id}: {e}", exc_info=True)
        return False 
    finally:
        if conn:
            conn.close()


def ensure_user_exists_and_get_profile(user_id: int, guild_id: int, username: str | None = None) -> sqlite3.Row | None:
    """
    Ensures a user profile and related stats rows exist, then retrieves the user's profile.
    """
    if not ensure_user_exists(user_id, guild_id, username):
        logger.error(f"ensure_user_exists_and_get_profile: Failed during ensure_user_exists for user {user_id}, guild {guild_id}.")
        return None
    
    profile = get_user_profile(user_id, guild_id)
    if profile is None:
        logger.warning(f"ensure_user_exists_and_get_profile: Profile not found for user {user_id}, guild {guild_id} after ensure_user_exists call.")
    return profile


# --- Analysis (IQ & Monkey) Stats Functions ---
def record_analysis_result(user_id: int, guild_id: int, iq_score: int, monkey_percentage: int, username: str) -> bool:
    """
    Records an analysis result (IQ and Monkey %) for a user.
    Stores it in history and updates their latest scores in the profile.
    """
    if not ensure_user_exists(user_id, guild_id, username):
        return False
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')

        # Insert into history table
        cursor.execute("""
            INSERT INTO user_analysis_history (user_id, guild_id, iq_score, monkey_percentage, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, guild_id, iq_score, monkey_percentage, timestamp))

        # Update user_profiles with last scores and increment tests_taken
        cursor.execute("""
            UPDATE user_profiles
            SET last_iq_score = ?,
                last_monkey_percentage = ?,
                analysis_tests_taken = analysis_tests_taken + 1,
                username = ?
            WHERE user_id = ? AND guild_id = ?
        """, (iq_score, monkey_percentage, username, user_id, guild_id)) # Added username update here too for consistency

        conn.commit()
        logger.info(f"Recorded analysis for user {user_id} in guild {guild_id}: IQ={iq_score}, Monkey%={monkey_percentage}. Stored in history and updated profile.")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error recording analysis for user {user_id}, guild {guild_id}: {e}", exc_info=True)
        if conn:
            conn.rollback() # Rollback if any part fails
        return False
    finally:
        if conn:
            conn.close()

def get_all_analysis_data_for_guild(guild_id: int) -> list[tuple[int, int, int]]:
    """
    Gets all users' AVERAGE analysis data (IQ, Monkey %) for a guild from their history.
    Returns list of (user_id, average_iq_score, average_monkey_percentage).
    Filters for users who have taken at least one analysis test (i.e., have history records).
    """
    conn = get_db_connection()
    if conn is None: return []
    results = []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                user_id,
                CAST(AVG(iq_score) AS INTEGER) as avg_iq,
                CAST(AVG(monkey_percentage) AS INTEGER) as avg_monkey
            FROM user_analysis_history
            WHERE guild_id = ?
            GROUP BY user_id
            HAVING COUNT(id) > 0
        """, (guild_id,))
        for row in cursor.fetchall():
            results.append((row['user_id'], row['avg_iq'], row['avg_monkey']))
        return results
    except sqlite3.Error as e:
        logger.error(f"Error getting all (average) analysis data for guild {guild_id}: {e}", exc_info=True)
        return []
    finally:
        if conn: conn.close()

def get_user_profile(user_id: int, guild_id: int):
    """Retrieves a user's profile data."""
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, last_iq_score, last_monkey_percentage, analysis_tests_taken
            FROM user_profiles
            WHERE user_id = ? AND guild_id = ?
        """, (user_id, guild_id))
        profile = cursor.fetchone()
        return profile
    except sqlite3.Error as e:
        logger.error(f"Error fetching user profile for user {user_id} in guild {guild_id}: {e}", exc_info=True)
        return None
    finally:
        if conn:
            conn.close()