import requests

import {{cookiecutter.package_name}}
from {{cookiecutter.package_name}}.commands.command_base import CommandBase


class VersionCmd(CommandBase):
    name = "version"
    help_message = "show versions"

    def __init__(self, options):
        super().__init__(options)
        self.api_version = None
        self.client_version = None
        self.server_host = options.server_host
        self.ssl_verify = options.cacert or not options.insecure

    @classmethod
    def _add_arguments(cls, parser):
        cls._add_serverhost_arg(parser)

    def _api_version(self):
        api_version = None
        try:
            client = self.server_client(
                self.server_host, requests_verify=self.ssl_verify
            )
            api_version = client.version()
        except requests.exceptions.RequestException:
            api_version = ".. Connection error"
        return api_version

    def _cli_version(self):
        return {{cookiecutter.package_name}}.__version__

    def _version(self):
        return {
            "api-version": self._api_version(),
            "client-version": self._cli_version(),
        }

    def _call(self):
        version = self._version()
        self.api_version = version["api-version"]
        self.client_version = version["client-version"]

    def _render_dict(self):
        return {"api-version": self.api_version, "client-version": self.client_version}

    def _render_console(self):
        return "\n".join(
            [
                "Api-version: %s" % self.api_version,
                "Client-version: %s" % self.client_version,
            ]
        )
