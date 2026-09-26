import requests

from backend.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, DISCORD_API_BASE_URL, BOT_SECRET, GUILD_ID
from aiolimiter import AsyncLimiter

rate_limit_get = AsyncLimiter(5,5)

rate_limit_post = AsyncLimiter(5,5)

rate_limit_put = AsyncLimiter(1,1)

rate_limit_patch = AsyncLimiter(1,1)



class DiscordApi:
    def __init__(self, client_id, client_secret, redirect_url,discord_api_base_url, bot_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.discord_api_base_url = discord_api_base_url
        self.bot_secret = bot_secret

#Using provided data from discord to get token that can manage user 
    async def get_user_token(self, code):

        async with rate_limit_post:

            if not code:
                return {'status': 400, 'error': "Authorization code not found"}

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

            return {'status': 200, 'access_token': token_response.json()["access_token"]}

#Accessing user informations with granted token
    async def get_user_discord_id(self, user_token):
        
        async with rate_limit_get:
        
            user_response = requests.get(
                f"{self.discord_api_base_url}/users/@me",
                headers={'Authorization': f'Bearer {user_token}'}
            )

            code = user_response.status_code

            if code != 200:
                return {'status': code, 'error': "Member id couldn't be found"}

            return {'status': code, 'user_discord_id': user_response.json().get('id')}

#Checking guild for member
    async def get_member(self,member_id):

        member_data = requests.get(f"{self.discord_api_base_url}/guilds/{GUILD_ID}/members/{member_id}",
                headers={'Authorization': f'Bot {self.bot_secret}',
                        "Content-Type": "application/json"
                        }
            )

        code = member_data.status_code

        if code == 200:
            json = member_data.json()
            return {'status': code, 'nick': json['nick'], 'roles' : json['roles']}

        else:
            return {'status': code, 'error' : "member couldn't be found in guild and wasn't given instant invite"}

#Adding user to the designated guild
    async def add_user_to_guild(self, access_token, user_discord_id):

        async with rate_limit_put:

            adding_user = requests.put(
                f"{self.discord_api_base_url}/guilds/{GUILD_ID}/members/{user_discord_id}",
                headers={'Authorization': f'Bot {self.bot_secret}',
                        "Content-Type": "application/json"
                        }
                ,json={
                    "access_token": access_token
                }
            )


            return {'status': adding_user.status_code, 'error' : "member couldn't be added to the guild"}

#Updating user with specified nick and roles

    async def user_update(self, user_discord_id, nick : str, roles : list):

        async with rate_limit_patch:

            updating_user = requests.patch(
                f"{self.discord_api_base_url}/guilds/{GUILD_ID}/members/{user_discord_id}",
                headers={'Authorization': f'Bot {self.bot_secret}',
                        "Content-Type": "application/json"
                        }
                ,json={
                    "nick" : nick,
                    "roles" : roles
                }
            )

            return {'status': updating_user.status_code, 'error' : "member wasn't given any roles nor nickname"}   



da = DiscordApi(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, DISCORD_API_BASE_URL, BOT_SECRET)


