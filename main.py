import traceback
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import json
from deta import Deta

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        err = traceback.format_exception(type(e), e, e.__traceback__)
        return JSONResponse(content={"traceback": err}, status_code=500)

app = FastAPI()
# app.middleware('http')(catch_exceptions_middleware)

deta = Deta('b01e4uo1_AKg3ZAFjdQkFwrUKxYPwmPRohk85egpb') # configure your Deta project
db = deta.Base('simpleDB')
db2 = deta.Base('simpleDB')

@app.patch("/lot/{lot_name}/increment/")
async def increment(lot_name):
    updates = {
        "count": db.util.increment()
    }
    return db.update(updates, lot_name)

@app.patch("/lot/{lot_name}/decrement/")
async def increment(lot_name):
    updates = {
        "count": db.util.increment()
    }
    return db.update(updates, lot_name)

@app.get("/lot/{lot_name}")
def getLot(lot_name):
    lot = db.get(lot_name)
    return lot

@app.post("/lot/{lot_name}")
def createLot(lot_name):
    lot = db.put({
        "name": lot_name,
        "count": 0,
    }, lot_name)
    return lot

@app.delete("/lot/{lot_name}")
def createLot(lot_name):
    lot = db.delete(lot_name)
    return lot

@app.get("/")
def getMap():
    f = open('map.geojson', 'r')
    map = json.load(f)
    features = map.get("features")

    for feature in features:
        feature['properties'] = db.get(feature['properties']['name'])
    
    f.close()
    return map

@app.post("/reset/")
def reset():
    print(db.fetch()._items)
    for item in db.fetch()._items:
        db.delete(item.name)

    f = open('map.geojson', 'r')
    map = json.load(f)
    features = map.get("features")

    for feature in features:
        db.put(feature['properties'], feature['properties']['name'])
        
    f.close()
    return db.fetch()