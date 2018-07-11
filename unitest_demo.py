import unittest
from HTMLTestRunner import HTMLTestRunner


class ParamikoTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual("a", "a", "相等")

    def test_2(self):
        self.assertEqual("a", "b", "不等")


if __name__ == "__main__":
    test_suit = unittest.TestSuite()
    test_suit.addTests([ParamikoTest("test_1"), ParamikoTest("test_2")])
    with open("report.html", "wb") as f:
        runner = HTMLTestRunner(stream=f, title="test_report", description="html", verbosity=2)
        runner.run(test_suit)
