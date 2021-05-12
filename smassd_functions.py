import datetime
import re
import random
import time
import hashlib

# Below are global functions

# Months hash simplifies processing timestamps:
months = {
   "Jan": "01",
   "Feb": "02",
   "Mar": "03",
   "Apr": "04",
   "May": "05",
   "Jun": "06",
   "Jul": "07",
   "Aug": "08",
   "Sep": "09",
   "Oct": "10",
   "Nov": "11",
   "Dec": "12"
}

# this function prints with timestamps
def log(m):
    print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ": "+m)
    return

# this function pauses for a random number of seconds to play nicely
def wait():
    num_seconds = random.randint(2,10)
    time.sleep(num_seconds)

# this function converts tweet timestamps into sqlite standard ones
def procTimestamp(c):
    a = c.split()
    z = a[5]+'-'+months[a[1]]+'-'+a[2]+' '+a[3]
    return z

# this function retrieves the file extension from a file name (i.e. .jpg)
def getFileExtension(a):
    b = re.search(r'\.[A-Za-z0-9]+$', a).group(0)
    return b

# this function calculates the unique hash for a file
def getMD5(file_name):
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


