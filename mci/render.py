import pathlib
import textwrap
from pathlib import Path

import imgkit
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)
template = jinja_env.get_template("markdown.html")


def render_image(text: str, target_file: Path):
    html = _render_html(text)
    _render_image_from_html(html, target_file)


def _render_html(text: str):
    rendered_md = markdown.markdown(text)
    return template.render(
        payload=rendered_md,
        font_path=pathlib.Path("fonts/PTSerif.ttc").absolute()
    )


def _render_image_from_html(html: str, target_file: Path):
    zoom = 10
    options = {
        "zoom": zoom,
        "width": 512 * zoom,
        "disable-smart-width": "",
        "transparent": "",
        "quality": "30",
        "enable-local-file-access": ""
    }

    imgkit.from_string(html, target_file, options=options)


if __name__ == '__main__':
    text = """
        <center>
        # WebKit
        </center>
        WebKit — свободный движок для отображения веб-страниц, разработанный компанией Apple на основе кода библиотек KHTML и KJS, используемых в графической среде KDE.
        
        ## TODO List
        - One
        - Two
        - Three
        """
    text = textwrap.dedent(text)
    html = _render_html(text)
    with open("test.html", "w") as file:
        file.write(html)
    _render_image_from_html(html, Path("out.png"))
