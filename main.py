from fastapi import FastAPI

app = FastAPI()
counter = 0

@app.get("/increment")
def increment():
    global counter
    counter += 1
    return {"message": "counter incremented", "value": counter}


@app.get("/decrement")
def decrement():
    global counter
    counter -= 1
    return {"message": "counter decremented", "value": counter}




