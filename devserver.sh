#!/bin/sh
source .venv/bin/activate
# Executa o servidor Flask, usando a porta definida em $PORT ou 8080 como padrão.
python -u -m flask --app main run --debug -p ${PORT:-8080}