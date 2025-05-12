from basic import *
import os


if __name__ == "__main__":
    if compiler == "g++":
        if os.path.isfile(f"src/std.cc"):
            run(f"g++ -std=c++26 -O3 -fmodules -c src/std.cc -o ./gcm.cache/std.o")
        else:
            print(f"{red}e.g.: cp .../c++/15.1.0/bits/std.cc src/std.cc")

    elif compiler == "clang++":
        if os.path.isdir(f"src/std") and os.path.isfile(f"src/std.cppm"):
            run(f"clang++ -std=c++26 -O3 --precompile -c ./src/std.cppm      -o ./pcm.cache/std.pcm")
            run(f"clang++ -std=c++26 -O3              -c ./pcm.cache/std.pcm -o ./pcm.cache/std.o"  )
        else:
            print(f"{red}e.g.: cp -r .../llvm/share/libc++/v1/std ./src/std && cp .../llvm/share/libc++/v1/std.cppm ./src/std.cppm{white}")
