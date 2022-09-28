
### Part two: The other rev

We've kind of ignored the L[ae]k[ae] functions up until now, but after the work
we've done in `Lake`, the previously gibberish sequences of traits have been 
decoded to almost readable sequences of instructions, the assembly of our `Lake` 
virtual machine.

First, let's put `Leka`, `Leke` and `Laka` one after the other, and
format them so each instruction appears in one line
```vim
'<,'>s/\(=>\|=\~:\)/\1\r/g
```
We fix any indentation complaints the compiler may give us, and continue with
our analysis.

Now, we start decoding these functions by their appearance in `VictoryCondition`

```scala
type VictoryCondition = Lake[
    Leka[FourthToTop],
    Concat[Flag, CharNul =~: EOS],
    Leka["main"] =~: EOS,
    NewTree[ZeroByte, 8],
    Leka
] =:= (I[20] =~: EOS)
```

Therefore, we start with `FourthToTop`

#### The first check

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

#### The second check
If the length of the flag is correct, we jump to `"stacktrace"`
```scala
  case "stacktrace" =>
    Push[I[0]] =~:
    Push[I[42]] =~:
    Call["strlen"] =~:
    Push[I[13]] =~:
    SubInstr =~:
    JumpIfZero["exception-landing-pad"] =~:
    Push[I[0]] =~:
    Exit =~:
    EOS
```

As we did before, we start with the analysis until we reach a call
```scala
  case "stacktrace" => //
    Push[I[0]] =~:     // 0
    Push[I[42]] =~:    // 42 0
    Call["strlen"] =~: // ?
```
And now we have a look at `"strleǹ"`, not to be confused with `Pop` which we 
previously saw worked like a `strlen` function. Totally different
```scala
  case "strlen" =>           // a b ...
    DoubleHead =~:           // a a b ...
    Load =~:                 // *a a b ...
    DoubleHead =~:           // *a *a a b ...
    JumpIfZero[SubInstr] =~: // *a a b ...
    ThirdToTop =~:           // b *a a ...
    XorInstr =~:             // (*a^b) a ...
    SecondToTop =~:          // a (*a^b)
    Push[I[1]] =~:           // 1 a (*a^b) 
    AddInstr =~:             // (a+1) (*a^b)
    Jump["strlen"] =~:       // (a+1) (*a^b)
    EOS
```

This function iterates over the values in memory, starting from `a`, and if
they are not 0, XORs them with `b` and continues to the next value in memory.
If the value is 0, it jumps to `SubInstr` 
```scala
  case SubInstr => // *a a b ...
    Pop =~:        // a b ...
    Pop =~:        // b ...
    Return =~:
    EOS
```
This one leaves only the accumulated XORs of the sequence in the stack and 
returns.

Therefore, we see that `"strlen"` xors all the elements in memory until it
encounters a 0, at which point it returns. It works like a `xorstr` function
```scala
def xorstr(a: Byte, b: Byte) =
    while(Memory(a) != 0)
        b = b ^ Memory(a)
        a += 1
    return b
```

Therefore, continuing the analysis of `SecondToTop`, we can finish the analysis
```scala
  case "stacktrace" =>                      //
    Push[I[0]] =~:                          // 0
    Push[I[42]] =~:                         // 42 0
    Call["strlen"] =~:                      // xor     [xor = xorstr(42,0)]
    Push[I[13]] =~:                         // 13 xor
    SubInstr =~:                            // (xor-13)
    JumpIfZero["exception-landing-pad"] =~: // 
    Push[I[0]] =~:                          // 0
    Exit =~:
    EOS
```
Afterwards we check if the xor of the flag is 13. If it isn't we fail as we did
before, which means gives us our second piece of information about the flag.

If the xor of the flag is indeed 13, we continue to `"exception-landing-pad"`

#### The third check

In `"exception-landing-pad"` we encounter the following code
```scala
  case "exception-landing-pad" =>
    Push[I[8]] =~:
    Push[I[42]] =~:
    Call[ThirdToTop] =~:
    Push[I[69]] =~:
    Push[I[42]] =~:
    Push[I[7]] =~:
    Call["main"] =~:
    Push[I[0]] =~:
    Push[I[40]] =~:
    Push[I[32]] =~:
    Push[I[24]] =~:
    Push[I[29]] =~:
    Push[I[48]] =~:
    Push[I[65]] =~:
    Push[I[49]] =~:
    Push[I[40]] =~:
    Push[I[111]] =~:
    Call[Pop] =~:
    Push[I[69]] =~:
    Push[I[111]] =~:
    Push[I[7]] =~:
    Call[Load] =~:
    Push[I[1]] =~:
    SubInstr =~:
    JumpIfZero[OffBit] =~:
    Push[I[0]] =~:
    Exit =~:
    EOS
```

