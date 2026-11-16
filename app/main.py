import os
import redis
from flask import Flask, jsonify

app = Flask(__name__)

cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


@app.route("/")
def index():
    hits = cache.incr("hits")
    return jsonify(message="Hello from Progree DevOps Task 2",
                   env=os.getenv("APP_ENV", "dev"), hits=hits)


@app.route("/health")
def health():
    cache.ping()
    return jsonify(status="ok")
