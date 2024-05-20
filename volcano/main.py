from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def hello():
    return {'message': 'World'}

handler = Mangum(app)