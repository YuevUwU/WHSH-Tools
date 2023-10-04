我把討厭的flake8打開了

因為最近在學C家族的語言，寫成`class ClassName() {}`

regex的內文採用了含`\`的方法，當然Python的Raw String功能不需寫`\/`和`\.`

關於程式語言兼容性與代碼可讀性我會偏好前者

值得一提的是，`\?`、`\*`、`\+`必須保留，否則將視為Quantifier

一開始我先用Enum作枚舉，到時候再看看效能

在此做個小筆記，`Alt + Up/Down`，遷移行的位置

在命名`data`下的dict時還蠻頭痛的，`result`、`content`、`suffix`、`keyword`都不泛用，最後是選擇了`uid`，在此希望徵求key名

我們來看看`WID`類別所需要傳遞的參數，以公佈欄為例
`field=time&order=DESC&pageNum=0&maxRows=20&keyword=&uid=WID_0_2_518cd2a7e52b7f65fc750eded8b99ffcc2a7daca&tf=1&auth_type=user`
即：
- field: time
- order: DESC
- pageNum: 0
- maxRows: 20
- keyword: 
- uid: WID_0_2_518cd2a7e52b7f65fc750eded8b99ffcc2a7daca
- flock: 
- tf: 1
- auth_type: user
- 欲請求的URL：https://web.whsh.tc.edu.tw/ischool/widget/site_news/news_query_json.php
- 方法：POST

同樣以公佈欄為例，return值如下(maxRows=1):

有HOT: 

```Python
[{'pageNum': 0, 'maxRows': 1, 'totalPages': 15927},
 {'newsId': '20625',
  'top': 1,
  'time': '2023/10/02',
  'attr': '1',
  'attr_name': '公告',
  'title': '112年度校園流感疫苗電子化系統(CIVS)意願簽署及注意事項',
  'title_color': '',
  'unit': '99',
  'unit_name': '衛生組',
  'issuer': '100071',
  'name': '衛生組',
  'clicks': '264',
  'content_type': 'content',
  'content': None,
  'is_sync': 1,
  'd_confirm': 1,
  'permission': '0',
  'news_image': 'https://web.whsh.tc.edu.tw/ischool/static/image/default_news.png',
  'news_image_width': 0,
  'news_image_height': 0}]
```

沒HOT:

```Python
 {'newsId': '20660',
  'top': 0,
  'time': '2023/10/04',
  'attr': '1',
  'attr_name': '公告',
  'title': '轉知：「教育部國民及學前教育署112學年度第2學期孝道教育多元補充教材申請暨發放實施計畫」資訊',
  'title_color': '',
  'unit': '87',
  'unit_name': '訓育組',
  'issuer': '100067',
  'name': '訓育組',
  'clicks': '1',
  'content_type': 'content',
  'content': '',
  'is_sync': 1,
  'd_confirm': 1,
  'permission': '0',
  'news_image': 'https://web.whsh.tc.edu.tw/ischool/static/image/default_news.png',
  'news_image_width': 0,
  'news_image_height': 0},
```

我們可以整理出
```Python
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
```