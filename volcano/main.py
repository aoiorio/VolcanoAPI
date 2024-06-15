from fastapi import FastAPI, UploadFile, File
from typing import Annotated

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


# def get_audio_url(data: bytes):
#     s3 = boto3.resource(
#         service_name="s3",
#         aws_access_key_id="a2zqH4VUSKLpf1Jq",
#         aws_secret_access_key="IHfnyUJF5wFjsMfMtCi5TvPJrm7kPiZamTdouX5w",
#         endpoint_url="https://s3.tebi.io",
#     )
#     bucket = s3.Bucket('volcano-bucket')
#     object = bucket.Object('IMG_2644.mp3')
#     response = object.get()
#     print(response)
#     body = response['Body']
#     print(body)
#     bucket.put_object(Key='test.mp3', Body=data)

#     return "https://s3.tebi.io/" + 'volcano-bucket/' + 'test.mp3'
#     # for bucket in s3.buckets.all():
#     #     return bucket.name


@app.get("/")
async def hello():
    return {"message": "Hi World"}


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     new_file = await file.read()
#     url = get_audio_url(new_file)

#     return {"bucket": url}


# NOTE This function is for creating tables
create_tables()

app.include_router(v1_routes, prefix="/api/v1")
handler = Mangum(app)
