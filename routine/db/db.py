import os
from functools import lru_cache

from surrealdb import Surreal


@lru_cache
def get_db():
    """Get and cache a SurrealDB connection."""
    db = Surreal(os.getenv("DB_URL"))
    db.signin({"username": os.getenv("DB_USER"), "password": os.getenv("DB_PWD")})
    db.use("default", "default")
    return db
