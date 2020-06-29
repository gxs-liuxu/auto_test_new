import time

class parameter_change():

    def __init__(self):
        pass

    @staticmethod
    def get_millisecond_timestamp():
        '''获取毫秒级时间戳'''
        return str(round(time.time() * 1000))