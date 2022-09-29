XOR = 13
LEN = 8
SUMS = [40, 49, 65, 48, 29, 24, 32, 40]

def gen_sol(x0, x1):
    x = [0]*LEN
    x[0], x[1] = x0, x1
    for i in range(2, LEN):
        x[i] = (SUMS[i-2] - x[i-2] - x[i-1]) & 0xFF
    return x

def test(x):
    xors = 0
    for e in x:
        if e not in range(1,26+1):
            return False
        xors ^= e
    return xors == XOR

for x0 in range(1,27):
    for x1 in range(1,27):
        x = gen_sol(x0,x1)
        if test(x):
            print("type Flag =",
                  " =~: ".join("Char"+chr(e+ord('A')-1) for e in x),
                  " =~: Checksum")
