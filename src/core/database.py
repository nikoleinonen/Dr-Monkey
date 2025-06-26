from datetime import datetime, timedelta, timezone
import sqlite3
import os
import logging
from src.core.logging import get_logger
logger = get_logger("DB_Manager")
# --- SQL Query Constants ---

# SQL for creating the user_profiles table.
CREATE_USER_PROFILES_TABLE = """
    CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER NOT NULL,
        guild_id INTEGER NOT NULL,
        username TEXT,
        last_iq_score INTEGER DEFAULT NULL,
        last_monkey_percentage INTEGER DEFAULT NULL,
        analysis_tests_taken INTEGER NOT NULL DEFAULT 0, -- Total analysis commands run
        monkeyoff_wins INTEGER NOT NULL DEFAULT 0,       -- Total monkeyoff wins
        monkeyoff_losses INTEGER NOT NULL DEFAULT 0,     -- Total monkeyoff losses
        total_monkeyoffs INTEGER NOT NULL DEFAULT 0,     -- Total monkeyoff commands participated in
        PRIMARY KEY (user_id, guild_id)
    )
"""
# SQL for creating the user_analysis_history table.
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
# SQL for creating the monkeyoff_history table.
CREATE_MONKEYOFF_HISTORY_TABLE = """
    CREATE TABLE IF NOT EXISTS monkeyoff_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challenger_id INTEGER NOT NULL,
        opponent_id INTEGER NOT NULL,
        guild_id INTEGER NOT NULL,
        challenger_percentage INTEGER NOT NULL,
        opponent_percentage INTEGER NOT NULL,
        winner_id INTEGER, -- NULL if tie
        timestamp TEXT NOT NULL
    )
"""

# SQL for creating an index on user_analysis_history.
CREATE_ANALYSIS_HISTORY_INDEX = "CREATE INDEX IF NOT EXISTS idx_user_analysis_history_user_guild ON user_analysis_history (user_id, guild_id)"
# SQL to get table info (for schema migration checks).
PRAGMA_TABLE_INFO = "PRAGMA table_info(user_profiles)"
# SQL to add 'username' column.
ALTER_ADD_USERNAME = "ALTER TABLE user_profiles ADD COLUMN username TEXT"
# SQL to add 'last_iq_score' column.
ALTER_ADD_LAST_IQ = "ALTER TABLE user_profiles ADD COLUMN last_iq_score INTEGER DEFAULT NULL"
# SQL to add 'last_monkey_percentage' column.
ALTER_ADD_LAST_MONKEY = "ALTER TABLE user_profiles ADD COLUMN last_monkey_percentage INTEGER DEFAULT NULL"
# SQL to add 'analysis_tests_taken' column.
ALTER_ADD_TESTS_TAKEN = "ALTER TABLE user_profiles ADD COLUMN analysis_tests_taken INTEGER NOT NULL DEFAULT 0"
# SQL to add 'monkeyoff_wins' column.
ALTER_ADD_MONKEYOFF_WINS = "ALTER TABLE user_profiles ADD COLUMN monkeyoff_wins INTEGER NOT NULL DEFAULT 0"
# SQL to add 'monkeyoff_losses' column.
ALTER_ADD_MONKEYOFF_LOSSES = "ALTER TABLE user_profiles ADD COLUMN monkeyoff_losses INTEGER NOT NULL DEFAULT 0"
# SQL to add 'total_monkeyoffs' column.
ALTER_ADD_TOTAL_MONKEYOFFS = "ALTER TABLE user_profiles ADD COLUMN total_monkeyoffs INTEGER NOT NULL DEFAULT 0"

# Data Manipulation and Retrieval
# SQL for upserting user profiles.
UPSERT_USER_PROFILE = """
    INSERT INTO user_profiles (user_id, guild_id, username)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, guild_id) DO UPDATE SET
        username = EXCLUDED.username;
"""

# SQL for inserting analysis history.
INSERT_ANALYSIS_HISTORY = """
    INSERT INTO user_analysis_history (user_id, guild_id, iq_score, monkey_percentage, timestamp)
    VALUES (?, ?, ?, ?, ?)
"""
# SQL for inserting monkey-off history.
INSERT_MONKEYOFF_HISTORY = """
    INSERT INTO monkeyoff_history (challenger_id, opponent_id, guild_id, challenger_percentage, opponent_percentage, winner_id, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""
# SQL for updating user profile after an analysis.
UPDATE_USER_PROFILE_ANALYSIS = """
    UPDATE user_profiles
    SET last_iq_score = ?,
        last_monkey_percentage = ?,
        analysis_tests_taken = analysis_tests_taken + 1
    WHERE user_id = ? AND guild_id = ?
