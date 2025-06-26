# 🐒 Dr. Monkey - Your Primate Analysis Discord Bot 🍌

Dr. Monkey is a fun and interactive Discord bot designed to bring a touch of primate chaos and analytical humor to your server. It allows users to get their "primate analysis" (IQ and Monkey Purity scores), challenge others to "monkey-offs," and view various leaderboards and rankings.

## ✨ Features

-   **🔬 Primate Analysis (`/analyze`)**:
    -   Generates a unique IQ score and "Monkey Purity" percentage for each user.
    -   Provides humorous, context-aware responses based on the generated scores.
    -   Records analysis results in a local SQLite database for historical tracking.
    -   Cleans up messages in non-designated bot channels to keep chat tidy.

-   **⚔️ Monkey-Offs (`/monkeyoff <@user>`)**:
    -   Challenge another user to a random "monkey-off" duel.
    -   Determines a winner based on randomly generated percentages.
    -   Records win/loss statistics and participation in the database.
    -   Offers a variety of entertaining responses for wins, losses, and ties.
    -   Cleans up messages in non-designated bot channels.

-   **📊 Rankings & Leaderboards (`/ranks`)**:
    -   Displays comprehensive leaderboards for various metrics, including:
        -   Average Combined Score (IQ + Monkey %)
        -   Average IQ Score
        -   Average Monkey Purity %
        -   Top/Lowest Single Analysis Scores (Combined, IQ, Monkey %)
        -   Total Monkey-Off Wins
        -   Monkey-Off Win Rate
    -   Features an interactive button-based interface to switch between different ranking types.
    -   Generates visual bar plots for leaderboards, highlighting the requesting user.

-   **💾 Persistent Data Storage**:
    -   Utilizes a local SQLite database to store user profiles, analysis history, and monkey-off results, ensuring data persists across bot restarts.

-   **⚙️ Highly Configurable**:
    -   All sensitive information and key settings are managed via environment variables (`.env` file).
    -   Supports whitelisting specific Discord guilds (servers) where the bot will operate.
    -   Allows designation of specific "bot channels" for commands, with automatic message cleanup in other channels.

-   ** robust Error Handling & Logging**:
    -   Includes global error handling for application commands to provide user-friendly messages and log unhandled exceptions.
    -   Comprehensive logging system with configurable levels and optional file output for easy debugging and monitoring.

## 🚀 Getting Started

Follow these steps to get Dr. Monkey up and running on your server.

### Prerequisites

-   **Python 3.8+**: Download and install from python.org.
-   **Discord Account**: You'll need a Discord account to create a bot application.
-   **Discord Bot Application**:
    1.  Go to the Discord Developer Portal.
    2.  Click "New Application" and give it a name (e.g., "Dr. Monkey").
    3.  Navigate to the "Bot" tab, click "Add Bot," and confirm.
    4.  **IMPORTANT**: Enable the `SERVER MEMBERS INTENT` under "Privileged Gateway Intents" in the Bot tab. Without this, the bot will not function correctly.
    5.  Copy your bot's **TOKEN**. Keep this secret!

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/nikoleinonen/Dr-Monkey
    cd Dr-Monkey
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a file named `.env` in the root directory of the project (`Dr-Monkey/.env`) and fill it with your bot's configuration:

    ```env
    DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
    DATABASE_FILE_PATH="data/your_database_name.db"
    LOG_LEVEL="INFO" # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_PATH="logs/dr_monkey.log" # Optional: Leave empty for console only
    WHITELISTED_GUILD_IDS="YOUR_GUILD_ID_1,YOUR_GUILD_ID_2" # Optional: Comma-separated list of Discord Server IDs. Leave empty to allow all.
    BOT_CHANNEL_IDS="YOUR_CHANNEL_ID_1,YOUR_CHANNEL_ID_2" # Optional: Comma-separated list of Discord Channel IDs. Leave empty to allow all channels.
    ```
    -   Replace `YOUR_BOT_TOKEN_HERE` with the token you copied from the Discord Developer Portal.
    -   Replace `YOUR_GUILD_ID_X` and `YOUR_CHANNEL_ID_X` with the actual IDs of your Discord server(s) and channel(s). You can enable Developer Mode in Discord settings (User Settings -> Advanced -> Developer Mode) to easily copy IDs by right-clicking.

### Running the Bot

1.  **Run the bot**:
    ```bash
    python main.py
    ```
    The bot should now connect to Discord. You will see log messages in your console (and optionally in the log file) indicating its status.

## 🤖 Usage

Once the bot is online and invited to your server, you can use the following slash commands:

-   **`/analyze`**: Get your personalized primate analysis, including an IQ score and Monkey Purity percentage.
-   **`/monkeyoff <@user>`**: Challenge another user to a monkey-off and see who comes out on top!
-   **`/ranks`**: View various leaderboards and rankings for analysis scores, monkey-off wins, and win rates. Use the interactive buttons to navigate.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new features, improvements, or bug fixes, please feel free to open an issue or submit a pull request.

But I'll be completely honest with you, I CBA

## 📄 License

This project is open-source and available under the MIT License.

---

Enjoy your time with Dr. Monkey! If you encounter any issues, please refer to the logs or open an issue on the GitHub repository.

```