STB mod builder
===============

WIP project.

Goal: generate a Docker image that runs a webservice able to build a Super Tilt Bro. mod into a downloadable ROM.

Notes
=====

::

	# Build and start service
	#   use "docker build --no-cache" to get the latest git revision of STB
	docker build -t stb-mod-builder:latest .
	docker run -p 127.0.0.1:8000:8000 stb-mod-builder:latest

	# Build a full game mod
	./json_to_dict.py ~/workspace/nes/tilt/game-mod/mod.json > /tmp/stb25mod.json
	curl -XPOST -vv http://127.0.0.1:8000/build/mod -d @/tmp/stb25mod.json -H 'Content-Type: application/json' > /tmp/out.json
	cat /tmp/out.json | jq -r .roms.unrom | base64 -d > /tmp/tilt_unrom\(E\).nes

	# Build only a character
	~/workspace/nes/tools/json_to_dict.py --base-path ~/workspace/nes/tilt/game-mod ~/workspace/nes/tilt/game-mod/characters/sunny/sunny.json > /tmp/mysunny.json
	curl -XPOST -vv http://127.0.0.1:8000/build/char -d @/tmp/mysunny.json -H 'Content-Type: application/json' > /tmp/out.json