"""
# SQL for updating user profile after a monkey-off.
UPDATE_USER_PROFILE_MONKEYOFF_STATS = """
    UPDATE user_profiles
    SET monkeyoff_wins = monkeyoff_wins + ?,
        monkeyoff_losses = monkeyoff_losses + ?,
        total_monkeyoffs = total_monkeyoffs + 1
    WHERE user_id = ? AND guild_id = ?
"""
# SQL for selecting average analysis data for a guild.
SELECT_AVERAGE_ANALYSIS_FOR_GUILD = """
    SELECT
        user_id,
        CAST(AVG(iq_score) AS REAL) as avg_iq,
        CAST(AVG(monkey_percentage) AS REAL) as avg_monkey
    FROM user_analysis_history
    WHERE guild_id = ?
    GROUP BY user_id
    HAVING COUNT(id) > 0
"""
# Base SQL for selecting a single analysis record per user.
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
# SQL for selecting a user's profile.
SELECT_USER_PROFILE = """
    SELECT username, last_iq_score, last_monkey_percentage, analysis_tests_taken
    FROM user_profiles
    WHERE user_id = ? AND guild_id = ?
"""
# SQL for selecting top monkey-off wins for a guild.
SELECT_TOP_WINS_FOR_GUILD = """
    SELECT user_id, monkeyoff_wins
    FROM user_profiles
    WHERE guild_id = ? AND monkeyoff_wins > 0
    ORDER BY monkeyoff_wins DESC
    LIMIT 10
"""
# SQL for selecting top monkey-off win rates for a guild.
SELECT_TOP_WIN_RATE_FOR_GUILD = """
    SELECT user_id, CAST(monkeyoff_wins AS REAL) * 100 / total_monkeyoffs AS win_rate
    FROM user_profiles
    WHERE guild_id = ? AND total_monkeyoffs > 0
    ORDER BY win_rate DESC
    LIMIT 10
