

## **os.mkdir()**
必须要有上级目录

## **os.makedir()**

直接无脑创建

## **os.path.relpath()**
```python
#os.path.relpath(path[, start])
'''
功能：绝对路径转换为相对路径
从start后面第一个文件夹或者文件开始计算相对路径：path一般是绝对路径，而start是path的一部分。
'''

import os
#1.绝对路径转换为相对路径
os.getcwd() #'D:\\source code\\SR'
print(os.path.relpath('D:\\source code\\SR\\experiments\\S', 'experiments'))# S
```

## **os.chdir(path)**
| 参数 | 描述 |
| :-- | :--: |
| 概述 | os.chdir() 方法用于改变当前工作目录到指定的路径。 |
| 语法 | os.chdir(path) |
| 参数 | path：要切换到的新路径 |
| 返回值 | 如果允许访问返回 True , 否则返回False。 |

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
path = "/tmp"
retval = os.getcwd() # 查看当前工作目录
print "当前工作目录为 %s" % retval              # 输出：当前工作目录为 /www
os.chdir( path )    # 修改当前工作目录
retval = os.getcwd() # 查看修改后的工作目录
print "目录修改成功 %s" % retval                # 输出：目录修改成功 /tmp
```