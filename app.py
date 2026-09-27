from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from backend.DiscordUserManager import DiscordUserManager
from backend.DataBase import Database
from backend.DiscordApi import DiscordApi

import uvicorn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    discordApi = DiscordApi()
    dataBase = Database()

    await discordApi.start()
    await dataBase.start()

    app.state.dum = DiscordUserManager(discordapi = discordApi, database = dataBase)

    try:
        yield
    finally:
        await discordApi.close()


app = FastAPI(lifespan=lifespan)

@app.get("/callback")
async def callback(code : str, state : str):

    action = await app.state.dum.manage_user(token_code=code, state_code=state)

    if action['status'] == 200:

        return RedirectResponse(url="https://discord.com/channels/@me")

    else:

        return action

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)