import time
import threading
import sys
import cv2
import cv2.aruco as aruco


class CameraStream:
	def __init__(self, src=0, width = 640, height=480):
		if sys.platform == "win32":
			backend = cv2.CAP_DSHOW
		elif sys.platform.startswith("linux"):
			backend = cv2.CAP_V4L2
		else:
			backend = cv2.CAP_ANY
		self.stream = cv2.VideoCapture(src, backend)

		if not self.stream.isOpened():
			raise RuntimeError(f"Failed to open camera at index {src}")

		self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
		self.stream.set(cv2.CAP_PROP_FPS, 30)

		self.grabbed, self.frame = self.stream.read()

		self.started = False
		self.read_lock = threading.Lock()

		self._fresh = False

	def start(self):
		if self.started:
			return None
		self.started = True
		self.thread = threading.Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()
		return self

	def update(self):
		while self.started:
			grabbed, frame = self.stream.read()
			with self.read_lock:
				self.grabbed = grabbed
				self.frame = frame
				self._fresh = True

	def read(self):
		with self.read_lock:
			frame = self.frame.copy() if self.frame is not None else None
			grabbed = self.grabbed
			self._fresh = False
		return grabbed, frame

	def read_fresh_only(self):
		with self.read_lock:
			if not self._fresh or self.frame is None:
				return False, None
			frame = self.frame.copy()
			self._fresh = False
		return True, frame

	def stop(self):
		self.started = False
		self.stream.release()
		if self.thread.is_alive():
			self.thread.join()


class VisionEngine:
	def __init__(self, camera_index=0):
		self.camera = CameraStream(src=camera_index).start()
		self.centerPos = None
		self.running = True
		self.lock = threading.Lock()

		self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
		self.parameters = aruco.DetectorParameters()
		self.detector = aruco.ArucoDetector(self.aruco_dict, self.parameters)

		self.thread = threading.Thread(target=self._update_loop, daemon=True)
		self.thread.start()

	def calculateCoordinates(self, corners, ids):
		# considering mono-z-axis map
		return corners, ids

	def _update_loop(self):
		while self.running:
			fresh, frame = self.camera.read_fresh_only()
			if not fresh or frame is None:
				continue

			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			corners, ids, _ = self.detector.detectMarkers(gray)

			if ids is not None:
				new_pos = self.calculateCoordinates(corners, ids)
				with self.lock:
					self.centerPos = new_pos

	def getLatestPos(self):
		with self.lock:
			return self.centerPos

	def stop(self):
		self.running = False
		self.camera.stop()

ve = VisionEngine()
prev = None
while True:
	print(ve.getLatestPos())
	time.sleep(1)