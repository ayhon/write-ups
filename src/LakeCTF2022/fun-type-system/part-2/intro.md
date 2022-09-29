# Part 2: The other rev

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
