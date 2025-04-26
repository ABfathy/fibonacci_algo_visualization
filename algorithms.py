# algorithms.py

def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

# Memoized Fibonacci (DP)
def fib_dp(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fib_dp(n-1, memo) + fib_dp(n-2, memo)
    return memo[n]
