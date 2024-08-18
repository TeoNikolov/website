import frontmatter
import calendar
from PIL import Image
import os
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

    def parse(self, data):
        for arg in self.required_args:
            if arg not in data:
                raise ValueError(f"Missing required argument: {arg}")
            self.required_args[arg] = data[arg]
        
        for arg in self.optional_args:
            if arg in data:
                self.optional_args[arg] = data[arg]

parsers = {
    "experience" : FrontmatterParser(
        name="experience",
        required_args=["name"],
        optional_args=["start_year"]
    ),
    "education" : FrontmatterParser(
        name="education",
        required_args=["name"],
        optional_args=["start_year"]
    ),
    "project" : FrontmatterParser(
        name="project",
        required_args=["name"],
        optional_args=["start_year"]
    )
}


def define_env(env):
    
    def load_banner(path, target_width, target_height):
        if not path:
            return None

        # Open image
        img = Image.open(path)

        # Calculate aspect ratio
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height

        # Determine the new size of the image
        if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            new_width = int(target_height * img_ratio)
            new_height = target_height

        # Resize the image
        resized_img = img.resize((new_width, new_height))

        # Create a new image with transparent background
        new_img = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))

        # Paste the resized image onto the new image
        paste_position = ((target_width - new_width) // 2, (target_height - new_height) // 2)
        new_img.paste(resized_img, paste_position, resized_img.convert("RGBA"))

        # Return banner image
        return new_img

    @env.macro
    def grid_entry(path):
        page = frontmatter.load(path)

        # Frontmatter Parser

        if 'type' not in page:
            raise KeyError(f"Missing \"type\" in frontmatter of \"{path}\"")

        if page['type'] not in parsers:
            raise ValueError(f"No parser available for type \"{page['type']}\" in frontmatter of \"{path}\"")

        parser = parsers[page['type']]

        # Variables

        if 'name' not in page:
            raise KeyError(f"Missing \"name\" in frontmatter of \"{path}\"")
        name = page['name']

        start_month = ""
        if 'start_month' in page:
            start_month = calendar.month_abbr[int(page['start_month'])]
        
        start_year = ""
        if 'start_year' in page:
            start_year = page['start_year']

        end_month = ""
        if 'end_month' in page:
            end_month = calendar.month_abbr[int(page['end_month'])]
        
        end_year = ""
        if 'end_year' in page:
            end_year = page['end_year']

        project = ""
        if 'project' in page:
            project = page['project']

        banner = ""
        if 'banner' in page:
            banner = "/assets/" + page['banner']

        # # Process banner
        # if banner:
        #     banner_width = 800
        #     banner_height = 200
        #     banner_img = load_banner("docs" + banner, banner_width, banner_height)

        #     if banner_img:
        #         banner_dir = os.path.dirname(banner)
        #         banner_dir_new = banner_dir + "/banners"
        #         banner_filename = os.path.basename(banner)
        #         banner_filename_base, banner_filename_extension = os.path.splitext(banner_filename)
        #         banner_filename_new = banner_dir_new + "/" + banner_filename_base + "_banner.png"

        #         if banner_dir_new and not os.path.exists(banner_dir_new):
        #             os.makedirs(banner_dir_new)
                
        #         ### This saves to the docs, we want a temporary file instead like social cards!!! Fix this some day if we nee this functionality
        #         # banner_img.save(banner_filename_new)

        #         # Update original variable with new image
        #         # banner = "/" + banner_filename_new

        # Text blocks

        end_date_str = ""
        if end_month == 0 or end_year == 0:
            end_date_str = "Ongoing"
        else:
            end_date_str = f"{end_month} {end_year}"

        header_str = '\n'.join([
            f"\t**{name}**",
            f"\t",
            f"\t> {start_month} {start_year} - {end_date_str}",
        ])

        project_str = ""
        if project:
            project_str = '\n'.join([
                f"\t**Project** : *{project}*"
            ])

        banner_str = ""
        if banner:
            banner_str = '\n'.join([
                f"\t<span class='card_banner'>",
                f"\t<img src=\"{banner}\" alt=\"This is an automatically generated banner image.\">"
                f"\t</span>"
            ])

        # Construct the card

        md = '\n'.join([
            f"-" +
            banner_str,
            f"\t",
            header_str,
            f"\t",
            f"\t---",
            f"\t",
            project_str,
            ""
        ])
        
        if page is None:
            return "noooo"
        else:
            return md
