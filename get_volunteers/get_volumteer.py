import requests, time, random
f = open('volunteers.csv', 'w', encoding='utf-8')
for i in range(100):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    try:
        url = f'https://web.whsh.tc.edu.tw/ischool/public/volunteer/volunteer_query_json.php?pageNum=0&maxRows=10&keyword=&bid={i}&query_action=queryallconfirm&auth_type=user'
        r = requests.get(url, headers=headers)
        if r.headers['Content-Encoding'] == 'gzip':
            if len(r.json()) >= 2:
                print(f'{i} passed')
                f.write(f'{r.json()[1]["person_name"]},https://web.whsh.tc.edu.tw/ischool/public/volunteer/index.php?bid={i}\n')
            else:
                print(f'{i} failed')
        else:
            print(f'{i} failed')
    except KeyError:
        print(f'{i} failed')
    time.sleep(random.randint(6,15)/10)
f.close()