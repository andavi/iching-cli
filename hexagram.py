from random import randint as numIn

# for the changing line calculations
table = [
  '―――― X ――――',
  '――――   ――――',
  '―――――Θ―――――',
  '―――――――――――'
]

# for the gua's w/o moving lines where 0 is yin and 1 in yang
key = [table[1], table[3]]


# this is to convert the coded guas to just zeros and ones for ease of printing,
# converting, and special caees
def sanitize(gx):
  return [l>>1 for l in gx]

# this returns the opposite of the inputted gua for all changing lines case
# not yet assuming all zeros and ones a bitwise NOT operator oughtta do it
def toOpposite(gx):
  # return [~l for l in gx]
  # return [int(not bool(l)) for l in gx]
  return [(l - 1) % 4 for l in gx]
  


def getLines():
  #######################################
  # Kennedy Method (see link)
  ######################################
  # this is for the most nitpicky calculation of probablities for how
  # the yarrow stalks were thrown and interpretted according to the blurb 
  # by/[about Andrew Kennedy](https://en.wikipedia.org/wiki/I_Ching_divination#Dice)
  # according to his analysis the odds are 8/38 moving yang, 2/38 moving yin, 11/38 static yang,
  # and 17/38 static yin. These probabilities can be achieved using a 19-sided die and a coin which I 
  # simulate below:
  # | c | d  |  P    | line     |
  # |---|----|-------|----------|
  # |0  |<=2 |2/38   |mov yin   |
  # |0  | >2 |17/38  |stat yin  | 
  # |1  |<=8 |8/38   |mov yan   |
  # |1  | >8 |11/39  |stat yan  |

  # create coin toss and die toss function
  c = lambda: numIn(0,1)
  d = lambda: numIn(1,19)

  # fill len=6 array w/ coin and die toss values
  h = [[c(), d()] for _ in range(6)]

  # tricky part: want to keep coin toss info so convert to string and 
  # concatenate rathher than add. then cast str to binary int. first bit
  # (coin toss) is larger in table: if c=0 then line will be table[0] or
  # table[1], so a binary zero needs to stay left in that case and v.v.
  hx = [int(str(l[0]) +  str(int(l[1] > 2 if l[0] == 0 else l[1] > 8)),2) for l in h]


  # get lines that match rolls
  return [table[i] for i in hx], hx


# print from first line at botttom up as is traditional
def printGuaDebug(gua, mx):
  for i in range(5,-1,-1):
    print(gua[i], mx[i])

  
def movingLinesToOne(metahex):
  # As per Master Huang's instructions there should be only one or less moving lines.
  # the original gua is reflecting your current situation, THe moving line then allows a line to alternative,
  # pointing to an approached gua. An original and an approached gua with readings linking how to make
  # the transition is the correct amount of info for a reading (or less ie no moving lines is fine).
  # For this reason The Complete I Ching outlines an algorithm to get any readings w/ moving lines down to the single
  # important moving line.. That is what this function does.
  # print(metahex)
  umx = list(metahex)
  
  
  
  # Helpers
  ################
  # only looking for moving lines which are coded 0 and 2 in our table at top so search and count evens
  def moving(n):
    return not n % 2

  ###################
  
  movingLines = [n for n in umx if moving(n)]

  # print(movingLines)
  numMovingLines = len(movingLines)
  
    
  
  # if <= 1 then no work needs to be done - all good. return to sender
  if numMovingLines <= 1:
    return metahex
  
  # if two moving lines and different types: consult yin only
  if numMovingLines == 2 and len(set(movingLines)) == 2:
    return [3 if l == 2 else l for l in umx ]
  
  # if two moving lines the same => consult upper only
  if numMovingLines == 2:
    for i, n in enumerate(umx):
      if moving(n):
        umx[i] += 1
        return umx
    
  # if three moving lines consult central only
  if numMovingLines == 3:
    for i, n in enumerate(umx):
      if moving(n):
        umx[i] += 1
        break;
    for i, n in reversed(list(enumerate(umx))):
      if moving(n):
        umx[i] += 1
        return umx
      
  # if 4 moving, consolut upper nonmoving
  if numMovingLines == 4:
    for i, n in reversed(list(enumerate(umx))):
      if not moving(n):
        umx[i] -= 1
        return [l + 1 if moving(l) else l for l in umx[:i]] +[umx[i]] + [l+1 if moving(l) else l for l in umx[i+1:]]
      
  # if 5 moving, consult only nonmoving
  if numMovingLines == 5:
    return [l + 1 if moving(l) else l - 1 for l in umx]

  # means all six lines are chaning - a spcecial case where the original gua becomes
  # the pointed to gua using all six changing linkes (aka its opposite)
  else:
    return toOpposite(umx)
    # return sanitize(umx)
  
def drawnGua(hx):
  return [table[l] for l in hx]
  
def printGua(gua):
  print()
  for i in range(5,-1,-1):
    print(gua[i])  
  print()  
  
  
  
  
mx = [0,3,2,2,1,2] 
gua = drawnGua(mx)
# gua, mx = getLines()
printGua(gua)  
hx = movingLinesToOne(mx)
printGua(drawnGua(hx))