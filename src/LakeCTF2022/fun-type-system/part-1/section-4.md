## Finding the integers

We can get our next clue from another definition right above the `CheckeComparison`
trait we found before, in the definition of the alphabet.
```scala
type Split[X] = X match
  case Sc => In
  case In => Sc
```
This one just seems to switch around `Sc` for `In` and `In` for `Sc`. Since it 
looks like a not function, let's call it `Not`.
```scala
:%s/Split/Not/g
```

Now, looking at places where `Not` is used, we find right bellow the `LeFeu` 
trait
```scala
type LeFeu[X, Y] = X match
  case EOS => EOS
  case Sc =~: x => Y match
    case b =~: y => b =~: LeFeu[x, y]
  case In =~: x => Y match
    case b =~: y => Not[b] =~: LeFeu[x, y]
```

If we observe the code, it looks to be processing two sequences by pairs of 
elements, where when the element of `X` is a `Sc`, it keeps the element of `Y`
the same, but if its a `In`, then it flips the element of `Y`. It continues 
processing all elements until it reaches the end of `X`, at which point it ends
the sequence.

Let's look at the outputs of `Levee` in a truth table

| `X`  | `Y`  | `LeFeu[X,Y]` |
|------|------|--------------|
| `Sc` | `Sc` | `Sc`         |
| `Sc` | `In` | `In`         |
| `In` | `Sc` | `In`         |
| `In` | `In` | `Sc`         |

From here it's easy to see that `LeFeu` is the xor operation. 
```vim
%s/LeFeu/Xor/g
```
Even more, we can deduce that `Sc` represents an off bit and `In` an on bit, 
since `Xor[In,Y] = Not[Y]`
```vim
%s/In/OnBit/g
%s/Sc/OffBit/g
```

With this, we can come back to `CheckedComparison` to see that it represents
a sequence of 8 off bites. This is a 0 byte in binary
```scala
type CheckedComparison = OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: EOS
```

We could have deduced it from `CharNul` being defined as `CheckedComparison`, but
it's good to know for sure.
```vim
%s/CheckedComparison/ZeroByte/g
```

After figuring out that `Sc` and `In` correspond to bits, we can start to decode
more traits. 

A couple of easy ones first, we find that `TheStart` and `BasicComparison` are
just sequences with a single on and off bit respectively. 
```scala
type TheStart = OnBit =~: EOS
type BasicComparison = OffBit =~: EOS
```
We rename them to `BitstringOne` and `BitstringZero` respectively, to illustrate
that they are sequences of bits.
```vim
%s/TheStart/BistringOne/g
%s/BasicComparison/BitstringZero/g
```

Also, we can go back to `CheckeComparison` to see that it corresponds to a byte 
with values 1, with a little endian encoding.
```scala
type CheckeComparison  = OnBit  =~: OffBit =~: OffBit =~: OffBit =~:
                         OffBit =~: OffBit =~: OffBit =~: OffBit =~: Checksum
type CheckedComparison = OffBit =~: OffBit =~: OffBit =~: OffBit =~:
                         OffBit =~: OffBit =~: OffBit =~: OffBit =~: Checksum
```
To figure out the little endianness, you could have deduced it from how the 
`Extend` trait works or just taken a leap of faith, and while the first option 
is more elegant, what's more likely to happen in a CTF is the second.

We rename it to `OneByte`.
```vim
%s/CheckeComparison/OneByte/g
```

Continuing with our traits that we can understand, we have `AuLac` which appears
to scan the sequence `X` for an `OnBit`, if it finds it outputs `F`, and if it
reaches the end without finding one outputs `T`.
```scala
type AuLac[X, T, F] = X match
  case OffBit =~: EOS => T
  case OffBit =~: t => AuLac[t, T, F]
  case OnBit =~: t => F
```
This is a pretty straightforward zero check, so let's rename `AuLac` to something
like `IfZero`
```vim
%s/AuLac/IfZero/g
```

