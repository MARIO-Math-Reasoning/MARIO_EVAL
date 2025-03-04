# gunicorn config
import os

# bind port and host
bind = "0.0.0.0:5000"

# workers = os.cpu_count() * 2
workers = 16

worker_class = "uvicorn.workers.UvicornWorker"

timeout = 120

# other configs
keepalive = 65
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# log config
loglevel = "info"
