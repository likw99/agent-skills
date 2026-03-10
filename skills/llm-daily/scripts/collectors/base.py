from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple


class BaseCollector(ABC):
    """Abstract base class for all data collectors"""

    @abstractmethod
    def collect_data(self, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def format_for_llm(self, data: Dict[str, Any]) -> str:
        pass

    def run(self, **kwargs) -> Tuple[str, Dict[str, Any]]:
        try:
            data = self.collect_data(**kwargs)
            formatted_data = self.format_for_llm(data)
            return formatted_data, data
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
            return f"Error collecting data: {e}", {}

    def get_statistics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {}
