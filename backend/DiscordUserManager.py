from .Config import ROLES_TO_SYNC, DEFAULT_ROLE

code_check_query = "SELECT uuid FROM auth_codes WHERE code = %s" 
code_remove_query = "DELETE FROM auth_codes WHERE code = %s"
connect_account_query = "INSERT INTO player_discord (uuid, discord_user_id) VALUES (%s, %s)" 
user_data_from_mc_query = "SELECT username, primary_group FROM luckperms_players WHERE uuid = %s" 

class DiscordUserManager():

    def __init__(self,database, discordapi):
        self.roles_to_sync = ROLES_TO_SYNC
        self.default_role = DEFAULT_ROLE
        self.database = database
        self.discordapi = discordapi


    async def validate_code_return_uuid(self, code):
        return await self.database.execute_query(code_check_query, (code,) )


    async def remove_code_from_database(self, code):
        await self.database.execute_query(code_remove_query, (code,), True)


    async def connect_accounts(self, uuid, discord_user_id):
        await self.database.execute_query(connect_account_query, (uuid, discord_user_id), True)


    async def retrive_user_mc_data(self, uuid):
        return await self.database.execute_query(user_data_from_mc_query, (uuid,))

    def retrive_external_roles(self, roles: list):

        for i in roles:
            if i in self.roles_to_sync:
                roles.remove(i)

        return roles


    async def manage_user(self,token_code, state_code):

        uuid = await self.validate_code_return_uuid(state_code)

        #Check if code is valid and returns uuid
        if uuid:

            uuid = uuid[0][0]

            #Removes code from database
            await self.remove_code_from_database(state_code)

            #Exchanging provided token for auth token
            print(token_code)
            
            user_token = await self.discordapi.get_user_token(token_code)

            if user_token['status'] != 200:
                return user_token

            #Gets user discord id
            user = await self.discordapi.get_user_discord_id(user_token['access_token'])

            if user['status'] != 200:
                return user

            user_discord_id = user['user_discord_id']

            #Check if member is already in guild
            member = await self.discordapi.get_member(user_discord_id)

            #Empty roles 
            roles = []

            if member['status'] == 200:

                roles = self.retrive_external_roles(member['roles'])
                

            elif member['status'] == 404:

                await self.discordapi.add_user_to_guild(access_token = user_token['access_token'],user_discord_id = user_discord_id)

                mc_data = await self.retrive_user_mc_data(uuid)

            else:
                return member

            #Retriving user mc data such as primary group and nickname
            mc_data = await self.retrive_user_mc_data(uuid)

            if mc_data != None:

                nick = mc_data[0][0]

                primary_role = self.roles_to_sync[mc_data[0][1]]

                base_role = self.roles_to_sync['base_role']

                default_role = self.roles_to_sync['default']

                roles.append(primary_role)

                if 'base_role' in self.roles_to_sync.keys():
                    roles.append(base_role)

                if primary_role != default_role and self.default_role:
                    roles.append(self.roles_to_sync['base_role'])
                    
                await self.discordapi.user_update(user_discord_id = user_discord_id, nick = nick ,roles = roles)


            else:

                return {'status' : 500, 'error' : "user has been added to the guild but not updated data couldn't be fetched"}

            await self.connect_accounts(uuid,user_discord_id)

            return {'status' : 200}
            
        else:

            return {'status' : 404, 'error' : "code is invalid or has already expired"}



            

            










    