from detail import *

repo              = "https://github.com/NVIDIA/stdexec.git"
src_dirs          = ["./include"]
import_modules    = ["std"]
import_headers    = ["<tbb/tbb.h>"]
export_module     = "stdexec"
export_headers    = [
    "<stdexec/concepts.hpp>", 
    "<stdexec/coroutine.hpp>", 
    "<stdexec/execution.hpp>", 
    "<stdexec/functional.hpp>", 
    "<stdexec/stop_token.hpp>", 
    "<exec/static_thread_pool.hpp>", 
    "<exec/when_any.hpp>",
    "<execpools/tbb/tbb_thread_pool.hpp>"
]
export_namespaces = ["stdexec", "exec", "execpools"]

if __name__ == "__main__":
    build(repo              = repo,
          src_dirs          = src_dirs,
          import_modules    = import_modules,
          import_headers    = import_headers,
          export_module     = export_module,
          export_headers    = export_headers,
          export_namespaces = export_namespaces,
          on_failure        = lambda: print(f"{green}remove above 'static' from the function declaration (totally about 2 times){white}"))



    