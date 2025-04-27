STB mod builder
===============

Docker image that runs a webservice able to build a Super Tilt Bro. mod into a downloadable ROM.

Build and start service
=======================

::

	docker build -t stb-mod-builder:latest .
	docker run -p 127.0.0.1:8000:8000 stb-mod-builder:latest

To rebuild with the latest version of Super Tilt Bro, use the ``--no-cache`` flag of ``docker build``.

Build the game
==============

Once the service is running, you can use it to build the game from an entire mod, or just a character. Both of which must be in a single JSON file.

Build a full mode by sending it to the ``/build/mod`` endpoint as POST data::

	curl -XPOST -vv http://127.0.0.1:8000/build/mod -d @/path/to/my_mod.json -H 'Content-Type: application/json' > /tmp/out.json

Build a single character by sending it to the ``/build/char`` endpoint as POST data::

	curl -XPOST -vv http://127.0.0.1:8000/build/char -d @/path/my_character.json -H 'Content-Type: application/json' > /tmp/out.json

You can reduce a mod or a character to a single JSON file with the script ``json_to_dict.py``, it depends on the ``stblib`` which is available in Super Tilt Bro.'s sources::

	stb_src=/path/to/stp/repository

	PYTHONPATH=/$stb_src/tools scripts/json_to_dict.py /$stb_src/game-mod/mod.json > /path/to/my_mod.json
	PYTHONPATH=/$stb_src/tools scripts/json_to_dict.py --base-path /$stb_src/game-mod /$stb_src/game-mod/characters/kiki/kiki.json > /path/to/my_mod.json
