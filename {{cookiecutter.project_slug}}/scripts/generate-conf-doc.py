import yaml
from {{cookiecutter.package_name}}.config import GCONFIG


print(yaml.safe_dump(GCONFIG.settings, indent=2))
