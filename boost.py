from detail import *
import re

repo_cmd          = f"cp -r {module_path}/boost-download"
src_dirs          = [
    "./libs/algorithm/include",
    "./libs/align/include",
    "./libs/asio/include",
    "./libs/assert/include",
    "./libs/beast/include",
    "./libs/bind/include",
    "./libs/charconv/include",
    "./libs/charconv/src",
    "./libs/concept_check/include",
    "./libs/config/include",
    "./libs/container/include",
    "./libs/container_hash/include",
    "./libs/core/include",
    "./libs/date_time/include",
    "./libs/date_time/src",
    "./libs/describe/include",
    "./libs/detail/include",
    "./libs/dll/include",
    "./libs/endian/include",
    "./libs/filesystem/include",
    "./libs/filesystem/src",
    "./libs/function/include",
    "./libs/gil/include",
    "./libs/integer/include",
    "./libs/intrusive/include",
    "./libs/io/include",
    "./libs/iostreams/include",
    "./libs/iostreams/src",
    "./libs/iterator/include",
    "./libs/lexical_cast/include",
    "./libs/logic/include",
    "./libs/move/include",
    "./libs/mp11/include",
    "./libs/mpl/include",
    "./libs/mysql/include",
    "./libs/numeric/conversion/include",
    "./libs/optional/include",
    "./libs/predef/include",
    "./libs/preprocessor/include",
    "./libs/process/include",
    "./libs/process/src",
    "./libs/range/include",
    "./libs/smart_ptr/include",
    "./libs/static_assert/include",
    "./libs/static_string/include",
    "./libs/system/include",
    "./libs/throw_exception/include",
    "./libs/tokenizer/include",
    "./libs/type_traits/include",
    "./libs/utility/include",
    "./libs/variant2/include"
]
import_modules    = ["std"]
import_headers    = [
    # "<openssl/ssl.h>"
    # "<jpeglib.h>",
    # "<png.h>",
    # "<tiff.h>",

]
import_macros     = {
    "BOOST_COMPUTE_HAVE_THREAD_LOCAL":          "", 
    "BOOST_COMPUTE_THREAD_SAFE":                "",
    "BOOST_DISABLE_ASSERTS":                    "", 
    "BOOST_STACKTRACE_GNU_SOURCE_NOT_REQUIRED": ""
}
export_module     = "boost"
export_headers    = [
    "<boost/asio.hpp>",
    "<boost/beast.hpp>",
    "<boost/date_time.hpp>",
    "<boost/dll.hpp>",
    "<boost/gil.hpp>",
    "<boost/gil/extension/io/bmp.hpp>",
    "<boost/gil/extension/io/pnm.hpp>",
    "<boost/gil/extension/io/targa.hpp>",
    "<boost/iostreams/filtering_stream.hpp>",
    "<boost/process.hpp>"


    # "<boost/asio/ssl.hpp>",                # requires <openssl/ssl.h>
    # "<boost/compute.hpp>",                 # requires <CL/cl.h>
    # "<boost/gil/extension/io/jpeg.hpp>",   # requires <jpeglib.h>
    # "<boost/gil/extension/io/png.hpp>",    # requires <png.h>
    # "<boost/gil/extension/io/tiff.hpp>",   # requires <tiff.h>
    # "<boost/iostreams/filter/bzip2.hpp>",
    # "<boost/iostreams/filter/gzip.hpp>",
    # "<boost/iostreams/filter/zlib.hpp>",   # requires <zlib.h>
    # "<boost/locale.hpp>",                  # requires icu
    # "<boost/mysql.hpp>",                   # requires <openssl/sha.h>
]
export_namespaces = [
    "std",
    "boost",
    "mpl_",
]

def on_preprocess(file):
    file = re.sub(r'^static\b',                                                                       "", file, flags=re.MULTILINE)
    file = re.sub(r'^constexpr static\b',                                                             
                  r'constexpr',                                                                           file, flags=re.MULTILINE)
    file = re.sub(r'^BOOST_STATIC_CONSTEXPR\b',
                  r'constexpr',                                                                           file, flags=re.MULTILINE)
    file = re.sub(r'^BOOST_CONSTEXPR static\b',
                  r'constexpr',                                                                           file, flags=re.MULTILINE)
    file = re.sub(r'namespace\s+(?P<namespace>\w+)\s*\{(\s|\\)*\bstatic\b(?=\s+(const|constexpr))',   
                  r'namespace \g<namespace> {',                                                           file                    )
    
    file = re.sub(r'\b(inline|BOOST_ASIO_DECL)\b(?=[a-zA-Z0-9_:<>&*\s,]+\([^\(\)]*\)[^\{\}]*;)',      "", file                    )
    file = re.sub(r'^BOOST_BEAST_INLINE_VARIABLE\((?P<name>.*), (?P<type>.*)\)$', 
                  r'constexpr auto& \g<name> = boost::beast::detail::static_const<\g<type>>::value;',     file, flags=re.MULTILINE)
    
    file = re.sub(r'extern\s+"C"\s+\{(?P<func>[^\{\}]*)\}',                                           
                  r'\g<func>',                                                                            file                    )
    file = re.sub(r'extern\s+"C"(?!\s+{)',                                                            "", file                    )
    file = re.sub(r'^BOOST_MOVE_STD_NS_BEG$(.|\n)*?^BOOST_MOVE_STD_NS_END$',                          "", file, flags=re.MULTILINE)
    return file

if __name__ == "__main__":
    build(repo_cmd          = repo_cmd,
          src_dirs          = src_dirs,
          import_modules    = import_modules,
          import_headers    = import_headers,
          import_macros     = import_macros,
          export_module     = export_module,
          export_headers    = export_headers,
          export_namespaces = export_namespaces,
          on_preprocess     = on_preprocess,
          on_failure        = lambda: print(f"{green}remove above 'static' from function declaration{white}"))




    