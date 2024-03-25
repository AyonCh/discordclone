from jwt import encode
from datetime import datetime, timezone, timedelta


def generate(payload):
    payload["exp"] = datetime.now(timezone.utc) + timedelta(days=30)
    token = encode(
        payload=payload,
        key="jxuETMWRmDDwcKOFxrapXIuXh4uc4ZlvZacf9TAYhBo=",
        algorithm="HS256",
    )

    return token
