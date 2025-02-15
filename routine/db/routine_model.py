import time

from surrealdb import RecordID

from .db import get_db

TABLE = "routine_model"


def get_latest_routine(user: str) -> dict | None:
    db = get_db()
    routine_model = db.query(
        f"SELECT * FROM ONLY {TABLE} WHERE user = $user ORDER BY timestamp DESC LIMIT 1",  # noqa: S608
        {"user": user},
    )
    return routine_model


def get_routine(ref: RecordID | str) -> dict:
    if isinstance(ref, str):
        ref = RecordID(TABLE, ref)
    db = get_db()
    routine_model = db.select(ref)
    return routine_model


def create_routine(data: dict, user: str) -> RecordID:
    db = get_db()
    ref: RecordID = db.create(TABLE, data | {"user": user, "timestamp": int(time.time())})["id"]
    return ref


def update_routine(ref: RecordID, data: dict, user: str) -> None:
    db = get_db()
    db.update(ref, data | {"user": user})
