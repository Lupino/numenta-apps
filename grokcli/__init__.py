#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Copyright (C) 2013 Numenta Inc. All rights reserved.
#
# The information and source code contained herein is the
# exclusive property of Numenta Inc.  No part of this software
# may be used, reproduced, stored or distributed in any form,
# without explicit written authorization from Numenta Inc.
#-------------------------------------------------------------------------------
import json
try:
  import yaml
except ImportError:
  pass
import sys
from functools import partial
from optparse import OptionParser

import commands
from exceptions import GrokCLIError


availableCommands = __import__("grokcli.commands", globals(), locals(), ['*'])

commands = dict([
    (cmd, getattr(availableCommands, cmd))
    for cmd in availableCommands.__all__
  ])

usage = "%prog [command] [options]\n\n" \
        "Available commands:\n"

for command in sorted(commands):
  usage += "\n    " + command

parser = OptionParser(usage=usage)


def handle(options, args):
  parser.print_help()


def printTerms():
  print
  print("By using the Grok CLI, you agree to terms and conditions "
        "outlined in the product End User License Agreement (EULA): "
        "https://aws.amazon.com/marketplace/agreement?asin=B00I18SNQ6")


def main():
  try:
    subcommand = sys.argv.pop(1)
  except IndexError:
    parser.print_help(sys.stderr)
    printTerms()
    sys.exit()

  submodule = commands.get(subcommand, sys.modules[__name__])

  (options, args) = submodule.parser.parse_args(sys.argv[1:])

  try:
    submodule.handle(options, args)
  except GrokCLIError as e:
    print >> sys.stderr, "ERROR:", e.message
    sys.exit(1)

  printTerms()


# Use yaml by default, if it's available
if "yaml" in sys.modules:
  load = yaml.safe_load
  dump = partial(yaml.safe_dump, default_flow_style=False)
else:
  load = json.loads
  dump = partial(json.dumps, indent=2)


def getCommonArgs(parser, args):
  try:
    server = args.pop(0)
    apikey = args.pop(0)
  except IndexError:
    parser.print_help(sys.stderr)
    sys.exit(1)

  return (server, apikey)