This one is longer than the others, but it doesn't take long to find a call to
another function we have to stop to analyze
```scala
  case "exception-landing-pad" => // 
    Push[I[8]] =~:                // 8
    Push[I[42]] =~:               // 42 8
    Call[ThirdToTop] =~:          // ?
```
In the instructions for `ThirdToTop` we find the following
```scala
  case ThirdToTop => // a b ...
    DoubleHead =~:   // a a b ...
    ThirdToTop =~:   // b a a ...
    AddInstr =~:     // (a+b) a ...
    SecondToTop =~:  // a (a+b) ...
    Load =~:         // *a (a+b) ...
    SecondToTop =~:  // (a+b) *a ...
    Store =~:        // ...      [a[b] = *a]
    Return =~:
    EOS
```
Which basically just copies whatever value was in memory at `a` to the 
address `a+b` and returns nothing. Since in our case, it's being called
with 42 and 8 as `a` and `b`, it's replacing the 0 delimiter in memory
with the first letter of the flag
```scala
  case "exception-landing-pad" => // 
    Push[I[8]] =~:                // 8
    Push[I[42]] =~:               // 42 8
    Call[ThirdToTop] =~:          //        [*50 = *42]
    Push[I[69]] =~:               // 69
    Push[I[42]] =~:               // 42 69
    Push[I[7]] =~:                // 7 42 69
    Call["main"] =~:              // ?
```
Now we perform a call to `"main"`, which is another big function
```scala
  case "main" =>
    DoubleHead =~:
    JumpIfZero[CharE] =~:
    ThirdToTop =~:
    DoubleHead =~:
    FourthToTop =~:
    DoubleHead =~:
    ThirdToTop =~:
    SecondToTop =~:
    Call[CharF] =~:
    Push[I[1]] =~:
    AddInstr =~:
    SecondToTop =~:
    Push[I[1]] =~:
    AddInstr =~:
    ThirdToTop =~:
    Push[I[1]] =~:
    SubInstr =~:
    ThirdToTop =~:
    SecondToTop =~:
    Jump["main"] =~:
    EOS
```

We analyze `"main"` until we find a call to `CharF`

```scala
  case "main" =>          // a b c ...
    DoubleHead =~:        // a a b c ...
    JumpIfZero[CharE] =~: // a b c ...
    ThirdToTop =~:        // c a b ...
    DoubleHead =~:        // c c a b ...
    FourthToTop =~:       // b c c a ...
    DoubleHead =~:        // b b c c a ...
    ThirdToTop =~:        // c b b c a ...
    SecondToTop =~:       // b c b c a ...
    Call[CharF] =~:       // ?
```
In `CharF`, we proceed to analyze as we've done so far
```scala
  case CharF =>     // a b ...
    DoubleHead =~:  // a a b ...
    Push[I[1]] =~:  // 1 a a b ...
    AddInstr =~:    // (a+1) a b ...
    DoubleHead =~:  // (a+1) (a+1) a b ...
    Push[I[1]] =~:  // 1 (a+1) (a+1) a b ...
    AddInstr =~:    // (a+2) (a+1) a b ...
    Load =~:        // *(a+2) (a+1) a b ...
    SecondToTop =~: // (a+1) *(a+2) a b ...
    Load =~:        // *(a+1) *(a+2) a b ...
    ThirdToTop =~:  // a *(a+1) *(a+2) b ...
    Load =~:        // *a *(a+1) *(a+2) b ...
    AddInstr =~:    // (*a+*(a+1)) *(a+2) b ...
    AddInstr =~:    // (*a+*(a+1)+*(a+2)) b ...
    SecondToTop =~: // b *a+*(a+1)+*(a+2) ...
    Store =~:       // ...                     [*b = a[0] + a[1] + a[2]]
    Return =~:
    EOS
```
We see that the whole purpose of this operation is to compute the sum of
the three successive values in memory starting at `a`, and we store them
at position `b`.

