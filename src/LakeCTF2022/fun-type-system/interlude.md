# Interlude: The deobfuscated code

Before we find the solution, I'll post the final deobfuscated `Main.scala` file
that we built in the process
```scala

@main
def main(args: String*) = println("much types, such recursion")

// Make me compile ;)
// Be patient, a successful compile takes 350s on my laptop.

// THIS IS THE ONLY LINE YOU HAVE TO CHANGE!
// if the flag were FLAG, enter it like this:
type Flag = CharF =~: CharL =~: CharA =~: CharG =~: EOS // keep the EOS at the end

// Use these (and only these) in the flag
type CharNul = ZeroByte
type CharA = ByteAdd[CharNul, OneByte]
type CharB = ByteAdd[CharA, OneByte]
type CharC = ByteAdd[CharB, OneByte]
type CharD = ByteAdd[CharC, OneByte]
type CharE = ByteAdd[CharD, OneByte]
type CharF = ByteAdd[CharE, OneByte]
type CharG = ByteAdd[CharF, OneByte]
type CharH = ByteAdd[CharG, OneByte]
type CharI = ByteAdd[CharH, OneByte]
type CharJ = ByteAdd[CharI, OneByte]
type CharK = ByteAdd[CharJ, OneByte]
type CharL = ByteAdd[CharK, OneByte]
type CharM = ByteAdd[CharL, OneByte]
type CharN = ByteAdd[CharM, OneByte]
type CharO = ByteAdd[CharN, OneByte]
type CharP = ByteAdd[CharO, OneByte]
type CharQ = ByteAdd[CharP, OneByte]
type CharR = ByteAdd[CharQ, OneByte]
type CharS = ByteAdd[CharR, OneByte]
type CharT = ByteAdd[CharS, OneByte]
type CharU = ByteAdd[CharT, OneByte]
type CharV = ByteAdd[CharU, OneByte]
type CharW = ByteAdd[CharV, OneByte]
type CharX = ByteAdd[CharW, OneByte]
type CharY = ByteAdd[CharX, OneByte]
type CharZ = ByteAdd[CharY, OneByte]
// end of alphabet

type VictoryCondition = Lake[Leka[FourthToTop], Concat[Flag, CharNul =~: EOS], Leka["main"] =~: EOS, NewTree[ZeroByte, 8], Leka] =:= (I[20] =~: EOS)

sealed trait Push[X]          
sealed trait OnBit              
sealed trait Pop                      
sealed trait AddInstr           
sealed trait Node[X]   
sealed trait SubInstr                    

type ByteAdd[X, Y] = ByteAddWithCarry[X, Y, OffBit]

type Map[L, F[_]] = L match
  case EOS => EOS
  case h =~: t => F[h] =~: Map[t, F]

type Fold[L, Z, F[_, _]] = L match
  case EOS => Z
  case h =~: t => F[h, Fold[t, Z, F]]

type Concat[L, R] = Fold[L, R, [h, t] =>> h =~: t]

type ZeroByte = OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: EOS

type I[X] = IntToBitstring[X, 8]

import scala.compiletime.ops.int.S
type Extend[X, I] = I match
  case 0 => EOS
  case S[n] => X match
    case EOS      => OffBit =~: Extend[X, n]
    case h =~: EOS => h =~: Extend[X, n]
    case h =~: t   => h =~: Extend[t, n]

type K[X] = X match
  case 0 => BitstringZero
  case S[n] => BitstringAddWithCarry[I[n], BistringOne, OffBit]

type BitstringAddWithCarry[X, Y, C] = (X, Y) match
  case (x =~: EOS, y =~: EOS) => BitAddWithCarry[x, y, C] match
    case (res, carry) => res =~: carry =~: EOS
  case (X, y =~: EOS) => BitstringAddWithCarry[X, y =~: OffBit =~: EOS, C]
  case (x =~: EOS, Y) => BitstringAddWithCarry[x =~: OffBit =~: EOS, Y, C]
  case (xh =~: xt, yh =~: yt) => BitAddWithCarry[xh, yh, C] match
    case (res, carry) => res =~: BitstringAddWithCarry[xt, yt, carry]

sealed trait XorInstr             
sealed trait OffBit
sealed trait Call[Bean]
sealed trait Jump[Smad]              
sealed trait Pair[L, R]

type BitAddWithCarry[X, Y, C] = X match
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

type BitstringZero = OffBit =~: EOS

type ReplaceNodeElement[T, N, X] = N match
  case EOS => T match
    case Node[x] => Node[X]
  case OffBit =~: bs => T match
    case Pair[l, r] => Pair[ReplaceNodeElement[l, bs, X], r]
  case OnBit =~: bs => T match
    case Pair[l, r] => Pair[l, ReplaceNodeElement[r, bs, X]]

type ByteAddWithCarry[X, Y, C] = (X, Y) match
  case (x =~: EOS, y =~: EOS) => BitAddWithCarry[x, y, C] match
    case (res, carry) => res =~: EOS
  case (xh =~: xt, yh =~: yt) => BitAddWithCarry[xh, yh, C] match
    case (res, carry) => res =~: ByteAddWithCarry[xt, yt, carry]

type ByteSub[X, Y] = ByteAdd[X, ByteAdd[Map[Y, Not], OneByte]]


sealed trait EOS
sealed trait JumpIfZero[Diplodocus]         
sealed trait Return                   
sealed trait =~:[Compare, To]
sealed trait Load             
sealed trait Store          
sealed trait DoubleHead                                      
sealed trait Exit     

type Not[X] = X match
  case OffBit => OnBit
  case OnBit => OffBit

type OneByte = OnBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: OffBit =~: EOS

type Xor[X, Y] = X match
  case EOS => EOS
  case OffBit =~: x => Y match
    case b =~: y => b =~: Xor[x, y]
  case OnBit =~: x => Y match
    case b =~: y => Not[b] =~: Xor[x, y]

type IfZero[X, T, F] = X match
  case OffBit =~: EOS => T
  case OffBit =~: t => IfZero[t, T, F]
  case OnBit =~: t => F

type IntToBitstring[X, Size] = Extend[K[X], Size]

type Lake[Instructions, Stack, Frames, Tree, Func[_]] = Instructions match
  case EOS => (Stack, Tree)
  case data1 =~: data2 => data1 match
    case Push[x] => Lake[data2, x =~: Stack, Frames, Tree, Func]
    case Pop => Stack match
      case smoothLike =~: butter => Lake[data2, butter, Frames, Tree, Func]
    case AddInstr => Stack match
      case bing =~: sucks =~: lmao => Lake[data2, ByteAdd[sucks, bing] =~: lmao, Frames, Tree, Func]
    case SubInstr => Stack match
      case owo =~: qwq =~: uwu => Lake[data2, ByteSub[qwq, owo] =~: uwu, Frames, Tree, Func]
    case XorInstr => Stack match
      case math =~: too =~: hard => Lake[data2, Xor[too, math] =~: hard, Frames, Tree, Func]
    case Call[x] => Lake[Func[x], Stack, data2 =~: Frames, Tree, Func]
    case Jump[localsCount] => Lake[Func[localsCount], Stack, Frames, Tree, Func]
    case JumpIfZero[roar] => Stack match
      case suchPredator =~: muchMonch => 
        IfZero[
          suchPredator,
          Magick[Lake[Func[roar], muchMonch, Frames, Tree, Func]]#trick,
          Magick[Lake[data2, muchMonch, Frames, Tree, Func]]#trick,
        ]
    case Return => Frames match
      case bigL =~: plusRatio => Lake[bigL, Stack, plusRatio, Tree, Func]
    case Load => Stack match
      case comeOn =~: waitFaster => Lake[data2, GetNodeElement[Memory, comeOn] =~: waitFaster, Frames, Memory, Func]
    case Store => Stack match
      case miam =~: withHummus =~: andCucumber => Lake[data2, andCucumber, Frames, ReplaceNodeElement[Memory, miam, withHummus], Func]
    case DoubleHead => Stack match
      case flag =~: checker  => Lake[data2, flag =~: flag =~: checker, Frames, Memory, Func]
    case SecondToTop => Stack match
      case                     aaaaaaa =~: aaaaaa =~: aaaaa => Lake[data2, aaaaaa =~: aaaaaaa =~: aaaaa, Frames, Memory, Func]
    case ThirdToTop => Stack match
      case         aaaaaaa =~: aaaaaa =~: aaaaaaaa =~: aaaaa => Lake[data2, aaaaaaaa =~: aaaaaaa =~: aaaaaa =~: aaaaa, Frames, Memory, Func]
    case FourthToTop => Stack match
      case aaaaaaa =~: aaaaaa =~: aaaaaaaa =~: aaaa =~: aaaaa => Lake[data2, aaaa =~: aaaaaaa =~: aaaaaa =~: aaaaaaaa =~: aaaaa, Frames, Memory, Func]
    case Exit => Stack

type NewTree[X, N] = N match
  case 0 => Node[X]
  case S[n] => Pair[NewTree[X, n], NewTree[X, n]]

type BistringOne = OnBit =~: EOS

type Leka[X] = X match
  case SecondToTop =>
    DoubleHead =~:
    Load =~:
    JumpIfZero["recurse-trampoline"] =~:
    Push[I[1]] =~:
    AddInstr =~:
    SecondToTop =~:
    Push[I[1]] =~:
    AddInstr =~:
    SecondToTop =~:
    Jump[SecondToTop] =~:
    EOS
  case ThirdToTop =>
    DoubleHead =~:
    ThirdToTop =~:
    AddInstr =~:
    SecondToTop =~:
    Load =~:
    SecondToTop =~:
    Store =~:
    Return =~:
    EOS
  case FourthToTop =>
    Push[I[42]] =~:
    Call[Pop] =~:
    Push[I[0]] =~:
    Push[I[42]] =~:
    Call[SecondToTop] =~:
    Push[I[8]] =~:
    SubInstr =~:
    JumpIfZero["stacktrace"] =~:
    Push[I[0]] =~:
    Exit =~:
    EOS
  case CharE =>
    Pop =~:
    Pop =~:
    Pop =~:
    Return =~:
    EOS
  case CharP =>
    Push[I[1]] =~:
    AddInstr =~:
    SecondToTop =~:
    Push[I[1]] =~:
    AddInstr =~:
    ThirdToTop =~:
    Push[I[1]] =~:
    SubInstr =~:
    Jump[Load] =~:
    EOS
  case CharF =>
    DoubleHead =~:
    Push[I[1]] =~:
    AddInstr =~:
    DoubleHead =~:
    Push[I[1]] =~:
    AddInstr =~:
    Load =~:
    SecondToTop =~:
    Load =~:
    ThirdToTop =~:
    Load =~:
    AddInstr =~:
    AddInstr =~:
    SecondToTop =~:
    Store =~:
    Return =~:
    EOS
  case CharL =>
    SecondToTop =~:
    Store =~:
    Return =~:
    EOS
  case _ =>
    Leke[X]
type Leke[X] = X match
  case "recurse-trampoline" =>
    Pop =~:
    Return =~:
    EOS
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
  case "strlen" =>
    DoubleHead =~:
    Load =~:
    DoubleHead =~:
    JumpIfZero[SubInstr] =~:
    ThirdToTop =~:
    XorInstr =~:
    SecondToTop =~:
    Push[I[1]] =~:
    AddInstr =~:
    Jump["strlen"] =~:
    EOS
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
  case _ =>
    Laka[X]
  type Laka[X] = X match
  case SubInstr =>
    Pop =~:
    Pop =~:
    Return =~:
    EOS
  case Pop =>
    SecondToTop =~:
    DoubleHead =~:
    JumpIfZero[CharL] =~:
    SecondToTop =~:
    DoubleHead =~:
    ThirdToTop =~:
    SecondToTop =~:
    Store =~:
    Push[I[1]] =~:
    AddInstr =~:
    Jump[Pop] =~:
    EOS
  case Load =>
    DoubleHead =~:
    JumpIfZero[EOS] =~:
    ThirdToTop =~:
    DoubleHead =~:
    Load =~:
    FourthToTop =~:
    DoubleHead =~:
    Load =~:
    ThirdToTop =~:
    SubInstr =~:
    JumpIfZero[CharP] =~:
    Pop =~:
    Pop =~:
    Pop =~:
    Push[I[0]] =~:
    Return =~:
    EOS
  case EOS =>
    Pop =~:
    Pop =~:
    Pop =~:
    Push[I[1]] =~:
    Return =~:
    EOS
  case OffBit =>
    Push[I[20]] =~:
    Exit =~:
    EOS


type GetNodeElement[T, N] = N match
  case EOS => T match
  case Node[x] => x
  case OffBit =~: bs => T match
  case Pair[l, r] => GetNodeElement[l, bs]
  case OnBit =~: bs => T match
  case Pair[l, r] => GetNodeElement[r, bs]

  sealed trait SecondToTop                   
  sealed trait ThirdToTop                    
  sealed trait FourthToTop  

  type =:=[X, Y] = X match
  case Y => Unit

class Magick[T]:
  type trick = T
```
