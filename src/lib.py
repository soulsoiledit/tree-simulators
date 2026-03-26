from fractions import Fraction
from typing import Collection

type IntCollection = Collection[int]
type StateConfig = list[IntCollection]
type State = tuple[int, ...]

type LogAmount = Fraction | float
type Logs = list[LogAmount]


def format_list[A](list: list[A]) -> str:
    return f"[{', '.join(map(str, list))}]"


def uniform(lower: int, upper: int) -> range:
    return range(lower, upper + 1)


def weighted(config: dict[int, int]) -> list[int]:
    return [k for k, v in config.items() for _ in range(v)]


def safe_inc[T: (float, Fraction)](
    logs: list[T], index: int, amount: T, fallback: T | None = None
):
    length = len(logs)
    if index >= length:
        if fallback is None:
            fallback = type(amount)()
        logs.extend([fallback] * (index - length + 1))
    logs[index] = logs[index] + amount
