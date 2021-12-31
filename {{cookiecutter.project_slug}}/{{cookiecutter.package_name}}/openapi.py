from {{cookiecutter.package_name}}.main import app


def openapi():
    return app.openapi()
