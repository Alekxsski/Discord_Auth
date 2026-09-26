from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from backend.DiscordUserManager import dum
import uvicorn

code_check_query = "SELECT uuid FROM auth_codes WHERE code = %s" 
code_remove_query = "DELETE FROM auth_codes WHERE code = %s"
connect_account_query = "INSERT INTO player_discord (uuid, discord_user_id) VALUES (%s, %s)"  

app = FastAPI()

@app.get("/callback")
async def callback(code : str, state : str):

    action = await dum.manage_user(token_code=code, state_code=state)

    if action['status'] == 200:

        return RedirectResponse(url="https://discord.com/channels/@me")

    else:
        
        return action

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
