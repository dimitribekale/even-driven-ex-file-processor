import os
from base_processor import BaseProcessor


class TextProcessor(BaseProcessor):

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith((".txt", ".md", ".log"))
    
    def process(self, file_path: str) -> dict:
        """Read and analyze text file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            words = content.split()
            result = {
                "processor": self.processor_name,
                "success": True,
                "stats": {
                    "lines": len(lines),
                    "words": len(words),
                    "characters": len(content),
                    "non_empty_lines": len([l for l in lines if l.strip()])
                },
                "preview": content[:500] + "..." if len(content) > 500 else content
            }
            return content
        
        except Exception as e:
            return {
                "processor": self.processor_name,
                "success": False,
                "error": str(e)
            }
        
    @property
    def processor_name(self) -> str:
        return "Text Processor"