import base64
import flask
import json
import logging
import pathlib
import subprocess
app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

stb_path = pathlib.Path("/root/super-tilt-bro")
original_mod_path = pathlib.Path("/root/original-mod.json")
mod_path = stb_path / "game-mod" / "mod.json"
build_bin_path = stb_path / "build.sh"
build_log_path = stb_path / "build.log"
rom_unrom_path = stb_path / "tilt_no_network_unrom_(E).nes"

running = False

@app.route("/build/char", methods=['POST'])
def hello():
	new_character = flask.request.json

	with open(original_mod_path, "r") as original_mod_file:
		mod = json.load(original_mod_file)

	replace_existing_character_id = None
	for character_id in range(len(mod["characters"])):
		if mod["characters"][character_id]["name"] == new_character.get("name"):
			replace_existing_character_id = character_id
			break

	if replace_existing_character_id:
		mod["characters"][replace_existing_character_id] = new_character
	else:
		mod["characters"].append(new_character)

	return build_roms(mod)

@app.route("/build/mod", methods=['POST'])
def hello2():
	return build_roms(flask.request.json)

def build_roms(mod):
	global running

	if running:
		return {"returncode": None, "output": "busy right now"}, 400

	try:
		running = True

		build_log_path.unlink(missing_ok=True)
		rom_unrom_path.unlink(missing_ok=True)

		with open(mod_path, "w") as mod_file:
			json.dump(mod, mod_file)
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
