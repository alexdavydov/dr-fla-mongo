#!/usr/bin/env python

from app.settings import create_app, parse_arguments

if __name__ == "__main__":
  args = parse_arguments()
  app = create_app(args.config, args.debug)
