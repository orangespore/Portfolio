import pytest, sys, logging
import pandas as pd
from time import sleep

# unittest와 동일하게 테스트 시작 전과 후에 실행하는 모듈이 존재함
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
        cls.data = pd.read_csv('C:/Users/admin/PycharmProjects/analysis/clf_module/dataset/train.csv')

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class."""
        logging.error(sys._getframe(0).f_code.co_name)
        pass

    #@pytest.mark.parametrize("fill_gaps_for_age_column", [cls.data], indirect=True)
    def test_fill_gaps_for_age_column(self, fill_gaps_for_age_column):
        assert self.data['Age'].isna().sum() > 0
        fill_gaps_for_age_column(self.data)
        assert self.data['Age'].isna().sum() == 0

    def test_0001(self):
        logging.info(sys._getframe(0).f_code.co_name)
        sleep(1)
        assert (True)

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