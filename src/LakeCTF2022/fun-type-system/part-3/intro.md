### Part 3: The solution

From our second rev, we've seen the conditions our flag has to meet to get our
program to compile.

Our flag is a sequence `x` such that
 1. `len(x) == 8`
 2. `XOR(x) == 13`
 3. `x[i] + x[i+1] + x[i+2] == SUMS[i]` where
```scala
SUMS = [49, 65, 48, 29, 24, 32, 40]
```

Therefore, we have 
```
SUMS(0) = 49 = x(0) + x(1) + x(2)
SUMS(1) = 65 =        x(1) + x(2) + x(3)
SUMS(2) = 48 =               x(2) + x(3) + x(4)
SUMS(3) = 29 =                      x(3) + x(4) + x(5)
SUMS(4) = 24 =                             x(4) + x(5) + x(6)
SUMS(5) = 32 =                                    x(5) + x(6) + x(7)
SUMS(6) = 40 =                                           x(6) + x(7) + x(8)
```

Recall that we have `x(8) == x(0)`, so we don't really need to compute it

The interesting thing is that, given `x(0)` and `x(1)` we can compute all successive 
values, so in order to generate the flag, we can check for all possible values
of `x(0)` and `x(1)`, generate the corresponding values of `x(i)` for i between
2 and 8 with
```scala
x(i) = SUMS(i-2) - x(i-2) - x(i-1)
```

Afterwards, we must check that:
 1. All values are between 1 and 26
 2. The xor of all values from 1 to 7 is 13
 3. `x(8)` is the same as `x(0)`

And with those conditions met, we've found a possible flag

We write a script to search for the flag, and wait
```python
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
```

And there you go!
```scala
// KITTYCAT
type Flag = CharK =~: CharI =~: CharT =~: CharT =~: CharY =~: CharC =~: CharA =~: CharT  =~: Checksum
// LJRUZABU
type Flag = CharL =~: CharJ =~: CharR =~: CharU =~: CharZ =~: CharA =~: CharB =~: CharU  =~: Checksum
// MGTVWCCR
type Flag = CharM =~: CharG =~: CharT =~: CharV =~: CharW =~: CharC =~: CharC =~: CharR  =~: Checksum
// NHRWXADS
type Flag = CharN =~: CharH =~: CharR =~: CharW =~: CharX =~: CharA =~: CharD =~: CharS  =~: Checksum
```
