"""
Utility functions for the RAG system
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class JSONHelper:
    """Helper for JSON operations"""
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """Load data from JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)

class FileHelper:
    """Helper for file operations"""
    
    @staticmethod
    def get_file_size(file_path: str) -> str:
        """Get human-readable file size"""
        size = Path(file_path).stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    @staticmethod
    def list_files(directory: str, extensions: List[str] = None) -> List[str]:
        """List files in directory with optional filtering by extension"""
        dir_path = Path(directory)
        if not dir_path.exists():
            return []
        
        files = list(dir_path.glob("**/*"))
        
        if extensions:
            files = [f for f in files if f.suffix.lower() in extensions]
        
        return [str(f) for f in files if f.is_file()]

class TimeHelper:
    """Helper for time operations"""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Format seconds into human-readable time"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
