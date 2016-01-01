# coding: utf-8
# python StringIO 模块
# StringIo 可以看作python 内存中的"文件"操作对象 ?: iostream ? :)
import string
import StringIO

s = StringIO.StringIO()  # 创建stringio对象
s.write('hello python')
lines = ['aaaa', 'bbbbb']
s.write(lines)

s.seek(0)
print s.read()
