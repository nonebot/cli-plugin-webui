from typing import List

from pydantic import BaseModel
from nb_cli.config import Driver


class DriverInResponse(BaseModel):
    drivers: List[Driver]
