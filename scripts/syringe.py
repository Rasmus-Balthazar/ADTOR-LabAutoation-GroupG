

import requests
from pump import Pump

URL = "http://localhost:8000/"
READINGS = URL + "sensor_readings"


class Syringe():
	def __init__(self):
		self.water_pump = Pump("pumpA")
		self.drain_pump = Pump("pumpC")
		self.color_pump = Pump("pumpB")

		while input("Is the Water Pump filled? (y/n)\n") != "y":
			self.water_pump.pump(1)
	
		while input("Is the Color Pump filled? (y/n)\n") != "y":
			self.color_pump.pump(1)

		self.mL = int(input("How much water do I have?\n"))


	def add_water(self, mL):
		self.water_pump.pump(mL)
		self.mL += mL

	def add_color(self, mL):
		self.color_pump.pump(mL)
		self.mL += mL

	def clean(self):
		"""
		Performs a full drain (~20mL) of the syringe then fills it with ~20mL of water. \\
		Takes ~2min. \\
		A *dump and pump*, if you will
		"""
		self.drain(self.mL)

		while all([c > 10 for c in self.get_rgb()]):
			self.add_water(5)
			self.clean()
			
		print("Finished cleaning")
	
	def drain(self, mL):
		mL = min(mL, self.mL)
		self.drain_pump.pump(self.mL)
		self.mL -= mL
	
	def get_rgb(self):
		res = requests.get(READINGS)
		json = res.json()
		rgb = json["readings"]
		while rgb is None:
			rgb = self.get_rgb()
		return rgb


    
		