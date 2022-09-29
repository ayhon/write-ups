## The second check
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


