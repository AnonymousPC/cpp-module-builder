# C++ Module Builder

This project aims to build traditionally-installed C++ libraries into [C++20 modules](https://en.cppreference.com/w/cpp/language/modules). That is to say, once we use a C++ library, we import a pre-compiled module:
```cpp
export module my_project;
import std;
import boost;
import Eigen;
import stdexec;
import tbb;
import thrust.openmp;
```
instead of `#include` and `link`.

The advantage of using `import` over `#include` is significant. Suppose we have `n` header units and `m` compilation units, the time complexity of compilation appears to be `O(n * m)` for `#include`, while `O(n + m)` for `import`. Same significant is the disadvantage that`import` **strictly** requires the sub/depended module to be built **before** main module, which brings challenge to traditional parallel-compilation.

The prebuilt libraries are:
- [std](https://en.cppreference.com/w/cpp/standard_library#Importing_modules)
- [stdexec](https://github.com/NVIDIA/stdexec) (*A C++26 proposal*)
- [plf_hive](https://github.com/mattreecebentley/plf_hive) (*A C++26 proposal*)
- [boost](https://www.boost.org)
- [Eigen](https://eigen.tuxfamily.org)
- [tbb](https://github.com/uxlfoundation/oneTBB)
- [thrust](https://github.com/NVIDIA/cccl) (*with openmp/tbb backend*)
- [clblast](https://github.com/CNugteren/CLBlast)

The libraries planned to be built are:
- [xlnt](https://github.com/tfussell/xlnt)

Usage:
- For library `lib`, run `python build/lib.py` in your console and follow the green instructions on screen.
- e.g. run `python build/boost.py` to build module `boost`.

