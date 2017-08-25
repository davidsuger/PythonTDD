def fib(n):
    if n<0:
        raise ValueError
    if n<2:
        return 1
    return fib(n-1)+fib(n-2)


print(fib(0))
print(fib(1))
print(fib(2))
print(fib(3))
print(fib(4))
print(fib(5))
print(fib(6))
print(fib(30))

