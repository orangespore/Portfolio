import pytest, sys, logging
from time import sleep


# unittest와 동일하게 class로 구현하여 진행 가능함함


# ------------------------------------------------------------------------------------------
# Class Test
# ------------------------------------------------------------------------------------------
class TestClassSample:
    def test_0003(self, fixture_testing_2):
        fixture_testing_2
        sleep(1)
        assert False


if __name__ == "__main__":

    pytest.main()