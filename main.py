"""
======================
Author:cc
Time:2023/8/27 0:14
Project: python0731
love:xz
=======================
"""
import unittest
from BeautifulReport import BeautifulReport
import os
DIR = os.path.dirname(os.path.abspath(__file__))

testLoader = unittest.TestLoader()


Environ = 'Online'  # 线上环境Online，测试环境Offline


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = 'report.html'
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告', report_dir='./')


if __name__ == '__main__':
    suite = testLoader.discover('./test_Case', 'test*.py')
    run(suite)



# runner = unittest.TextTestRunner()
# runner.run(suite)