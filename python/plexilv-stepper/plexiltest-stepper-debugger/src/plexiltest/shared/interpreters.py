from abc import ABC, abstractmethod


class StepperInterpreter(ABC):

    @abstractmethod
    def needs_step(self) -> bool:
        """Check if the interpreter can execute one more macro step."""
        pass

    @abstractmethod
    def step(self, script_input: str) -> None:
        """Execute the next macro step."""
        pass

    @abstractmethod
    def get_current_state(self) -> dict:
        """Returns the current state of execution of interpreter."""
        pass