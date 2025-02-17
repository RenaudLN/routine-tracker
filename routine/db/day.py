from surrealdb import RecordID

from .db import get_db

TABLE = "day"


def get_day(date: str, user: str) -> dict | None:
    """Get day."""
    db = get_db()
    day = db.query(
        f"SELECT * FROM ONLY {TABLE} WHERE date = $date AND user = $user LIMIT 1",  # noqa: S608
        {"date": date, "user": user},
    )
    return day


def get_day_ref(date: str, user: str) -> RecordID | None:
    """Get day."""
    db = get_db()
    ref: RecordID | None = db.query(
        f"SELECT VALUE id FROM ONLY {TABLE} WHERE date = $date AND user = $user LIMIT 1",  # noqa: S608
        {"date": date, "user": user},
    )
    return ref


def get_dates(user: str, limit: int = 31) -> list[str]:
    """Get dates."""
    db = get_db()
    dates: list[str] = db.query(
        f"SELECT VALUE date FROM {TABLE} WHERE user = $user ORDER BY date LIMIT $limit",  # noqa: S608
        {"user": user, "limit": limit},
    )
    return dates


def create_day(data: dict, user: str) -> RecordID:
    """Create day."""
    db = get_db()
    ref: RecordID = db.create(TABLE, data | {"user": user})["id"]
    return ref


def update_day(day_id: RecordID, data: dict, user: str) -> None:
    """Update day."""
    db = get_db()
    db.update(day_id, data | {"user": user})


def merge_day(day_id: RecordID, data: dict) -> None:
    """Update day."""
    db = get_db()
    db.merge(day_id, data)


def count_days_using_routine(routine_ref: RecordID, today: str) -> int:
    db = get_db()
    result = db.query(
        f"SELECT COUNT(), routine_ref FROM {TABLE} WHERE routine_ref = $routine_ref "  # noqa: S608
        "AND date < $today GROUP BY routine_ref",
        {"routine_ref": routine_ref, "today": today},
    )
    if result:
        return result[0]["count"]
    return 0
