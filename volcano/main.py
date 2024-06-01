from fastapi import FastAPI
from mangum import Mangum
from .core.config import APP_NAME, VERSION
from .infrastructure.postgresql.database import create_tables
from .api.v1.routes import routes as v1_routes
# This is Volcano

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    # root_path="/dev/",
)


@app.get("/")
async def hello():
    return {"message": "Hi World"}


# NOTE This function is for creating tables
create_tables()

app.include_router(v1_routes, prefix="/api/v1")
handler = Mangum(app)
