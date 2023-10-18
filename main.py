from collections import namedtuple
from enum import Enum
from pprint import pprint

import csv
import json
import re
import requests

DEBUG = False

data = []


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
def _match_url(link: str) -> re.Match[str] | None:
    for t in URLType:
        result = t.value.match(link)
        if result is not None:
            return (t.name, result.group(1))
    return (None, None)


def refresh_source(source_file="source.csv", output=False, output_file="generated_data/data.json"):
    with open(source_file, 'r', encoding='utf_8') as f:
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
            
            t_name, result = _match_url(link)

            if result is None:
                if DEBUG == True:
                    print(f"Warning: URL is unavailable. (URL: {link})")
            else: 
                data.append(
                        {"name": name, "link": link, "t_name": t_name, "uid": result}
                    )
    if output:
        with open(output_file, 'w') as f:
            json.dump(data, f)
    return data


def _get_data_WID(uid, field = "time", order = "DESC", pageNum = 0, maxRows = 20, keyword = "", flock = "-", tf = 1, auth_type = "user", timeout=60):
    """
    :param field:             str; ["time" | "unit" | "title" | "clicks"]; Sorted by what
    :param order:             str; ["DESC" | "ASC"]; Descending or Ascending
    :param pageNum:           int; Page from 0; return "Fail to query!" when < 0; NOT return any data when > totalPages
    :param maxRows:           int; Max rows if maxRows != 0, or return ''; return as [{"pageNum":0,"maxRows":-20,"totalPages":-796}] when < 0
    :param keyword:           str; Search by string
    :param flock:             str; Search with unit and/or category;Format: unit_\d+-attr_\d+
    :param tf:                int; g_show_time_format
    :param auth_type          str; Auth type
    :rtype                   list;
    :subret pageNum           int; same as parameter
    :subret maxRow            int; same as parameter
    :subret totalPages        int; Total pages
    :subret newsId            str; News ID for linking to content (usually int)
    :subret top               int; 1 for the news is HOT; 0 for normal news
    :subret time              int; Date (YYYY/MM/DD)
    :subret attr              str; Category ID (usually int)
    :subret attr_name         str; Category name
    :subret title             str; Title
    :subret title_color       str; Title color (CSS color)
    :subret unit              str; Unit ID (usually int)
    :subret unit_name         str; Unit name
    :subret issuer            str; Issuer ID (usually int)
    :subret name              str; Publisher
    :subret clicks            int; Click count
    :subret content_type      str; #Unknown
    :subret content      NoneType; #Unknown
    :subret is_sync           int; #Unknown
    :subret d_confirm         int; #Unknown
    :subret permission        str; >= 1 for lock and put lock.png; else 0
    :subret news_image        str; useless
    :subret news_image_width  int; useless
    :subret news_image_height  int; useless
    """

    url = "https://web.whsh.tc.edu.tw/ischool/widget/site_news/news_query_json.php"
    param = {
        "field": field,
        "order": order,
        "pageNum": pageNum,
        "maxRows": maxRows,
        "keyword": keyword,
        "flock": flock,
        "uid": uid,
        "tf": tf,
        "auth_type": auth_type
    }
    return requests.post(url, data=param, timeout=timeout).json()


def get_data(t_name, uid, field = "time", order = "DESC", pageNum = 0, maxRows = 20, keyword = "", flock = "-", tf = 1, auth_type = "user", timeout=60, output=False, output_file=None):
    
    if output and (output_file is not None):
        output_file = f'generated_data/{uid}.json'
    
    match t_name:
        case "WID":
            ret = _get_data_WID(uid, field, order, pageNum, maxRows, keyword, flock, tf, auth_type, timeout)
        case _:
            raise ValueError(f'Type {t_name} is currently unsupported')
        
    with open(output_file, 'w') as f:
        json.dump(f, ret)
    
    return ret
