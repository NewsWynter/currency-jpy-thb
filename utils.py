import math
def flattenNToRowCol(N:int) -> int:
    ...
    rows = math.ceil(math.sqrt(N))
    cols = math.ceil(N / rows)
    return rows, cols

for n in range(1, 30):
    # for j in range(1, 10):
    r, c = flattenNToRowCol(n)
    print(f"with N = {n} => r,c = [{r}, {c}] => mult = {r * c} => is ok {r * c >= n}")