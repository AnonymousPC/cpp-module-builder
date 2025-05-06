from basic.basic import *
import os

repo              = "clblast"
src_dirs          = ["./include", "./src"]
import_modules    = ["std"]
import_headers    = ["<OpenCL/opencl.h>"]
import_macros     = {"OPENCL_API": "true"}
export_module     = "clblast"
export_headers    = ["<clblast.h>"]
export_headers.append(f'"{module_path}/{repo}/src/utilities/utilities.cpp"')
for root, _, files in os.walk(f"{module_path}/{repo}/src"):
    for file in files:
        if     file.endswith(".cpp")                 and \
           not file.endswith("clblast_c.cpp")        and \
           not file.endswith("clblast_netlib_c.cpp") and \
           not file.endswith("clblast_cuda.cpp")     and \
           not "tuning" in f"{root}/{file}":
            export_headers.append(f'"{root}/{file}"')

export_namespaces = ["clblast"]

def on_preprocess(file, data):
    if file.endswith(".hpp") or \
       file.endswith(".cpp"):
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
          on_preprocess     = on_preprocess)



    