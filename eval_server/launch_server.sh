#!/bin/bash

gunicorn=/usr/local/bin/gunicorn

# start app
gunicorn eval_gunicorn:app \
    --config gunicorn_config.py \
    --preload
