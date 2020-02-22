#!/usr/bin/env bash

pipenv sync
pipenv run python src/run_reconfig.py "controls"
