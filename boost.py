from detail import *
import os
import re
import subprocess

repo     = "boost"
src_dirs = []
for subrepo_status in subprocess.run(f"cd {module_path}/boost && git submodule status", shell=True, check=True, capture_output=True, text=True).stdout.splitlines():
    try:
        subrepo = re.match(r'^[ \+][0-9a-f]+ libs/([\w/]+) .*$', subrepo_status)[1] # 123456 libs/asio (boost-1.0.0)
        if os.path.isdir(f"{module_path}/boost/libs/{subrepo}/include"):
            src_dirs.append(f"./libs/{subrepo}/include") 
        if os.path.isdir(f"{module_path}/boost/libs/{subrepo}/src"):
            src_dirs.append(f"./libs/{subrepo}/src") 
    except:
        pass

import_modules = ["std"]
import_headers = [
    "<jerror.h>",
    "<jpeglib.h>",
    "<OpenCL/opencl.h>",
    "<openssl/ssl.h>",
    "<png.h>",
    "<tiff.h>",
    "<tiffio.h>",
    "<tiffio.hxx>",
    "<unicode/brkiter.h>",
    "<unicode/calendar.h>",
    "<unicode/coll.h>",
    "<unicode/datefmt.h>",
    "<unicode/gregocal.h>",
    "<unicode/locid.h>",
    "<unicode/normlzr.h>",
    "<unicode/numfmt.h>",
    "<unicode/rbbi.h>",
    "<unicode/rbnf.h>",
    "<unicode/smpdtfmt.h>",
    "<unicode/stringpiece.h>",
    "<unicode/timezone.h>",
    "<unicode/ustring.h>",
    "<unicode/ucasemap.h>",
    "<unicode/uchar.h>",
    "<unicode/ucnv.h>",
    "<unicode/ucnv_err.h>",
    "<unicode/unistr.h>",
    "<unicode/ustring.h>",
    "<unicode/utf.h>",
    "<unicode/utf16.h>",
    "<unicode/utypes.h>",
    "<unicode/uversion.h>",
    "<zlib.h>",
]
import_macros = {
    "BOOST_COMPUTE_HAVE_THREAD_LOCAL":          "", 
    "BOOST_COMPUTE_THREAD_SAFE":                "",
    "BOOST_COMPUTE_USE_CPP11":                  "",
    "BOOST_LOCALE_WITH_ICU":                    "",
    "BOOST_STACKTRACE_GNU_SOURCE_NOT_REQUIRED": ""
}
if system == "windows":
    import_macros["BOOST_LOCALE_NO_POSIX_BACKEND"] = ""
elif system == "linux" or system == "macos":
    import_macros["BOOST_LOCALE_NO_WINAPI_BACKEND"] = ""

export_module  = "boost"
export_headers = [
    "<boost/asio.hpp>",
    "<boost/asio/ssl.hpp>",
    "<boost/beast.hpp>",
    "<boost/compute.hpp>",
    "<boost/compute/container/stack.hpp>"
    "<boost/date_time.hpp>",
    "<boost/dll.hpp>",
    "<boost/gil.hpp>",
    "<boost/gil/extension/io/bmp.hpp>",
    "<boost/gil/extension/io/jpeg.hpp>", 
    "<boost/gil/extension/io/png.hpp>",
    "<boost/gil/extension/io/pnm.hpp>",
    "<boost/gil/extension/io/targa.hpp>",
    "<boost/gil/extension/io/tiff.hpp>",
    "<boost/iostreams/filtering_stream.hpp>",
    "<boost/iostreams/filter/bzip2.hpp>",
    "<boost/iostreams/filter/gzip.hpp>",
    "<boost/iostreams/filter/zlib.hpp>",
    "<boost/locale.hpp>",
    "<boost/mysql.hpp>",
    "<boost/process.hpp>",
    "<boost/spirit/home/classic.hpp>",
    "<boost/spirit/home/karma.hpp>",
    "<boost/spirit/home/lex.hpp>",
    "<boost/spirit/home/qi.hpp>",
    "<boost/spirit/home/x3.hpp>",
    "<boost/stacktrace.hpp>",
]
for subrepo in ["charconv", "datetime", "filesystem", "iostreams", "locale", "process", "system", "thread"]:
    for root, _, files in os.walk(f"{module_path}/boost/libs/{subrepo}/src"):
        for file in files:
            if ( system == "windows"                     and not "posix" in f"{root}/{file}") or \
               ((system == "linux" or system == "macos") and not "win"   in f"{root}/{file}" and not "wconv" in f"{root}/{file}"):
                export_headers.append(f'"{root}/{file}"')
