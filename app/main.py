from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hallo ich bin lee"}
