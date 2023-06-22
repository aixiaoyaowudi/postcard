#! /usr/bin/python3

import json
import re
import os

def upper_text(ch):

    ret = ""

    for i in "ABCDEFGHIJKLM":
        if i == ch:
            ret += r"{\\color{red}{\\mathcal{%s}}}" % i
        else:
            ret += r"\\mathcal{%s}" % i
    
    return ret

def lower_text(ch):

    ret = ""

    for i in "NOPQRSTUVWXYZ":
        if i == ch:
            ret += r"{\\color{red}{\\mathcal{%s}}}" % i
        else:
            ret += r"\\mathcal{%s}" % i
    
    return ret

with open("./config.json","r") as f:
    data = json.load(f)

with open("./template.tex","r") as f:
    template = f.read()

compile_command = "xelatex -file-line-error -halt-on-error -interaction=nonstopmode -output-directory=./temp %s > /dev/null"
convert_command = "convert -density 600 -alpha remove %s %s > /dev/null"

for ch, _ in data.items():
    print("Processing %s" % ch)
    output = re.sub("UPPER_LEFT_TEXT", upper_text(ch), template)
    output = re.sub("LOWER_RIGHT_TEXT", lower_text(ch), output)
    output = re.sub("ALPHABET", r"\\mathcal{%s}" % ch, output)
    output = re.sub("SCALE_SIZE", str(_["scale"]), output)
    output = re.sub("FORMULA", _["formula"], output)
    output = re.sub("FORM_NAME", _["formula_name"], output)
    with open("./temp/%s.tex" % ch, "w") as f:
        f.write(output)
    
    print("Generating PDF")
    os.system(compile_command % ("./temp/%s.tex" % ch))

    print("Generating Image")
    os.system(convert_command % ("./temp/%s.pdf" % ch, "./output/%s.png" % ch))