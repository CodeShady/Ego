import sys
import os
import time
import re

# Config
replaces = {
    r"\bfunc\b": "def",
    r"\bpout\b": "print",
    r"--!": "!=",
    r"-->": "==",
    r"->": "=",
    r"{": "",
    r"}": "",
}
tmpfile = "./.egotmp.py"

# Functions
def open_file(filename):
	data = open(filename, "r").read()
	return data

def write_file(filename, data):
    file = open(filename, "w+")
    file.seek(0)
    for line in data:
        file.write(line + "\n")
    file.close()


def parse(data):
    variables = {}
    data = data.split("\n")
    newData = []

    for line in data:

        # Check for constant variable
        if "[const]" in line:
            try:
                variable_name = line[:line.index("[const]")].strip()
                variable_data = line[line.index("->")+2:].strip()
                variables[variable_name] = variable_data
                continue
            except ValueError as e:
                print("\n\t[EGO] Error! ValueError error!\n")
                print(e)

        newData.append(line)

    return newData, variables


def replace(data, variables):

    newData = []


    for line in data:
        lineData = line

        # Replace constant variables
        for var, value in variables.items():
            lineData = lineData.replace(var, value)

        # Replace the replaces
        for key, value in replaces.items():
            lineData = re.sub(key, value, lineData)

        newData.append(lineData)


    return newData


def run(code):
    write_file(tmpfile, code)
    os.system("python3 " + tmpfile)



# Main Code
if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(1)
    # Continue
    fileData = open_file(sys.argv[1])
    data, variables = parse(fileData)
    code = replace(data, variables)
    # print(code)
    run(code)