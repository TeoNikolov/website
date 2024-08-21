from typing import List, Dict, Optional, Any

class CardData:

    def __init__(self, category: str, required_args: Dict[str, Any], optional_args: Optional[Dict[str, Any]] = None):
        self.category = category
        self.required_args = required_args
        self.optional_args = optional_args or {}

    def get_value(self, key: str) -> Optional[Any]:
        if key in self.required_args:
            return self.required_args[key]
        elif key in self.optional_args:
            return self.optional_args[key]
        print(f"[WARNING] - Failed to get parsed value for \"{key}\"")
        return None
