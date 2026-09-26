from dotenv import load_dotenv
import os
import yaml

load_dotenv(dotenv_path=os.path.join("config",'.env'))  # Load environment variables from .env file

CLIENT_SECRET = os.getenv('client_secret')

BOT_SECRET = os.getenv('bot_secret')   

USER = os.getenv('user')

PASSWORD = os.getenv('password')

#Load data from ymal file

with open(file="config/config.yml",mode="r") as file:
    ymal_data = yaml.safe_load(file)

if type(ymal_data) != dict:
    raise ValueError("It's not a freaking dict you messed up your config file")

for i in ymal_data:
    if ymal_data[i] == ("" or None) :
        raise ValueError(f"value {i} is not set")

CLIENT_ID = ymal_data['client_id']

REDIRECT_URI = ymal_data['redirect_uri']

DISCORD_API_BASE_URL = ymal_data['discord_api_base_url']

GUILD_ID = ymal_data['guild_id']

ROLES_TO_SYNC = ymal_data['roles_to_sync']

DEFAULT_ROLE = ymal_data['default_role']


db_config = {
    "host": ymal_data['host'],
    "user": USER,
    "password": PASSWORD,
    "database": ymal_data['database'],
    "port": ymal_data['port']
}

pool_setting = {
    "pool_name": ymal_data['pool_name'],
    "pool_size": int(ymal_data['pool_size']),
    "pool_reset_session": True
}
