from typing import List

from pydantic import BaseModel
from nb_cli.config import Adapter


class AdapterInResponse(BaseModel):
    adapters: List[Adapter]
