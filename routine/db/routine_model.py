import time

from surrealdb import RecordID

from routine.routine_maker import get_default_routine_maker

from .db import get_db

TABLE = "routine_model"


def get_latest_routine(user: str) -> dict:
    db = get_db()
    routine_model = db.query(
        f"SELECT * FROM ONLY {TABLE} WHERE user = $user ORDER BY timestamp DESC LIMIT 1",  # noqa: S608
        {"user": user},
    )
    if not routine_model:
        data = get_default_routine_maker().model_dump()
        routine_ref = create_routine(data, user)
        return data | {"id": str(routine_ref)}
    return routine_model


def get_routine(ref: RecordID | str) -> dict:
    if isinstance(ref, str):
        if not ref.startswith(f"{TABLE}:"):
            raise ValueError(f"Invalid ref {ref} for {TABLE}")
        ref = RecordID(*ref.split(":", maxsplit=1))
    db = get_db()
    routine_model = db.select(ref)
    return routine_model


def create_routine(data: dict, user: str) -> RecordID:
    db = get_db()
    ref: RecordID = db.create(TABLE, data | {"user": user, "timestamp": int(time.time())})["id"]
    return ref


def update_routine(ref: RecordID, data: dict, user: str) -> None:
    db = get_db()
    db.update(ref, data | {"user": user, "timestamp": int(time.time())})
