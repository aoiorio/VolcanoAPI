# NOTE This file is for implementing todo_repository.py file in domain/repository folder
# NOTE You can use abc package to create class as implements class
from typing import Optional
from sqlalchemy.orm.session import Session
import boto3
import random, string
from datetime import datetime

import dateparser
import uuid

from volcano.domain.entity.goal_info import GoalInfo, MonthGoalObject, TodayGoalObject
from volcano.domain.entity.read_todo import ReadTodo


# NOTE Project Libraries
from ...domain.entity.todo import Todo
from ...domain.repository.todo import TodoRepository
from ..postgresql.dto.todo import TodoDTO
from ...core.config import (
    TEBI_ACCESS_KEY_ID,
    TEBI_SECRET_ACCESS_KEY,
    TEBI_URL,
    TEBI_BUCKET_NAME,
)


def generate_random_audio_name(range: int):
    return "".join(random.choices(string.ascii_letters + string.digits, k=range))


# NOTE I think I can prepare audio_url here as a function and set it in execute_post_todo method
def get_audio_url(data: bytes):
    s3 = boto3.resource(
        service_name="s3",
        aws_access_key_id=TEBI_ACCESS_KEY_ID,
        aws_secret_access_key=TEBI_SECRET_ACCESS_KEY,
        endpoint_url=TEBI_URL,
    )
    audio_name = generate_random_audio_name(12)
    print(audio_name)
    bucket = s3.Bucket(TEBI_BUCKET_NAME)
    bucket.put_object(Key=f"{audio_name}.mp3", Body=data)

    return f"{TEBI_URL}/{TEBI_BUCKET_NAME}/{audio_name}.mp3"


# NOTE search the values' index of title, description, period, type and priority (search where the value is)
def gen_idx_lst(text: str):
    split_voice_text = text.split()
    # TODO add due date here and see what will happen
    value_lst = ["title", "description", "period", "type", "priority"]
    idx_lst = []

    for i in range(len(split_voice_text)):
        value = split_voice_text[i]
        if value in value_lst:
            idx = text.find(value)
            idx_lst.append(idx)
    idx_lst.sort()
    return idx_lst


# NOTE add the values to specific key of dictionary(todo_dict)
def add_value_to_todo(text: str, todo_dict: dict):
    try:
        split_text = text.split()
        value = split_text[0]
        split_text.pop(0)

        # NOTE join values that is not including the value name
        result_value = " ".join(split_text)

        # NOTE add to todo dictionary the value
        todo_dict[value] = result_value
    except IndexError:
        print(
            "index error occurred, I do not know but it will be succeeded so it will be ok"
        )


