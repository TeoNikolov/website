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
        lines_joined = '\n'.join(lines)
        return lines_joined

    def _render_template(self, **kwargs) -> str:
        template = Template(self._convert_to_join_format(self.TEMPLATE))
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
\t
\t > ${start_month} ${start_year} - ${end_date_str}
\t >
\t > ${organization} @ ${location}
\t
\t ${project_html}
\n"""

    def render(self, card_data: CardData) -> str:
        degree = card_data.get_value("degree")
        organization = card_data.get_value("organization")
        location = card_data.get_value("location")
        start_month = calendar.month_abbr[int(card_data.get_value("start_month"))]
        start_year = card_data.get_value("start_year")
        end_month = calendar.month_abbr[int(card_data.get_value("end_month"))]
        end_year = card_data.get_value("end_year")
        project = card_data.get_value("project")
        image = card_data.get_value("image")

        end_date_str = f"{end_month} {end_year}" if end_month and end_year else "Ongoing"

        image_html = f"""\
\t<span class='card_banner'><img src="{image}" alt="This is an automatically generated image."></span>
\t
\t ---
\t""" if image else ""

        project_html = f"""\
\t
\t---
\t
\t<strong>Project:</strong> {project}""" if project else ""

        result = self._render_template(
            degree=degree,
            organization=organization,
            location=location,
            start_month=start_month,
            start_year=start_year,
            end_date_str=end_date_str,
            image_html=image_html,
            project_html=project_html
        )

        return result

class ExperienceCardRenderer(CardRenderer):
    TEMPLATE = """\
- ${image_html}
\t
\t ${start_month} ${start_year} - ${end_date_str}
\t
\t ---
\t
\t **${role}**
\t
\t ${organization} @ ${location}
\n"""

    def render(self, card_data: CardData) -> str:
        role = card_data.get_value("role")
        role_alt = card_data.get_value("role_alt")
        organization = card_data.get_value("organization")
        location = card_data.get_value("location")
        start_month = calendar.month_abbr[int(card_data.get_value("start_month"))]
        start_year = card_data.get_value("start_year")
        end_month_value = card_data.get_value("end_month")
        end_month = calendar.month_abbr[int(end_month_value)] if end_month_value is not None else None
        end_year = card_data.get_value("end_year")
        ongoing = card_data.get_value("ongoing")
        image = None

        if ongoing:
            end_date_str = "Ongoing"
        elif end_month and end_year:
            end_date_str = f"{end_month} {end_year}"
        else:
            end_date_str = ""

        image_html = f"""\
\t<span class='card_banner'><img src="{image}" alt="This is an automatically generated image."></span>
\t
\t ---
\t""" if image else ""

        result = self._render_template(
            role=role,
            organization=organization,
            location=location,
            start_month=start_month,
            start_year=start_year,
            end_date_str=end_date_str,
            image_html=image_html
        )

        return result

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
