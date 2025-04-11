from detail import *
import re

repo              = "https://gitlab.com/libeigen/eigen.git"
src_dirs          = ["./Eigen"]
import_modules    = ["std"]
import_headers    = []
export_module     = "Eigen"
export_headers    = [
    "<Eigen>"
]
export_namespaces = ["Eigen"]

if __name__ == "__main__":
    print(f"{yellow}You might meat about 30-40 redundant 'static'. Remove them after 'git clone' and before 'compile'.{white}")
    input(f"{yellow}Press Enter to start.{white}")

    compile(repo              = repo,
            src_dirs          = src_dirs,
            import_modules    = import_modules,
            import_headers    = import_headers,
            export_module     = export_module,
            export_headers    = export_headers,
            export_namespaces = export_namespaces,
            on_preprocess     = lambda file: file = re.sub(r'\binline\b', "", file)
            on_failure        = lambda: print(f"{green}remove above 'static' from the function declaration (totally about 30-40 times){white}"))



    