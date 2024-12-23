from pydantic import BaseModel
from typing import Hashable


class PlayerDDM(BaseModel):
    """
    Represents a player in the game.
    """

    id: Hashable

    def __str__(self) -> str:
        return f"Player {self.id}"
