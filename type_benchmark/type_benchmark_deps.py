import random
import re

from enum import Enum

def random_url() -> str:
    letters = '0123456789abcdef'
    len = random.randint(38, 42)
    result_str = ''.join(random.choice(letters) for i in range(len))
    return result_str

pattern = r"^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/widget\/site_news\/main2\.php\?uid=(WID_\d+_\d_[0-9a-f]{39,40})&maximize=1&allbtn=0$"
sample = [random_url() for i in range(50)]

"""URLTypes"""

class classURLType(Enum):
    Volunteer = re.compile(r'^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/public\/volunteer\/index\.php\?bid=(\d+)$')
    WID = re.compile(pattern)
    BulletBoard = re.compile(r'^field=time&order=DESC&pageNum=0&maxRows=20&keyword=&flock=unit_(\d+)&uid=(WID_\d+_\d_[0-9a-f]{39,40})&tf=1&auth_type=user$')


dictURLType = {
    "Volunteer": re.compile(r'^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/public\/volunteer\/index\.php\?bid=(\d+)$'),
    "WID": re.compile(pattern),
    "BulletBoard": re.compile(r'^field=time&order=DESC&pageNum=0&maxRows=20&keyword=&flock=unit_(\d+)&uid=(WID_\d+_\d_[0-9a-f]{39,40})&tf=1&auth_type=user$')
}

listURLType = [
    ("Volunteer", re.compile(r'^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/public\/volunteer\/index\.php\?bid=(\d+)$')),
    ("WID", re.compile(pattern)),
    ("BulletBoard", re.compile(r'^field=time&order=DESC&pageNum=0&maxRows=20&keyword=&flock=unit_(\d+)&uid=(WID_\d+_\d_[0-9a-f]{39,40})&tf=1&auth_type=user$'))
]

tupleURLType = (
    ("Volunteer", re.compile(r'^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/public\/volunteer\/index\.php\?bid=(\d+)$')),
    ("WID", re.compile(pattern)),
    ("BulletBoard", re.compile(r'^field=time&order=DESC&pageNum=0&maxRows=20&keyword=&flock=unit_(\d+)&uid=(WID_\d+_\d_[0-9a-f]{39,40})&tf=1&auth_type=user$'))
)


