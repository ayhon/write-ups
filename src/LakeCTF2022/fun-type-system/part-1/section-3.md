## Functions on lists

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
