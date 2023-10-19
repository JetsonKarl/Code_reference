
# **functools.partial**

functools.partial 这个高阶函数用于部分应用一个函数。 部分应用是指， 基于一个函数创建一个新的可调用对象， 把原函数的某些参数固定。 使用这个函数可以把接受一个或多个参数的函数改编成需要回调的API， 这样参数更少。 

Python中的闭包:

```python
def fun(m):
    def innerf(n):
        return m*n
    return innerf
func=fun(3)
print(func(4))#12
```
functools中的partial就是跟上面定义的函数相似。
不过并不相同，固定函数的部分参数
```python
def f(m,n):
    return m*n
re=partial(f,3)
print(re(4))#12
```
这个固定部分的参数个数可以是多个
```python
def f(m,n,p):
    return m*n*p
re=partial(f,3,4)
print(re(5))#60
```