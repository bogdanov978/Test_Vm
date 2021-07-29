# encoding: utf-8
import time
import sys
import os
from psutil import virtual_memory
from random import randrange


class BaseTestCase:
    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

    def prep(self):
        print("stage skipped")

    def run(self):
        print("stage skipped")

    def clean_up(self):
        print("stage skipped")

    def execute(self):
        print("executing test case {id}: {name}".format(id=self.tc_id, name=self.name))
        try:
            print("starting prep")
            self.prep()
            print("prep completed")
        except:
            print("prep error:", sys.exc_info()[1])
            print("test case execution interrupted!\n")
            return

        try:
            print("starting run")
            self.run()
            print("run completed")
        except:
            print("run error:", sys.exc_info()[1])
            print("test case execution interrupted!\n")
            return

        try:
            print("starting clean_up")
            self.clean_up()
            print("clean_up completed")
        except:
            print("clean_up error:", sys.exc_info()[1])
            print("test case execution interrupted\n")
            return

        print("execution of test case {id} ({name}) has finished successfully\n".format(id=self.tc_id, name=self.name))


class TestCase1(BaseTestCase):
    def __init__(self):
        BaseTestCase.__init__(self, 1, "list of files")

    def prep(self):
        if int(time.time()) % 2 != 0:
            raise ValueError("seconds count is odd!")

    def run(self):
        home = os.path.expanduser("~")
        print("user home directory:", home)
        for file in os.listdir(home):
            if os.path.isfile(os.path.join(home, file)):
                print(file)


class TestCase2(BaseTestCase):
    __BYTES_IN_GiB = 1073741824  # 2**30
    __BYTES_IN_MiB = 1048576  # 2**20

    def __init__(self):
        BaseTestCase.__init__(self, 2, "random file")
        self.filename = "test.txt"

    def prep(self):
        memory = virtual_memory()  # всего оперативной памяти в байтах
        if memory.total < TestCase2.__BYTES_IN_GiB:
            raise MemoryError("total RAM < 1 GiB")

    def run(self):
        rand_content = [randrange(256) for j in range(TestCase2.__BYTES_IN_MiB)]
        with open(self.filename, 'wb') as the_file:
            the_file.write(bytes(rand_content))

    def clean_up(self):
        os.remove(self.filename)


if __name__ == "__main__":
    TestCase1().execute()
    TestCase2().execute()
