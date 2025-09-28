"""Shell handler interface"""

from abc import ABC, abstractmethod


class IShell(ABC):
    """Abstract base class for shell handlers."""

    @abstractmethod
    def run(self, command: str) -> None:
        """Run a command in the shell."""
        raise NotImplementedError

    @abstractmethod
    def readline(self) -> str:
        """Read a line from the shell output."""
        raise NotImplementedError
