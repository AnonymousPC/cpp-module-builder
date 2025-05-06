from basic.basic import *

repo              = "stdexec"
src_dirs          = ["./include"]
import_modules    = ["std", "tbb"]
import_headers    = []
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
    "<execpools/tbb/tbb_thread_pool.hpp>"
]
export_namespaces = ["stdexec", "exec", "execpools"]

if __name__ == "__main__":
    build(repo              = repo,
          src_dirs          = src_dirs,
          import_modules    = import_modules,
          import_headers    = import_headers,
          import_macros     = import_macros,
          export_module     = export_module,
          export_headers    = export_headers,
          export_namespaces = export_namespaces,
          on_failure        = lambda: print(f"{green}remove above 'static' from the function declaration{white}"))



    