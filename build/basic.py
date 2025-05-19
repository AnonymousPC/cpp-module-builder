import os
import re
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

red     = "\033[38;2;240;0;0m"
yellow  = "\033[38;2;240;240;0m"
green   = "\033[38;2;0;240;0m"
white   = "\033[38;2;192;192;192m"



# Config

if system == "windows":
    compiler     = "cl"
    include_path = "F:/msys/ucrt64/include"
    lib_path     = "F:/msys/ucrt64/lib"
elif system == "linux":
    compiler     = "g++"
    include_path = "/usr/include"
    lib_path     = "/usr/lib"
elif system == "macos":
    compiler     = "clang++"
    include_path = "/opt/homebrew/include"
    lib_path     = "/opt/homebrew/lib"

compile_args = [
    "-std=c++26", 
    "-O3", 
    "-g", 
    "-w",
    "-fdiagnostics-color=always",
]
if compiler == "g++":
    compile_args.append("-fmodules")
elif compiler == "clang++":
    compile_args.append("-fprebuilt-module-path=./pcm.cache")




# Compile
     
def build(repo,                                    # "stdexec"
          src_dirs,                                # ["./include"]
          import_modules,                          # ["std", "boost", "tbb"]
          import_headers,                          # []
          import_macros,                           # None
          export_module,                           # "stdexec"
          export_headers,                          # ["<stdexec/concepts.hpp>", "<stdexec/coroutine.hpp>", "<stdexec/execution.hpp>", ...]
          export_namespaces,                       # ["stdexec", "exec", "asioexec", "nvexec", "tbbexec", "execpools"]
          on_preprocess = lambda file, data: data, # data = data.replace(...)
          on_success    = lambda           : None, # None
          on_failure    = lambda           : None  # print("remove above 'static' from the function declaration")
         ):
    
    run(f"cd src/{repo} && git reset --hard origin/HEAD --recurse-submodules")

    # for src_dir in src_dirs:
    #     for root, _, files in os.walk(f"./src/{repo}/{src_dir.replace("./", "")}"): # usr/module/stdexec/include
    #         for file in files:
    #             try:
    #                 data = ""

    #                 with open(f"{root}/{file}", 'r', encoding="utf-8") as reader:
    #                     data = reader.read()

    #                 for import_module in import_modules:
    #                     data = re.sub(fr'#\s*include\s*<{import_module.replace('.', '/')}[^<>]*>', "", data) # include <boost/asio.hpp>

    #                 for export_namespace in export_namespaces:
    #                     data = re.sub(fr'\b(?<!using )(?<!export )(?<!// )namespace\s+{export_namespace}(?=(::[a-zA-Z0-9:_]*)?\b)', f"export namespace {export_namespace}", data) # export namespace stdexec

    #                 data = re.sub(r'\bnamespace(?=[\s\\]*{)', f"inline namespace __anonymous_{count()}__", data) # namespace {}

    #                 data = on_preprocess(f"{root}/{file}".replace('\\', '/'), data)

    #                 with open(f"{root}/{file}", 'w', encoding="utf-8") as writer:
    #                     writer.write(data)

    #             except Exception as e:
    #                 print(f"{red}preprocessing {file} failed: {e}{white}")

    with open(f"./src/{export_module}.cppm", 'w') as cppm: # /usr/module/stdexec.cppm
        cppm.write(global_module) # module;

        for import_macro in import_macros.items():
            cppm.write(f"#define {import_macro[0]} {import_macro[1]}\n") # define 

        for import_header in import_headers:
            cppm.write(f"#include {import_header}\n") # include <header/file>

        cppm.write(f"export module {export_module};\n") # export module stdexec;

        for import_module in import_modules:
            cppm.write(f"import {import_module};\n") # import std;
            
        for export_header in export_headers:
            if re.match(r'<[^<>]*>', export_header):
                cppm.write(f"#include {export_header}\n") # include <stdexec/execution.hpp>
            else:
                cppm.write(f'#include "{os.path.abspath(export_header)}"\n') # include <stdexec/implemention.cpp>

    while True:
        try:
            if compiler == "g++":
                run(f"{compiler} "
                    f"{' '.join(compile_args)} "
                    f"{' '.join(f"-I./src/{repo}/{src_dir.replace("./", "")}" for src_dir in src_dirs)} "
                    f"-I{include_path} "
                    f"-c ./src/{export_module}.cppm "
                    f"-o ./gcm.cache/{export_module}.o")
            elif compiler == "clang++":
                run(f"{compiler} "
                    f"{' '.join(compile_args)} "
                    f"{' '.join(f"-I./src/{repo}/{src_dir.replace("./", "")}" for src_dir in src_dirs)} "
                    f"-I{include_path} "
                    f"--precompile ./src/{export_module}.cppm "
                    f"-o ./pcm.cache/{export_module}.pcm")
                run(f"{compiler} "
                    f"{' '.join(compile_args)} "
                    f"-c ./pcm.cache/{export_module}.pcm "
                    f"-o ./pcm.cache/{export_module}.o")
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




# Detail

counter = 0
def count():
    global counter
    counter += 1
    return counter

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
    #include <errhandlingapi.h>                                                             
    #include <fileapi.h>                                                                    
    #include <handleapi.h>                                                                  
    #include <heapapi.h>                                                                    
    #include <libloaderapi.h>                                                               
    #include <memoryapi.h>                                                                                                                                                                                     
    #include <processthreadsapi.h>                                                          
    #include <profileapi.h>                                                                 
    #include <stringapiset.h>                                                               
    #include <synchapi.h>                                                                   
    #include <sysinfoapi.h>                                                                 
    #include <threadpoollegacyapiset.h>                                                     
    #include <timezoneapi.h>                                                                                                                                
    #include <wincrypt.h>                                                                 
    #include <winnt.h> 
    #include <winsock2.h>   
    #include <ws2tcpip.h>                                                                  
    #include <winbase.h>    
#elifdef __linux__
    // Nothing...
#elifdef __APPLE__
    #define _XOPEN_SOURCE
    #include <dirent.h>
    #include <dispatch/dispatch.h>
    #include <mach/host_info.h>
    #include <mach/task_info.h>
    #include <mach/arm/thread_status.h>
    #include <mach-o/dyld.h>
    #include <mach-o/nlist.h>
    #include <netdb.h>
    #include <net/route.h>
    #include <os/workgroup.h>
    #include <sys/event.h>
    #include <sys/fcntl.h>
    #include <sys/ioctl.h>
    #include <sys/mount.h>
    #include <sys/poll.h>
    #include <sys/proc.h>
    #include <sys/proc_info.h>
    #include <sys/select.h>
    #include <sys/socket.h>
    #include <sys/stat.h>
    #include <sys/sysctl.h>
    #include <sys/termios.h>
    #include <sys/time.h>
    #include <sys/unistd.h>
    #include <sys/_select.h>
    #include <ucontext.h>
    #include <unwind.h>
    #include <utime.h>
#endif
#ifdef __GNUC__
    #include <cxxabi.h>
#endif
#if defined(__GNUC__) and not defined(__clang__)
    #include <stacktrace>
#elifdef __clang__
    #include <mdspan>
#endif
'''
