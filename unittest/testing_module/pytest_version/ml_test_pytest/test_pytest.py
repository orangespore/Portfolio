import pytest, sys, logging
from time import sleep

# unittest와 동일하게 테스트 시작 전과 후에 실행하는 모듈이 존재함
def setup_function(function):
    """ setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """
    logging.info(sys._getframe(0).f_code.co_name)

def teardown_function(function):
    """ teardown any state that was previously setup with a setup_function
    call.
    """
    logging.info(sys._getframe(0).f_code.co_name)

def test_function_01():
    """ Test Function"""
    logging.info(sys._getframe(0).f_code.co_name)
    assert (True)

def test_function_02():
    """ Test Function"""
    logging.info(sys._getframe(0).f_code.co_name)
    assert (True)



# unittest와 동일하게 class로 구현하여 진행 가능함함


# ------------------------------------------------------------------------------------------
# Class Test
# ------------------------------------------------------------------------------------------
class TestClassSample():
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        logging.info(sys._getframe(0).f_code.co_name)
        cls.name= 'test'
        cls.members = [1, 2, 3, 4]

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class."""
        logging.error(sys._getframe(0).f_code.co_name)
        pass


    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a class.
        setup_method is invoked for every test method of a class.
        """
        logging.info(sys._getframe(0).f_code.co_name)

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method call.
        """
        logging.info(sys._getframe(0).f_code.co_name)
    # 해당 함수만 실행해야할 때 사용하는 데코레이터
    # pytest.ini 파일에 해당 내용을 추가해야함
    # markers = mandatory: mark tests that should be executed
    # 실행시 pytest -m mandatory
    @pytest.mark.mandatory
    def test_0001(self):
        logging.info(sys._getframe(0).f_code.co_name)
        sleep(1)
        assert (True)

    @pytest.mark.skip(reason="Skip reasson")
    def test_0002(self):
        logging.info(sys._getframe(0).f_code.co_name)
        sleep(1)
        assert (True)

    def test_0003(self,fixture_testing_2):
        logging.info(sys._getframe(0).f_code.co_name)
        sleep(1)
        assert fixture_testing_2 == "test"

class MyPlugin:
    def pytest_sessionfinish(self):
        pass

if __name__ == "__main__":
    # args_str = '--html=report/report.html --self-contained-html '+ __file__
    # args_str = ' --capture=tee-sys '+ __file__
    args_str = '--html=report/report.html ' + __file__

    args = args_str.split(" ")

    pytest.main(args, plugins=[MyPlugin()])
    #pytest.main()