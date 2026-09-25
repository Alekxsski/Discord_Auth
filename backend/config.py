from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')
REDIRECT_URI = os.getenv('redirect_uri')
DISCORD_API_BASE_URL = os.getenv('discord_api_base_url')
BOT_SECRET = os.getenv('bot_secret')

db_config = {
    "host": os.getenv('host'),
    "user": os.getenv('user'),
    "password": os.getenv('password'),
    "database": os.getenv('database'),
    "port": int(os.getenv('port'))
}

pool_setting = {
    "pool_name": os.getenv('pool_name'),
    "pool_size": int(os.getenv('pool_size')),
    "pool_reset_session": True
}