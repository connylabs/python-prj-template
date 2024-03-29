import uvicorn
from {{cookiecutter.package_name}}.commands.command_base import CommandBase


class RunServerCmd(CommandBase):
    name = "run-server"
    help_message = "Run the API server (with uvicorn)"
    parse_unknown = False

    def __init__(self, options, unknown=None) -> None:
        super().__init__(options)
        self.options = options
        self.status = {}

    def _call(self) -> None:
        uvicorn.run(
            "{{ cookiecutter.project_slug }}.main:app",
            host=self.options.bind,
            port=self.options.port,
            log_level="debug",
        )

    @classmethod
    def _add_arguments(cls, parser) -> None:
        parser.add_argument(
            "-p", "--port", nargs="?", default=8000, type=int, help="server port listen"
        )
        parser.add_argument(
            "-b", "--bind", nargs="?", default="0.0.0.0", help="server bind address"
        )

    def _render_dict(self):
        return self.status

    def _render_console(self):
        return self.status["result"]
