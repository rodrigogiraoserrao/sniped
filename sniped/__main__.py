from __future__ import annotations

import enum
import json
import pathlib
from urllib.request import Request, urlopen
import sys
from typing import Optional

import typer

from .configs import CARBON, SNAPPIFY

app = typer.Typer()


class Service(enum.Enum):
    CARBON = "carbon"
    SNAPPIFY = "snappify"


ENDPOINTS = {
    Service.CARBON: "https://carbonara-42.herokuapp.com/api/cook",
    Service.SNAPPIFY: "https://api.snappify.io/snap/simple",
}
CONFIGS = {
    Service.CARBON: CARBON,
    Service.SNAPPIFY: SNAPPIFY,
}


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
        metavar="CODE_OR_PATH",
        help=(
            "Code to include in the image or path to code file."
            + " Use '-' to read from stdin."
        ),
    ),
    language: str = typer.Option(
        "auto",
        metavar="LANG",
        help="Language for syntax highlighting; 'auto' only works for carbon.",
    ),
    key: str = typer.Option(
        "",
        metavar="KEY_OR_PATH",
        help="(Path to file with) API key for Snappify.",
        envvar="SNAPPIFY_API_KEY",
    ),
    out: Optional[pathlib.Path] = typer.Option(
        None,
        metavar="PATH",
        help="Write to given file instead of stdout.",
        dir_okay=False,
        writable=True,
    ),
):
    """Create a beautiful image from a snippet of code."""

    request = Request(ENDPOINTS[service])
    request.add_header("Content-Type", "application/json")

    if service == Service.SNAPPIFY:
        # Abort if we don't have a valid API key.
        if not key:
            typer.echo("Option '--key' required for the Snappify service.", err=True)
            raise typer.Abort()
        key = try_reading_from_file(key)
        request.add_header("Authorization", key)

    code = read_code_from_stdin() if code == "-" else try_reading_from_file(code)

    config = CONFIGS[service]
    config["code"] = code
    config["language"] = language

    with urlopen(request, data=json.dumps(config).encode()) as response:
        image = response.read()

    if out is None:
        sys.stdout.buffer.write(image)
    else:
        with open(out, "wb") as f:
            f.write(image)


if __name__ == "__main__":
    app()
