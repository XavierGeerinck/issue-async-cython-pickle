import pickle
import ray

from my_module.demo_counter import DemoCounter

DEMO_CONFIG = {"config": "test"}


def test_pickle_coroutine():
    """
    """
    # Test Pickle
    a = DemoCounter(12)
    print(a.get_counter_async())
    a_serialized = ray._private.serialization.pickle_dumps(a.get_counter_async(), "ERROR PICKLING")
    a_deserialized = pickle.loads(a_serialized)


    # Test Cloudpickle
    a = DemoCounter(12)
    print(a.get_counter_async())
    a_serialized = ray.cloudpickle.dumps(a.get_counter_async())
    a_deserialized = ray.cloudpickle.loads(a_serialized)

    # assert a.counter == a_deserialized