from basic.basic import *
import os
import re

repo              = "cccl"
src_dirs          = ["./thrust", "./libcudacxx/include"]
import_modules    = ["std", "tbb"]
import_headers    = []
for file in os.listdir(f"{module_path}/{repo}/libcudacxx/include/cuda/std"):
    if os.path.isfile(file):
        import_headers.append(file)

import_macros     = {
    "THRUST_HOST_SYSTEM":   "THRUST_HOST_SYSTEM_CPP",
    "THRUST_DEVICE_SYSTEM": "THRUST_DEVICE_SYSTEM_TBB"
}
export_module     = "thrust.tbb"
export_headers    = []
for root, _, files in os.walk(f"{module_path}/{repo}/thrust/thrust"):
    for file in files:
        if not "openmp" in f"{root}/{file}" and \
           not "cuda"   in f"{root}/{file}" and \
           not "detail" in f"{root}/{file}":
            export_headers.append(f'"{root}/{file}"')

export_namespaces = ["thrust", "cuda"]

def on_preprocess(file, data):
    data = re.sub(r'^static\b',                     "", data, flags=re.MULTILINE)
    data = re.sub(r'\b_LIBCUDACXX_HIDE_FROM_ABI\b', "", data, flags=re.MULTILINE)
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