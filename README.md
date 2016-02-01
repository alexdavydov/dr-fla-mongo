# dr-fla-mongo

Entry point is at application/app.py
Dependencies:
- Flask
- Flask-PyMongo
- dateutil
- argparse
- ConfigParser

TODO:
- mongo auth
- connecting to mongos instances (not tested, might be irrelevant with PyMongo 3.2+)
- unit tests still don't work as expected

Interface:
* /store - POST endpoint, accepts a JSONObject or JSONArray of "uid,name,date,md5checksum". Expects application/json content-type, all fields are mandatory. Checksum is calculated as MD5 hash of JSON string of date,name,uid sorted by key name. Stores the structure in Mongo backend. See tests/ directory for sample JSON.
* /count - GET endpoint, accepts 2 mandatory parameters, "uid" and "date". Returns a number of occurences of particular uid on a given day.

Configuration:
application/app.py accepts "-c" parameter with path to config file, otherwise "config/test.cfg" is used. -d enables Flask debug mode.
Config file parameters:
* host, port - define the listening socket
* dbname, mongohost, mongoport *or* mongouri - backend database parameters

DB structure:
Data is stored in specified database in a collection named "data". Following BSON types are in use:
* _id - Mongo primary key
* uid - Int (32 or 64 depending on size)
* name - String
* date - Date
