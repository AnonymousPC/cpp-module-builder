from basic import *
import os


if __name__ == "__main__":
    if compiler == "g++":
        if os.path.isfile(f"module/std.cppm"):
            run(f"g++ -std=c++26 -O3 -fmodules -fmodule-only module/std.cppm -c")
        else:
            print(f"{red}e.g.: cp .../c++/15.1.0/bits/std.cc module/std.cppm")

    elif compiler == "clang++":
        if os.path.isdir(f"module/std") and os.path.isfile(f"module/std.cppm"):
            run(f"clang++ -std=c++26 -O3 --precompile module/std.cppm           -c -o module/pcm.cache/std.pcm")
            run(f"clang++ -std=c++26 -O3              module/pcm.cache/std.pcm  -c -o module/pcm.cache/std.o"  )
        else:
            print(f"{red}e.g.: cp -r .../llvm/share/libc++/v1/std module/std && cp .../llvm/share/libc++/v1/std.cppm module/std.cppm{white}")