```scala
  case "main" =>          // a b c ...
    DoubleHead =~:        // a a b c ...
    JumpIfZero[CharE] =~: // a b c ...
    ThirdToTop =~:        // c a b ...
    DoubleHead =~:        // c c a b ...
    FourthToTop =~:       // b c c a ...
    DoubleHead =~:        // b b c c a ...
    ThirdToTop =~:        // c b b c a ...
    SecondToTop =~:       // b c b c a ...
    Call[CharF] =~:       // b c a ...             [*c = b[0] + b[1] + b[2]]
    Push[I[1]] =~:        // 1 b c a ...
    AddInstr =~:          // (b+1) c a ...
    SecondToTop =~:       // c (b+1) a ...
    Push[I[1]] =~:        // 1 c (b+1) a ...
    AddInstr =~:          // (c+1) (b+1) a ...
    ThirdToTop =~:        // a (c+1) (b+1) ...
    Push[I[1]] =~:        // 1 a (c+1) (b+1) ...
    SubInstr =~:          // (a-1) (c+1) (b+1) ...
    ThirdToTop =~:        // (b+1) (a-1) (c+1) ... 
    SecondToTop =~:       // (a-1) (b+1) (c+1) ... 
    Jump["main"] =~:      // (a-1) (b+1) (c+1) ...
    EOS
```
We see that `"main"` stores the sums of the sub-sequence of 3 elements
starting at `b` in `c`, and moves on to the next element. The iteration stops when the
counter in `a` reaches 0, at which point we jump to `CharE`
```scala
  case CharE => // a b c ...
    Pop =~:     // b c ...
    Pop =~:     // c ...
    Pop =~:     // ...
    Return =~:
    EOS
```
Which just gets rid of the values of `a`, `b` and `c` and returns from `"main"`.

In short, `"main"` stores in `c` the sums of the first `a` sums of subsequences
of length 3 in `b`. In pseudocode, this would be
```scala
def sumOfThree(b: Byte, c: Byte) =
    Memory(c) = Memory(b) + Memory(b+1) + Memory(b+2)
def sumsOfThree(a: Byte, b: Byte, c: Byte) =
    while(a != 0)
        sumOfThree(b,c)
        b+=1
        c+=1
        a-=1
```
Here `CharF` corresponds to `sumOfThree(b,c)` and `"main"` to `sumsOfThree(a,b,c)`

```scala
  case "exception-landing-pad" => // 
    Push[I[8]] =~:       // 8
    Push[I[42]] =~:      // 42 8
    Call[ThirdToTop] =~: //                      [*50 = *42]
    Push[I[69]] =~:      // 69
    Push[I[42]] =~:      // 42 69
    Push[I[7]] =~:       // 7 42 69
    Call["main"] =~:     //                      [sumsOfThree(7,42,69)]
    Push[I[0]] =~:       // 0
    Push[I[40]] =~:      // 40 0
    Push[I[32]] =~:      // 32 40 0
    Push[I[24]] =~:      // 24 32 40 0
    Push[I[29]] =~:      // 29 24 32 40 0
    Push[I[48]] =~:      // 48 29 24 32 40 0
    Push[I[65]] =~:      // 65 48 29 24 32 40 0
    Push[I[49]] =~:      // 49 65 48 29 24 32 40 0
    Push[I[40]] =~:      // 40 49 65 48 29 24 32 40 0
    Push[I[111]] =~:     // 111 49 65 48 29 24 32 40 0
    Call[Pop] =~:        //                      [loadstr(111, 49 65 ... 40 0)]
    Push[I[69]] =~:      // 69
    Push[I[111]] =~:     // 111 69
    Push[I[7]] =~:       // 7 111 69
    Call[Load] =~:       // ?
```
We encounter a call to `Pop` again, which we've already seen loads the contents
of the stack into memory until a 0 is found, at which point it's stored and the
subroutine stops

After loading the sequence `49 65 48 29 24 32 40 0` at position `111`, it calls
`Load` with the `7`, `111` and `69` in the stack

