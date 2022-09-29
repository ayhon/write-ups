## The Lake
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
type parameter. If the top of the stack isn't zero, execution continues as normal.

The `Magick[...]#trick` may distract us at first, but this is using a mechanism
(called [type projection](https://www.scala-lang.org/files/archive/spec/2.13/03-types.html#type-projection)
for the curious) which just creates a type inside `Magick` called `trick` and 
outputs it again.

Notice how I used the word *execution*. We have addition, subtraction and xor 
instructions, and now we've found a branching instruction. We can easily see now 
that `SadeYouWereOnSilent` and `Sadge` are `Call` and `Jump` instructions 
respectively, `TRex` a `JumpIfZero` instruction, and reading ahead, we find 
`Cringe`.
```scala
    case Cringe => ListInstructions match
      case bigL =~: plusRatio => Lake[bigL, Stack, plusRatio, Tree, Func]
```
Which implements the final control flow operation we need to make `Lake` into a
virtual machine, the `Return` instruction.

Therefore, with this new findings we can guess that `ListInstructions` are just
the stack frames of the virtual machine, and that `Func` gives us a mapping
between keywords and instructions, almost like a jump table.

I don't know about you, but it's at this point when I realized that this was
going to take more time than expected. And it did.

With these new findings, we have much renaming to do
```vim
%s/ListInstructions/Frames/g
%s/SadeYouWereOnSilent/Call/g
%s/Sadge/Jump/g
%s/TRex/JumpIfZero/g
%s/Cringe/Return/g
```
And we carry on with our analysis, to see what other instructions we've defined
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
`NewMemory`, although the change in name would fit nevertheless
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

We rename them to more proper names
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
