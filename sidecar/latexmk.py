#!/usr/bin/python3

import sys
from urllib import request, parse

TIMEOUT=600

HOST="http://127.0.0.1:6666/compile"

COMPILER = ["-pdf", "-pdfdvi", "-lualatex", "-xelatex"]

compiler = ""
infile = ""
auxdir = ""
outdir = ""

# len because latex container too old for .removeprefix
for arg in sys.argv:
  if arg.startswith("-auxdir"):
    auxdir = arg[len("-auxdir="):]
  elif arg.startswith("-outdir"):
    outdir = arg[len("-outdir="):]
  elif arg in COMPILER:
    compiler = arg[len("-"):]
  elif arg == sys.argv[-1]:
   infile = arg

args = {
    "compiler" : compiler,
    "infile" : infile,
    "auxdir" : auxdir,
    "outdir" : outdir,
}

arg_string = parse.urlencode(args)

with request.urlopen("%s?%s"%(HOST, arg_string), timeout=TIMEOUT) as f:
    print(f.read().decode('utf-8'))


