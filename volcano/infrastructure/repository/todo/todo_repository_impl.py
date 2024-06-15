# NOTE This file is for implementing todo_repository.py file in domain/repository folder
# NOTE You can use abc package to create class as implements class
from typing import Optional
from sqlalchemy.orm.session import Session
from fastapi import UploadFile
import boto3
import random, string
from datetime import datetime

# NOTE Project Libraries
from ....domain.entity.todo import Todo
from ....domain.repository.todo.todo_repository import TodoRepository
from ...postgresql.dto.todo_dto import TodoDTO
from ..auth.auth_repository_impl import AuthRepository, AuthRepositoryImpl
from ....core.config import TEBI_ACCESS_KEY_ID, TEBI_SECRET_ACCESS_KEY, TEBI_URL, TEBI_BUCKET_NAME


def generate_random_audio_name(range: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=range))

# NOTE I think I can prepare audio_url here as a function and set it in execute_post_todo method
def get_audio_url(data: bytes):
    s3 = boto3.resource(
        service_name="s3",
        aws_access_key_id=TEBI_ACCESS_KEY_ID,
        aws_secret_access_key=TEBI_SECRET_ACCESS_KEY,
        endpoint_url="https://s3.tebi.io",
    )
    audio_name = generate_random_audio_name(12)
    print(audio_name)
    bucket = s3.Bucket(TEBI_BUCKET_NAME)
    bucket.put_object(Key=f"{audio_name}.mp3", Body=data)

    # return "https://s3.tebi.io/" + 'volcano-bucket/' + audio_name
    return f"{TEBI_URL}/{TEBI_BUCKET_NAME}/{audio_name}.mp3"


class TodoRepositoryImpl(TodoRepository):
    def __init__(self, db: Session):
        self.db: Session = db

    def post_todo(self, user_id: str, bytes_audio: bytes) -> Optional[Todo]:
        # NOTE Convert Todo that is from user to TodoDTO
        try:
            # TODO Create function that returns Todo that are recognized from bytes_audio and define it as recognized_todo
            # TODO if there's no type in the audio I'll return type "other"
            recognized_todo = Todo(title="Create Voice-Recognized feature", type="Programming", period=datetime.now())
            todo_dto = TodoDTO.from_entity(recognized_todo)
            todo_dto.audio_url = get_audio_url(bytes_audio)
            print(todo_dto.audio_url)
            # NOTE I will write the code of getting user_id by using authRepository in UseCase file
            # ! This file mustn't use other repository's methods, use case file will do it
            todo_dto.user_id = user_id

            # NOTE store data to db
            self.db.add(todo_dto)
            self.db.commit()

            return todo_dto.to_entity()
        except:
            raise
