from typing import Annotated
from fastapi import Cookie

getSessionIdDep = Annotated[
    str, Cookie(None, alias="session_id")
]  # TODO: romove None from here in future
getUserIdDep = Annotated[
    str, Cookie(None, alias="user_id")
]  # TODO: romove None from here in future
