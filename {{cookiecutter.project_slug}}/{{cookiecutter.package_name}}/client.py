3import os
import logging

import requests
from requests.utils import urlparse

import {{cookiecutter.package_name}}

logger = logging.getLogger(__name__)
DEFAULT_SERVER = "http://localhost:8080"


class {{cookiecutter.baseclass}}Client:
    def __init__(
        self,
        endpoint: str = DEFAULT_SERVER,
        token: str = "",
        requests_verify: bool = True,
        headers: Mapping | None = None,
    ):
        self.endpoint: ParseResult = self._configure_endpoint(endpoint)
        self.host: str = self.endpoint.geturl()
        self.token = token
        self._headers: dict = {
            "Content-Type": "application/json",
            "User-Agent": f"gmail2s3py-cli/{gmail2s3.__version__}",
        }
        if headers:
            self._headers.update(headers)
        self.verify = requests_verify


    def _url(self, path: str) -> str:
        return self.endpoint.geturl() + path

    def _configure_endpoint(self, endpoint):
        return urlparse(endpoint)

    def headers(self, content_type: Literal["json", "form"] = "json") -> Dict[str, str]:
        headers: dict = {}
        headers.update(self._headers)
        if content_type == "json":
            headers["Content-Type"] = "application/json"
        elif content_type == "form":
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        if self.token:
            headers["token"] = self.token

        return headers

    def version(self) -> dict:
        path: str = "/version"
        resp = requests.get(self._url(path), headers=self.headers(), verify=self.verify)
        resp.raise_for_status()
        return resp.json()

    def _request(self, method: str, path: str, params: dict | None = None, body: dict | None = None):
        if params:
            path = path + "?" + urlencode(params)
        if body:
            data = json.dumps(body)
        return getattr(requests, method)(
            path,
            data=json.dumps(body),
            headers=self.headers(),
        )

    def get(self, path, params=None, body=None):
        return self._request("get", path, params, body)

    def delete(self, path, params=None, body=None):
        return self._request("delete", path, params, body)

    def post(self, path, params=None, body=None):
        return self._request("post", path, params, body)
