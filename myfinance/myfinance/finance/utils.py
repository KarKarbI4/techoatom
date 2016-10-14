import random
import time
from datetime import datetime, timedelta

from collections import namedtuple



t_html = '''
<!doctype html>
<html lang="en">
{}
</html>
'''

t_head = '''
<head>
  <meta charset="utf-8">

  <title>{} - Myfinance</title>
  <meta name="description" content="Myfinance - online finance management service">
  <meta name="author" content="Victor Tyunyakov">
  <link rel="stylesheet" href="styles.css" />
</head>
'''

t_body = '''
<body>
  {}
</body>
'''

d_frmt = '%d.%m.%Y'
dt_frmt = '%d.%m.%Y %H:%M'

Charge = namedtuple('Charge', ('id', 'type', 'card_num', 'date', 'sum', 'status'))
types = ('Transfer to other client', 'Service payment', 'Balance accomplishment')
statuses = ('Success', 'Fail', 'Pending')
card_nums = ('4632 3243 0000 3233', '9999 2344 0987 4444')

def tag_wrap(tag, content=None):
    tag_wrap = '<{0}>\n{1}</{0}>'
    tag_wrap = tag_wrap.format(tag, '{}')
    if content is not None:
        tag_wrap = tag_wrap.format(content)
    return tag_wrap

def get_html(title='', body=''):
    return t_html.format(t_head.format(title) + t_body.format(body))

def html_table(headers=None, content=None):
    html_table = ''
    hw = ''
    for h in headers:
        hw += tag_wrap('th', h)
    html_table += tag_wrap('tr', hw)

    for row in content:
        rw = ''
        for cell in row:
            rw += tag_wrap('td', cell)
        html_table += tag_wrap('tr', rw)

    html_table = tag_wrap('table', html_table)
    return html_table

def str_time_prop(start, end, frmt, prop):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))

    ptime = stime + prop * (etime - stime)

    return time.strftime(frmt, time.localtime(ptime))

def random_dt(days_ago):
    curdate = datetime.now().date()
    days_ago = curdate + timedelta(days=-days_ago)
    prop = random.random()
    return str_time_prop(curdate.strftime(dt_frmt), days_ago.strftime(dt_frmt), dt_frmt, prop)

def gen_rand_charge(_id):
    r_type = random.choice(types)
    r_card_num = random.choice(card_nums)
    r_date = random_dt(30 * 6)
    r_sum = random.randrange(-30000, 30000 + 1)
    r_status = random.choice(statuses)
    return Charge(_id, r_type, r_card_num, r_date, r_sum, r_status)

def gen_table():
    n = random.randint(5, 20)
    charges = [gen_rand_charge(i) for i in range(n)]
    headers = [h.title() for h in Charge._fields]
    headers[0] = '#'
    return html_table(headers, charges)
        

if __name__ == '__main__':
    print(random_dt(30 * 6))
    print(tag_wrap('table').format('Hello, table'))
    headers = Charge._fields
    content = [gen_rand_charge(i) for i in range(5)]
    print(html_table(headers, content))