# README

This issue reproduces the issue as reported on:

- https://github.com/cloudpipe/cloudpickle/issues/531
- https://github.com/ray-project/ray/issues/39736

Where cloudpickle is not able to handle Cythonized Async methods (coroutines) throwing the error: `TypeError: cannot pickle '_cython_3_0_8.coroutine' object`.

## Running

```bash
./scripts/test-with-cython.sh  my_module/tests/test_async_cython.py
```

## Result

When running the above, we get:

```bash
__________________________________________________________________________________________________________________________ test_pickle_coroutine __________________________________________________________________________________________________________________________

obj = <_cython_3_0_8.coroutine object at 0x7f5b595e1f40>, error_msg = 'ERROR PICKLING'

    def pickle_dumps(obj: Any, error_msg: str):
        """Wrap cloudpickle.dumps to provide better error message
        when the object is not serializable.
        """
        try:
>           return pickle.dumps(obj)

../../../.pyenv/versions/3.9.18/lib/python3.9/site-packages/ray/_private/serialization.py:65:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
../../../.pyenv/versions/3.9.18/lib/python3.9/site-packages/ray/cloudpickle/cloudpickle_fast.py:88: in dumps
    cp.dump(obj)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <ray.cloudpickle.cloudpickle_fast.CloudPickler object at 0x7f5b5bde37c0>, obj = <_cython_3_0_8.coroutine object at 0x7f5b595e1f40>

    def dump(self, obj):
        try:
>           return Pickler.dump(self, obj)
E           TypeError: cannot pickle '_cython_3_0_8.coroutine' object

../../../.pyenv/versions/3.9.18/lib/python3.9/site-packages/ray/cloudpickle/cloudpickle_fast.py:733: TypeError

The above exception was the direct cause of the following exception:

    def test_pickle_coroutine():
        """
        """
        # Test Pickle
        a = DemoCounter(12)
        print(a.get_counter_async())
>       a_serialized = ray._private.serialization.pickle_dumps(a.get_counter_async(), "ERROR PICKLING")

tests/test_async_cython.py:15:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

obj = <_cython_3_0_8.coroutine object at 0x7f5b595e1f40>, error_msg = 'ERROR PICKLING'

    def pickle_dumps(obj: Any, error_msg: str):
        """Wrap cloudpickle.dumps to provide better error message
        when the object is not serializable.
        """
        try:
            return pickle.dumps(obj)
        except TypeError as e:
            sio = io.StringIO()
            inspect_serializability(obj, print_file=sio)
            msg = f"{error_msg}:\n{sio.getvalue()}"
>           raise TypeError(msg) from e
E           TypeError: ERROR PICKLING:
E           ==============================================================================
E           Checking Serializability of <_cython_3_0_8.coroutine object at 0x7f5b595e1f40>
E           ==============================================================================
E           !!! FAIL serialization: cannot pickle '_cython_3_0_8.coroutine' object
E               Serializing 'cr_await' None...
E               Serializing 'cr_code' <code object get_counter_async at 0x7f5b595b39d0, file "my_module/demo_counter.py", line 12>...
E               Serializing 'cr_frame' <frame at 0x7f5b595a19a0, file 'my_module/demo_counter.py', line 12, code get_counter_async>...
E               !!! FAIL serialization: cannot pickle 'frame' object
E                   Serializing 'f_back' <frame at 0x55a767cf4dd0, file '/home/xanrin/.pyenv/versions/3.9.18/lib/python3.9/inspect.py', line 368, code getmembers>...
E                   !!! FAIL serialization: cannot pickle 'frame' object
E                       Serializing 'f_back' <frame at 0x55a767d5bc00, file '/home/xanrin/.pyenv/versions/3.9.18/lib/python3.9/site-packages/ray/util/check_serialize.py', line 127, code _inspect_generic_serialization>...
E                       !!! FAIL serialization: cannot pickle 'frame' object
E           ==============================================================================
E           Variable:
E
E               FailTuple(f_back [obj=<frame at 0x55a767d5bc00, file '/home/xanrin/.pyenv/versions/3.9.18/lib/python3.9/site-packages/ray/util/check_serialize.py', line 143, code _inspect_generic_serialization>, parent=<frame at 0x55a767cf4dd0, file '/home/xanrin/.pyenv/versions/3.9.18/lib/python3.9/inspect.py', line 368, code getmembers>])
E
E           was found to be non-serializable. There may be multiple other undetected variables that were non-serializable.
E           Consider either removing the instantiation/imports of these variables or moving the instantiation into the scope of the function/class.
E           ==============================================================================
E           Check https://docs.ray.io/en/master/ray-core/objects/serialization.html#troubleshooting for more information.
E           If you have any suggestions on how to improve this error message, please reach out to the Ray developers on github.com/ray-project/ray/issues/
E           ==============================================================================

../../../.pyenv/versions/3.9.18/lib/python3.9/site-packages/ray/_private/serialization.py:70: TypeError
```
