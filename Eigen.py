from basic import *
import re

repo              = "Eigen"
src_dirs          = ["./Eigen", "./unsupported/Eigen"]
import_modules    = ["std"]
import_headers    = []
import_macros     = {}
export_module     = "Eigen"
export_headers    = [
    "<Eigen>",
    "<FFT>",
    "<CXX11/Tensor>"
]
export_namespaces = ["Eigen"]

def on_preprocess(file, data):
    data = re.sub(r'^static\b',                                            "", data, flags=re.MULTILINE)
    data = re.sub(r'(?<=^inline )static\b',                                "", data, flags=re.MULTILINE)
    data = re.sub(r'(?<=^EIGEN_DEVICE_FUNC )static\b',                     "", data, flags=re.MULTILINE) 
    data = re.sub(r'(?<=^EIGEN_STRONG_INLINE )static\b',                   "", data, flags=re.MULTILINE)
    data = re.sub(r'(?<=^EIGEN_ALWAYS_INLINE )static\b',                   "", data, flags=re.MULTILINE)
    data = re.sub(r'(?<=^EIGEN_DEVICE_FUNC EIGEN_STRING_INLINE )static\b', "", data, flags=re.MULTILINE)
    data = re.sub(r'(?<=^EIGEN_DEVICE_FUNC EIGEN_ALWAYS_INLINE )static\b', "", data, flags=re.MULTILINE)
    data = re.sub(r'\b(inline|EIGEN_ALWAYS_INLINE|EIGEN_STRONG_INLINE|'
                  r'EIGEN_DEFINE_FUNCTION_ALLOWING_MULTIPLE_DEFINITIONS)\b'
                  r'(?=[a-zA-Z0-9_:<>&*\s,]+\([^\(\)]*\)[^\{\}]*;)',       "", data                    ) 
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
          on_failure        = lambda: log("remove above 'inline' from the function declaration", color="green"))


