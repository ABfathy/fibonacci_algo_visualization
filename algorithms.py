def fib_recursive_count(n):
    count = 0

    def helper(k):
        nonlocal count
        count += 1
        if k <= 1:
            return k
        return helper(k - 1) + helper(k - 2)

    result = helper(n)
    return result, count


def fib_dp_count(n):
    count = 0
    memo = {}

    def helper(k):
        nonlocal count
        count += 1
        if k in memo:
            return memo[k]
        if k <= 1:
            memo[k] = k
        else:
            memo[k] = helper(k - 1) + helper(k - 2)
        return memo[k]

    result = helper(n)
    return result, count