Next is a big one. Although `SelectSection` has a lot of code, it's not actually
doing nothing much, just a couple of control statements.
```scala
type SelectSection[X, Y, C] = X match
  case OffBit => Y match
    case OffBit => C match
      case OffBit => (OffBit, OffBit)
      case OnBit => (OnBit, OffBit)
    case OnBit => C match
      case OffBit => (OnBit, OffBit)
      case OnBit => (OffBit, OnBit)
  case OnBit => Y match    
    case OffBit => C match
      case OffBit => (OnBit, OffBit)
      case OnBit => (OffBit, OnBit)
    case OnBit => C match
      case OffBit => (OffBit, OnBit)
      case OnBit => (OnBit, OnBit)
```
We can easily understand it better by building a truth table, like we did for `Xor`.
For simplicity, let's represent `OffBit` with 0 and `OnBit` with 1

| `X` | `Y` | `C` | `SelectSection[X,Y,C]` |
|-----|-----|-----|------------------------|
|  0  |  0  |  0  |          0, 0          |
|  0  |  0  |  1  |          1, 0          |
|  0  |  1  |  0  |          1, 0          |
|  0  |  1  |  1  |          0, 1          |
|  1  |  0  |  0  |          1, 0          |
|  1  |  0  |  1  |          0, 1          |
|  1  |  1  |  0  |          0, 1          |
|  1  |  1  |  1  |          1, 1          |

It may be hard to see at first, but this corresponds to a binary addition with a
carry, where the first bit out is the result of the operation, and the second 
one is the overflow bit. It can also be seen as an output of a 2 bit integer, 
which since it's little endian is read backwards. Therefore, `1 0 1 == 0 1` since 
1 + 0 + the carry bit 1 equals 2 = `0b10` = 0,1.

You can make this connection by staring at the truth table long enough, but you
can also look where `SelectSection` is being used to find some type parameter
names which give it away much easier, in the previously named `CheckChecksum`
trait, but since renamed to `CheckEOS` when we renamed `Checksum` to `EOS`.
```scala
type CheckEOS[X, Y, C] = (X, Y) match
  case (x =~: EOS, y =~: EOS) => SelectSection[x, y, C] match
    case (res, carry) => res =~: carry =~: EOS
  case (X, y =~: EOS) => CheckEOS[X, y =~: OffBit =~: EOS, C]
  case (x =~: EOS, Y) => CheckEOS[x =~: OffBit =~: EOS, Y, C]
  case (xh =~: xt, yh =~: yt) => SelectSection[xh, yh, C] match
    case (res, carry) => res =~: CheckEOS[xt, yt, carry]
```
We see that here `SelectSection` is being used to get the traits `res` and 
`carry`, whose names nicely match with our previous interpretation. More so, 
looking at `CheckEOS` closely we can see that it corresponds to a binary
addition with a carry `C`. If the bitstrings X and Y are not the same length,
the shorter one is extended until it matches the longer one, after which the
final result is calculated and appended to the end of the solution.

We therefore have that `SelectSection` is a `BitAddWithCarry` and `CheckEOS` is
a `BitstringAddWithCarry`
```vim
%s/SelectSection/BitAddWithCarry/g
%s/CheckEOS/BitstringAddWithCarry/g
```

Looking at traits which use `BitAddWithCarry` and `BitstringAddWithCarry`, 
we find the traits `K` and `Yea`

