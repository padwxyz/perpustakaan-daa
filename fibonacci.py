def fibonacci_search(arr, x):       # 1
    fib_m_minus_2 = 0       # 1
    fib_m_minus_1 = 1       # 1
    fib_current = fib_m_minus_1 + fib_m_minus_2     # 1

    while fib_current < len(arr):       # log n
        fib_m_minus_2 = fib_m_minus_1       # 1
        fib_m_minus_1 = fib_current       # 1
        fib_current = fib_m_minus_1 + fib_m_minus_2       # 1

    offset = -1           # 1

    while fib_current > 1:      # log n
        i = min(offset + fib_m_minus_2, len(arr) - 1)       # 2 (log n)

        if arr[i]['tahun'] < x['tahun']:    # log n
            fib_current = fib_m_minus_1     # 1
            fib_m_minus_1 = fib_m_minus_2       # 1
            fib_m_minus_2 = fib_current - fib_m_minus_1     # 1
            offset = i      # 1

        elif arr[i]['tahun'] > x['tahun']:       # log n
            fib_current = fib_m_minus_2     # 1
            fib_m_minus_1 = fib_m_minus_1 - fib_m_minus_2       # 1
            fib_m_minus_2 = fib_current - fib_m_minus_1     # 1

        else:
            return i        # 1

    if fib_m_minus_1 and arr[offset + 1]['tahun'] == x['tahun']:    # 1
        return offset + 1       # 1

    return -1       # 1
