from reg_module.config import config
from reg_module.logging.logging import  *
import pandas as pd

class LoadData():
    def load_dataset(self, file_name, VERSION):

        try:
            _data = pd.read_csv(config.DATAPATH + self.file_name)
        except OSError as e:
            print(repr(e))
            get_logger(self.VERSION).error("please modify name of file : "+repr(e))
            exit(1)
        return _data

    def testing_unittest(self):
        return 'okay'

    def hello(self):
        return "Hello!"
