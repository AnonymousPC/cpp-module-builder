from basic import *
import os
import re

repo              = "cccl"
src_dirs          = ["./thrust", "./libcudacxx/include"]
import_modules    = ["std", "cuda", "tbb"]
import_headers    = [
    "<cuda/__cccl_config>",
    "<cuda/std/detail/__config>",
    "<cuda/std/__cccl/compiler.h>",
    "<cuda/std/__cccl/preprocessor.h>",
    "<cuda/std/__cccl/assert.h>",
    "<cuda/std/__cccl/attributes.h>",
    "<cuda/std/__cccl/deprecated.h>",
    "<cuda/std/__cccl/diagnostic.h>",
    "<cuda/std/__cccl/dialect.h>",
    "<cuda/std/__cccl/execution_space.h>",
    "<cuda/std/__cccl/sequence_access.h>",
    "<cuda/std/__cccl/version.h>",
    "<cuda/std/__cccl/visibility.h>",
    "<cuda/std/__internal/namespaces.h>",
    "<nv/target>"
]
import_macros     = {
    "_CCCL_TEMPLATE(...)":  "template <__VA_ARGS__>",
    "_CCCL_REQUIRES(...)":  "requires __VA_ARGS__",
    "_CCCL_AND":            "&&",
    "THRUST_HOST_SYSTEM":   "THRUST_HOST_SYSTEM_CPP",
    "THRUST_DEVICE_SYSTEM": "THRUST_DEVICE_SYSTEM_TBB"
}
export_module     = "thrust"
export_headers    = []
for root, _, files in os.walk(f"module/cccl/thrust/thrust"):
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