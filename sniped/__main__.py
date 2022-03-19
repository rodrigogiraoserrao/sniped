from __future__ import annotations

import enum
import json
import pathlib
from urllib.request import Request, urlopen
import sys

import typer

from .configs import CARBON, SNAPPIFY

app = typer.Typer()


class Service(enum.Enum):
    CARBON = "carbon"
    SNAPPIFY = "snappify"


CARBON_ENDPOINT = "https://carbonara-42.herokuapp.com/api/cook"
SNAPPIFY_ENDPOINT = "https://api.snappify.io/snap/simple"


def read_code_from_stdin():
    return "".join([line for line in sys.stdin])


def try_reading_from_file(possible_file_path: str) -> str:
    """Try reading from a file with the given path or return the arg unchanged."""

    possible_file = pathlib.Path(possible_file_path)
    if possible_file.exists() and possible_file.is_file():
        with open(possible_file, "r") as f:
            return f.read()

    return possible_file_path


def load_config(config_file_path: str | pathlib.Path) -> dict:
    with open(config_file_path) as f:
        return json.load(f)


def make_image_from_request(
    code: str, language: str, out: str, request: Request, config: dict
):

    request.add_header("Content-Type", "application/json")

    code = read_code_from_stdin() if code == "-" else try_reading_from_file(code)
    config["code"] = code
    config["language"] = language

    with urlopen(request, data=json.dumps(config).encode()) as response:
        image = response.read()

    with open(out, "wb") as f:
        f.write(image)


@app.command(options_metavar="[options]")
def create(
    service: Service = typer.Argument(..., case_sensitive=False),
    code: str = typer.Argument(
        ...,
        metavar="code",
        help=(
            "Code to include in the image or path to code file."
            + " Use '-' to read from stdin."
        ),
    ),
    language: str = typer.Option(
        "auto",
        metavar="lang",
        help="Language for syntax highlighting; 'auto' only works for carbon.",
    ),
    key: str = typer.Option(
        "api.key",
        metavar="key_or_path",
        help="(Path to file with) API key for Snappify.",
    ),
    out: str = typer.Option("out.png", metavar="path"),
):
    pass


@app.command()
def carbon(
    code: str,
    language: str = typer.Argument("auto"),
    out: str = typer.Argument("out.png"),
):
    make_image_from_request(
        code,
        language,
        out,
        Request(CARBON_ENDPOINT),
        CARBON,
    )


@app.command()
def snappify(code: str, key: str, language: str, out: str = typer.Argument("out.png")):
    req = Request(SNAPPIFY_ENDPOINT)
    key = try_reading_from_file(key)
    req.add_header("Authorization", key)
    make_image_from_request(
        code,
        language,
        out,
        Request(SNAPPIFY_ENDPOINT),
        SNAPPIFY,
    )


if __name__ == "__main__":
    app()
