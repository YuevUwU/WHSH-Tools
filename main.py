from enum import Enum

import csv
import re

DEBUG = False

target = {
    'Available': [],
    'Unavailable': []
}


# PEP8: `CapitalizedWords`` (or CapWords, or CamelCase – so named because of the bumpy look of its letters ^[4]). This is also sometimes known as StudlyCaps.
# PEP8: Class names should normally use the CapWords convention.
# Both string and bytes literals may optionally be prefixed with a letter 'r' or 'R'; such strings are called raw strings and treat backslashes as literal characters.
class URLType(Enum):
    WID = re.compile(r"^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/widget\/site_news\/main2\.php\?uid=(WID_\d+_\d_[0-9a-f]{39,40})&maximize=1&allbtn=0$")
    Volunteer = re.compile(r'^https:\/\/web\.whsh\.tc\.edu\.tw\/ischool\/public\/volunteer\/index\.php\?bid=(\d+)$')
    BulletBoard = re.compile(r'^field=time&order=DESC&pageNum=0&maxRows=20&keyword=&flock=unit_(\d+)&uid=(WID_\d+_\d_[0-9a-f]{39,40})&tf=1&auth_type=user$')


# https://docs.python.org/zh-tw/3/library/re.html#search-vs-match
# re.match() 只在字符串的开头位置检测匹配。
# re.search() 在字符串中的任何位置检测匹配（这也是 Perl 在默认情况下所做的）
# re.fullmatch() 检测整个字符串是否匹配
def match_url(link: str) -> re.Match[str] | None:
    for t in URLType:
        type = t.value
        result = type.match(link)
        if result is not None:
            return type, result.group(1)
    return None, None


with open('source.csv', 'r', encoding='utf_8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 2:
            raise TypeError(f"URL Match Process takes exactly 2 argument ({len(row)} given)")
        name, link = row[0], row[1]

        if (name, link) == ('', ''):
            continue

        # Skip if name with `!` prefix
        if name[0] == '!':
            continue
        
        type, result = match_url(link)

        if DEBUG == True:
            if result is None:
                print(f"Warning: URL is unavailable. (URL: {link})")
