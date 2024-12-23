import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Hashable
from pydantic import BaseModel

ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))


class GameStateNotfound(Exception):
    """
    Exception raised when a game state is not found.
    """

    pass


class GameStateDDM(BaseModel):
    """
    Data model for game state.

    :param id: Unique identifier for the game state.
    :param session_id: Identifier for the session associated with the game state.
    """

    id: Hashable
    session_id: Hashable


class GameStateManager(ABC):
    """
    Abstract base class for managing game states.
    """

    @abstractmethod
    def save(self, state: GameStateDDM) -> None:
        """
        Save the game state.

        :param state: The game state to save.
        """

        pass

    @abstractmethod
    def load(self, state_id: Hashable) -> GameStateDDM:
        """
        Load the game state.

        :param state_id: The identifier of the game state to load.
        :return: The loaded game state.
        :raises GameStateNotfound: If the game state is not found.
        """

        pass

    @abstractmethod
    def delete(self, state_id: Hashable) -> None:
        """
        Delete the game state.

        :param state_id: The identifier of the game state to delete.
        :raises GameStateNotfound: If the game state is not found.
        """

        pass

    @abstractmethod
    def update(self, state_id: Hashable, state: GameStateDDM) -> None:
        """
        Update the game state.

        :param state_id: The identifier of the game state to update.
        :param state: The updated game state.
        :raises GameStateNotfound: If the game state is not found.
        """

        pass


class MemoryGameStateManager(GameStateManager):
    """
    In-memory implementation of GameStateManager.
    """

    def __init__(self):
        """
        Initialize the in-memory storage.
        """

        self.storage = {}

    def save(self, state: GameStateDDM) -> None:
        """
        Save the game state in memory.

        :param state: The game state to save.
        """

        self.storage[state.id] = state

    def load(self, state_id: Hashable) -> GameStateDDM:
        """
        Load the game state from memory.

        :param state_id: The identifier of the game state to load.
        :return: The loaded game state.
        :raises GameStateNotfound: If the game state is not found.
        """

        state = self.storage.get(state_id)
        if state is None:
            raise GameStateNotfound(f"State for session {state_id} not found.")
        return state

    def delete(self, state_id: Hashable) -> None:
        """
        Delete the game state from memory.

        :param state_id: The identifier of the game state to delete.
        :raises GameStateNotfound: If the game state is not found.
        """

        if state_id not in self.storage:
            raise GameStateNotfound(f"State for session {state_id} not found.")
        del self.storage[state_id]

    def update(self, state_id: Hashable, state: GameStateDDM) -> None:
        """
        Update the game state in memory.

        :param state_id: The identifier of the game state to update.
        :param state: The updated game state.
        :raises GameStateNotfound: If the game state is not found.
        """

        if state_id not in self.storage:
            raise GameStateNotfound(f"State for session {state_id} not found.")
        self.storage[state_id] = state
