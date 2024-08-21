import frontmatter
from PIL import Image
from pathlib import Path

import card_renderer as cr
import card_data as cd
import card_parser as cp

# Methods

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
    
        # # Example code for future ref
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

    @env.macro
    def grid_entry(path):
        # Prerequisites
        property_spec = cp.parse_card_spec(Path("./cards.yaml"))
        parsers = cp.construct_frontmatter_parsers(property_spec)

        # Parse page
        page = frontmatter.load(path)
        parser = parsers[page['type']]
        parsed_data = parser.parse(page, Path(path).absolute())
        card_data = cd.CardData(
            category=page['type'],
            required_args=parsed_data["required"],
            optional_args=parsed_data["optional"]
        )

        # Render content
        renderer = cr.create_renderer(card_data)
        return renderer.render(card_data)
