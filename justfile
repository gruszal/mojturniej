#!/usr/bin/env just --justfile

run-server:
    python -m http.server 8000

generate-new-pages:
    python main.py