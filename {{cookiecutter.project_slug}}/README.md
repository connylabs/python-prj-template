{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}

# {{ cookiecutter.project_name }}

Your main CLI program should be written `{{ cookiecutter.package_name }}.cli:cli`
and will then be registered as the CLI command `{{ cookiecutter.project_slug }}` .


{{ cookiecutter.project_short_description }}
Features
--------

* TODO
