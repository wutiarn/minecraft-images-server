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

_default_params = {
    "text_align": "left",
    "font_size": "16px",
    "margin_override": None,
    "width": 3 * 128
}

def render_image(text: str, target_file: Path):
    params = _default_params.copy()
    html = _render_html(text, params)
    _render_image_from_html(html, target_file, params)


def _render_html(text: str, params: dict):
    if text.startswith("!"):
        # Allow style customization if first line looks like "!f32,w1024,c,m0"
        first_line_end = text.find("\n")
        if first_line_end == -1:
            raise ValueError("Text starting with ! must be multiline")
        params_line = text[1:first_line_end]
        text = text[first_line_end + 1:len(text)]
        _update_params(params_line, params)
    elif all([line.startswith("#") for line in text.splitlines()]):
        # Use title style
        params["text_align"] = "center"
        params["font_size"] = "26"
        params["margin_override"] = "0"
    rendered_md = markdown.markdown(text)
    return template.render(
        payload=rendered_md,
        base_path=pathlib.Path(".").absolute(),
        **params
    )


def _update_params(params_line: str, params: dict):
    split = params_line.split(",")
    for param in split:
        if param == "c":
            params["text_align"] = "center"
        elif param.startswith("m"):
            params["margin_override"] = param[1:len(param)]
        elif param.startswith("f"):
            params["font_size"] = param[1:len(param)] + "px"
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
        "enable-local-file-access": "",
        "enable-javascript": "",
        "javascript-delay": 3000,
        "no-stop-slow-scripts": ""
    }

    imgkit.from_string(html, target_file, options=options)


if __name__ == '__main__':
    params = _default_params.copy()
    text = """
    # Insertion Sort

    Сложность по времени: O($n^2$)
    
    Сложность по памяти: O(1)
    
    Основная идея:
    
    - Берем элемент из массива, сохраняем его во временную переменную
    - Перемещаем все элементы, меньшие по размеру, вправо. Высвобождая тем самым место для вставки выбранного выше элемента.
    - Вставляем выбранный элемент на его законное место
    
    Особенности:
    
    - Быстрый на небольших массивах
    - Нет накладных расходов по памяти
    """
    text = textwrap.dedent(text).strip()
    html = _render_html(text, params)
    with open("test.html", "w") as file:
        file.write(html)
    _render_image_from_html(html, Path("out.png"), params)
