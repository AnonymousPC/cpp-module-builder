from detail import *
import os

if __name__ == "__main__":
    if os.path.isdir(f"{module_path}/std") and os.path.isfile(f"{module_path}/std.cppm"):
        run(f"clang++ -std=c++26 -Wno-reserved-module-identifier --precompile {module_path}/std.cppm -o {module_path}/std.pcm")
    else:
        print(f"{red}You should prepare standard module manually in {module_path}{white}")
        print(f"{red}e.g.: cp .../llvm/share/libc++/v1/std {module_path}/std && cp .../llvm/share/libc++/v1/std.cppm {module_path}/std.cppm{white}")
        exit(-1)