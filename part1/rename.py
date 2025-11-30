# find: my5grantester-logs-1-*-***-*.csv
# and rename to my5grantester-logs-n-*-***-*.csv

import os
import glob

inputs = "my5grantester-logs-2"
outputs = "my5grantester-logs-9"

counter = 0
files = glob.glob(inputs + '-*-*-*.csv')
for f in files:
    new_name = f.replace(inputs, outputs)
    os.rename(f, new_name)
    print(f'Renamed: {f} -> {new_name}')
    counter += 1
print(f'Total files renamed: {counter}')