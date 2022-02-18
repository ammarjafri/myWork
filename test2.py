from imutils.video import VideoStream
from flask import Response, Flask, render_template 
import threading, datetime, imutils, time, cv2, argparse
from utils import Main
my_main = Main()
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

def detect_motion(frameCount):
	pass

def generate():
	# global outputFrame, lock
	fps = curr_fps = 0.0
	ptime= time.time()
	while True:
		img = vs.read()
	# img = imutils.resize(img, width=400)
		time.sleep(0.0000001)
		my_main.show_time(img)
		ntime = time.time()
		dif = ntime - ptime
		if dif != 0:
			curr_fps = 1.0 /dif 
		fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
		ptime=ntime
		
		my_main.add_fps(img,fps)
		with lock:
			flag, encodedImage = cv2.imencode(".jpg", img)
			if not flag:
				continue
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, default="0.0.0.0",
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, default=27011,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)
vs.stop()