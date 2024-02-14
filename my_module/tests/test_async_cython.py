import pickle
import ray
import cloudpickle
import dill

from my_module.demo_counter import DemoCounter

DEMO_CONFIG = {"config": "test"}

def test_is_coroutine():
    a = DemoCounter(12)

    # a.get_counter_async() is a <_cython_3_0_8.coroutine object at 0x7f5b595e1f40> 
    assert a.get_counter_async().__class__.__name__.rsplit('.', 1)[-1] in ('coroutine', '_GeneratorWrapper')


def test_cloudpickleray_coroutine():
    # Test Pickle
    a = DemoCounter(12)
    ray._private.serialization.pickle_dumps(a.get_counter_async(), "ERROR PICKLING")


def test_cloudpickle_coroutine():
    a = DemoCounter(12)
    cloudpickle.dumps(a.get_counter_async())
    

def test_pickle_coroutine():
    a = DemoCounter(12)
    pickle.dumps(a.get_counter_async())
    

def test_dill_coroutine():
    a = DemoCounter(12)
    dill.dumps(a.get_counter_async())