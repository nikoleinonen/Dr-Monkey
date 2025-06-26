from datetime import datetime, timedelta, timezone
import sqlite3
import os
import logging
from src.core.logging import get_logger
logger = get_logger("DB_Manager")

# --- SQL Query Constants ---

# Table Creation and Alteration
CREATE_USER_PROFILES_TABLE = """
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER NOT NULL,
        guild_id INTEGER NOT NULL,
        username TEXT,
        last_iq_score INTEGER DEFAULT NULL,
        last_monkey_percentage INTEGER DEFAULT NULL,
        analysis_tests_taken INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, guild_id)
    )
"""

CREATE_USER_ANALYSIS_HISTORY_TABLE = """
    CREATE TABLE IF NOT EXISTS user_analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        guild_id INTEGER NOT NULL,
        iq_score INTEGER NOT NULL,
        monkey_percentage INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (user_id, guild_id) REFERENCES user_profiles(user_id, guild_id) ON DELETE CASCADE
    )
"""

CREATE_ANALYSIS_HISTORY_INDEX = "CREATE INDEX IF NOT EXISTS idx_user_analysis_history_user_guild ON user_analysis_history (user_id, guild_id)"

PRAGMA_TABLE_INFO = "PRAGMA table_info(user_profiles)"

ALTER_ADD_USERNAME = "ALTER TABLE user_profiles ADD COLUMN username TEXT"
ALTER_ADD_LAST_IQ = "ALTER TABLE user_profiles ADD COLUMN last_iq_score INTEGER DEFAULT NULL"
ALTER_ADD_LAST_MONKEY = "ALTER TABLE user_profiles ADD COLUMN last_monkey_percentage INTEGER DEFAULT NULL"
ALTER_ADD_TESTS_TAKEN = "ALTER TABLE user_profiles ADD COLUMN analysis_tests_taken INTEGER NOT NULL DEFAULT 0"

# Data Manipulation and Retrieval
UPSERT_USER_PROFILE = """
    INSERT INTO user_profiles (user_id, guild_id, username, last_iq_score, last_monkey_percentage, analysis_tests_taken) 
    VALUES (?, ?, ?, NULL, NULL, 0)
    ON CONFLICT(user_id, guild_id) DO UPDATE SET
        username = EXCLUDED.username;
"""

INSERT_ANALYSIS_HISTORY = """
    INSERT INTO user_analysis_history (user_id, guild_id, iq_score, monkey_percentage, timestamp)
    VALUES (?, ?, ?, ?, ?)
"""

UPDATE_USER_PROFILE_ANALYSIS = """
    UPDATE user_profiles
    SET last_iq_score = ?,
        last_monkey_percentage = ?,
        analysis_tests_taken = analysis_tests_taken + 1
    WHERE user_id = ? AND guild_id = ?
"""

SELECT_AVERAGE_ANALYSIS_FOR_GUILD = """
    SELECT
        user_id,
        CAST(AVG(iq_score) AS INTEGER) as avg_iq,
        CAST(AVG(monkey_percentage) AS INTEGER) as avg_monkey
    FROM user_analysis_history
    WHERE guild_id = ?
    GROUP BY user_id
    HAVING COUNT(id) > 0
"""

SELECT_SINGLE_RECORD_ANALYSIS_BASE = """
    SELECT user_id, iq_score, monkey_percentage
    FROM (
        SELECT
            user_id,
            iq_score,
            monkey_percentage,
            ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY {order_by_clause} {direction}) as rn
        FROM user_analysis_history
        WHERE guild_id = ?
    )
    WHERE rn = 1
"""

SELECT_USER_PROFILE = """
    SELECT username, last_iq_score, last_monkey_percentage, analysis_tests_taken
    FROM user_profiles
    WHERE user_id = ? AND guild_id = ?
"""

