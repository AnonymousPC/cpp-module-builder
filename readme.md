# C++ Module Builder

This project aims to build traditionally-installed C++ libraries into [C++20 modules](https://en.cppreference.com/w/cpp/language/modules). That is to say, once we use a library such as C++ `boost`, we import a pre-compiled module:
```cpp
export import std;
export import boost;
import Eigen;
import stdexec;
import tbb;
import clblast;
import plf;
...
export module my_project;
```
instead of `#include` and `link`.

The advantage of using `import` over `#include` is significant. Suppose we have `n` header units and `m` compilation units, the time complexity of compilation appears to be `O(n * m)` for `#include`, while `O(n + m)` for `import`. Same significant is the disadvantage that`import` **strictly** requires the sub/depended module to be built **before** main module, which brings challenge to traditional parallel-compilation.

The prebuilt libraries are:
- [std](https://en.cppreference.com/w/cpp/standard_library#Importing_modules)
- [stdexec](https://github.com/NVIDIA/stdexec) (*A [C++26 proposal](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)*)
- [plf_hive](https://github.com/mattreecebentley/plf_hive) (*A [C++26 proposal](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p0447r15.html)*)
- [boost](https://www.boost.org)
- [Eigen](https://eigen.tuxfamily.org)
- [tbb](https://github.com/uxlfoundation/oneTBB)
- [clblast](https://github.com/CNugteren/CLBlast)

The libraries planned to be built are:
- [thrust](https://github.com/NVIDIA/thrust) (*with cuda runtime*)
- [xlnt](https://github.com/tfussell/xlnt)

With supported compilers:
- `g++` >= 15.0
- `clang++` >= 20.1

*Although `C++20 modules` intended to name modules in different levels e.g. `export module boost.asio` -> `export module boost; export import boost.asio`, this project currently **do not differs submodules** and pack them all into `module boost` because of the huge and complex dependency chain.*

# Usage

## std

Notice that both `g++` and `clang++` provides a pre-built standard module or a method to build standard module. This project only calles that method.

```sh
python std.py
```

The output will be put into `std.gcm` (if `g++`) or `std.pcm` (if `clang++`)

## boost

run
```sh
python boost.py
```
and then follow the intructions on screen. 

There are many `static` variables and global-functions (which refers to internal linkage, but we desire a module linkage such as `inline`). Most of them is substituded inside `boost.py`, while we still need to handle some corner-case manually.

The output will be put into `boost.(gcm|pcm)`

# Eigen

run
```sh
python Eigen.py
```
and everything goes ok.

# stdexec

`stdexec` is a recently-published project, together with modern and high-quality codes, so the `stdexec.py` does not needs to apply any change(s) on the source code and it will compiled into module successfully. run
```sh
python stdexec.py
```
and everything goes ok.

# tbb

Similiar to boost.

# clblast

Similiar to Eigen. 

# plf

Similiar to Eigen.

