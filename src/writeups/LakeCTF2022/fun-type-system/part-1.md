### Part one: The rev

#### First steps

The first thing you see when you open the file are some instructions about
how to solve the challenge. 
```scala
// THIS IS THE ONLY LINE YOU HAVE TO CHANGE!
// if the flag were FLAG, enter it like this:
// type Flag = CharF =~: CharL =~: CharA =~: CharG =~: Checksum // keep the Checksum at the end
type Flag = CharQ =~: CharI =~: CharY =~: CharZ =~: CharY =~: CharH =~: CharG =~: CharNul =~: Checksum
```

This gives us a couple of clues. The input we control in the program is the definition of
the `Flag` type. We still don't understand what `=~:` means, but from it's usage
we can deduce that it's some kind of operator to create a sequence, and that this
sequence must end in `Checksum`, at least for the flag. This deduction is proven
to be right, as if we search for `sealed trait =~:` we'll find the line where 
it's begin defined
```scala
sealed trait =~:[Compare, To]
```
<details><!--{{{ -->
<summary>A note on traits</summary>
In Scala, there exists the concepts of classes and interfaces, mainly form an 
interest to keep it compatible with Java code, which Scala was designed to 
[interoperate](https://en.wikipedia.org/wiki/Language_interoperability) with.
However, in pure Scala code, you won't find any mention of classes or interfaces,
but only traits. Think of a trait as a more powerful type of interface, with the
ability to be instantiated as an object. Thought this write up, I'll use type and
traits almost interchangeably, the same way that I'll refer to [kinds](https://kubuszok.com/compiled/kinds-of-types-in-scala/#kinds-and-higher-kinded-types) as if they were 
functions. In practice, it's easier to reason about them this way for the 
challenge, and they aren't that far off the truth.

The keyword `sealed` just tells the Scala compiler that all objects implementing
that trait are defined in the same file the trait definition is in. It's a
mechanism for controlling the creation of new objects which implement a trait.

Finally, for those who haven't had any experience with Scala, it may look weird
that we define a type with the symbols `=~:`. In Scala you don't have the usual
restrictions for a keyword you'll find in other languages. 

Also, if your type takes 2 generics as "type arguments", you can use the infix
syntax to apply them. These are called [infix operators](https://www.scala-Lang.org/files/archive/spec/2.11/03-types.html#infix-types), which means that the following two are
equivalent
```scala
=~:[Flag,Flag]
Flag =~: Flag
```
</details>
<!--}}}-->

Having a lead to hold on to, we look for where `Flag` is being used in the file,
which leads us to `LPlusRatio`
```scala
type LPlusRatio = Lake[Leka[Miaouss], Lust[Flag, CharNul =~: Checksum], Leka["main"] =~: Checksum, TrimMetadata[CheckedComparison, 8], Leka] =:= (I[20] =~: Checksum)
```
We see another symbol we don't recognize `=:=`, but it isn't hard to see from 
it's shape and definition that it consists of another infix type which does an 
equality check
```scala
type =:=[X, Y] = X match
  case Y => Unit
```
Therefore, we must construct a type `Flag` such that the output of `Lake` is
`I[20] =~: Checksum`, whatever that may be.
<!-- TODO: Add reference to  -->

We'll rename `LPlusRatio` to `VictoryCondition`
```vim
%s/LPlusRatio/VictoryCondition/g
```


#### Knocking down the easy ones first
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

#### Functions on lists

From this finding, we can deduce the function of many other types which don't
use more than `EOS` and generic type parameters.
```scala
type Sloth[L, F[_]] = L match
  case EOS => EOS
  case h =~: t => F[h] =~: Sloth[t, F]
```
This one appears to take a sequence `L` and apply a type `F[_]` over it as if
it were a function, returning a new sequence with the results from `F` as their
elements. This looks like a map operation on cons-lists, so let's rename it as
such
```vim
%s/Sloth/Map/g
```
We can find the fold left operation right after `Map`, under the name of `Wrath`
```scala
type Wrath[L, Z, F[_, _]] = L match
  case EOS => Z
  case h =~: t => F[h, Wrath[t, Z, F]]
```
As we see, this one just takes a type `F[_,_]` with two type parameters, and
continuously applies this "function" with each element of the sequence and the
result of the operation on the rest of the sequence. We rename it to `Fold`
```vim
%s/Wrath/Fold/g
```
Continuing with our scan we find `Lust`, which uses `Fold` to concatenate two lists
```scala
type Lust[L, R] = Fold[L, R, [h, t] =>> h =~: t]
```
The equivalent Scala code wouldn't be much different
```scala
def lust(l: List, r: List) = fold(l, r, (x,r) => x :: r)
```
Don't be afraid by the `=>>`, that's just a handy new Scala 3 feature called 
[type lambdas](https://docs.scala-lang.org/scala3/reference/new-types/type-lambdas.html)

We rename `Lust` to `Concat`
```vim
%s/Lust/Concat/g
```

Further down, we encounter `YaPas`. We have enough information to see what it's
doing.
```scala
import scala.compiletime.ops.int.S
type YaPas[X, I] = I match
  case 0 => EOS
  case S[n] => X match
    case EOS      => Sc =~: YaPas[X, n]
    case h =~: EOS => h =~: YaPas[X, n]
    case h =~: t   => h =~: YaPas[t, n]
```
the `scala.compiletime.ops.int.S` seems daunting at first, but it's easy enough
to look at [the Scala 3 documentation](https://docs.scala-lang.org/scala3/reference/metaprogramming/compiletime-ops.html) to figure out what it does.

From above
> Note that S is the type of the successor of some singleton type. For example the type S[1] is the singleton type 2.

The example here gives us the key. Looking at uses of `YaPas` in the code, it's
always called with an integer as its second argument. To be precise, `YaPas` is
only used to define `IIIIIIIII` (With 9 `I`s!), which in turn is only used to 
define `I`, which makes it so the only value `YaPas` ever receives in the second
argument is 8.
```scala
type I[X] = IIIIIIIII[X, 8]
type IIIIIIIII[X, Size] = YaPas[K[X], Size]
```
From the example we know that `8 = S[7]`, and so the match statement in this
case only serves to do a subtraction by one.
```scala
import scala.compiletime.ops.int.S
type YaPas[X, I] = I match
  case 0 => EOS
  case S[n] => X match
    case EOS      => Sc =~: YaPas[X, n]
    case h =~: EOS => h =~: YaPas[X, n]
    case h =~: t   => h =~: YaPas[t, n]
```
Knowing this we can see that what `YaPas` does is either truncate a sequence to
8 elements, if it's longer than that, or copy the last element over and over
until there are 8 elements in the Sequence. Therefore, `YaPas` will extend the
sequence to fill 8 elements. We'll rename `YaPas` to `Extend`
```vim
%s/YaPas/Extend/g
```

#### Finding the integers

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

Let's look at the outputs of `LeFeu` in a truth table
| `X`  | `Y`  | `LeFeu[X,Y]` |
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
which since it's little endian is read backwards. Therefore, `1 0 1 = 0 1" Since 
1 + 0 + the carry bit 1 = 2 = 0b10 = 0,1.

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

#### Wait, there's a tree?
Starting from the top, the first undecoded trait which looks simple enough is
`AnUnexpctedGift`. Notice how the sentence is misspelled in the name.
```scala
type AnUnexpctedGift[T, N, X] = N match
  case EOS => T match
    case Remove[x] => Remove[X]
  case OffBit =~: bs => T match
    case Swap[l, r] => Swap[AnUnexpctedGift[l, bs, X], r]
  case OnBit =~: bs => T match
    case Swap[l, r] => Swap[l, AnUnexpctedGift[r, bs, X]]
```
Some new traits are used in the definition. Thankfully, their definitions looks 
to be simple enough
```scala
sealed trait Swap[L, R]
sealed trait Remove[X]   
```
`Swap` is but a simple pair of types, and `Remove` just a wrapper agains another
type, like a node. We rename `Swap` to `Pair` and `Remove` to `Node` accordingly.
```vim
%s/Swap/Pair/g
%s/Remove/Node/g
```
This makes the code in `AnUnexpctedGift` (misspelled) more readable
```scala
type AnUnexpctedGift[T, N, X] = N match
  case EOS => T match
    case Node[x] => Node[X]
  case OffBit =~: bs => T match
    case Pair[l, r] => Pair[AnUnexpctedGift[l, bs, X], r]
  case OnBit =~: bs => T match
    case Pair[l, r] => Pair[l, AnUnexpctedGift[r, bs, X]]
```
From here we can recognize a tree structure, where `Pair`s are the disjunctions
and `Node` are the leafs. In this case, `AnUnexpctedGift` (misspelled) just 
traverses the tree using `N` as a path, where an `OffBit` means taking a turn
left and `OnBit` a turn right, and once a `Node` leaf is found, replaces its
inside value with `X`. Therefore, `AnUnexpctedGift` (misspelled) finds a node in
the tree and replaces its element. From this deduction we decide to rename
`AnUnexpctedGift` to `ReplaceNodeElement`
```vim
%s/AnUnexpctedGift/ReplaceNodeElement/g
```
The reason I stressed that the trait we were talking about was the misspelled 
`AnUnexpctedGift` was because there is a correctly spelled version of the trait.
```scala
type AnUnexpectedGift[T, N] = N match
  case EOS => T match
    case Node[x] => x
  case OffBit =~: bs => T match
    case Pair[l, r] => AnUnexpectedGift[l, bs]
  case OnBit =~: bs => T match
    case Pair[l, r] => AnUnexpectedGift[r, bs]
```
This one is another operation over a tree `T`, which takes a path `N` encoded in
the same way as before, but now simply returns the element at the `Node` leaf,
instead of modifying the tree. We'll therefore rename this trait to `GetNodeElement`
```vim
%s/AnUnexpectedGift/GetNodeElement/g
```
There's one last trait using the `Node` and `Pair` traits in its body, `TrimMetadata`.
```scala
type TrimMetadata[X, N] = N match
  case 0 => Node[X]
  case S[n] => Pair[TrimMetadata[X, n], TrimMetadata[X, n]]
```
From a glance, we can see that `TrimMetadata` constructs a tree of height `N`,
with each node having the type `X` as its default element. Therefore, we rename
`TrimMetadata` to `NewTree`, to enphasize how it's a constructor
```scala
%s/TrimMetadata/NewTree/g
```

What an assortment of data structures we've ended up with. Lists, numbers, and
even trees. [Ola](https://theory.epfl.ch/osven/) would've been proud!

#### The Lake
It's finally time to address the big elephant in the room. While jumping from
one trait to the other, I've been avoiding the `Lk`-traits, traits whose names
are of the form `L[ae]k[ae]`. These also seem to be the ones where interesting
things are happening, since all we've done up until now is construct basic data
structures.

Although dauntingly big, the traits `Leke`, `Laka` and `Leka` just take a type
parameter `X` and return a specific sequence of traits by matching it. For `Leka`
and `Leke`, they have a default matching `case _` which calls `Leke` and `Laka`
respectively if the type `X` wasn't matched previously. Therefore, we can see
this traits as a long list of matchings which for a given traits return a sequence
of traits, starting from `Leka`.

Therefore, it seems that the only think keeping us from the flag is the `Lake`
trait, since the trait we control, `Flag`, is only used inside `VictoryCondition`,
which makes use of `Lake` and the previously decoded traits.
```scala
type VictoryCondition = Lake[Leka[Miaouss], Concat[Flag, CharNul =~: EOS], Leka["main"] =~: EOS, NewTree[ZeroByte, 8], Leka] =:= (I[20] =~: EOS)
```

Before going into decoding `Lake` let's look at what information can we get on
its parameters from its use in `VictoryCondition`
```scala
type VictoryCondition = Lake[
    Leka[Miaouss],
    Concat[Flag, CharNul =~: EOS],
    Leka["main"] =~: EOS,
    NewTree[ZeroByte, 8],
    Leka
] =:= (I[20] =~: EOS)
```

We see that `Lake` takes 
 1. As its first argument, a sequence of traits, since that's what `Leka` returns
 2. As its second argument, a sequence of bytes (In our trait sequence 
 representation). We even know that starting value, which is the flag followed 
 by a char byte. We use `Concat` to concatenate both into one sequence.
 3. As its third argument, we have a sequence of sequences of traits. We must
not be deceived by the `=~:` operator. `Leka["main"]` returns a sequence of 
traints, and by appending it an end of sequence, we convert it into a sequence of
one sequence of taits
 4. As its fourth argument, a tree of height 8 filled with 0 bytes
 5. As its fifth argument, the trait `Leka`. This is a type "function" which takes
 a trait and gives a sequence of traits.

In Scala non-type-system equivalent code, the signature of `Lake` would be
```scala
def Lake( 
    a: List[Trait], 
    b: List[Bytes], 
    c: List[List[Trait]],
    d: Tree[8],
    e: Trait => List[Trait]
    )
```

With this in mind, we rename the arguments of `Lake` to better reflect what types
they hold and proceed to study the `Lake` trait.
```vim
%s/Kale/ListTraits/g
%s/Ekal/ListBytes/g
173,208s/Leka/ListListTraits/g
%s/Akel/Tree/g
%s/Keal/Func/g
```
Be careful when renaming `Leka` inside the body of `Lake`, since `Leka` is already
a trait defined outside `Lake`.

Thanks to these renames, the code in `Lake` has become much more readable much more readable
```scala
type Lake[ListTraits, ListBytes, ListListTraits, Tree, Func[_]] = ListTraits match
  case EOS => (ListBytes, Tree)
```
We first match the first argument, and if it's an empty sequence, we output the
second and fourth arguments. These are a sequence of bytes and a tree of height
8 respectively
```scala
  case data1 =~: data2 => data1 match
```
If the first argument isn't an empty sequence, we take the first element an match
it. From this point onward we start encountering some never seen before traits.
These are all sealed traits which may have a type parameter, and that do nothing
else with it than store it. 

Reading ahead in the code, we see that we always end up calling `Lake` again with
some modified arguments, except with the last trait, `Truman`, where we simply
return the `ListBytes`
```scala
    case Truman => ListBytes
```
This seems to be an exit condition for `Lake`, so we'll rename it to `Exit`
```vim
%s/Truman/Exit/g
```
We come back to the beginning of the match and proceed sequentially
```scala
    case Notification[x] => Lake[data2, x =~: ListBytes, ListListTraits, Tree, Func]
```
This trait takes the element it stored and puts it at the beginning of `ListBytes`.
```scala
    case Bts => ListBytes match
      case smoothLike =~: butter => Lake[data2, butter, ListListTraits, Tree, Func]
```
This trait takes the first element in `ListBytes` and ignores it.

These two cases seem to be doing push and pop operations on `ListBytes`. 
Because of this, we rename `Notification` to `Push`, `Bts` to `Pop` and 
`ListBytes` to `Stack`
```vim
%s/ListBytes/Stack/g
%s/Notification/Push/g
%s/Bts/Pop/g
```
Thanks to these findings, we start to get a feel about what `Lake` is doing
```scala
    case GoogleBusiness => Stack match
      case bing =~: sucks =~: lmao => Lake[data2, ByteAdd[sucks, bing] =~: lmao, ListListTraits, Tree, Funk]
```
This trait takes the next two elements of `Stack`, `bing` and `sucks`, adds them
together and puts them back in the `Stack` on top of the rest of the elements 
(`lmao`). Therefore, `GoogleBusiness` seems to be an add **instruction**, so
we rename it as such.
```vim
%s/GoogleBusiness/AddInstr/g
```
We also find out that `Stack` is a sequence of bytes. This we could have deduced
from the call to `Lake` in `VictoryCondition`, but here we see that these values are
being treated as integers, which is some extra bit of information we didn't have
```scala
    case MeUwU => Stack match
      case owo =~: qwq =~: uwu => Lake[data2, ByteSub[qwq, owo] =~: uwu, ListListTraits, Tree, Func]
    case CryptoBeLike => Stack match
      case math =~: too =~: hard => Lake[data2, Xor[too, math] =~: hard, ListListTraits, Tree, Func]
```
`MeUwU` and `CryptoBeLike` are almost equivalent to the previous `GoogleBusiness`, 
but now performing a subtraction and xor instead of addition, so we rename them 
to `SubInstr` and `XorInstr`
```vim
%s/MeUwU/SubInstr/g
%s/CryptoBeLike/XorInstr/g
```

```scala
    case SadeYouWereOnSilent[x] => Lake[Func[x], Stack, data2 =~: ListListTraits, Tree, Func]
```
We finally see the use of the other parameters. With this trait, we take its type
parameter and use it to replace its first argument with whatever list of traits
the parameter `Func` gives when applied to `x`. Also, the rest of traits which 
going to be processed are saved in the third parameter.

We notice how the traits we've been processing until know all seem to be instructions
on what to do within `Lake`. We therefore rename `ListTraits` to `Instructions`
and `ListListTraits` to `ListInstructions`
```vim
%s/ListTraits/Instructions/g
```
We continue
```scala
    case Sadge[localsCount] => Lake[Func[localsCount], Stack, ListInstructions, Tree, Func]
```
This is pretty similar to `SadeYouWereOnSilent`, with the exception that it doesn't
save the remaining instructions in `ListInstructions`. We start to see some kind
of pattern here, but let's analyze the next trait before uncovering it
```scala
    case TRex[roar] => Stack match
      case suchPredator =~: muchMonch => 
        IfZero[
          suchPredator,
          Magick[Lake[Func[roar], muchMonch, ListInstructions, Tree, Func]]#trick,
          Magick[Lake[data2, muchMonch, ListInstructions, Tree, Func]]#trick,
        ]
```
For this trait, we take the top of the stack and it it's zero, we change the 
instructions for whatever list of instructions `Func` gives us when given `TRex`'s
typ paramter. If the top of the stack isn't zero, execution continues as normal.

Notice the word execution. We have addition, subtraction and xor instructions, 
and now we've found a branching instruction. We can easily see now that 
`SadeYouWereOnSilent` and `Sadge` are `Call` and `Jump` instructinos respectively,
`TRex` a `JumpIfZero` instruction, and reading ahead, we find `Cringe`.
```scala
    case Cringe => ListInstructions match
      case bigL =~: plusRatio => Lake[bigL, Stack, plusRatio, Tree, Func]
```
Which implements the final control flow operation we need to make `Lake` into a
virtual machine, the `Return` instruction.

Therefore, with this new findings we can guess that `ListInstructions` are just
the stack frames of the virtual machine, and that `Func` gives us a mapping
between keywords and instructions, almost like a jump table.

With these new findings, we have much renaming to do
```vim
%s/ListInstructions/Frames/g
%s/SadeYouWereOnSilent/Call/g
%s/Sadge/Jump/g
%s/TRex/JumpIfZero/g
%s/Cringe/Return/g
```
```scala
    case StillWaiting => Stack match
      case comeOn =~: waitFaster => Lake[data2, GetNodeElement[Tree, comeOn] =~: waitFaster, Frames, Tree, Func]
    case OmwToBuyCarrots => Stack match
      case miam =~: withHummus =~: andCucumber => Lake[data2, andCucumber, Frames, ReplaceNodeElement[Tree, miam, withHummus], Func]
```
`StillWaiting` and `OmwToBuyCarrots` are the tree operations we were missing, which
respectively put a node element on the stack and replace a node element with an 
value in the stack. In the context of a virtual machine, we see that our `Tree`
is doing the job of the main memory, and that `StillWaiting` and `OmwToBuyCarrots`
are `Load` and `Store` operations
```vim
%s/StillWaiting/Load/g
%s/OmwToBuyCarrots/Store/g
173,208s/Tree/Memory/g
```
Be careful again when renaming `Tree` to not rename as well `NewTree` into 
`NewMemory`, although the change in name wouldn't be too bad.
```scala
    case Win => Stack match
      case flag =~: checker  => Lake[data2, flag =~: flag =~: checker, Frames, Memory, Func]
```
The `Win` trait instructs to double the head of the stack, so we rename it to 
`DoubleHead`
```vim
%s/Win/DoubleHead/g
```
```scala
    case Jessie => Stack match
      case                     aaaaaaa =~: aaaaaa =~: aaaaa => Lake[data2, aaaaaa =~: aaaaaaa =~: aaaaa, Frames, Memory, Func]
    case James => Stack match
      case         aaaaaaa =~: aaaaaa =~: aaaaaaaa =~: aaaaa => Lake[data2, aaaaaaaa =~: aaaaaaa =~: aaaaaa =~: aaaaa, Frames, Memory, Func]
    case Miaouss => Stack match
      case aaaaaaa =~: aaaaaa =~: aaaaaaaa =~: aaaa =~: aaaaa => Lake[data2, aaaa =~: aaaaaaa =~: aaaaaa =~: aaaaaaaa =~: aaaaa, Frames, Memory, Func]
```
The following three traits, named after Team Rocket celebrities, do some juggling
in the stack by bringing to the top the second, third and fourth elements respectively

We rename them to proper names
```vim
%s/Jessie/SecondToTop/g
%s/James/ThirdToTop/g
%s/Miaouss/FourthToTop/g
```
```scala
    case Exit => Stack
```
And we're finally on the last branch of the match, with the exit condition

Since we want the evaluation of `Lake` to be `I[20] =~: EOS`, we can already
see that the only way we'll get there is by triggering an `Exit` instruction.

We know just have to figure out how to get there.

Yes, that's right. You're revving again. Let's dive into the L[ae]k[ae]
