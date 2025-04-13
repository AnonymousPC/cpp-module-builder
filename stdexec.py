from detail import *

repo_cmd          = "git clone https://github.com/NVIDIA/stdexec.git --depth=1"
src_dirs          = ["./include"]
import_modules    = ["std"]
import_headers    = ["<tbb/tbb.h>"]
import_macros     = {}
export_module     = "stdexec"
export_headers    = [
    "<stdexec/concepts.hpp>", 
    "<stdexec/coroutine.hpp>", 
    "<stdexec/execution.hpp>", 
    "<stdexec/functional.hpp>", 
    "<stdexec/stop_token.hpp>", 
    "<exec/static_thread_pool.hpp>", 
    "<exec/when_any.hpp>",
]
export_namespaces = ["stdexec", "exec"]

if __name__ == "__main__":
    build(repo_cmd          = repo_cmd,
          src_dirs          = src_dirs,
          import_modules    = import_modules,
          import_headers    = import_headers,
          import_macros     = import_macros,
          export_module     = export_module,
          export_headers    = export_headers,
          export_namespaces = export_namespaces,
          on_failure        = lambda: print(f"{green}remove above 'static' from the function declaration{white}"))



    