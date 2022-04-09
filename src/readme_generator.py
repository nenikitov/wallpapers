import os
from path import from_root


for file in os.listdir(from_root('img')):
    print(file)
