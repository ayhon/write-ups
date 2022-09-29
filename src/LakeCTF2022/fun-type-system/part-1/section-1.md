## First steps

The first thing you see when you open the file are some instructions about
how to solve the challenge. 
```scala
// THIS IS THE ONLY LINE YOU HAVE TO CHANGE!
// if the flag were FLAG, enter it like this:
type Flag = CharF =~: CharL =~: CharA =~: CharG =~: Checksum // keep the Checksum at the end
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
<a href="https://en.wikipedia.org/wiki/Language_interoperability">interoperate</a> with.
However, in pure Scala code, you won't find any mention of classes or interfaces,
but only traits. Think of a trait as a more powerful type of interface, with the
ability to be instantiated as an object. Throughout this write up, I'll use type and
traits almost interchangeably, the same way that I'll refer to 
<a href="https://kubuszok.com/compiled/kinds-of-types-in-scala/#kinds-and-higher-kinded-types">kinds</a> 
as if they were functions. In practice, it's easier to reason about them this 
way for the challenge, and they aren't that far off the truth.

The keyword `sealed` just tells the Scala compiler that all objects implementing
that trait are defined in the same file the trait definition is in. It's a
mechanism for controlling the creation of new objects which implement a trait.

Finally, for those who haven't had any experience with Scala, it may look weird
that we define a type with the symbols `=~:`. In Scala you don't have the usual
restrictions for a keyword you'll find in other languages. 

Also, if your type takes 2 generics as "type arguments", you can use the infix
syntax to apply them. These are called <a href="https://www.scala-Lang.org/files/archive/spec/2.11/03-types.html#infix-types">infix operators</a>, which means that the following two are
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

