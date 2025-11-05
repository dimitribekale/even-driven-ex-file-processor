from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseProcessor(ABC):

    @abstractmethod
    def can_process(self, file_path: str) -> bool:
        """Check if this processor can handle the given file"""
        pass

    @abstractmethod
    def process(self, file_path: str) -> Dict[str, Any]:
        """Process the file and return results"""
        pass

    @property
    @abstractmethod
    def process_name(self) -> str:
        """Return the name of the processor"""
        pass