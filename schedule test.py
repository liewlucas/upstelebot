import schedule
import time


def hello():
    print("hello")


schedule.every(10).seconds.do(hello)
