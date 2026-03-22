from fastapi import FastAPI , Path , Query

import json 

app = FastAPI()


def load_all_the_text ():
    with open ("practice.json", "r") as f:
        practice_data = json.load(f)
    return practice_data

@app.get("/search")
def get_all_the_data (name : str = Query (...) ):
    data = load_all_the_text()
    return data[name]




