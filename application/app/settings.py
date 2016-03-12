import os
from ConfigParser import SafeConfigParser
from argparse import ArgumentParser

from flask import Flask

from db import mongo
from views import views


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="Configuration file path",
                        default="config/test.cfg")
    parser.add_argument("-d", "--debug",
                        help="Start in debug mode",
                        action="store_true")
    return parser.parse_args()


def parse_config(path):
    parser = SafeConfigParser(defaults={"host": "0.0.0.0",
                                        "port": "8080"})
    try:
        open(path)
    except IOError as e:
        raise EnvironmentError("{} - {}".format(path, os.strerror(e.errno)))
    parser.read(path)
    return parser


def create_app(config_file, debug_mode=False):
    app = Flask(__name__)
    config = parse_config(config_file)
    if config.has_option("mongo", "dbname"):
        app.config.update({"MONGO_DBNAME": config.get("mongo", "dbname"),
                           "MONGO_HOST": config.get("mongo", "mongohost"),
                           "MONGO_PORT": config.get("mongo", "mongoport")})
    elif config.has_option("mongo", "mongouri"):
        app.config.update({"MONGO_URI": config.get("mongo", "mongouri")})
    mongo.init_app(app)
    app.register_blueprint(views)
    app.run(host=config.get("app", "host"),
            port=config.getint("app", "port"),
            debug=debug_mode)
    return app
