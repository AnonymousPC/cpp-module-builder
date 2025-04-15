from detail import *
import os
import re

repo              = "oneTBB"
src_dirs          = ["./include", "./src"]
import_modules    = ["std"]
import_headers    = []
import_macros     = {}
export_module     = "tbb"
export_headers    = [
    "<tbb/tbb.h>"
]
for root, _, files in os.walk(f"{module_path}/{repo}/src"):
    for file in files:
        if file.endswith(".cpp"):
            export_headers.append(f'"{root}/{file}"')

export_namespaces = ["tbb"]

def on_preprocess(file, data):
    data = re.sub(r'^static\b', "", data, flags=re.MULTILINE)

    if file.endswith("./include/oneapi/tbb/detail/_task_handle.h"):
        data = re.sub(r'^(?= \w)', "static" , data, flags=re.MULTILINE)

    if file.endswith("./src/tbb/governor.cpp"):
        data = re.sub(r'system_topology', "__system_topology__", data)

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
          on_preprocess     = on_preprocess)


