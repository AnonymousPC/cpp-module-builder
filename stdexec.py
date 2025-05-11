from basic import *

repo              = "stdexec"
src_dirs          = ["./include"]
import_modules    = ["std", "boost", "tbb"]
import_headers    = []
import_macros     = {
    "ASIOEXEC_USES_BOOST":     "true",
    "STDEXEC_ASIO_USES_BOOST": "true"
}
export_module     = "stdexec"
export_headers    = [
    "<stdexec/concepts.hpp>", 
    "<stdexec/coroutine.hpp>", 
    "<stdexec/execution.hpp>", 
    "<stdexec/functional.hpp>", 
    "<stdexec/stop_token.hpp>", 
    "<exec/static_thread_pool.hpp>", 
    "<exec/when_any.hpp>",
    "<asioexec/completion_token.hpp>",
    "<asioexec/use_sender.hpp>",
    "<execpools/asio/asio_thread_pool.hpp>",
    "<execpools/tbb/tbb_thread_pool.hpp>",
]
export_namespaces = ["stdexec", "exec", "asioexec", "nvexec", "tbbexec", "execpools"]

def on_preprocess(file, data):
    data = re.sub(r'^#cmakedefine.*$', "",                   data, flags=re.MULTILINE)
    data = re.sub(r'asio_config.hpp',  "asio_config.hpp.in", data)
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
          on_failure        = lambda: print(f"{green}remove above 'static' from the function declaration{white}"))



    