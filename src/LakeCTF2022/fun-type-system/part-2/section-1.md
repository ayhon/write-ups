## The first check

The instructions returned by `FourthToTop` are the following
```scala
  case FourthToTop =>
    Push[I[42]] =~:
    Call[Pop] =~:
    Push[I[0]] =~:
    Push[I[42]] =~:
    Call[SecondToTop] =~:
    Push[I[8]] =~:
    SubInstr =~:
    JumpIfZero["stacktrace"] =~:
    Push[I[0]] =~:
    Exit =~:
    EOS
```
We can start simulating the state of the stack and see how each instruction 
modifies it
```scala
  case FourthToTop => // f l a g 0
    Push[I[42]] =~:      // 42 f l a g 0
    Call[Pop] =~:        // ?
```
We run into a call to `Pop`, which we don't know how it affects the stack, so 
before proceeding with `FourthToTop`, we take a look at `Pop`
```scala
  case Pop =>             // a b ...
    SecondToTop =~:       // b a ...
    DoubleHead =~:        // b b a ...
    JumpIfZero[CharL] =~: // b a ...
    SecondToTop =~:       // a b ...
    DoubleHead =~:        // a a b ...
    ThirdToTop =~:        // b a a ...
    SecondToTop =~:       // a b a ...
    Store =~:             // a ...     [*a = b]
    Push[I[1]] =~:        // 1 a ...
    AddInstr =~:          // (a+1) ...
    Jump[Pop] =~:         // (a+1) c ..
    EOS
```

`Pop` does three things:
 1. It keeps a counter in `a`
 2. If `b` isn't 0, it stores it in memory address a
 3. It increments `a` and calls `Pop` again

Since `b` was consumed, for this next call of `Pop`, `b` is taken to be the next 
element in the stack. From this we see that `Pop` performs a scan of the stack,
storing its elements in memory consecutively, starting at address `a`, until it
finds a `0` in the stack, after which it jumps to `CharL`.

```scala
  case CharL =>     // 0 a ... // Since b = 0
    SecondToTop =~: // a 0 ...
    Store =~:       // ...     [*a = 0]
    Return =~:
    EOS
```

In `CharL` we simply store the `0` in memory and return from `Pop`

Therefore, we've seen that `Pop` loads into memory the contents in the stack, 
starting at the position given by the head of the stack. It functions kind of 
like a `loadstr` function

Some pseudocode for it would be
```scala
def loadstr(a: Byte, stack: List[Byte]) =
    for (b <- stack) do
        Memory(a) = b
        if (b == 0)
            return
        a += 1
```
Now we can come back to `FourthToTop` and continue with our analysis
```scala
  case FourthToTop =>     // f l a g 0
    Push[I[42]] =~:       // 42 f l a g 0
    Call[Pop] =~:         //               [loadstr(42, f l a g 0)]
    Push[I[0]] =~:        // 0
    Push[I[42]] =~:       // 42
    Call[SecondToTop] =~: // ?
```

Now we perform a second call, this time to `SecondToTop` which we analyze like
with `Pop`
```scala
  case SecondToTop =>                    // a b ...
    DoubleHead =~:                       // a a b ...
    Load =~:                             // *a a b ...
    JumpIfZero["recurse-trampoline"] =~: // a b ...
    Push[I[1]] =~:                       // 1 a b ...
    AddInstr =~:                         // (a+1) b ...
    SecondToTop =~:                      // b (a+1) ...
    Push[I[1]] =~:                       // 1 b (a+1) ...
    AddInstr =~:                         // (b+1) (a+1) ...
    SecondToTop =~:                      // (a+1) (b+1) ...
    Jump[SecondToTop] =~:                // (a+1) (b+1) ...
    EOS
```
From what we can see, `SecondToTop` scans memory, starting from `a`, and checks
if it stores a 0. If it doesn't, it moves to the next byte in memory, and
increases the value in `b` by 1. If the value in memory is 0, it jumps to 
`"recurse-trampoline"
```scala
  case "recurse-trampoline" => // a b ...
    Pop =~:                    // b ...
    Return =~:
    EOS
```
This just gets rid of the memory address and returns the counting value we had
in the second position.

Since `SecondToTop` is called with `a=42` and `b=0`, what this ends up doing is
computing the length of the string we just loaded with `Pop` (`loadstr`). It 
works like `strlen` in C

In pseudocode
```scala
def strlen(a: Byte, b: Byte) =
    while(Memory(a) != 0)
        a += 1
        b += 1
    return b
```

With this, we have enough information to finish decoding `FourthToTop`
```scala
  case FourthToTop =>            // f l a g 0
    Push[I[42]] =~:              // 42 f l a g 0
    Call[Pop] =~:                //               [loadstr(42, f l a g 0)]
    Push[I[0]] =~:               // 0
    Push[I[42]] =~:              // 42 0 
    Call[SecondToTop] =~:        // len           [len = strlen(42,0)]
    Push[I[8]] =~:               // 8 len
    SubInstr =~:                 // (len-8)
    JumpIfZero["stacktrace"] =~: //
    Push[I[0]] =~:               // 0
    Exit =~:
    EOS
```
After getting the length of the flag, we check whether the length of the flag is
8. If it isn't, we end execution with a 0 in the stack. Since we've seen that we
need to exit with a 20, exiting with a 0 is a failure, so we now know the length
of the flag must be 8


