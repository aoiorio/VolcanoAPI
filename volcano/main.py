from fastapi import FastAPI
from mangum import Mangum
from .core.config import APP_NAME, VERSION
from .model.base_model import init_db
from .api.v1.routes import routes as v1_routes
# This is Volcano

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
)


@app.get("/")
async def hello():
    return {"message": "World"}



init_db()

app.include_router(v1_routes, prefix="/api/v1")
handler = Mangum(app)
