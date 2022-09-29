## Wait, there's a tree?
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