"""

class DatabaseManager:
    """Manages SQLite database connections and operations for the bot."""
    def __init__(self) -> None:
        # Private attribute to store the database file path.
        self._db_file_path: str | None = None

    def configure_database_path(self, path: str) -> None:
        """Sets the database file path."""
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
        # Create directory if it doesn't exist and establish connection.
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
        """Creates necessary tables and performs schema migrations if they don't exist."""
        if self._db_file_path is None:
            logger.critical("Database path not configured for initialization. Call configure_database_path() first.")
            return
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                
                # Create user_profiles table.
                cursor.execute(CREATE_USER_PROFILES_TABLE)
                
                # Check existing columns for schema migrations.
                cursor.execute(PRAGMA_TABLE_INFO)
                columns = [column['name'] for column in cursor.fetchall()]
                
                # Add 'username' column if missing.
                if 'username' not in columns:
                    cursor.execute(ALTER_ADD_USERNAME)
                    logger.info("Added 'username' column to 'user_profiles' table.")
                # Add 'last_iq_score' column if missing.
                if 'last_iq_score' not in columns:
                    cursor.execute(ALTER_ADD_LAST_IQ)
                    logger.info("Added 'last_iq_score' column to 'user_profiles' table.")
                # Add 'last_monkey_percentage' column if missing.
                if 'last_monkey_percentage' not in columns:
                    cursor.execute(ALTER_ADD_LAST_MONKEY)
                    logger.info("Added 'last_monkey_percentage' column to 'user_profiles' table.")
                # Add 'analysis_tests_taken' column if missing.
                if 'analysis_tests_taken' not in columns:
                    cursor.execute(ALTER_ADD_TESTS_TAKEN)
                    logger.info("Added 'analysis_tests_taken' column to 'user_profiles' table.")
                # Add 'monkeyoff_wins' column if missing.
                if 'monkeyoff_wins' not in columns:
                    cursor.execute(ALTER_ADD_MONKEYOFF_WINS)
                    logger.info("Added 'monkeyoff_wins' column to 'user_profiles' table.")
                # Add 'monkeyoff_losses' column if missing.
                if 'monkeyoff_losses' not in columns:
                    cursor.execute(ALTER_ADD_MONKEYOFF_LOSSES)
                    logger.info("Added 'monkeyoff_losses' column to 'user_profiles' table.")
                # Add 'total_monkeyoffs' column if missing.
                if 'total_monkeyoffs' not in columns:
                    cursor.execute(ALTER_ADD_TOTAL_MONKEYOFFS)
                    logger.info("Added 'total_monkeyoffs' column to 'user_profiles' table.")
                
                # Create user_analysis_history table and its index.
                cursor.execute(CREATE_USER_ANALYSIS_HISTORY_TABLE)
                cursor.execute(CREATE_ANALYSIS_HISTORY_INDEX)
                logger.info("Checked/created 'user_profiles' table.")
                logger.info("Checked/created 'user_analysis_history' table and index.")
                
                # Create monkeyoff_history table.
                cursor.execute(CREATE_MONKEYOFF_HISTORY_TABLE)
                logger.info("Checked/created 'monkeyoff_history' table.")
                
                # The 'with' statement handles commit on success and rollback on exception.
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
    def record_analysis_result(self, user_id: int, guild_id: int, iq_score: int, monkey_percentage: int, username: str, guild_name: str) -> bool:
        """
        Records an analysis result (IQ and Monkey %) for a user in a single transaction.
        Ensures the user profile exists, stores the result in history, and updates the profile.
        """
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
                # 1. Ensure user profile exists or update username
                cursor.execute(UPSERT_USER_PROFILE, (user_id, guild_id, username))
                # Insert into history table
                cursor.execute(INSERT_ANALYSIS_HISTORY, (user_id, guild_id, iq_score, monkey_percentage, timestamp))
                # Update user_profiles with last scores and increment tests_taken.
                cursor.execute(UPDATE_USER_PROFILE_ANALYSIS, (iq_score, monkey_percentage, user_id, guild_id))
            return True
        except sqlite3.Error as e:
            logger.error(f"Error recording analysis for user {user_id}, guild {guild_id}: {e}", exc_info=True)
            return False

    def record_monkeyoff_result(self, challenger_id: int, opponent_id: int, guild_id: int,
                                challenger_percentage: int, opponent_percentage: int, winner_id: int | None) -> bool:
        """
        Records a monkey-off result in history and updates participant profiles.
        """
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
                # Insert into history table
                cursor.execute(INSERT_MONKEYOFF_HISTORY, (challenger_id, opponent_id, guild_id,
                                                          challenger_percentage, opponent_percentage, winner_id, timestamp))
                # Update challenger's stats
                challenger_wins = 1 if winner_id == challenger_id else 0
                challenger_losses = 1 if winner_id == opponent_id else 0
                cursor.execute(UPDATE_USER_PROFILE_MONKEYOFF_STATS, (challenger_wins, challenger_losses, challenger_id, guild_id))
                # Update opponent's stats
                opponent_wins = 1 if winner_id == opponent_id else 0
                opponent_losses = 1 if winner_id == challenger_id else 0
                cursor.execute(UPDATE_USER_PROFILE_MONKEYOFF_STATS, (opponent_wins, opponent_losses, opponent_id, guild_id))
            return True
        except sqlite3.Error as e:
            logger.error(f"Error recording monkey-off for challenger {challenger_id} vs opponent {opponent_id} in guild {guild_id}: {e}", exc_info=True)
            return False
    def get_average_analysis_data_for_guild(self, guild_id: int) -> list[tuple[int, float, float]]:
        """
        Gets all users' AVERAGE analysis data (IQ, Monkey %) for a guild from their history.
        Returns list of (user_id, average_iq_score, average_monkey_percentage) as floats.
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
        except sqlite3.Error as e:
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

    def get_top_wins_data_for_guild(self, guild_id: int) -> list[tuple[int, int]]:
        """
        Gets top users by monkeyoff wins for a guild.
        Returns list of (user_id, monkeyoff_wins).
        """
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SELECT_TOP_WINS_FOR_GUILD, (guild_id,))
                results = []
                for row in cursor.fetchall():
                    results.append((row['user_id'], row['monkeyoff_wins']))
                return results
        except sqlite3.Error as e:
            logger.error(f"Error getting top wins data for guild {guild_id}: {e}", exc_info=True)
            return []

    def get_top_win_rate_data_for_guild(self, guild_id: int) -> list[tuple[int, float]]:
        """
        Gets top users by monkeyoff win rate for a guild.
        Returns list of (user_id, win_rate).
        """
        try:
            with self._get_new_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(SELECT_TOP_WIN_RATE_FOR_GUILD, (guild_id,))
                results = []
                for row in cursor.fetchall():
                    results.append((row['user_id'], row['win_rate']))
                return results
        except sqlite3.Error as e:
            logger.error(f"Error getting top win rate data for guild {guild_id}: {e}", exc_info=True)
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
