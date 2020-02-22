#!/usr/bin/env bash

pipenv sync
pipenv run python src/helpers/reconfig.py
