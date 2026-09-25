from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from backend.Discord_Oauth import da
from backend.database import db
import uvicorn

code_check_query = "SELECT uuid FROM auth_codes WHERE code = %s" 
code_remove_query = "DELETE FROM auth_codes WHERE code = %s"
connect_account_query = "INSERT INTO player_discord (uuid, discord_user_id) VALUES (%s, %s)"  

app = FastAPI()

@app.get("/callback")
async def callback(code : str, state : str):

    uuid = db.execute_query(code_check_query, (state,) )

    if uuid:

        uuid = uuid[0][0]

        get_user_token = await da.get_user_token(code = code, state = state)

        if get_user_token[0] != 200:
            return {"Wystąpił bład niepoprawny token": 'przyjdź na nasz discord i spróbujemy to naprawić!', "błąd" : get_user_token[0]}

        get_user_data = await da.get_user_data(get_user_token[1])

        db.execute_query(code_remove_query,(state,),True)

        if get_user_data[0] in [200,201,204] :

            db.execute_query(connect_account_query,(uuid, get_user_data[1],),True)

            return RedirectResponse('https://discord.com/channels/@me')
        
        else:
            
            return {"Wystąpił bład twoje konto nie zostało połaczone": 'przyjdź na nasz discord i spróbujemy to naprawić!', "błąd" : get_user_data[0]}

    return {"Wystąpił bład": 'Kod wygasł'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
