# README

This issue reproduces an issue in Ray Actors that does not support Cythonized Async methods. It will throw `TypeError: cannot pickle '_cython_3_0_2.coroutine' object` when trying to use Actors that return an async method.

## Running

```bash
./scripts/test-with-cython.sh  my_module/tests/test_async_cython.py
```
