
from flask import Flask, request, jsonify
from datetime import datetime
import subprocess
import os
import json

app = Flask(__name__)
#app.logger.setLevel(logging.DEBUG)

A2S_COMMAND = [os.environ["A2S_COMMAND"], 'info', '-j', str(os.environ["A3_SERVER_ADDRESS"])]

missionStatus = {
	"status": "Started",
	"modsetName": "RR Custom Mods",
	"map": "",
	"players": 0,
	"playersMax": 99
}

mission = {
	"title": "",
	"date": str(datetime.now().date().isoformat())
}

@app.route('/')
def default_func():
	return "ok", 200

@app.route('/status', methods=['GET'])
def get_status():
	print(f'Request: {request.remote_addr} /status')
	if not (update_status()):
		return jsonify({"status": "Stopped"})
	if missionStatus["map"] == "":
		return jsonify({"status": "Starting", "modsetName": "RR Custom Mods"})
	return jsonify(missionStatus)

@app.route('/missions', methods=['GET'])
def get_missions():
	return jsonify([mission])

@app.route('/currentMission', methods=['GET'])
def get_current_mission():
	return jsonify(mission)

@app.route('/attendances', methods=['POST'])
def post_attendance():
	return jsonify({"detail": "Good"})


def update_status():
	result = subprocess.run(A2S_COMMAND, capture_output=True, text=True)
	if result.returncode != 0:
		return False

	output = result.stdout
	json_output = json.loads(output)
	mission["title"] = json_output["game"]
	mission["date"] = str(datetime.now().date().isoformat())

	missionStatus["map"] = json_output["map"]
	missionStatus["players"] = int(json_output["players"])
	missionStatus["playersMax"] = int(json_output["max_players"])
	return True


def main():
	app.run(debug=True, host="0.0.0.0", port="61611")

if __name__ == "__main__":
	main()
