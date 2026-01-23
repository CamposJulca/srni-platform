#!/usr/bin/env bash
set -e

PYTHON_BIN=python3.12

echo "▶ Creating virtual environment"
rm -rf .venv
$PYTHON_BIN -m venv .venv
source .venv/bin/activate

echo "▶ Upgrading tooling"
pip install --upgrade pip setuptools wheel

echo "▶ Installing dependencies"
pip install -r requirements.txt

echo "▶ Running Django checks"
python backend/rni_web/src/manage.py check

echo "✔ Environment ready"
