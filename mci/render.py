import pathlib
import re
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

_int_regex = re.compile("\d+")

def render_image(text: str, target_file: Path):
    html = _render_html(text)
    _render_image_from_html(html, target_file)


def _render_html(text: str):
    params = {
        "text_align": "left",
        "font_size": "16px",
        "zero_margin": False
    }
    if text.startswith("!"):
        # Allow style customization if first line looks like "!32,c,m0"
        first_line_end = text.find("\n")
        if first_line_end == -1:
            raise ValueError("Text starting with ! must be multiline")
        params_line = text[1:first_line_end]
        text = text[first_line_end + 1:len(text)]
        _update_params(params_line, params)
    elif all([line.startswith("#") for line in text.splitlines()]):
        # Use title style
        params["text_align"] = "center"
        params["font_size"] = "32"
        params["zero_margin"] = True
    rendered_md = markdown.markdown(text)
    return template.render(
        payload=rendered_md,
        font_path=pathlib.Path("fonts/PTSerif.ttc").absolute(),
        **params
    )


def _update_params(params_line: str, params: dict):
    split = params_line.split(",")
    for param in split:
        if param == "m0":
            params["zero_margin"] = True
        elif param == "c":
            params["text_align"] = "center"
        elif _int_regex.fullmatch(param):
            params["font_size"] = int(param)


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
    # Алгоритмы сортировки
    #### в прикладных системах
    """
    text = textwrap.dedent(text).strip()
    html = _render_html(text)
    with open("test.html", "w") as file:
        file.write(html)
    _render_image_from_html(html, Path("out.png"))