```scala
  case Load =>            // a b c ...
    DoubleHead =~:        // a a b c ...
    JumpIfZero[EOS] =~:   // a b c ...
    ThirdToTop =~:        // c a b ... 
    DoubleHead =~:        // c c a b ...
    Load =~:              // *c c a b ...
    FourthToTop =~:       // b *c c a ...
    DoubleHead =~:        // b b *c c a ...
    Load =~:              // *b b *c c a ...
    ThirdToTop =~:        // *c *b b c a ...
    SubInstr =~:          // (*c-*b) b c a ...
    JumpIfZero[CharP] =~: // b c a ...
    Pop =~:               // c a ...
    Pop =~:               // a ...
    Pop =~:               // ...
    Push[I[0]] =~:        // 0
    Return =~:
    EOS
```

`Load` first checks if `a` is 0, and if it isn't, checks whether the bytes at
positions `b` and `c` have the same value in memory. If they aren't the same, 
the function returns a 0.

If `a` is 0, then we jump to `EOS`, where we return from `Load` with a 1 instead
```scala
  case EOS =>      // a b c ...
    Pop =~:        // b c ...
    Pop =~:        // c ...
    Pop =~:        // ...
    Push[I[1]] =~: // 1
    Return =~:
    EOS
```

If the bytes in `c` and `b` hold the same value in memory, then we jump to 
`CharP`
```scala
  case CharP =>     // b c a
    Push[I[1]] =~:  // 1 b c a
    AddInstr =~:    // (b+1) c a
    SecondToTop =~: // c (b+1) a
    Push[I[1]] =~:  // 1 c (b+1) a 
    AddInstr =~:    // (c+1) (b+1) a 
    ThirdToTop =~:  // a (c+1) (b+1)
    Push[I[1]] =~:  // 1 a (c+1) (b+1)
    SubInstr =~:    // (a-1) (c+1) (b+1)
    Jump[Load] =~:  // (a-1) (c+1) (b+1)
    EOS
```
In `CharP` we increment `b` and `c` by one and decrement the counting value `a`
by 1.

It's easy to see now that `Load` is performing a string comparison, although it
switches around the address variables over each iteration, but this has no 
effect in the comparison. A pseudocode version of `Load` would be a function 
`strncmp` like the following
```scala
def strncmp(a: Byte, b: Byte, c: Byte) =
    while(a != 0)
        if (Memory(a) != Memory(b))
            return 0
        b += 1
        c += 1
        swap(a,b) // This has no effect over the output
        a -= 1
    return 1
```

Thanks to this, we can finally completely analyze the behaviour of 
`"exception-landing-pad"`

```scala
  case "exception-landing-pad" => // 
    Push[I[8]] =~:         // 8
    Push[I[42]] =~:        // 42 8
    Call[ThirdToTop] =~:   //                     [*50 = *42]
    Push[I[69]] =~:        // 69
    Push[I[42]] =~:        // 42 69
    Push[I[7]] =~:         // 7 42 69
    Call["main"] =~:       //                     [sumsOfThree(7,42,69)]
    Push[I[0]] =~:         // 0
    Push[I[40]] =~:        // 40 0
    Push[I[32]] =~:        // 32 40 0
    Push[I[24]] =~:        // 24 32 40 0
    Push[I[29]] =~:        // 29 24 32 40 0
    Push[I[48]] =~:        // 48 29 24 32 40 0
    Push[I[65]] =~:        // 65 48 29 24 32 40 0
    Push[I[49]] =~:        // 49 65 48 29 24 32 40 0
    Push[I[40]] =~:        // 40 49 65 48 29 24 32 40 0
    Push[I[111]] =~:       // 111 49 65 48 29 24 32 40 0
    Call[Pop] =~:          //                     [loadstr(111, 49 65 ... 40 0)]
    Push[I[69]] =~:        // 69
    Push[I[111]] =~:       // 111 69
    Push[I[7]] =~:         // 7 111 69
    Call[Load] =~:         // res                 [res = strncmp(7,111,69)]
    Push[I[1]] =~:         // 1 res
    SubInstr =~:           // (res-1)
    JumpIfZero[OffBit] =~: //
    Push[I[0]] =~:         // 0
    Exit =~:
    EOS
```

And so, what `"exception-landing-pad"` does is check if the flag's sums of three
consecutive elements are `49 65 48 29 24 32 40`. If this is true, then we jump
to `OffBit`
```scala
  case OffBit =>    // 
    Push[I[20]] =~: // 20
    Exit =~:
    EOS
```
Which ends the evaluation, returning a 20 and successfully compiling the program.

