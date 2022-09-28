# Wiser Hub Spoof
## Used to emulate a wiser hub for testing with user provided json files

* Utilises flask for web server
* Need to run the setcap.sh file to allow flask to run on port 80

Place a diagnotics file in the json dir (or sub dir under it).  Make sure it ends with .json.
Run python3 webserver.py -d json/[dir name]
