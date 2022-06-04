from random import randint as numIn


table = [
  '―――― X ――――',
  '――――   ――――',
  '―――――Θ―――――',
  '―――――――――――'
]

# this is for the most nitpicky calculation of probablities for how
# the yarrow stalks were thrown and interpretted according to the blurb 
# by/[about Andrew Kennedy](https://en.wikipedia.org/wiki/I_Ching_divination#Dice)
# according to his analysis the odds are 8/38 moving yang, 2/38 moving yin, 11/38 static yang,
# and 17/38 static yin

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
hexagram = [table[i] for i in hx]

# print from first line at botttom up as is traditional
for i in range(5,-1,-1):
  print(hexagram[i])