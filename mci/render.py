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


def render_image(text: str, target_file: Path):
    params = {
        "text_align": "left",
        "font_size": "16px",
        "zero_margin": False,
        "width": 512
    }
    html = _render_html(text, params)
    _render_image_from_html(html, target_file, params)


def _render_html(text: str, params: dict):
    if text.startswith("!"):
        # Allow style customization if first line looks like "!f32,c,m0"
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
        elif param.startswith("f"):
            params["font_size"] = int(param[1:len(param)])
        elif param.startswith("w"):
            params["width"] = int(param[1:len(param)])


def _render_image_from_html(html: str, target_file: Path, params: dict):
    zoom = 10
    options = {
        "zoom": zoom,
        "width": params["width"] * zoom,
        "disable-smart-width": "",
        "transparent": "",
        "quality": "30",
        "enable-local-file-access": ""
    }

    imgkit.from_string(html, target_file, options=options)


if __name__ == '__main__':
    params = {
        "text_align": "left",
        "font_size": "16px",
        "zero_margin": False,
        "width": 512
    }
    text = """
    !w1024,m0
    # Алгоритмы сортировки
    #### в прикладных системах
    """
    text = textwrap.dedent(text).strip()
    html = _render_html(text, params)
    with open("test.html", "w") as file:
        file.write(html)
    _render_image_from_html(html, Path("out.png"), params)
