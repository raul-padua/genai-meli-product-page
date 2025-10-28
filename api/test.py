from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def test():
    return {"message": "API is working!"}

handler = app

