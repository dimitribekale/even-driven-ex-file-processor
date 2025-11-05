import os
from PIL import Image
from processors.base_processor import BaseProcessor

class ImageProcessor(BaseProcessor):

    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"))
    
    def process(self, file_path: str) -> dict:
        """Read and analyze image file"""
        try:
            with Image.open(file_path) as img:
                result = {
                    "processor": self.process_name,
                    "success": True,
                    "stats": {
                        "format": img.format,
                        "mode": img.mode,
                        "width": img.width,
                        "height": img.height,
                        "size": f"{img.width}x{img.height}",
                        "file_size": f"{os.path.getsize(file_path) / 1024:.2f} KB"
                    }
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
        return "Image Processor"