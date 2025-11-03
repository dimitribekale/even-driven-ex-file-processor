import os
import pandas as pd
from base_processor import BaseProcessor

class CSVProcessor(BaseProcessor):

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith(".csv")
    
    def process(self, file_path: str) -> dict:
        """Read and analyze CSV file."""
        try:
            df = pd.read_csv(file_path)

            result = {
                "processor": self.processor_name,
                "succes": True,
                "stats": {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist(),
                    "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
                },
                "preview": df.head(5).to_dict(orient="records")
            }
            return result
        
        except Exception as e:
            return {
                "processor": self.processor_name,
                "success": False,
                "error": str(e)
            }
    @property
    def processor_name(self) -> str:
        return "CSV Processor"