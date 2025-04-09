import os
import shutil
import subprocess
import sys

dirs = ["stdexec", "exec", "nvexec", "tbbexec", "execpools"]

for dir in dirs:
    try:
        shutil.rmtree(dir)
    except:
        pass
    shutil.copytree(f"../../include/{dir}", f"{dir}")

    for root, _, files in os.walk(dir):
        for file in files:
            with open(f"{root}/{file}", 'r') as reader, \
                 open(f"{root}/{file}", 'w') as writer:
                for line in reader:
                    writer.write(line.replace(f"namespace {dir}", f"export namespace {dir}"))


with open("stdexec.cppm", 'w') as cppm:
    cppm.write("export module stdexec;\n")
    cppm.write("import std;\n")
    for dir in dirs:
        for file in os.listdir(dir):
            if os.path.isfile(file):
                cppm.write(f"#include \"{dir}/{file}\"\n") # depth = 1

try:
    subprocess.run("clang++ -std=c++26 -O3 -g -fprebuilt-module-path=.. stdexec.cppm --precompile -o ../stdexec.pcm", shell=True, check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    print(e.stderr, file=sys.stderr)

    