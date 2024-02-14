# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

class DemoCounter:
    def __init__(self, counter: int = 0):
        self.counter = counter

    def get_counter(self):
        return self.counter

    async def get_counter_async(self):
        return self.counter

    def increment(self) -> None:
        self.counter += 1

    async def increment_async(self) -> None:
        self.counter += 1

    def throw(self):
        raise ValueError("This is a sync test error")

    async def throw_async(self):
        raise ValueError("This is an async test error")