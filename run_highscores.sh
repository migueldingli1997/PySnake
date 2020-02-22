#!/usr/bin/env bash

pipenv sync
pipenv run python src/run_highscores.py highscores
