import os
import asyncio
import logging
import tempfile
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ParseMode

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").split(",")

# Use temp directory instead of persistent storage
TEMP_DIR = tempfile.gettempdir()

# Define user states
user_states = {}
user_data = {}

# Initialize bot
app = Client(
    "anime_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    """Handle the /start command"""
    photo_url = "https://graph.org/saitama-02-27-2"
    caption = (
        "𝙷𝚎𝚕𝚕𝚘 𝚄𝚜𝚎𝚛! 𝙸 𝚊𝚖 𝚂𝚊𝚒𝚝𝚊𝚖𝚊 𝚊 𝚙𝚘𝚠𝚎𝚛𝚏𝚞𝚕 𝚕𝚎𝚎𝚌𝚑 𝚛𝚎𝚗𝚊𝚖𝚎𝚛 𝚋𝚘t.\n"
        "𝚃𝚘 𝚞𝚜𝚎 𝚖𝚎 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝚑𝚊𝚟𝚎 𝚝𝚘 𝚋𝚞𝚢 𝚊 𝚜𝚞𝚋𝚜𝚌𝚛𝚒𝚙𝚝𝚒𝚘𝚗, 𝙵𝚘𝚛 𝟷𝟶𝟶 𝙸𝙽𝚁 – 𝙼𝚘𝚗𝚝𝚑𝚕𝚢. "
        "𝚈𝚘𝚞 𝚊𝚕𝚜𝚘 𝚐𝚎𝚝 𝚊𝚌𝚌𝚎𝚜𝚜 𝚝𝚘 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚕𝚎𝚎𝚌𝚑 𝚐𝚛𝚘𝚞𝚙 𝚠𝚒𝚝𝚑 𝚞𝚗𝚕𝚒𝚖𝚒𝚝𝚎𝚍 "
        "𝚕𝚎𝚎𝚌𝚑 𝚌𝚊𝚙𝚊𝚌𝚒𝚝𝚢 𝚠𝚒𝚝𝚑𝚘𝚞𝚝 𝚊𝚗𝚢 𝚕𝚒𝚖𝚒𝚝𝚜!\n\n"
        "𝚃𝚑𝚒𝚜 𝚋𝚘𝚝 𝚒𝚜 𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚍 𝚊𝚗𝚍 𝚖𝚊𝚒𝚗𝚝𝚊𝚒𝚗𝚎𝚍 𝚋𝚢 @Aakash1230. 𝙾𝚠𝚗𝚎𝚛 𝚘𝚏 @Anime_Warior"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("My Channel", url="https://t.me/Anime_Warior")],
        [InlineKeyboardButton("Developer", url="https://t.me/Aakash1230")]
    ])
    
    await message.reply_photo(photo=photo_url, caption=caption, reply_markup=keyboard)

@app.on_message(filters.command("anime"))
async def anime_command(client, message):
    """Handle the /anime command"""
    user_id = str(message.from_user.id)
    
    # Check if user is allowed
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        await message.reply_text("You are not authorized to use this command.")
        return
    
    # Set user state to wait for anime name
    user_states[user_id] = "WAITING_FOR_ANIME_NAME"
    await message.reply_text("Please enter the name of the anime:")

@app.on_message(filters.command("get_doujin"))
async def get_doujin_command(client, message):
    """Handle the /get_doujin command"""
    # Extract URL from command
    command_parts = message.text.split(" ", 1)
    if len(command_parts) != 2:
        await message.reply_text("Please provide a valid Multporn.net URL.")
        return
    
    url = command_parts[1].strip()
    if "multporn.net" not in url:
        await message.reply_text("Invalid URL. Please send a valid Multporn.net link.")
        return
    
    # Send processing message
    status_message = await message.reply_text("Fetching images... Please wait.")
    
    try:
        # Scrape images
        image_urls = await scrape_images(url)
        if not image_urls:
            await status_message.edit_text("No images found or invalid URL.")
            return
        
        # Update status
        await status_message.edit_text(f"Found {len(image_urls)} images. Downloading and uploading...")
        
        # Download and upload images one by one to save memory
        for index, img_url in enumerate(image_urls):
            # Update progress every 5 images
            if index % 5 == 0:
                await status_message.edit_text(f"Processing image {index+1}/{len(image_urls)}...")
            
            # Download image
            img_data = await download_image(img_url)
            if not img_data:
                continue
                
            # Save temporarily
            file_path = os.path.join(TEMP_DIR, f"image_{index+1}.jpg")
            with open(file_path, "wb") as img_file:
                img_file.write(img_data)
            
            # Upload to Telegram
            try:
                await client.send_document(
                    message.chat.id,
                    file_path,
                    caption=f"Image {index+1}/{len(image_urls)}"
                )
                # Remove temporary file
                os.remove(file_path)
                
                # Sleep to avoid hitting rate limits
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"Error uploading image {index+1}: {e}")
        
        await status_message.edit_text("All images uploaded successfully!")
            
    except Exception as e:
        logger.error(f"Error processing doujin: {e}")
        await status_message.edit_text("An error occurred while processing the request.")

@app.on_callback_query()
async def handle_callbacks(client, callback_query):
    """Handle callback queries from inline buttons"""
    user_id = str(callback_query.from_user.id)
    
    # Handle quality selection for anime
    if user_states.get(user_id) == "WAITING_FOR_QUALITY":
        quality = callback_query.data
        anime_name = user_data.get(user_id, {}).get("anime_name", "")
        
        # Update user data
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]["quality"] = quality
        
        # Fetch anime info
        await callback_query.answer("Fetching anime information...")
        anime_info = await get_anime_info(anime_name, quality)
        
        if anime_info:
            # Send anime image and info
            await callback_query.message.reply_photo(
                photo=anime_info["image_url"],
                caption=anime_info["caption"]
            )
            
            # Reset user state
            user_states[user_id] = None
        else:
            await callback_query.message.reply_text("Anime not found or an error occurred.")
    
    # Acknowledge the callback query
    await callback_query.answer()

@app.on_message(filters.text & ~filters.command)
async def handle_text_messages(client, message):
    """Handle text messages according to user state"""
    user_id = str(message.from_user.id)
    
    # Check if waiting for anime name
    if user_states.get(user_id) == "WAITING_FOR_ANIME_NAME":
        anime_name = message.text.strip()
        
        # Save anime name
        if user_id not in user_data:
            user_data[user_id] = {}
        user_data[user_id]["anime_name"] = anime_name
        
        # Update state
        user_states[user_id] = "WAITING_FOR_QUALITY"
        
        # Create quality selection keyboard
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("480p", callback_data="480p")],
            [InlineKeyboardButton("720p", callback_data="720p")],
            [InlineKeyboardButton("1080p", callback_data="1080p")],
            [InlineKeyboardButton("720p & 1080p", callback_data="720p & 1080p")],
            [InlineKeyboardButton("480p, 720p & 1080p", callback_data="480p, 720p & 1080p")]
        ])
        
        await message.reply_text("What quality?", reply_markup=keyboard)

async def get_anime_info(anime_name, quality):
    """Fetch anime details from AniList API and format output"""
    url = "https://graphql.anilist.co/"
    query = '''
    query ($search: String) {
        Media(search: $search, type: ANIME) {
            id
            title { romaji english }
            episodes
            genres
            coverImage { extraLarge }
        }
    }
    '''
    variables = {"search": anime_name}

    try:
        async with requests.Session() as session:
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: session.post(url, json={"query": query, "variables": variables})
            )
            
            if response.status_code == 200:
                data = response.json()
                anime_data = data.get("data", {}).get("Media")

                if anime_data:
                    anime_id = anime_data["id"]
                    title = anime_data["title"]["english"] or anime_data["title"]["romaji"]
                    episodes = anime_data["episodes"] or "Unknown"
                    genres = ", ".join(["Hanime"] + anime_data["genres"])
                    
                    # Use the Anilist image URL format
                    image_url = f"https://img.anili.st/media/{anime_id}"

                    caption = (
                        f"💦 {title}\n"
                        "╭──────────────────────\n"
                        f"├ 📺 Episode : {episodes}\n"
                        f"├ 💾 Quality : {quality}\n"
                        f"├ 🎭 Genres: {genres}\n"
                        "├ 🔊 Audio track : Sub\n"
                        "├ #Censored\n"
                        "├ #Recommendation +++++++\n"
                        "╰──────────────────────"
                    )

                    return {"image_url": image_url, "caption": caption}
    except Exception as e:
        logger.error(f"Error fetching anime info: {e}")
    
    return None

async def scrape_images(url):
    """Scrape image URLs from Multporn.net asynchronously"""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # Run in executor to not block the event loop
        response_text = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: requests.get(url, headers=headers).text
        )
        
        # Parse HTML
        soup = BeautifulSoup(response_text, "html.parser")
        image_tags = soup.find_all("img")

        image_urls = []
        for img in image_tags:
            src = img.get("src")
            if src and "uploads" in src:
                if not src.startswith("http"):
                    src = "https://multporn.net" + src
                image_urls.append(src)

        return image_urls
    except Exception as e:
        logger.error(f"Error scraping images: {e}")
        return []

async def download_image(url):
    """Download an image asynchronously"""
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # Run in executor to not block the event loop
        response = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: requests.get(url, headers=headers)
        )
        
        if response.status_code == 200:
            return response.content
    except Exception as e:
        logger.error(f"Error downloading image {url}: {e}")
    
    return None

def main():
    """Start the bot"""
    logger.info("Starting bot...")
    app.run()

if __name__ == "__main__":
    main()
