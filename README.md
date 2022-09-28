# Wiser Hub Spoof
## Used to emulate a wiser hub for testing with user provided json files

* Utilises flask for web server
* Provides MDNS functionality so that Home Assistant will discover it as a new hub

Install

Clone this repo.

```code
git clone https://github.com/msp1974/wisermockserver.git
```

Create a python 3.x venv

```code
cd wisermockserver
python3 -m venv venv
```

Switch to venv

```code
source /venv/bin/activate
```

Install flask and mdns_beacon

```code
pip3 install flask mdns_beacon
```

By default, flask will not have permissions to run on port 80 and you will get an error running this.  Run the following command to allow flask to run on port 80.

**NOTE** You may need to modify this file if you are not running python3.10 to point to your version of python.

```code
sudo ./setcap.sh
```

Place a Wiser diagnotics file (sourced from download diagnostics in Home Assistant) in a subdirectory under the json dir.  Copy your diagnostics file into that subdirectory and ensure sure it ends with .json

To then run the server

```code
python3 webserver.py -d json/[dir name]
```
