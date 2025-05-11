from basic import *
import os


if __name__ == "__main__":
    if compiler == "g++":
        if os.path.isfile(f"src/std_g++.cppm"):
            run(f"g++ -std=c++26 -O3 -fmodules -fmodule-only src/std_g++.cppm -c")
        else:
            print(f"{red}e.g.: cp .../c++/15.1.0/bits/std.cc src/std_g++.cppm")

    elif compiler == "clang++":
        if os.path.isdir(f"src/std") and os.path.isfile(f"src/std_clang++.cppm"):
            run(f"clang++ -std=c++26 -O3 --precompile src/std_clang++.cppm -c -o pcm.cache/std.pcm")
            run(f"clang++ -std=c++26 -O3              pcm.cache/std.pcm    -c -o pcm.cache/std.o"  )
        else:
            print(f"{red}e.g.: cp -r .../llvm/share/libc++/v1/std src/std && cp .../llvm/share/libc++/v1/std.cppm src/std_clang++.cppm{white}")