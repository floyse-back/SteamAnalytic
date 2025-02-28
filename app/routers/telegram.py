from fastapi import APIRouter

app = APIRouter()

@app.get("/telegram")
async def telegram():
    return {"message":"add"}

@app.get("/telegram/best_games")
async def steam_best_salles():
    return {"message":"Steam salles"}