class TodoRepositoryImpl(TodoRepository):
    def __init__(self, db: Session):
        self.db: Session = db

    def post_todo(
        self,
        user_id: uuid.UUID,
        bytes_audio: bytes,
        title: str,
        description: str,
        type: str,
        period: datetime,
        priority: int,
    ) -> Optional[Todo]:
        # NOTE Convert Todo that is from user to TodoDTO
        try:
            # TODO Create function that returns Todo that are recognized from bytes_audio and define it as recognized_todo
            # TODO if there's no type in the audio I'll return type "other"
            recognized_todo = Todo(
                user_id=user_id,
                title=title,
                description=description,
                period=period,
                type=type,
                priority=priority,
                audio_url=get_audio_url(bytes_audio),
            )
            todo_dto = TodoDTO.from_entity(recognized_todo)
            # LINK- I will write the code of getting user_id by using authRepository in UseCase file
            # ! This file mustn't use other repository's methods, use case file will do it

            # NOTE store data to db
            self.db.add(todo_dto)
            self.db.commit()

            return todo_dto.to_entity()
        except:
            raise

    def text_to_todo(self, voice_text: str) -> Optional[Todo]:
        todo = Todo()
        todo_dict = {
            "title": "",
            "description": "",
            "period": "",
            "type": "",
            "priority": 1,
        }
        # NOTE change voice_text to lowercase letters
        voice_text = voice_text.lower()

        voice_text = voice_text.replace(".", " period")
        # NOTE replace due date to period to cover all expressions
        voice_text = voice_text.replace("due date", " period")
        idx_lst = gen_idx_lst(voice_text)

        for i in range(len(idx_lst)):
            text = ""

            # NOTE if i is the last value
            if len(idx_lst) - 1 == i:
                text = voice_text[idx_lst[i]:]
                add_value_to_todo(text, todo_dict)
                break

            text = voice_text[idx_lst[i]:idx_lst[i + 1]]
            add_value_to_todo(text, todo_dict)
        print(todo_dict)

        if todo_dict["period"] == "":
            todo_dict["period"] = "tomorrow"

        fix_period = dateparser.parse(todo_dict["period"])

        # NOTE fix the dates to property one (e.g. tomorrow to 2024-xxxx-xxxx)
        # ! search_dates method takes too long
        # fix_period = search_dates(todo_dict["period"])
        if fix_period is not None:
            todo_dict["period"] = fix_period
        else:
            fix_period = dateparser.parse("tomorrow")
            todo_dict["period"] = fix_period
        print("add period")

        if todo_dict["type"] == "":
            todo_dict["type"] = "others"

        # NOTE convert todo_dict to todo
        todo.title = todo_dict["title"]
        todo.description = todo_dict["description"]
        todo.period = todo_dict["period"]
        todo.type = todo_dict["type"]

        # NOTE if priority is a string, I'll return 3
        try:
            todo.priority = int(todo_dict["priority"])
        except:
            todo.priority = 3

        return todo

    def post_todo_from_text(
        self,
        user_id: uuid.UUID,
        title: str,
        description: str,
        type: str,
        period: datetime,
        priority: int,
    ) -> Optional[Todo]:
        try:
            recognized_todo = Todo(
                user_id=user_id,
                title=title,
                description=description,
                period=period,
                type=type,
                priority=priority,
            )
            todo_dto = TodoDTO.from_entity(recognized_todo)

            # NOTE store data to db
            self.db.add(todo_dto)
            self.db.commit()

            return todo_dto.to_entity()
        except:
            raise

    def read_todo(self, user_id: uuid.UUID) -> Optional[list[ReadTodo]]:
        try:
            user_todo: list[TodoDTO] = (
                self.db.query(TodoDTO).filter_by(user_id=user_id).all()
            )
            # NOTE distinguish the todo with type (e.g. [{"type": "programming", "values": [todo...]}, {"type": "programming", "values": [todo...]}])
            user_todo_with_type = []

            for todo in user_todo:
                # NOTE check the dict is including todo.type key or not
                if any(value["type"] == todo.type for value in user_todo_with_type):
                    # NOTE index will be the index that its dict["type"] equals to todo.type in user_todo_with_type
                    index = next(
                        i
                        # NOTE i is like an index such as 0, 1, 2, 3...., dict is the content of user_todo_with_type
                        for i, dict in enumerate(user_todo_with_type)
                        # NOTE if todo.type equals to dict["type"], return i
                        if todo.type == dict["type"]
                    )
                    user_todo_with_type[index]["values"].append(todo)
                else:
                    # NOTE if there's no type called todo.type, I will add the dict of the type
                    user_todo_with_type.append({"type": todo.type, "values": [todo]})

            return user_todo_with_type
        except:
            raise

    def update_todo(self, todo_id: str, new_todo: Todo) -> Optional[Todo]:
        try:
            todo: Todo = self.db.query(TodoDTO).filter_by(todo_id=todo_id).first()

            if todo is None:
                raise

            # NOTE update values
            todo.title = new_todo.title
            todo.description = new_todo.description
            todo.priority = new_todo.priority
            todo.period = new_todo.period
            todo.audio_url = new_todo.audio_url
            todo.type = new_todo.type
            todo.is_completed = new_todo.is_completed

            self.db.commit()

            return todo
        except:
            raise

    def delete_todo(self, todo_id: str) -> Optional[Todo]:
        try:
            todo = self.db.query(TodoDTO).filter_by(todo_id=todo_id).first()

            self.db.delete(todo)
            self.db.commit()
        except:
            raise

    def get_goal_info(self, user_id: uuid.UUID) -> Optional[GoalInfo]:
        today = datetime.today()

        today_goal_count = 0
        month_goal_count = 0
        today_todo_count = 0
        month_todo_count = 0
        today_goal_percentage = 0
        month_goal_percentage = 0

        try:
            todo: list[Todo] = self.db.query(TodoDTO).filter_by(user_id=user_id).all()
        except:
            raise

        today_todo = []
        month_todo = []

        # summarize today todo and month todo
        for item in todo:
            if item.period.day == today.day and item.period.month == today.month:
                today_todo.append(item)
            if item.period.month == today.month:
                month_todo.append(item)

        for item in todo:
            # NOTE if the todo's period matches today and it completed, 1 adds to today_goal_percentage
            if (
                item.period.year == today.year and item.period.month == today.month and item.period.day == today.day
            ):
                today_todo_count += 1

                if item.is_completed:
                    today_goal_count += 1

            if item.period.year == today.year and item.period.month == today.month:
                month_todo_count += 1

                if item.is_completed:
                    month_goal_count += 1

        # NOTE if there's no today's goal or month's goal, it'll be 100.0
        if today_todo_count == 0:
            today_goal_percentage = 100.0
        else:
            today_goal_percentage = round(today_goal_count / today_todo_count * 100, 1)

        if month_todo_count == 0:
            month_goal_percentage = 100.0
        else:
            month_goal_percentage = round(month_goal_count / month_todo_count * 100, 1)

        # NOTE get today goal object
        today_goal_object = TodayGoalObject(
            today_goal_percentage=today_goal_percentage,
            today_todo=today_todo,
        )

        # NOTE get month goal object
        month_goal_object = MonthGoalObject(
            month_goal_percentage=month_goal_percentage,
            month_todo=month_todo
        )

        goal_info = GoalInfo(today_goal=today_goal_object, month_goal=month_goal_object)

        return goal_info
