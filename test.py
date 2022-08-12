from cmath import sqrt
import math
import sys
type = int(input("Func type: "))

if type == 1:
    numb = int(input("Num: "))
    numb = sqrt(numb)
    numb = (1/numb)
    numb = numb * 100
    print(numb)
elif type == 2:
    numb = int(input("Num: "))
    numb = sqrt(numb)
    numb = (1/numb)
    numb = numb * 200
    print(numb)
elif type == 3:
    numb = int(input("Num: "))
    numb2 = int(input("Num2: "))
    numb = sqrt(numb)
    numb = (1/numb)
    numb2 = sqrt(numb2)
    numb2 = (1/numb2)
    numb = ((numb + numb2)/2) * 1.5
    numb = numb * 100
    print(numb)
else:
    sys.exit("invalid")