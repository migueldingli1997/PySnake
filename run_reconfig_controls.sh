#!/usr/bin/env bash

pipenv sync
pipenv run python src/reconfig_controls.py
