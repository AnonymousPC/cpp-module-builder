import os
import random
import re
import shutil
import subprocess
import sys

# Global

system = ""
if sys.platform == "win32":
    system = "windows"
elif sys.platform == "linux":
    system = "linux"
elif sys.platform == "darwin":
    system = "macos"

red     = "\033[38;2;240;240;0m"
yellow  = "\033[38;2;240;240;0m"
green   = "\033[38;2;0;240;0m"
white   = "\033[38;2;192;192;192m"
random.seed(0)



# Config

if system == "windows":
    compiler     = "g++"
    include_path = "F:/msys/ucrt64/include"
    lib_path     = "F:/msys/ucrt64/lib"
    module_path  = "F:/msys/ucrt64/module"
elif system == "linux":
    compiler     = "g++"
    include_path = "/usr/include"
    lib_path     = "/usr/lib"
    module_path  = "/usr/module"
elif system == "macos":
    compiler     = "clang++"
    include_path = "/opt/homebrew/include"
    lib_path     = "/opt/homebrew/lib"
    module_path  = "/opt/homebrew/module"

compile_args = ["-std=c++26", "-O3", "-g", "-Wall", "-fdiagnostics-color=always", "-Wno-include-angled-in-module-purview"]
link_args    = []




# Compile
     
def build(repo_cmd,                          # "git clone https://github.com/NVIDIA/stdexec.git"
          src_dirs,                          # ["./include"]
          import_modules,                    # ["std"]
          import_headers,                    # ["<tbb/tbb.h>m"]
          import_macros,                     # None
          export_module,                     # "stdexec"
          export_headers,                    # ["<stdexec/concepts.hpp>", "<stdexec/coroutine.hpp>", "<stdexec/execution.hpp>", ...]
          export_namespaces,                 # ["stdexec", "exec", "execpools"]
          on_preprocess = lambda file: file, # None
          on_success    = lambda     : None, # None
          on_failure    = lambda     : None  # print("remove above 'static' from the function declaration (totally about 1-2 times)")
         ):
    repo_dir = f"{module_path}/{export_module}" # "/usr/module/stdexec"

    try:
        shutil.rmtree(repo_dir) # /usr/module/stdexec
    except:
        pass
    run(f"{repo_cmd} {repo_dir}")

    for src_dir in src_dirs:
        for root, _, files in os.walk(f"{repo_dir}/{src_dir}"): # usr/module/stdexec/include
            for file in files:
                try:
                    data = ""

                    with open(f"{root}/{file}", 'r') as reader:
                        data = reader.read()

                    for export_namespace in export_namespaces:
                        data = re.sub(fr'\b(?<!using )(?<!export )namespace\s+{export_namespace}(?=(::[a-zA-Z0-9:_]*)?\b)', f"export namespace {export_namespace}", data) # export namespace stdexec

                    data = re.sub(r'\bnamespace(?=\s+{)', f"inline namespace __anonymous_{random.randint(0, 65535)}__", data) # namespace {}

                    data = on_preprocess(data)

                    with open(f"{root}/{file}", 'w') as writer:
                        writer.write(data)

                except Exception as error:
                    print(f"{red}warning: processing {root}/{file} failed: {error}{white}")

    with open(f"{module_path}/{export_module}.cppm", 'w') as cppm: # /usr/module/stdexec.cppm
        cppm.write(global_module) # module;

        for import_macro in import_macros.items():
            cppm.write(f"#define {import_macro[0]} {import_macro[1]}\n")

        for import_header in import_headers:
            cppm.write(f"#include {import_header}\n") # include <tbb/tbb.h>

        cppm.write(f"export module {export_module};\n") # export module stdexec;
        for import_module in import_modules:
            cppm.write(f"import {import_module};\n") # import std;
            
        for export_header in export_headers:
            cppm.write(f"#include {export_header}\n") # include <stdexec/execution.hpp>

    while True:
        try:
            run(f"{compiler} "
                f"{' '.join(compile_args)} "
                f"{' '.join(link_args)} "
                f"{' '.join(f"-I{repo_dir}/{src_dir}" for src_dir in src_dirs)} "
                f"-fprebuilt-module-path={module_path} "
                f"{module_path}/{export_module}.cppm "
                f"--precompile -o {module_path}/{export_module}.pcm")
            on_success()
            break
        except Exception:
            on_failure()
            try:
                input(f"{yellow}Press Enter to re-compile, or Ctrl-C to abort:{white}")
            except KeyboardInterrupt:
                exit(-1)



def run(command):
    print(f"{yellow}{command}{white}")
    subprocess.run(command, shell=True, check=True)



global_module = \
'''
module;
#include <algorithm>
#include <any>
#include <array>
#include <atomic>
#include <barrier>
#include <bit>
#include <bitset>
#include <cassert>
#include <cctype>
#include <cerrno>
#include <cfenv>
#include <cfloat>
#include <charconv>
#include <chrono>
#include <cinttypes>
#include <climits>
#include <clocale>
#include <cmath>
#include <codecvt>
#include <compare>
#include <complex>
#include <concepts>
#include <condition_variable>
#include <coroutine>
#include <csetjmp>
#include <csignal>
#include <cstdarg>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cuchar>
#include <cwchar>
#include <cwctype>
#include <deque>
#include <exception>
#include <execution>
#include <expected>
#include <filesystem>
#include <flat_map>
#include <format>
#include <forward_list>
#include <fstream>
#include <functional>
#include <future>
#include <initializer_list>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <iterator>
#include <latch>
#include <limits>
#include <list>
#include <locale>
#include <map>
#include <mdspan>
#include <memory>
#include <memory_resource>
#include <mutex>
#include <new>
#include <numbers>
#include <numeric>
#include <optional>
#include <ostream>
#include <print>
#include <queue>
#include <random>
#include <ranges>
#include <ratio>
#include <regex>
#include <scoped_allocator>
#include <semaphore>
#include <set>
#include <shared_mutex>
#include <source_location>
#include <span>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <stop_token>
#include <streambuf>
#include <string>
#include <string_view>
#include <strstream>
#include <syncstream>
#include <system_error>
#include <thread>
#include <tuple>
#include <type_traits>
#include <typeindex>
#include <typeinfo>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <valarray>
#include <variant>
#include <vector>
#include <version>

#ifdef _WIN32
    #include <windows.h>
    #include <winsock2.h>
#elifdef __linux__
    // Nothing...
#elifdef __APPLE__
    #include <netdb.h>
    #include <sys/event.h>
    #include <sys/fcntl.h>
    #include <sys/ioctl.h>
    #include <sys/poll.h>
    #include <sys/socket.h>
    #include <sys/stat.h>
    #include <sys/termios.h>
    #include <sys/time.h>
    #include <sys/unistd.h>
    #include <sys/_select.h>
    #include <mach/arm/thread_status.h>
    #include <mach-o/dyld.h>
    #include <mach-o/nlist.h>
#endif

#ifdef __GNUC__
    #include <cxxabi.h>
#endif
'''
