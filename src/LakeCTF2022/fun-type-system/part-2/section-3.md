## The third check

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
    Push[I[111]] =~:       // 111 40 49 65 48 29 24 32 40 0
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
consecutive elements are `40 49 65 48 29 24 32 40`. If this is true, then we jump
to `OffBit`
```scala
  case OffBit =>    // 
    Push[I[20]] =~: // 20
    Exit =~:
    EOS
```
Which ends the evaluation, returning a 20 and successfully compiling the program.

