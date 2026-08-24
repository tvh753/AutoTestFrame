import time

import pytest




class Test:

    def setup_method(self):
        print(f'用例开始执行：{time.time()}')



    def test_a(self):
        assert 1 == 1

    def test_b(self):
        assert 1 == 2

