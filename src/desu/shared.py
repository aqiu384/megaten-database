#!/usr/bin/python3
def load_id_file(fname):
    with open(fname) as tsvfile:
        next(tsvfile)
        return [x.strip() for x in tsvfile]

def printif_notequal(dname, field, lhs, rhs):
    if str(lhs) != str(rhs):
        print(dname, field, lhs, rhs)
