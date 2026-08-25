from abc import ABC, abstractmethod


class Interpreter(ABC):

    @abstractmethod
    def needs_step(self) -> bool:
        """Check if the interpreter can execute one more macro step."""
        pass

    @abstractmethod
    def step(self) -> None:
        """Execute the next macro step."""
        pass

    @abstractmethod
    def get_current_state(self) -> dict:
        """Returns the current state of execution of interpreter."""
        pass
