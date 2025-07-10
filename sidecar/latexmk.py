#!/usr/bin/python3

import sys
import re
from urllib import request, parse

TIMEOUT=600
INFILE_REGEX="[a-zA-Z0-9\ _-]+\.tex"

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

infile_without_path = args["infile"][len(args["auxdir"])+1:]
if not re.match(INFILE_REGEX, infile_without_path):
  print("latexmk Error: We only support input files with letters, hyphens, underscores and spaces in the filename before the .tex")
  with open(args["auxdir"] + "/output.log", "a") as f:
    f.write("Error: Filename not supported. Please only use letters, hyphens, underscores and spaces before the .tex\n")
  sys.exit(0)

if len(infile_without_path) > 64:
  with open(args["auxdir"] + "/output.log", "a") as f:
    f.write("Error: Filename too long. 64 characters should be enough")

arg_string = parse.urlencode(args)

with request.urlopen("%s?%s"%(HOST, arg_string), timeout=TIMEOUT) as f:
    print(f.read().decode('utf-8'))
