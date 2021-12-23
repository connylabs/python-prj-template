#!/bin/bash
PORT=${PORT:-8000}
gunicorn {{ cookiecutter.project_slug }}.main:app -b :$PORT --timeout 120 -w 4 --reload -c conf/gunicorn.py
# uvicorn {{ cookiecutter.project_slug }}.main:app  --reload
