import pickle
import ray
import cloudpickle

from my_module.demo_counter import DemoCounter

DEMO_CONFIG = {"config": "test"}


def test_cloudpickleray_coroutine():
    """
    """
    # Test Pickle
    a = DemoCounter(12)
    
    # a.get_counter_async() is a <_cython_3_0_8.coroutine object at 0x7f5b595e1f40> 
    ray._private.serialization.pickle_dumps(a.get_counter_async(), "ERROR PICKLING")


def test_cloudpickle_coroutine():
    # Test Pickle
    a = DemoCounter(12)
    
    # a.get_counter_async() is a <_cython_3_0_8.coroutine object at 0x7f5b595e1f40> 
    cloudpickle.dumps(a.get_counter_async())
    

def test_pickle_coroutine():
    """
    """
    # Test Pickle
    a = DemoCounter(12)
    
    # a.get_counter_async() is a <_cython_3_0_8.coroutine object at 0x7f5b595e1f40> 
    pickle.dumps(a.get_counter_async())