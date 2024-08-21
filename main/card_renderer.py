from string import Template
from card_data import CardData
import calendar
import textwrap
import inspect

# Base class
class CardRenderer:
    TEMPLATE = ""

    def render(self, card_data: CardData) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    def _convert_to_join_format(self, template_string: str) -> str:
        lines = [line for line in template_string.splitlines()]
        for l in lines:
            print(repr(l))
        lines_joined = '\n'.join(lines)
        return lines_joined

    def _render_template(self, **kwargs) -> str:
        print(repr(self.TEMPLATE))
        print()
        template = Template(self._convert_to_join_format(self.TEMPLATE))
        print()
        print(repr(template))
        print()
        print()
        return template.safe_substitute(**kwargs)

# Used to display a card that shows an error
class ErrorCardRenderer(CardRenderer):
    def render(self, card_data: CardData) -> str:
        return "error card: unknown category"

class EducationCardRenderer(CardRenderer):
    TEMPLATE = """\
- ${image_html}
\t
\t **${degree}**
\t <p>${start_month} ${start_year} - ${end_date_str}</p>
\t ${project_html}
\n"""

    def render(self, card_data: CardData) -> str:
        degree = card_data.get_value("degree")
        start_month = calendar.month_abbr[int(card_data.get_value("start_month"))]
        start_year = card_data.get_value("start_year")
        end_month = calendar.month_abbr[int(card_data.get_value("end_month"))]
        end_year = card_data.get_value("end_year")
        project = card_data.get_value("project")
        image = card_data.get_value("image")

        end_date_str = f"{end_month} {end_year}" if end_month and end_year else "Ongoing"

        image_html = f"""\
<span class='card_banner'>
    <img src="{image}" alt="This is an automatically generated image.">
</span>""" if image else ""

        project_html = f"<p><strong>Project:</strong> {project}</p>" if project else ""

        result = self._render_template(
            degree=degree,
            start_month=start_month,
            start_year=start_year,
            end_date_str=end_date_str,
            image_html=image_html,
            project_html=project_html
        )

        return result

class ExperienceCardRenderer(CardRenderer):
    def render(self, card_data: CardData) -> str:
        # Implement specific rendering logic for 'experience'
        return "experience card"

class ProjectCardRenderer(CardRenderer):
    def render(self, card_data: CardData) -> str:
        # Implement specific rendering logic for 'project'
        return "project card"

class DefaultCardRenderer(CardRenderer):
    def render(self, card_data: CardData) -> str:
        # Implement specific rendering logic for 'default'
        return "default card"

# Map card categories to renderer
_RENDERER_MAPPING = {
    'education': EducationCardRenderer,
    'experience': ExperienceCardRenderer,
    'project': ProjectCardRenderer,
    'default': DefaultCardRenderer
}

# Main function used to create a CardRenderer object
def create_renderer(card_data: CardData) -> CardRenderer:
    renderer_class = _RENDERER_MAPPING.get(card_data.category, ErrorCardRenderer)
    return renderer_class()
