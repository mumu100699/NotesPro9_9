"""
======================
Author:cc
Time:2023/8/29 14:31
Project: interface828
love:xz
=======================
"""
import unittest


class CheckTools(unittest.TestCase):
    def check_output(self, expect, actual):  # 校验返回体的规则
        """
        :except: {'responseTime': int, 'contentVersion': int}
        :actual: response.json()
        校验点：
        1.必填项是否存在
        2.返回字段的类型是否一致
        3.没有多余的字段出现
        4.如果需要精确到值的校验，直接传递值即可

        :return: None
        """
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='字段长度不匹配')  # 1:校验字段长度是否一致
        for k, v in expect.items():
            if type(v) == dict:  # 遇到嵌套的字典，进行递归，调用函数本身
                self.check_output(expect[k], actual[k])
            elif type(v) == list:  # 遇到是有列表的，进行递归
                for item in range(len(expect[k])):  # 用列表的索引遍历
                    if type(expect[k][item]) == dict:  # 列表中嵌套字典（列表中的元素值是字典）
                        self.check_output(expect[k][item], actual[k][item])  # 校验列表的索引值，实际结果和期望结果是否一致
                    else:
                        if type(expect[k][item]) == type:  # 校验列表的值是否一致
                            self.assertEqual(expect[k][item], type(actual[k][item]), msg=f'{k} 字段类型不一致')  # 校验类型
                        else:
                            self.assertEqual(type(expect[k][item]), type(actual[k][item]), msg=f'{k} 字段类型不一致')  # 校验类型
                            self.assertEqual(expect[k][item], actual[k][item], msg=f'{k} 字段值不一致')  # 校验类型
            else:
                self.assertIn(k, actual.keys(), msg=f'{k} 字段不存在')  # 校验字段是否存在
                if type(v) == type:  # 校验返回的值是否一样
                    self.assertEqual(v, type(actual[k]), msg=f'{k} 字段类型不一致')  # 校验类型
                else:
                    self.assertEqual(type(v), type(actual[k]), msg=f'{k} 字段类型不一致')  # 校验类型，前置步骤校验类型
                    self.assertEqual(v, actual[k], msg=f'{k} 字段值不一致')  # 后置步骤再校验值


"""
1.什么是递归:调用函数本身的方法，当返回的值有嵌套关系，比如嵌套字典，嵌套列表
2.在自动化框架中哪里实现递归
3.你们的断言方法是怎么封装的

"""
