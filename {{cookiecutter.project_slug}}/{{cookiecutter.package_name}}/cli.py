import logging

import click
import uvicorn

from {{cookiecutter.package_name}}.openapi import openapi
from {{cookiecutter.package_name}}.main import app

@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--host", default="0.0.0.0", type=str, show_default=True)
@click.option("--port", default=8000, type=int, show_default=True)
def cli(ctx, host, port):
    if ctx.invoked_subcommand is None:
        log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        logger = logging.getLogger(__name__)

        logger.info(f"Using host {host}")
        logger.info(f"Using port {port}")
        uvicorn.run(app, host=host, port=port, log_level="debug")


cli.command("openapi")(openapi)

if __name__ == "__main__":
    cli()
