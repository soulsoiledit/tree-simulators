from lib import Logs, State, StateConfig


class Tree:
    def __init__(self, states: StateConfig) -> None:
        self.states = states

    def grow(self, state: State) -> Logs:
        raise NotImplementedError("please implement grow()")
