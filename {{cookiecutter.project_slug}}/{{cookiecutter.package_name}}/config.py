"""
Acquire runtime configuration from environment variables (etc).
"""

import os
import yaml


def logfile_path(jsonfmt=False, debug=False):
    """
    Returns the a logfileconf path following this rules:
      - conf/logging_debug_json.conf # jsonfmt=true,  debug=true
      - conf/logging_json.conf       # jsonfmt=true,  debug=false
      - conf/logging_debug.conf      # jsonfmt=false, debug=true
      - conf/logging.conf            # jsonfmt=false, debug=false
    Can be parametrized via envvars: JSONLOG=true, DEBUGLOG=true
    """
    _json = ""
    _debug = ""

    if jsonfmt or os.getenv("JSONLOG", "false").lower() == "true":
        _json = "_json"

    if debug or os.getenv("DEBUGLOG", "false").lower() == "true":
        _debug = "_debug"

    return os.path.join({{cookiecutter.varEnvPrefix}}_CONF_DIR, "logging%s%s.conf" % (_debug, _json))


def getenv(name, default=None, convert=str):
    """
    Fetch variables from environment and convert to given type.

    Python's `os.getenv` returns string and requires string default.
    This allows for varying types to be interpolated from the environment.
    """

    # because os.getenv requires string default.
    internal_default = "$(none)$"
    val = os.getenv(name, internal_default)

    if val == internal_default:
        return default

    if callable(convert):
        return convert(val)

    return val


def envbool(value: str):
    return value and (value.lower() in ("1", "true", "True", "yes"))


APP_ENVIRON = getenv("APP_ENV", "development")

{{cookiecutter.varEnvPrefix}}_API = getenv("{{cookiecutter.varEnvPrefix}}_API", "https://{{cookiecutter.package_name}}.conny.dev")
{{cookiecutter.varEnvPrefix}}_SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
{{cookiecutter.varEnvPrefix}}_ROOT_DIR = os.path.abspath(os.path.join({{cookiecutter.varEnvPrefix}}_SOURCE_DIR, "../"))
{{cookiecutter.varEnvPrefix}}_CONF_DIR = os.getenv(
    "{{cookiecutter.varEnvPrefix}}_CONF_DIR", os.path.join({{cookiecutter.varEnvPrefix}}_ROOT_DIR, "conf/")
)
{{cookiecutter.varEnvPrefix}}_CONF_FILE = os.getenv("{{cookiecutter.varEnvPrefix}}_CONF_FILE", None)
{{cookiecutter.varEnvPrefix}}_DOWNLOAD_DIR = os.getenv("{{cookiecutter.varEnvPrefix}}_DOWNLOAD_DIR", "/tmp/{{cookiecutter.package_name}}")
{{cookiecutter.varEnvPrefix}}_TOKEN = os.getenv(
    "{{cookiecutter.varEnvPrefix}}_TOKEN", "changeme"
)  # Set to None or empty to skip the token

{{cookiecutter.varEnvPrefix}}_TMP_DIR = os.getenv("{{cookiecutter.varEnvPrefix}}_TMP_DIR", "/tmp/{{cookiecutter.package_name}}")
{{cookiecutter.varEnvPrefix}}_SENTRY_URL = os.getenv("{{cookiecutter.varEnvPrefix}}_SENTRY_URL", None)
{{cookiecutter.varEnvPrefix}}_SENTRY_ENV = os.getenv("{{cookiecutter.varEnvPrefix}}_SENTRY_ENV", "development")
{{cookiecutter.varEnvPrefix}}_DEBUG = getenv("{{cookiecutter.varEnvPrefix}}_DEBUG", False, envbool)

PROMETHEUS_MULTIPROC_DIR = os.getenv(
    "PROMETHEUS_MULTIPROC_DIR", os.path.join({{cookiecutter.varEnvPrefix}}_TMP_DIR, "prometheus")
)
os.environ["PROMETHEUS_MULTIPROC_DIR"] = PROMETHEUS_MULTIPROC_DIR


class {{cookiecutter.baseclass}}Config:
    """
    Class to initialize the projects settings
    """

    def __init__(self, defaults=None, confpath=None):
        self.settings = {
            "{{cookiecutter.package_name}}": {
                "debug": {{cookiecutter.varEnvPrefix}}_DEBUG,
                "env": APP_ENVIRON,
                "url": {{cookiecutter.varEnvPrefix}}_API,
                "download_dir": {{cookiecutter.varEnvPrefix}}_DOWNLOAD_DIR,
                "token": {{cookiecutter.varEnvPrefix}}_TOKEN,
                "tmp_dir": {{cookiecutter.varEnvPrefix}}_TMP_DIR,
                "prometheus_dir": PROMETHEUS_MULTIPROC_DIR,
            },
            "sentry": {
                "url": {{cookiecutter.varEnvPrefix}}_SENTRY_URL,
                "environment": {{cookiecutter.varEnvPrefix}}_SENTRY_ENV,
            },
        }

        if defaults:
            self.load_conf(defaults)

        if confpath:
            self.load_conffile(confpath)

    @property
    def {{cookiecutter.package_name}}(self):
        return self.settings["{{cookiecutter.package_name}}"]

    @property
    def sentry(self):
        return self.settings["sentry"]

    def reload(self, confpath, inplace=False):
        if inplace:
            instance = self
            instance.load_conffile(confpath)
        else:
            instance = {{cookiecutter.baseclass}}Config(defaults=self.settings, confpath=confpath)
        return instance

    def load_conf(self, conf):
        for key, val in conf.items():
            self.settings[key].update(val)

    def load_conffile(self, confpath):
        with open(confpath, "r", encoding="utf-8") as conffile:
            self.load_conf(yaml.safe_load(conffile.read()))


GCONFIG = {{cookiecutter.baseclass}}Config(confpath={{cookiecutter.varEnvPrefix}}_CONF_FILE)