```scala
type K[X] = X match
  case 0 => BitstringZero
  case S[n] => BitstringAddWithCarry[I[n], BistringOne, OffBit]
```
Te trait `K` receives an integer as `X` and matches 0 with `BistringZero` and
n with 1 + `K[X-1]`, where `X-1` we obtain thanks to [`S`](https://docs.scala-lang.org/scala3/reference/metaprogramming/compiletime-ops.html) and the addition is done with 
`BistringAddWithCarry`. Therefore, `K` is just a constructor for the integers in
bitstring format. The name `K` seems proper, so we don't change it.

```scala
type Yea[X, Y, C] = (X, Y) match
  case (x =~: EOS, y =~: EOS) => BitAddWithCarry[x, y, C] match
    case (res, carry) => res =~: EOS
  case (xh =~: xt, yh =~: yt) => BitAddWithCarry[xh, yh, C] match
    case (res, carry) => res =~: Yea[xt, yt, carry]
```
`Yea` just takes two bitstrings of the same length and adds them together. The
difference with `BitstringAddWithCarry` is that it requires both `X` and `Y` be
the same length, and the result itself ignores the last carry to ensure that the
result also has the same length as the inputs.

This trait is only used to define `IIIIIIIIII` (With 10 `I`s!), which is the
same as `Yea`, but fixing the carry parameter `C` as `OffBit`. This is important
since the `IIIIIIIIII` with 10 `I`s is the trait used to define the alphabet
```scala
type CharA = IIIIIIIIII[CharNul, OneByte]
type CharB = IIIIIIIIII[CharA, OneByte]
type CharC = IIIIIIIIII[CharB, OneByte]
type CharD = IIIIIIIIII[CharC, OneByte]
type CharE = IIIIIIIIII[CharD, OneByte]
type CharF = IIIIIIIIII[CharE, OneByte]
type CharG = IIIIIIIIII[CharF, OneByte]
type CharH = IIIIIIIIII[CharG, OneByte]
type CharI = IIIIIIIIII[CharH, OneByte]
type CharJ = IIIIIIIIII[CharI, OneByte]
type CharK = IIIIIIIIII[CharJ, OneByte]
type CharL = IIIIIIIIII[CharK, OneByte]
type CharM = IIIIIIIIII[CharL, OneByte]
type CharN = IIIIIIIIII[CharM, OneByte]
type CharO = IIIIIIIIII[CharN, OneByte]
type CharP = IIIIIIIIII[CharO, OneByte]
type CharQ = IIIIIIIIII[CharP, OneByte]
type CharR = IIIIIIIIII[CharQ, OneByte]
type CharS = IIIIIIIIII[CharR, OneByte]
type CharT = IIIIIIIIII[CharS, OneByte]
type CharU = IIIIIIIIII[CharT, OneByte]
type CharV = IIIIIIIIII[CharU, OneByte]
type CharW = IIIIIIIIII[CharV, OneByte]
type CharX = IIIIIIIIII[CharW, OneByte]
type CharY = IIIIIIIIII[CharX, OneByte]
type CharZ = IIIIIIIIII[CharY, OneByte]
```
Now the encoding finally makes sense. Since `IIIIIIIIII` with 10 `I`s is just an
addition on bytes, the encoding is achieved by starting with `CharNul` being 0
and giving each successive letter a successive number, so A is 1, B is 2, and so
on until Z, which gets 26.

With these finds, we decide to rename `Yea` to `ByteAddWithCarry` and `IIIIIIIII`
with 10 `I`s to `ByteAdd`
```vim
%s/Yea/ByteAddWithCarry/g
%s/IIIIIIIIII/ByteAdd/g
```

Since we've started to substitute succesive `I`s with different names, we might
as well address the `I`-traits, traits whose names are made exclusively out of 
`I`s. From here we find the now `ByteAddI`, previously `IIIIIIIIIII` with 11 `I`s
```scala
type ByteAddI[X, Y] = ByteAdd[X, ByteAdd[Map[Y, Not], OneByte]]
```
What `ByteAddI` does is add `X` with the negated `Y`, and add one to the result.
We observe that a negated `Y` + 1 is the [C2](https://en.wikipedia.org/wiki/Two%27s_complement)
representation of -Y, so `ByteAddI` is just a byte substraction. We rename it to
`ByteSub`
```
%s/ByteAddI/ByteSub/g
```

There are other `I`-traits which weren't affected by our previous renames
```scala
type I[X] = IIIIIIIII[X, 8]
type IIIIIIIII[X, Size] = Extend[K[X], Size]
```
These are both traits we've already encountered. We observe that `IIIIIIIII` with
9 `I`s is just taking a number and a size, converting that number into bitstring
representation with `K` and extending it to the provided size. `I` is just fixing
the size to be 8, which forms a byte. We'll rename `IIIIIIIII` to be called
`IntToBitstring`, but we'll keep `I` as it is. Like with `K` being a constructor
of integer bitstrings, `I` is a constructor of integer bytes, so the name seems
convenient.
```vim
%s/IIIIIIIII/IntToBitstring/g
```

With this, we can finally understand what the `VictoryCondition` was
testing for.
`I[20] =~: EOS` is a sequence containing a single byte with a 20 in
binary.

With this we've uncovered all operations on integers implemented in the type
system. However, there are a couple of traits still not decoded. We'll focus
on those next