export_headers.append(f'"{module_path}/boost/libs/stacktrace/src/basic.cpp"')

export_namespaces = [
    "std",
    "boost",
    "mpl_",
]

def on_preprocess(file, data):
    # static
    data = re.sub(r'^static\b',                                                                       "", data, flags=re.MULTILINE)
    data = re.sub(r'^constexpr static\b',                                                             
                  r'constexpr',                                                                           data, flags=re.MULTILINE)
    data = re.sub(r'^BOOST_STATIC_CONSTEXPR\b',
                  r'constexpr',                                                                           data, flags=re.MULTILINE)
    data = re.sub(r'^BOOST_CONSTEXPR static\b',
                  r'constexpr',                                                                           data, flags=re.MULTILINE)
    data = re.sub(r'namespace\s+(?P<namespace>\w+)\s*\{[\s\\]*'
                  r'\bstatic\b(?=\s+(const|constexpr)\b)',   
                  r'namespace \g<namespace> {',                                                           data                    )
    data = re.sub(r'namespace\s+(?P<namespace>\w+)\s*\{(\s*//[^\n]*\n)*[\s\\]*'
                  r'\btemplate\s*<(?P<template>[^<>]*)>\s*(static|inline static)\b',
                  r'namespace \g<namespace> { template <\g<template>>',                                   data, flags=re.MULTILINE)
    data = re.sub(r'namespace\s+(?P<namespace>\w+)\s*\{[\s\\]*'
                  r'\bBOOST_STATIC_CONSTANT\b\((?P<type>[\w\s:<>=+]+),(?P<assignment>[\w\s:<>=+]+)\)',
                  r'namespace \g<namespace> { constexpr \g<type> \g<assignment>;',                        data                    )
    data = re.sub(r'static(?=\s+inline\s+BOOST_FUSION_GPU_ENABLED\b)',                                "", data                    )

    # inline
    data = re.sub(r'\b(inline|BOOST_ASIO_DECL|BOOST_STACKTRACE_FUNCTION)\b'
                  r'(?=[a-zA-Z0-9_:<>&*\s,]+\([^\(\)]*\)[^\{\}]*;)',                                  "", data                    )
    data = re.sub(r'^BOOST_BEAST_INLINE_VARIABLE\((?P<name>.*), (?P<type>.*)\)$', 
                  r'constexpr auto& \g<name> = boost::beast::detail::static_const<\g<type>>::value;',     data, flags=re.MULTILINE)
    
    # extern "C"
    data = re.sub(r'extern\s+"C"\s+\{(?P<func>[^\{\}]*)\}',                                           
                  r'\g<func>',                                                                            data                    )
    data = re.sub(r'extern\s+"C"(?!\s+{)',                                                            "", data                    )

    # other
    data = re.sub(r'^BOOST_MOVE_STD_NS_BEG$(.|\n)*?^BOOST_MOVE_STD_NS_END$',                          "", data, flags=re.MULTILINE)
    data = re.sub(r'(?<=::)template(?=\s+\w+\()',                                                     "", data                    )

    # certain file
    if file.endswith("./libs/charconv/include/boost/charconv/detail/fast_float/fast_table.hpp"):
        data = re.sub(r'^constexpr', "constexpr static", data, flags=re.MULTILINE)

    if file.endswith("./libs/charconv/src/from_chars.cpp") or \
       file.endswith("./libs/charconv/src/to_chars.cpp"  ):
        data = re.sub(r'(?<!template <typename T>\n)^boost', "export boost", data, flags=re.MULTILINE)
        data = re.sub(r'static constexpr',                   "constexpr",    data)
        data = re.sub(r'static void',                        "void",         data)

    if file.endswith("./libs/locale/src/shared/date_time.cpp"):
        data = re.sub(r'using namespace period;', "",                    data)
        data = re.sub(r'period_type',             "period::period_type", data)

    if file.endswith("./libs/locale/src/shared/mo_hash.hpp"):
        data = "#pragma once\n" + data

    if file.endswith("./libs/thread/src/pthread/once_atomic.cpp"):
        data = "#pragma once\n" + data

    return data
        

if __name__ == "__main__":
    build(repo              = repo,
          src_dirs          = src_dirs,
          import_modules    = import_modules,
          import_headers    = import_headers,
          import_macros     = import_macros,
          export_module     = export_module,
          export_headers    = export_headers,
          export_namespaces = export_namespaces,
          on_preprocess     = on_preprocess,
          on_failure        = lambda: print(f"{green}remove above 'static' from function declaration{white}"))




    