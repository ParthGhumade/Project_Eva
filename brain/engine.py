import math
import serial
import time


class RobotEngine:
	def __init__(self, port = '/dev/ttyACM0', baud = 115200, timeout = 0.1):
		# self.centerPos = centerPos

		try:
			self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)
			time.sleep(2) # reduce this value if your hardware is good
		except Exception as e:
			print(f"Connection Failed: {e}")

	def sendCommand(self, cmd_str: str):
		self.ser.write(f"{cmd_str}\n".encode('utf-8'))
		return self.ser.readline().decode('utf-8').strip()

	def moveForward(self, speed):
		return self.sendCommand(f"M:{speed}")

	def turnRad(self, radians, direction):
		return self.sendCommand(f"T:{int(radians*180.0/math.pi)}:{direction}") # direction is 1 for clockwise and 0 for anti-clockwise

	def turnDeg(self, degrees, direction):
		return self.sendCommand(f"T:{direction}:{degrees}") # direction is 1 for clockwise and 0 for anti-clockwise

	def stop(self):
		return self.sendCommand("X")

	def resolveCollisions(self, proximity=[1.0], level=1):
		assert level == len(proximity), 'incorrect number of proximities provided!'
		
		response = self.sendCommand(f"C:{level}") # data format '2.3 4.5 6.4' depends on level, space separated floats
		data = [float(i) for i in response.split(' ')]
		
		assert len(data) == level, 'your hardware could not return readings as per the level set.'
		
		collision = False
		for i in range(0, len(proximity)):
			if data[i] < proximity[i]:
				collision = True
				break

		if collision:
			response = self.stop()
			if response:
				print('successfully stoped!')
			else:
				print('could not resolve collision because the hardware actively refused to stop')

		return collision