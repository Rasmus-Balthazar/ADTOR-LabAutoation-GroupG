
from time import sleep
import requests

URL = "http://localhost:8000/"
ACTIONS = URL + "actions"
STATUS = URL + "status"



class Pump():
	def __init__(self, name, dir = True, speed = 4000):
		self.name = name
		self.dir = "true" if dir else "false"
		self.speed = speed

	def mL_to_seconds(self, mL):
		res = (1 / self.calc_calibration(15, 20, 4000)) * mL
		return int(res)

	def seconds_to_mL(self, s):
		res = self.calc_calibration(15, 20, 4000) * s
		return int(res)
	
	def fill(self):
		print(f"Filling up {self.name}!")
		return self._action(10000) # 10 seconds
	
	def pump(self, mL):
		time = self.mL_to_seconds(mL)
		return self._action(time)
	
	def _action(self, time):
		payload = {
						self.name : {
							"state": "true", 
							"dir": self.dir, 
							"speed": self.speed
						}, 
						"id": "1", 
						"time": time*1000
					 }
		# print(payload)
		res = requests.post(ACTIONS, json=payload)
		print(f"Pump is PUMPING for {time} seconds! I will now sleep for", (time) + 1, "seconds.. Zzz...")
		sleep(time + 1) # Without the 1 extra second, it will not take any further requests after this
		while requests.get(STATUS).status_code == 503:
			print("Not ready yet!")
			sleep(1)
		return res.ok
	

	def calc_calibration(self, mL, time, speed):
		calced_speed = mL / time
		speed_frac = self.speed / speed
		return calced_speed / speed_frac


