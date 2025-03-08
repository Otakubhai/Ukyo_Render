# Anime & Doujin Bot

A Telegram bot for fetching anime information and downloading images from Multporn.net, optimized for deployment on Render.com's free tier.

## Features

- **Anime Information**: Fetch anime details from AniList with proper formatting and media image
- **Quality Selection**: Choose from multiple quality options (480p, 720p, 1080p)
- **Doujin Downloader**: Download and send images from Multporn.net directly to Telegram
- **Memory Optimized**: Downloads and uploads one image at a time to reduce memory usage
- **User Authentication**: Only allowed users can access certain commands

## Commands

- `/start` - Display bot introduction and information
- `/anime` - Search for an anime (will prompt for name and quality)
- `/get_doujin <URL>` - Download images from a Multporn.net URL

## Environment Variables

The bot requires the following environment variables:

- `API_ID` - Telegram API ID from my.telegram.org
- `API_HASH` - Telegram API Hash from my.telegram.org
- `BOT_TOKEN` - Bot token from BotFather
- `ALLOWED_USERS` - Comma-separated list of Telegram user IDs allowed to use the bot (optional)

## Deployment on Render.com

### Prerequisites
- A Render.com account
- Environment variables (API_ID, API_HASH, BOT_TOKEN) ready

### Steps

1. Fork/Clone this repository to your GitHub account
2. Log in to your Render.com account
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Use the following settings:
   - **Environment**: Docker
   - **Build Command**: Leave empty (uses Dockerfile)
   - **Start Command**: Leave empty (specified in Dockerfile)
   - **Instance Type**: Free (512 MB RAM, 0.1 CPU)
6. Add the required environment variables
7. Deploy!

### Environment Variables Setup on Render

1. In your Render dashboard, select your service
2. Go to "Environment" tab
3. Add the following key-value pairs:
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API Hash
   - `BOT_TOKEN`: Your Telegram Bot Token
   - `ALLOWED_USERS`: Comma-separated Telegram user IDs (optional)

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with the required environment variables
4. Run the bot: `python main.py`

## Optimizations for Render Free Tier

- Images are processed one at a time to minimize memory usage
- Sleep between operations to prevent hitting rate limits
- Temporary files are removed immediately after use
- Uses BeautifulSoup for efficient HTML parsing
- Asynchronous operations with Pyrogram to maximize throughput

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
