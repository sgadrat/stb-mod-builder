import base64
import flask
import json
import logging
import pathlib
import subprocess
app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

stb_path = pathlib.Path("/root/super-tilt-bro")
mod_path = stb_path / "game-mod" / "mod.json"
build_bin_path = stb_path / "build.sh"
build_log_path = stb_path / "build.log"
rom_unrom_path = stb_path / "tilt_no_network_unrom_(E).nes"

running = False

@app.route("/build/char", methods=['POST'])
def hello():
    return flask.request.json

@app.route("/build/mod", methods=['POST'])
def hello2():
	global running

	if running:
		return {"returncode": None, "output": "busy right now"}, 400

	try:
		running = True

		with open(mod_path, "w") as mod_file:
			json.dump(flask.request.json, mod_file)
		result = subprocess.run(
			[str(build_bin_path)],
			text=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT
		)

		def load_file(path, mode):
			try:
				with open(path, f"r{mode}") as log_file:
					return log_file.read()
			except Exception as e:
				logging.error(f"Failed to open \"{path}\": {e}")
				if mode == "t":
					return ""
				elif mode == "b":
					return b""
				else:
					assert False

		return (
			{
				"returncode": result.returncode,
				"output": result.stdout,
				"build_log": load_file(build_log_path, "t"),
				"roms": {
					"unrom": base64.b64encode(load_file(rom_unrom_path, "b")).decode(),
				}
			},
			200 if result.returncode == 0 else 400
		)
	finally:
		running = False
