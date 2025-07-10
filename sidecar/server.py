#!/usr/bin/env python3

from flask import Flask, request, redirect
from time import sleep
import os
import pprint
import subprocess
import re


# latex commands look like this:
# latexmk -cd -jobname=output -auxdir=/var/lib/sharelatex/data/compiles/67dbe26e588f6f00a1dfbf22-671b49b29b04a8171df57c5d -outdir=/var/lib/sharelatex/data/compiles/67dbe26e588f6f00a1dfbf22-671b49b29b04a8171df57c5d -synctex=1 -interaction=batchmode -f -xelatex /var/lib/sharelatex/data/compiles/67dbe26e588f6f00a1dfbf22-671b49b29b04a8171df57c5d/script.tex

TEXLIVE_IMAGE=os.environ.get('TEXLIVE_IMAGE',
        'docker.io/texlive/texlive:TL2024-historic')
UID=os.environ.get('SHARELATEX_UID', '33')
GID=os.environ.get('SHARELATEX_UID', '33')
TIMEOUT=os.environ.get("COMPILE_TIMEOUT", 600)
INFILE_REGEX="[a-zA-Z0-9\ _-]+\.tex"

#CMD_TEMPLATE="timeout {timeout} podman run -u{uid}:{gid} -v {auxdir}:{auxdir} --network=none {image} {command}"
CMD_TEMPLATE="timeout {timeout} podman run -u{uid}:{gid} -v {auxdir}:/mnt --network=none {image} {command}"
#LATEX_COMMAND_TEMPLATE='latexmk -cd -jobname=output -auxdir={auxdir} -outdir={outdir} -synctex=1 -interaction="batchmode" -f -{compiler} {infile}'
LATEX_COMMAND_TEMPLATE='latexmk -cd -jobname=output -auxdir=/mnt -outdir=/mnt -synctex=1 -interaction="batchmode" -f -{compiler} {infile}'

app = Flask(__name__)

@app.route("/")
def main():
    return "Nothing to see here."

@app.route("/compile")
def callback():
    latexmk_args = {
        "compiler" : request.args.get('compiler'),
        "infile" : request.args.get('infile'),
        "auxdir" : request.args.get('auxdir'),
        "outdir" : request.args.get('outdir'),
    }
    latexmk_args["infile"] = latexmk_args["infile"].removeprefix(
        latexmk_args["auxdir"] + "/")
    if not re.match(INFILE_REGEX, latexmk_args["infile"]):
      return "Error: We only support input files with letters, underscores, hyphens and spaces in the filaneme before the .tex"
    if len(latexmk_args["infile"]) > 64:
      return "64 characters should be enough for everone"

    latexmk_args["infile"] = '"%s"'%latexmk_args["infile"]

    latexmk = LATEX_COMMAND_TEMPLATE.format_map(latexmk_args)

    args = {
        "uid" : UID,
        "gid" : GID,
        "image" : TEXLIVE_IMAGE,
        "auxdir" : latexmk_args["auxdir"],
        "command" : latexmk,
        "timeout" : TIMEOUT,
    }
    command = CMD_TEMPLATE.format_map(args)

    try:
      code, output = subprocess.getstatusoutput(command)
      return output
    except subprocess.CalledProcessError as e:
      return output

if __name__=="__main__":
  app.run(host='0.0.0.0', port=6666, debug=True)

