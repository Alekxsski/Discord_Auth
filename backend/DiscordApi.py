import aiohttp

from .Config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, DISCORD_API_BASE_URL, BOT_SECRET, GUILD_ID
from aiolimiter import AsyncLimiter

rate_limit_get = AsyncLimiter(5,5)

rate_limit_post = AsyncLimiter(5,5)

rate_limit_put = AsyncLimiter(1,1)

rate_limit_patch = AsyncLimiter(1,1)



class DiscordApi:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_url = REDIRECT_URI
        self.bot_secret = BOT_SECRET
        self.guild_id = GUILD_ID
        self.base_url = DISCORD_API_BASE_URL
        self.session = None

    async def start(self):
        self.session = aiohttp.ClientSession(base_url=self.base_url)
        print("session has been created")

    async def close(self):
        self.session.close()

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

            response = await self.session.request(method = "POST", url = "oauth2/token", data=data, headers=headers)

            if response.status == 200:
                json = await response.json()
                
                return {'status': 200, 'access_token': json["access_token"]}

            else:

                return{'status': response.status, 'error' : "there was issue with token authorization"}

#Accessing user informations with granted token
    async def get_user_discord_id(self, user_token):
        
        async with rate_limit_get:

            response = await self.session.request(method = "GET",url = "users/@me", headers={'Authorization': f'Bearer {user_token}'})

            code = response.status

            if code != 200:
                return {'status': code, 'error': "Member id couldn't be found"}

            else:
                json = await response.json()
                return {'status': code, 'user_discord_id': json['id']}

#Checking guild for member
    async def get_member(self,member_id):

        response = await self.session.request(method = "GET", url=f"guilds/{self.guild_id}/members/{member_id}", headers={'Authorization': f'Bot {self.bot_secret}',
                        "Content-Type": "application/json"
                        })

        code = response.status

        if code == 200:
            json = await response.json()
            return {'status': code, 'nick': json['nick'], 'roles' : json['roles']}

        else:

            return {'status': code, 'error' : "member couldn't be found in guild and wasn't given instant invite"}

#Adding user to the designated guild
    async def add_user_to_guild(self, access_token, user_discord_id):

        async with rate_limit_put:

            response = await self.session.request(method = "PUT", url=f"guilds/{self.guild_id}/members/{user_discord_id}",headers={'Authorization': f'Bot {self.bot_secret}',
                "Content-Type": "application/json"}, json={"access_token": access_token})

            return {'status': response.status, 'error' : "member couldn't be added to the guild"}

#Updating user with specified nick and roles

    async def user_update(self, user_discord_id, nick : str, roles : list):

        async with rate_limit_patch:

            response = await self.session.request(method = "PATCH", url = f"guilds/{self.guild_id}/members/{user_discord_id}", headers={'Authorization': f'Bot {self.bot_secret}',
                "Content-Type": "application/json"}, json={"nick" : nick, "roles" : roles})

            return {'status': response, 'error' : "member wasn't given any roles nor nickname"}   



