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
- ${project_html}
\t
${image_html}
\t
\t **${role}**
\t
\t > ${start_month} ${start_year} ${end_date_str}
\t >
\t > ${organization} — ${location}
\t
\n"""

    def render(self, card_data: CardData) -> str:
        image = card_data.get_value("image")
        image_attribution = card_data.get_value("image_attribution")
        link = card_data.get_value("link")
        role = card_data.get_value("role")
        organization = card_data.get_value("organization")
        location = card_data.get_value("location")
        project = card_data.get_value("project")
        start_month = calendar.month_abbr[int(card_data.get_value("start_month"))]
        start_year = card_data.get_value("start_year")
        end_month_value = card_data.get_value("end_month")
        end_month = calendar.month_abbr[int(end_month_value)] if end_month_value is not None else None
        end_year = card_data.get_value("end_year")
        ongoing = card_data.get_value("ongoing")

        if ongoing:
            end_date_str = "— Ongoing"
        elif end_month and end_year:
            end_date_str = f"— {end_month} {end_year}"
        else:
            end_date_str = ""

        hyperlink_start = f"<a href=\"{link}\">" if link else ""
        hyperlink_end = "</a>" if link else ""

        if image_attribution is None:
            image_attribution = ""

        image_attribution_html = f"> <i>{image_attribution}</i>" if image_attribution else ""
        image_html = f"""\
\t<span class='card_banner'><img src="{image}" alt="This is an automatically generated image."></span>
\t
\t {image_attribution_html}
\t
\t---
\t""" if image else ""

        project_html = f"""\
\t<span style="display: flex; justify-content: center;"><i><b>{project}</b></i></span>
\t
\t ---
\t""" if project else ""

        result = self._render_template(
            role=role,
            organization=organization,
            location=location,
            project_html=project_html,
            start_month=start_month,
            start_year=start_year,
            end_date_str=end_date_str,
            image_html=image_html,
            hyperlink_start=hyperlink_start,
            hyperlink_end=hyperlink_end
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
