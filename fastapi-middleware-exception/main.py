from fastapi import FastAPI , Request 
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/hello")
async def first_sample():
    return { "message": "Hello, Welcome to FastAPI!" }

@app.get("/unknown")
def trigger_execption ():
    raise RouteNotFoundExecption ("/unknown")


@app.middleware("http")
async def first_middleware(request : Request, call_next):
    print ("Before the request.", request.url , request.method)
    response =  await call_next(request)

    print ("after the processing ")

    return response

class RouteNotFoundExecption (Exception):
    def __init__(self , name :str):
        self.name = name 


@app.exception_handler(RouteNotFoundExecption)

async def handle_route_not_found_exe(request: Request, exc : RouteNotFoundExecption):
    return JSONResponse (
        status_code=404,
        content= 
        {
         "message": "The requested resource was not found"
        }
        )




