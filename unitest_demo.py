import unittest
from HTMLTestRunner import HTMLTestRunner
from paramiko_demo import *
from unittest import findTestCases, makeSuite, TestLoader
import time


class ParamikoTest(unittest.TestCase):
    # def __init__(self):
    #     self.ssh = SshClient()
    #     super().__init__()

    def setUp(self):
        self.ssh = SshClient()
        self.ssh.connect()

    def tearDown(self):
        self.ssh.close()

    def test_paramiko_exec_cmd(self):
        out = self.ssh.exec_cmd("touch chen/guang1")
        print(not(out))
        out1 = out.split("\n")
        print(repr(out), out1)
        self.assertSetEqual(set(["chen1", "chen2", "chen3"]), set(out1))

    def test_paramiko_send_cmd(self):
        self.ssh.get_result_from_chan()
        time.sleep(1)
        self.ssh.send_cmd("ls chen/\n")
        time.sleep(2)
        ret = self.ssh.get_result_from_chan()
        print(repr(ret))
        self.assertSetEqual(set(["chen1", "chen2", "chen3"]), set(ret))

    def test_1(self):
        self.assertEqual("a", "a", "相等")

    def test_2(self):
        self.assertEqual("a", "b", "不等")


if __name__ == "__main__":
    # test_suit = unittest.TestSuite()
    test_suit = TestLoader().loadTestsFromTestCase(ParamikoTest)
    # test_suit.addTests([ParamikoTest("test_1"), ParamikoTest("test_2")])
    suit = unittest.TestSuite([test_suit])
    with open("report.html", "wb") as f:
        runner = HTMLTestRunner(stream=f, title="test_report", description="html", verbosity=2)
        runner.run(suit)
