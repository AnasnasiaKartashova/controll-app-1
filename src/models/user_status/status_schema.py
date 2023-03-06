from typing import Optional
from pydantic import BaseModel


class UserStatusSchema(BaseModel):
    last_lesson: Optional[str]
    # numbers_of_test_topic: Optional[str]
    # days: Optional[str]