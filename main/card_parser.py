import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any

class FrontmatterParser:
    def __init__(self, name: str, required_args: List[str], optional_args: Optional[List[str]] = None):
        if not isinstance(required_args, list) or not all(isinstance(arg, str) for arg in required_args):
            raise ValueError("required_args must be a list of strings")
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if optional_args and (not isinstance(optional_args, list) or not all(isinstance(arg, str) for arg in optional_args)):
            raise ValueError("optional_args must be a list of strings")
        
        self.required_args: Dict[str, Optional[Any]] = {arg: None for arg in required_args}
        self.optional_args: Dict[str, Optional[Any]] = {arg: None for arg in optional_args} if optional_args else {}
        self.name: str = name

    def parse(self, data, target_string: str):
        try:
            for arg in self.required_args:
                if arg not in data:
                    raise ValueError(f"Missing required argument: {arg}")
                self.required_args[arg] = data[arg]
            
            for arg in self.optional_args:
                if arg in data:
                    self.optional_args[arg] = data[arg]
        except:
            raise RuntimeError(f"Parsing failed for '{target_string}'")

        return {"required": self.required_args, "optional": self.optional_args}

# Parses a ".yaml" file containing the spec of properties for different card types
def parse_card_spec(file_path: Path) -> List[Dict[str, Any]]:
    with file_path.open('r') as file:
        parsed_yaml = yaml.safe_load(file)
        assert parsed_yaml

    properties_section = parsed_yaml.get('properties', [])
    properties_array = []

    # Extract common properties
    common_required = []
    common_optional = []
    for category in properties_section:
        if 'common' in category:
            common_properties = category['common']
            common_required = [key for prop in common_properties for key, value in prop.items() if value]
            common_optional = [key for prop in common_properties for key, value in prop.items() if not value]
            break

     # Process other categories
    for category in properties_section:
        for category_name, properties in category.items():
            if category_name == 'common':
                continue

            required = [key for prop in properties for key, value in prop.items() if value] + common_required
            optional = [key for prop in properties for key, value in prop.items() if not value] + common_optional

            properties_array.append({
                "category": category_name,
                "required": required,
                "optional": optional
            })

    return properties_array

# Constructs frontmatter parsers given a card spec
def construct_frontmatter_parsers(property_spec: List[Dict[str, Any]]) -> Dict[str, FrontmatterParser]:
    parsers = {}

    for spec in property_spec:
        category = spec["category"]
        required_args = spec["required"]
        optional_args = spec["optional"]
        
        parsers[category] = FrontmatterParser(
            name=category,
            required_args=required_args,
            optional_args=optional_args
        )
    
    return parsers
