# importing sys
import sys

# adding Folder_2 to the system path
# 동일 경로의 서로 다른 디렉토리안의 파일을 임포트하고 싶을 때,
# 해당 동일 경로의 바로 상위 경로를 path에 등록해준다.
sys.path.insert(0, r'/')

import unittest
from unittest.mock import patch
from unittest_version.ml_unit.unit_v1 import  ClsHello

# Note: It is expected that the following environment variables will be
# set so that the house price model will be able to locate its training
# data:
#
# SALES_DATA_PATH:  The path of the sales data training file, e.g.: "~/directory"
# SALES_DATA_FILE:  The name of the sales data training file, e.g.: "File.csv"

# mock은 a라는 함수를 실행시키기 위해 b라는 함수를 실행해야 하는데, 이 b라는 함수가
# 시간/리소스 측면에서 너무 소모가 클 경우, return value로 출력값만 받아오는 식으로 사용할 때 적용
# 예시) 전처리가 이미 다 된 데이터로 진행/ 학습된 모델로 진행/ 예측없이 예측해서 나온 값을 임의로 지정


@patch('ml_unit.unit_v1.ClsHello.hello')
class mytest(unittest.TestCase):
    def test(self, mok_hello):
        mok_hello.return_value='no okay'
        f=ClsHello()
        self.assertEqual(f.hello(), 'hello')



if __name__ == "__main__":

    unittest.main()