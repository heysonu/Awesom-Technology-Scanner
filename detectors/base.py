from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class Technology:
    def __init__(self, name: str, version: Optional[str] = None, confidence: float = 1.0):
        self.name = name
        self.version = version
        self.confidence = confidence

    def __repr__(self):
        return f"Technology(name={self.name}, version={self.version}, confidence={self.confidence})"


class Detector(ABC):
    @abstractmethod
    def detect(self, url: str) -> List[Technology]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
