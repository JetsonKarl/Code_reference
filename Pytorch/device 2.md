

```python
device_id = torch.cuda.current_device()
```


# torch.backends.cudnn.benchmark
 

torch.backends.cudnn.benchmark主要针对Pytorch的cudnn底层库进行设置，输入为布尔值True或者False
```python
torch.backends.cudnn.benchmark = True
```


设置为True，会使得cuDNN来衡量自己库里面的多个卷积算法的速度，然后选择其中最快的那个卷积算法。

# torch.backends.cudnn.deterministic

```python
torch.backends.cudnn.deterministic = True 
```
为什么使用相同的网络结构，跑出来的效果完全不同，用的学习率，迭代次数，batch size 都是一样？固定随机数种子是非常重要的。但是如果你使用的是PyTorch等框架，还要看一下框架的种子是否固定了。还有，如果你用了cuda，别忘了cuda的随机数种子。这里还需要用到torch.backends.cudnn.deterministic.

torch.backends.cudnn.deterministic是啥？顾名思义，将这个 flag 置为True的话，每次返回的卷积算法将是确定的，即默认算法。如果配合上设置 Torch 的随机种子为固定值的话，应该可以保证每次运行网络的时候相同输入的输出是固定的，代码大致这样:

```python
def init_seeds(seed=0):
    torch.manual_seed(seed) # sets the seed for generating random numbers.
    torch.cuda.manual_seed(seed) # Sets the seed for generating random numbers for the current GPU. It’s safe to call this function if CUDA is not available; in that case, it is silently ignored.
    torch.cuda.manual_seed_all(seed) # Sets the seed for generating random numbers on all GPUs. It’s safe to call this function if CUDA is not available; in that case, it is silently ignored.

    if seed == 0:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
```