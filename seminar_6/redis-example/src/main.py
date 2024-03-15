from fastapi import FastAPI
import redis

app = FastAPI()


@app.on_event("startup")
def startup_event():
    app.state.redis = redis.Redis(host="redis", port=6379, db=0)


@app.post("/api/set")
def set_kv(key: str, value: str):
    app.state.redis.set(key, value)


@app.get("/api/get/{key}")
def get_kv(key: str):
    return {key: app.state.redis.get(key)}
