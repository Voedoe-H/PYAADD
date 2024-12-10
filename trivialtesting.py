from pydd.builder import *
from pydd.aadd import *
from pydd.affine_form import *

context = Builder()

af1 = AffineForm(1,{"1":1.0},context)
af2 = AffineForm(1,{"2":1.0},context)
af3 = af1 + af2
print(af3)

#ad1 = context.