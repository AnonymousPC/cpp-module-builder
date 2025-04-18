from detail import *

repo              = "plf"
src_dirs          = ["."]
import_modules    = ["std"]
import_headers    = []
import_macros     = {}
export_module     = "plf"
export_headers    = ["<plf_hive.h>"]
export_namespaces = [
    "std",
    "plf"
]

if __name__ == "__main__":
    build(repo              = repo,
          src_dirs          = src_dirs,
          import_modules    = import_modules,
          import_headers    = import_headers,
          import_macros     = import_macros,
          export_module     = export_module,
          export_headers    = export_headers,
          export_namespaces = export_namespaces)



    