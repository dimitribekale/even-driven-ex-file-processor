import os
import json
from processors.base_processor import BaseProcessor

class JSONProcessor(BaseProcessor):

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(".json")
    
    def process(self, file_path: str) -> dict:
        """Read and validate JSON file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            result = {
                "processor": self.process_name,
                "success": True,
                "stats": {
                    "type": type(data).__name__,
                    "size": len(data) if isinstance(data, (list, dict)) else 1,
                    "keys": list(data.keys()) if isinstance(data, dict) else None
               },
               "preview": str(data)[:500] + "..." if len(str(data)) > 500 else str(data)
            }
            return result
        
        except Exception as e:
            return {
                "processor": self.process_name,
                "success": False,
                "error": str(e)
            }
        
    @property
    def process_name(self) -> str:
        return "JSON Processor"