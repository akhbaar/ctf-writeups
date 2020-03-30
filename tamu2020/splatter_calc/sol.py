#! /usr/bin/python3.7

import z3


c1, c2, c3 = z3.BitVecs('c1 c2 c3', 64)
rbx, r13, rbp, = c1, c2, c3


# rbx must equal 0x471DE8678AE30BA1

r13 =  0x83F66D0E3
rbp = 0x24A452F8E
rbx = rbx * r13
rbx = rbx + rbp


rbx = rbx * r13 
rbx = rbx + rbp

rbx = rbx * r13
rbx = rbx + rbp


rbx = rbx * r13
rbx = rbx + rbp


rbx = rbx * r13
rbx = rbx + rbp


rbx = rbx * r13
rbx = rbx + rbp


rbx = rbx * r13
rbx = rbx + rbp


rbx = rbx * r13
rbx = rbx + rbp
#print(z3.simplify(rbx))

solver = z3.Solver()
solver.add(rbx == 0x471DE8678AE30BA1)
if solver.check() == z3.sat:
    m = solver.model()
    print(m)
    print("result=%08X" % m[c1].as_long())
else:
    print("No sol :(")

