from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def raed_root():
    return {"message": "Привет, это мой первый сервер!"}