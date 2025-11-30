# find: my5grantester-logs-1-*-***-*.csv
# and rename to my5grantester-logs-n-*-***-*.csv

import os
import glob

counter = 0
files = glob.glob('my5grantester-logs-2-*-*-*.csv')
for f in files:
    new_name = f.replace('my5grantester-logs-2-', 'my5grantester-logs-5-')
    os.rename(f, new_name)
    print(f'Renamed: {f} -> {new_name}')
    counter += 1
print(f'Total files renamed: {counter}')