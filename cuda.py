from basic import *
import os
import re

repo              = "cccl"
src_dirs          = ["./libcudacxx/include"]
import_modules    = []
import_headers    = ["<nv/target>"]
import_macros     = {}
export_module     = "cuda"
export_headers    = []
for file in os.listdir(f"./src/cccl/libcudacxx/include/cuda/std"):
    if os.path.isfile (f"./src/cccl/libcudacxx/include/cuda/std/{file}"):
        export_headers.append(f"<cuda/std/{file}>")
for file in os.listdir(f"./src/cccl/libcudacxx/include/cuda"):
    if os.path.isfile (f"./src/cccl/libcudacxx/include/cuda/{file}"):
        if not "access_property" in file and \
           not "annotated_ptr"   in file and \
           not "mdspan"          in file and \
           not "stream_ref"      in file:
            export_headers.append(f"<cuda/{file}>")

export_namespaces = ["cuda"]

def on_preprocess(file, data):
    data = re.sub(r'^static\b',                     "", data, flags=re.MULTILINE)
    data = re.sub(r'\b_LIBCUDACXX_HIDE_FROM_ABI\b', "", data, flags=re.MULTILINE)
    data = re.sub(r'^_CCCL_HOST_DEVICE static\b',   "", data, flags=re.MULTILINE)
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