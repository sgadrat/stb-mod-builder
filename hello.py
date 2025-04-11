import flask
import json
import pathlib
import subprocess
app = flask.Flask(__name__)

stb_path = pathlib.Path("/root/super-tilt-bro")
mod_path = stb_path / "game-mod" / "mod.json"
build_bin_path = stb_path / "build.sh"

running = False

@app.route("/build/char", methods=['POST'])
def hello():
    return flask.request.json

@app.route("/build/mod", methods=['POST'])
def hello2():
	global running

	if running:
		return (400, {"returncode": None, "output": "busy right now"})

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
		return (
			200 if result.returncode == 0 else 400,
			{
				"returncode": result.returncode,
				"output": result.stdout,
			}
		)
	finally:
		running = False
