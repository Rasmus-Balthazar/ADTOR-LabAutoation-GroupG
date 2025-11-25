import requests
from time import sleep

URL = "http://localhost:8000/"
ACTIONS = URL + "actions"
READINGS = URL + "sensor_readings"
STATUS = URL + "status"

WATER = "pumpA"
DRAIN = "pumpC"


def water_cycle_syringe():
    """
    Performs a full drain (~20mL) of the syringe then fills it with ~20mL of water. \\
    Takes ~2min. \\
    A *dump and pump*, if you will
    """
    drain_load = {DRAIN : {"state": "true", "dir": "true", "speed": 2000}, "id": "1", "time": 65000}
    res = requests.post(ACTIONS, json=drain_load)
    assert res.ok, res.text 
    sleep(60)
    while requests.get(STATUS).status_code == 503:
        sleep(1)
    pump_load = {WATER : {"state": "true", "dir": "true", "speed": 2000}, "id": "1", "time": 60000}
    res = requests.post(ACTIONS, json=pump_load)
    assert res.ok, res.text 
    sleep(55)
    while requests.get(STATUS).status_code == 503:
        sleep(1)
    
    
def clean_syringe():
    res = requests.get(READINGS)
    json = res.json()
    rgb = json["readings"]

    while all([c > 50 for c in rgb]):
        water_cycle_syringe()
        
    print("Finished cleaning")

clean_syringe()