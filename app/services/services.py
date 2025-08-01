def power(x: int, y: int) -> float:
    return x ** y

def fibonacci(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be > 0")
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
