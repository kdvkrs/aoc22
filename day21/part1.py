#!/usr/bin/env python

import sys
import z3

def main(part=1):
    MD = {}
    MV = {}
    
    for l in sys.stdin:
        l = l.strip()
        m, exp = l.split(": ")
        MD[m] = exp.split(" ")
        MV[m] = z3.Int(m)

    s = z3.Solver()
    for m, exp in MD.items():
        if m == "humn" and part==2:
            pass
        else:
            if len(exp) == 3:
                lm, op, rm = exp
                if m == "root" and part==2:
                    s.add(MV[lm] == MV[rm])
                else:
                    op = exp[1]
                    if op == "*":
                        s.add(MV[m] == (MV[lm]*MV[rm]))
                    elif op == "/":
                        s.add(MV[m] == (MV[lm]/MV[rm]))
                    elif op == "+":
                        s.add(MV[m] == (MV[lm]+MV[rm]))
                    elif op == "-":
                        s.add(MV[m] == (MV[lm]-MV[rm]))
            elif len(exp) == 1:
                s.add(MV[m] == int(exp[0]))

    s.check()
    m = s.model()
    print(m[MV["root" if part==1 else "humn"]])


if __name__ == "__main__":
    main(part=1)