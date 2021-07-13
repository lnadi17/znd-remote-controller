import os
import numpy as np

is_first = True
for file in os.listdir():
    if '.dat' not in file:
        continue
    with open(file, 'r') as src:
        with open(f"parsed/{file.split('.')[0]}.npy", 'w') as dst:
            rows = []
            while True:
                line = src.readline()
                if line == '':
                    break
                if line[0] == '%':
                    continue
                row = ','.join(line.split(',')[:-1])
                dst.write(row + '\n')
print('El Psy Congroo.')
