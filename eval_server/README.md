# How to use

## Install the dependencies with pip
- `gunicorn`
- `uvicorn`
- `pebble`
- `fastapi`
- `ray`

## Launch the application
`bash launch_server.sh`

## Run batch example
`python batch_eval.py`

## Possible extensions
1. If CPU resources are sufficient, launch multiple servers (on possible different nodes).
2. Evaluation by randomly selecting a server url.