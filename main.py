from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

@app.patch("/increment/{lot_name}")
async def increment(lot_name):
    f = open('map.geojson', 'r+')
    map = json.load(f)
    features = map.get("features")

    for feature in features:
        if(feature["properties"]["name"] == lot_name):
            feature["properties"]["count"] += 1
            json_object = json.dumps(map, indent=4)
            f.seek(0)
            f.truncate()
            f.write(json_object)
            f.close()
            return feature["properties"]
    f.close()
    raise HTTPException(status_code=404, detail="Parking lot not found")
    

@app.patch("/decrement/{lot_name}")
async def increment(lot_name):
    f = open('map.geojson', 'r+')
    map = json.load(f)
    features = map.get("features")

    for feature in features:
        if(feature["properties"]["name"] == lot_name):
            feature["properties"]["count"] -= 1
            json_object = json.dumps(map, indent=4)
            f.seek(0)
            f.truncate()
            f.write(json_object)
            f.close()
            return feature["properties"]
    f.close()
    raise HTTPException(status_code=404, detail="Parking lot not found")

@app.get("/")
def getMap():
    f = open('map.geojson')
    map = json.load(f)
    f.close()
    return map