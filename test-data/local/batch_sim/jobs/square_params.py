#!/usr/bin/env python
import sys
import json
import random
import time

keys = ["W1", "W2", "W3"]

def square_file(input_file, output_file):
    with open(input_file) as fin:
        data0 = json.load(fin)
    out = []
    for key in keys:
        data1 = data0[key]
        try:
            out.extend([str(v ** 2) for _, v in data1.items()])
        except AttributeError:
            out.append(str(data1 ** 2))
    with open(output_file, "w") as fout:
        fout.write("\n".join(out))



if __name__ == "__main__":
    square_file("WELL_ORDER.json", "ORDER_0")
    time.sleep(random.randint(0, 2))
    square_file("WELL_ON_OFF.json", "ON_OFF_0")
    time.sleep(random.randint(0, 2))
