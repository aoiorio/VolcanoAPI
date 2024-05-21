from fastapi import FastAPI
from mangum import Mangum

# This is Volcano

app = FastAPI()

@app.get("/")
async def hello():
    return {'message': 'World'}

handler = Mangum(app)