class DatabaseManager:
    def __init__(self) -> None:
        self._db_file_path: str | None = None

    def configure_database_path(self, path: str) -> None:
        """Sets the database file path for the module to use."""
        self._db_file_path = path
        logger.info(f"Database path has been configured internally to: {self._db_file_path}")

    def _get_new_connection(self) -> sqlite3.Connection:
        """
        Opens a new SQLite database connection.
        This method is intended to be called within the thread where the connection is used.
        """
        if self._db_file_path is None:
            logger.critical("Database path not configured. Call configure_database_path() first.")
            raise RuntimeError("Database path not configured before attempting connection.")
        try:
            db_dir = os.path.dirname(self._db_file_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            conn = sqlite3.connect(self._db_file_path, timeout=15.0)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to open database connection: {e}", exc_info=True)
            raise

    def initialize_database(self):
        """Creates the necessary tables if they don't exist."""
        if self._db_file_path is None:
            logger.critical("Database path not configured for initialization. Call configure_database_path() first.")
            return
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(CREATE_USER_PROFILES_TABLE)

                cursor.execute(PRAGMA_TABLE_INFO)
                columns = [column['name'] for column in cursor.fetchall()]
                if 'username' not in columns:
                    cursor.execute(ALTER_ADD_USERNAME)
                    logger.info("Added 'username' column to 'user_profiles' table.")

                if 'last_iq_score' not in columns:
                    cursor.execute(ALTER_ADD_LAST_IQ)
                    logger.info("Added 'last_iq_score' column to 'user_profiles' table.")

                if 'last_monkey_percentage' not in columns:
                    cursor.execute(ALTER_ADD_LAST_MONKEY)
                    logger.info("Added 'last_monkey_percentage' column to 'user_profiles' table.")

                if 'analysis_tests_taken' not in columns:
                    cursor.execute(ALTER_ADD_TESTS_TAKEN)
                    logger.info("Added 'analysis_tests_taken' column to 'user_profiles' table.")

                # New table to store historical analysis results
                cursor.execute(CREATE_USER_ANALYSIS_HISTORY_TABLE)
                cursor.execute(CREATE_ANALYSIS_HISTORY_INDEX)

                logger.info("Checked/created 'user_profiles' table.")
                logger.info("Checked/created 'user_analysis_history' table and index.")

                # The 'with' statement handles commit on success, rollback on exception
                logger.info("Database tables checked/created successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}", exc_info=True)

    def ensure_user_exists(self, user_id: int, guild_id: int, username: str | None = None) -> bool:
        """
        Ensures a user profile exists for a given user and guild.
        Inserts a new record with default values if not present, or updates the username if it is.
        """
        current_username = username if username is not None else "UnknownUser"

        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                # Use INSERT ... ON CONFLICT DO UPDATE to handle both insertion and updating username atomically.
                cursor.execute(UPSERT_USER_PROFILE, (user_id, guild_id, current_username))
            return True

        except sqlite3.Error as e:
            logger.error(f"Error ensuring user profile exists for user {user_id} in guild {guild_id}: {e}", exc_info=True)
            return False

    def ensure_user_exists_and_get_profile(self, user_id: int, guild_id: int, username: str | None = None) -> sqlite3.Row | None:
        """
        Ensures a user profile and related stats rows exist, then retrieves the user's profile.
        """
        if not self.ensure_user_exists(user_id, guild_id, username):
            logger.error(f"ensure_user_exists_and_get_profile: Failed during ensure_user_exists for user {user_id}, guild {guild_id}.")
            return None

        profile = self.get_user_profile(user_id, guild_id)
        if profile is None:
            logger.warning(f"ensure_user_exists_and_get_profile: Profile not found for user {user_id}, guild {guild_id} after ensure_user_exists call.")
        return profile

    # --- Analysis (IQ & Monkey) Stats Functions ---
    def record_analysis_result(self, user_id: int, guild_id: int, iq_score: int, monkey_percentage: int, username: str, guild_name: str) -> bool:
        """
        Records an analysis result (IQ and Monkey %) for a user.
        Stores it in history and updates their latest scores in the profile.
        This operation is now wrapped in a transaction for atomicity.
        """
        # ensure_user_exists will open its own connection and close it.
        
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')

                # Insert into history table
                cursor.execute(INSERT_ANALYSIS_HISTORY, (user_id, guild_id, iq_score, monkey_percentage, timestamp))

                # Update user_profiles with last scores and increment tests_taken.
                cursor.execute(UPDATE_USER_PROFILE_ANALYSIS, (iq_score, monkey_percentage, user_id, guild_id))
            return True
        except sqlite3.Error as e:
            logger.error(f"Error recording analysis for user {user_id}, guild {guild_id}: {e}", exc_info=True)
            return False

    def get_average_analysis_data_for_guild(self, guild_id: int) -> list[tuple[int, int, int]]:
        """
        Gets all users' AVERAGE analysis data (IQ, Monkey %) for a guild from their history.
        Returns list of (user_id, average_iq_score, average_monkey_percentage).
        Filters for users who have taken at least one analysis test (i.e., have history records).
        """
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SELECT_AVERAGE_ANALYSIS_FOR_GUILD, (guild_id,))
                results = []
                for row in cursor.fetchall():
                    results.append((row['user_id'], row['avg_iq'], row['avg_monkey']))
                return results
        except sqlite3.Error as e: # Catch specific SQLite errors
            logger.error(f"Error getting all (average) analysis data for guild {guild_id}: {e}", exc_info=True)
            return []

    def get_single_record_analysis_data_for_guild(self, guild_id: int, metric: str, order: str = "DESC") -> list[tuple[int, int, int]]:
        """
        Gets a single analysis record per user for a guild, based on a specific metric.

        Args:
            guild_id: The ID of the guild.
            metric: The metric to order by ('iq', 'monkey', 'combined').
            order: The direction to order by ('DESC' for top, 'ASC' for lowest).

        Returns:
            List of (user_id, iq_score, monkey_percentage) tuples.
        """
        if metric == 'iq':
            order_by_clause = "iq_score"
        elif metric == 'monkey':
            order_by_clause = "monkey_percentage"
        elif metric == 'combined':
            order_by_clause = "(iq_score + monkey_percentage)"
        else:
            logger.error(f"Invalid metric '{metric}' for get_single_record_analysis_data_for_guild.")
            return []

        if order.upper() not in ["ASC", "DESC"]:
            logger.error(f"Invalid order '{order}' for get_single_record_analysis_data_for_guild.")
            return []

        query = SELECT_SINGLE_RECORD_ANALYSIS_BASE.format(order_by_clause=order_by_clause, direction=order.upper())

        results = []
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (guild_id,))
                for row in cursor.fetchall():
                    results.append((row['user_id'], row['iq_score'], row['monkey_percentage']))
                return results
        except sqlite3.Error as e:
            logger.error(f"Error getting single record analysis data for guild {guild_id}: {e}", exc_info=True)
            return []

    def get_user_profile(self, user_id: int, guild_id: int):
        """Retrieves a user's profile data."""
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
            cursor.execute(SELECT_USER_PROFILE, (user_id, guild_id))
            profile = cursor.fetchone()
            return profile
        except sqlite3.Error as e:
            logger.error(f"Error fetching user profile for user {user_id} in guild {guild_id}: {e}", exc_info=True)
            return None
