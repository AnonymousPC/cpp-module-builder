from basic.basic import *
import os
import re

repo              = "tbb"
src_dirs          = ["./include", "./src"]
import_modules    = ["std"]
import_headers    = ["<hwloc.h>"]
import_macros     = {
    "TBB_PREVIEW_CONCURRENT_LRU_CACHE": "true",
    "__TBB_PREVIEW_PARALLEL_PHASE"    : "true"
}
export_module     = "tbb"
export_headers    = [
    "<tbb/tbb.h>"
    "<tbb/concurrent_lru_cache.h>"
]
for root, _, files in os.walk(f"{module_path}/{repo}/src"):
    for file in files:
        if file.endswith(".cpp"):
            export_headers.append(f'"{root}/{file}"')

export_namespaces = ["tbb"]

def on_preprocess(file, data):
    # static
    data = re.sub(r'^static\b', "", data, flags=re.MULTILINE)

    # struct
    data = re.sub(r'static struct',         "struct",        data)
    data = re.sub(r'struct _malloc_zone_t', "malloc_zone_t", data)

    # certain file
    if file.endswith("./include/oneapi/tbb/detail/_task_handle.h"):
        data = re.sub(r'^(?= \w)', "static" , data, flags=re.MULTILINE)

    if file.endswith("./src/tbb/governor.cpp"):
        data = re.sub(r'system_topology', "__system_topology__", data)

    if file.endswith("./src/tbb/parallel_pipeline.cpp"):
        data = re.sub(r'(?<!d1::)task_group_context', "d1::task_group_context", data)

    if file.endswith("./src/tbbmalloc/frontend.cpp"):
        data = re.sub(r'^(?=void mallocThreadShutdownNotification)', 'extern "C" ', data, flags=re.MULTILINE)

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
          on_failure        = lambda: print(f"{green}remove above 'static' and redefinitions{white}"))


