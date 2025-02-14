import re
import unicodedata


def slugify(string):
    """Slugify string."""

    return (
        re.sub(r"[^\w\s-]", "", unicodedata.normalize("NFKD", string).encode("ascii", "ignore").decode("utf-8"))
        .strip()
        .lower()
    )
