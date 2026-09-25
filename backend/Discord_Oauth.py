import requests

from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, DISCORD_API_BASE_URL, BOT_SECRET
from aiolimiter import AsyncLimiter

rate_limit_get = AsyncLimiter(5,5)

rate_limit_post = AsyncLimiter(5,5)

rate_limit_put = AsyncLimiter(1,1)



class Discord_Oauth:
    def __init__(self, client_id, client_secret, redirect_url,discord_api_base_url, bot_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.discord_api_base_url = discord_api_base_url
        self.bot_secret = bot_secret

    async def get_user_token(self, code, state):
        async with rate_limit_post:
            if not code:
                return 400, "Brak kodu autoryzacyjnego"

            # 1. Wymiana kodu na Access Token
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_url
            }

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            
            token_response = requests.post(f"{self.discord_api_base_url}/oauth2/token", data=data, headers=headers)

            user_token = token_response.json()["access_token"]

            return 200, user_token, state

    async def get_user_data(self, user_token):
        async with rate_limit_get:
        
            user_response = requests.get(
                f"{self.discord_api_base_url}/users/@me",
                headers={'Authorization': f'Bearer {user_token}'}
            )

            if user_response.status_code != 200:
                return user_response.status_code

            user_data = user_response.json().get('id')

            return await self.add_user_to_guild(user_token, user_data), user_data

    async def add_user_to_guild(self, access_token, user_data):
        async with rate_limit_put:

            adding_user = requests.put(
                f"{self.discord_api_base_url}/guilds/1365051003732234284/members/{user_data}",
                headers={'Authorization': f'Bot {self.bot_secret}',
                        "Content-Type": "application/json"
                        }
                ,json={
                    "access_token": access_token
                }
            )


            return adding_user.status_code

da = Discord_Oauth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, DISCORD_API_BASE_URL, BOT_SECRET)

