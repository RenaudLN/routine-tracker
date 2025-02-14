from surrealdb import RecordID

from .db import get_db

DAY_TABLE = "day"


def get_day(date: str, user: str) -> dict | None:
    """Get day."""
    db = get_db()
    day = db.query(
        f"SELECT * FROM ONLY {DAY_TABLE} WHERE date = $date AND user = $user LIMIT 1",  # noqa: S608
        {"date": date, "user": user},
    )
    return day


def get_day_ref(date: str, user: str) -> RecordID | None:
    """Get day."""
    db = get_db()
    ref: RecordID | None = db.query(
        f"SELECT VALUE id FROM ONLY {DAY_TABLE} WHERE date = $date AND user = $user LIMIT 1",  # noqa: S608
        {"date": date, "user": user},
    )
    return ref


def get_dates(user: str, limit: int = 31) -> list[str]:
    """Get dates."""
    db = get_db()
    dates: list[str] = db.query(
        f"SELECT VALUE date FROM {DAY_TABLE} WHERE user = $user ORDER BY date LIMIT $limit",  # noqa: S608
        {"user": user, "limit": limit},
    )
    return dates


def create_day(data: dict, user: str) -> None:
    """Create day."""
    db = get_db()
    db.create("day", data | {"user": user})


def update_day(day_id: str, data: dict, user: str) -> None:
    """Update day."""
    db = get_db()
    db.update(day_id, data | {"user": user})
