from db import mongo
from werkzeug import exceptions
from collections import OrderedDict
from types import ListType, DictType
from hashlib import md5
import json
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from datetime import datetime, time


def query_db(date, next_date, uid):
  """
  Count all occurences of uid in a given day
  """
  res = mongo.db.data.find({"uid": uid,
                            "date": {"$gte": date, "$lt": next_date}
                            }).count()
  print res
  return res


def parse_input(data):
  content = []
  if type(data) is ListType:
    for i in xrange(len(data)):
      content.append(parse_dict(data[i]))
  elif type(data) is DictType:
    content.append(parse_dict(data))
  else:  # in case we get smth other than JSONArray or JSONObject
    raise exceptions.BadRequest("Unexpected format")
  print content
  return content


def parse_dict(dct):
  """
  Validate the data, convert strings to proper types for storage
  """
  if sorted(dct.keys()) != sorted(["date", "md5checksum", "name", "uid"]):
    raise exceptions.BadRequest("Bad format, missing or extra fields")
  # Lamda magic, lifted straight from docs :D creates a dict sorted by key
  content = OrderedDict(sorted(dct.items(), key=lambda t: t[0]))
  print content
  sum_1 = content.pop("md5checksum", None)
  sum_2 = md5()
  sum_2.update(json.dumps(content))
  if sum_1 != sum_2.hexdigest():
    raise exceptions.BadRequest("Bad MD5 sum in message")
  try:
    content["uid"] = int(content["uid"])  # store uid as int
  except:
    raise exceptions.BadRequest("Expecting a numeric uid")
  try:
    #content["date"] = datetime.strptime(content["date"],
    #                                    "%Y-%m-%dT%H:%M:%S.%f")
    content["date"] = parse_date(content["date"])  # convert str to datetime
  except:
    raise exceptions.BadRequest("Unexpected date format")
  return content


def insert_data(data):
  try:
    mongo.db.data.insert(data)
    return 0
  except:
    raise exceptions.InternalServerError("Database insertion failed")
    return 1


def get_date(date):
  """
  Get current date at midnight and the next day from timestamp
  """
  req_date = parse_date(date)
  # Set time to midnight
  req_date = datetime.combine(req_date.date(), time.min)
  next_day = req_date + relativedelta(days=+1)
  return (req_date, next_day)
