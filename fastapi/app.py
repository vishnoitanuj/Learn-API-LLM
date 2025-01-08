from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()

class Numbers(BaseModel):
    x: int
    y: int

@app.post("/add")
def add_numbers_api(numbers: Numbers):
    return {"result": add_numbers(numbers.x, numbers.y)}

def add_numbers(x, y):
    return x + y