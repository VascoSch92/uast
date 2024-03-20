from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

import numpy as np

CONST = Path().cwd()
GLOBAL, ANOTHER_GLOBAL = "GLOBAL", "ANOTHER_GLOBAL"


class Base(ABC):
    @abstractmethod
    def base(self, d: Union[str, int], c: np.ndarray):
        raise NotImplementedError


class Foo(Base):
    CONST_1 = 0
    CONST_2: str = "A"

    def __init__(self, a: int, b: str):
        self.a = a
        self.b = b

    def base(self, d, c: float = 0.99) -> int:
        return self.a + 0


class Bar:
    @staticmethod
    def bar() -> int:
        return 0
