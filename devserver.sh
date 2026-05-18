#!/bin/sh
source .venv/bin/activate
python -u -m flask --app main run --port ${PORT:-8080} --debug --host=0.0.0.0
