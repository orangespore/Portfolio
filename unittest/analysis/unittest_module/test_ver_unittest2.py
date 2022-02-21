"""
Contains unit tests for the 2nd house price model.
"""
import sys
sys.path.insert(0, r'C:/Users/admin/PycharmProjects/analysis')

import unittest
from reg_module.load_data.load_data import LoadData
from unittest.mock import patch

# Note: It is expected that the following environment variables will be
# set so that the house price model will be able to locate its training
# data:
#
# SALES_DATA_PATH:  The path of the sales data training file, e.g.: "~/directory"
# SALES_DATA_FILE:  The name of the sales data training file, e.g.: "File.csv"

# mock은 a라는 함수를 실행시키기 위해 b라는 함수를 실행해야 하는데, 이 b라는 함수가
# 시간/리소스 측면에서 너무 소모가 클 경우, return value로 출력값만 받아오는 식으로 사용할 때 적용
# 예시) 전처리가 이미 다 된 데이터로 진행/ 학습된 모델로 진행/ 예측없이 예측해서 나온 값을 임의로 지정
# patch를 이용해 다른 디렉토리의 모듈을 가져올 경우, 그 모듈은 클래스여야함.


class mytest(unittest.TestCase):
    @patch('reg_module.load_data.load_data.LoadData.testing_unittest')
    def test(self, mock_testing_unittest):
        mock_testing_unittest.return_value='no okay'
        f=LoadData()
        self.assertEqual(f.testing_unittest(), 'no okay')



if __name__ == "__main__":
    unittest.main()
