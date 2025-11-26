from fastapi import FastAPI, BackgroundTasks
import uvicorn
from driver import RealMicrocontrollerService, get_logger
from action_models import ActionRequest
import asyncio
from time import sleep

    
app = FastAPI()
micro = RealMicrocontrollerService()

log = get_logger(__name__)
busy = False
stop_requested = False

main_event_loop = None

@app.on_event("startup")
async def startup_event():
    global main_event_loop
    main_event_loop = asyncio.get_running_loop()

@app.post("/actions")
async def perform_actions(request: ActionRequest, background_tasks: BackgroundTasks):
    global busy, stop_requested
    if busy:
        return {"status": "busy"}
    busy = True
    stop_requested = False
    sleep(request.time/1000)
    busy = False
    stop_requested = False
    return {"status": "accepted", "id": request.id}

@app.get("/sensor_readings")
async def get_sensor_readings():
    readings = ["1", "2", "3"]
    return {"readings": readings}

@app.post("/stop")
async def emergency_stop():
    global stop_requested, busy
    stop_requested = True
    busy = False  # Fallback: ensure busy is reset if stop is called
    log.info("/stop called: busy set to False")
    return {"status": "stopped"}


@app.get("/status")
def get_status():
    global busy
    status = 503 if busy else 200
    return {"busy": busy}, status

if __name__ =="__main__":
    uvicorn.run(app, port=8000)