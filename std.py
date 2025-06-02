from basic import *
import os


if __name__ == "__main__":
    if compiler == "g++":
        if os.path.isfile("./src/std.cc"):
            run("g++ -std=c++26 -O3 -fmodules -c src/std.cc -o ./module/std.o")
        else:
            log("e.g.: cp .../c++/15.1.0/bits/std.cc ./src/std.cc", color="red")

    elif compiler == "clang++":
        if os.path.isdir("./src/std") and os.path.isfile("./src/std.cppm"):
            run("clang++ -std=c++26 -O3 --precompile -c ./src/std.cppm   -o ./module/std.pcm")
            run("clang++ -std=c++26 -O3              -c ./module/std.pcm -o ./module/std.o"  )
        else:
            log("e.g.: cp -r .../llvm/share/libc++/v1/std ./src/std && cp .../llvm/share/libc++/v1/std.cppm ./src/std.cppm", color="red")

    elif compiler == "cl":
        if os.path.isfile("./src/std.ixx"):
            run("cl /std:c++latest /O2 /c ./src/std.ixx")
        else:
            log("e.g.: cp .../%VCToolsInstallDir%/modules/std.ixx ./src/std.ixx", color="red")
