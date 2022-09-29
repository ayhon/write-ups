## Knocking down the easy ones first
Having lost our only lead, we proceed to look at the general type definitions in
the files, hoping to guess what some of them do, and work from there

The first eye-catching thing we see is the alphabet, defined in terms of weird
type of enconding
```scala
type CharNul = CheckedComparison
type CharA = IIIIIIIIII[CharNul, CheckeComparison]
type CharB = IIIIIIIIII[CharA, CheckeComparison]
type CharC = IIIIIIIIII[CharB, CheckeComparison]
type CharD = IIIIIIIIII[CharC, CheckeComparison]
type CharE = IIIIIIIIII[CharD, CheckeComparison]
type CharF = IIIIIIIIII[CharE, CheckeComparison]
type CharG = IIIIIIIIII[CharF, CheckeComparison]
type CharH = IIIIIIIIII[CharG, CheckeComparison]
type CharI = IIIIIIIIII[CharH, CheckeComparison]
type CharJ = IIIIIIIIII[CharI, CheckeComparison]
type CharK = IIIIIIIIII[CharJ, CheckeComparison]
type CharL = IIIIIIIIII[CharK, CheckeComparison]
type CharM = IIIIIIIIII[CharL, CheckeComparison]
type CharN = IIIIIIIIII[CharM, CheckeComparison]
type CharO = IIIIIIIIII[CharN, CheckeComparison]
type CharP = IIIIIIIIII[CharO, CheckeComparison]
type CharQ = IIIIIIIIII[CharP, CheckeComparison]
type CharR = IIIIIIIIII[CharQ, CheckeComparison]
type CharS = IIIIIIIIII[CharR, CheckeComparison]
type CharT = IIIIIIIIII[CharS, CheckeComparison]
type CharU = IIIIIIIIII[CharT, CheckeComparison]
type CharV = IIIIIIIIII[CharU, CheckeComparison]
type CharW = IIIIIIIIII[CharV, CheckeComparison]
type CharX = IIIIIIIIII[CharW, CheckeComparison]
type CharY = IIIIIIIIII[CharX, CheckeComparison]
type CharZ = IIIIIIIIII[CharY, CheckeComparison]
```
We see that every character is defined as a "function" of the previous character's
type and some `CheckeComparison`, except the `Nul` character, which is 
`CheckedComparison`. Please, don't let the off-by-a-letter difference make you 
think that these types are both the same. We'll find more of this wonderful 
naming later on. 

```scala
type CheckedComparison = Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Checksum
type CheckeComparison  = In =~: Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Sc =~: Checksum
```

From these definitions we can see that they're both defined in terms of 9 types,
put together in a sequence. Both types follow the same kind of structure, with 
one type off. We also see the `Checksum` type which marked the end of the flag 
in these definitions. From here we can deduce that `Checksum` is some kind of 
`EndOfSequence` signal. So we'll rename it as such.
```vim
%s/Checksum/EOS/g
```
