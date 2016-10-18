import random
import time
from datetime import datetime, timedelta

from collections import namedtuple

d_frmt = '%d.%m.%Y'
dt_frmt = '%d.%m.%Y %H:%M'

Charge = namedtuple('Charge', ('id', 'type', 'card_num', 'date', 'sum', 'status'))
types = ('Transfer to other client', 'Service payment', 'Balance accomplishment')
statuses = ('Success', 'Fail', 'Pending')
card_nums = ('1111 2222 3333 4444', '5555 6666 7777 8888')

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

def gen_charges():
    n = random.randint(5, 20)
    charges = [gen_rand_charge(i) for i in range(n)]
    return charges

def gen_headers():
	headers = [h.title() for h in Charge._fields]
	headers[0] = '#'
	return headers

if __name__ == '__main__':
    print(random_dt(30 * 6))
    print(tag_wrap('table').format('Hello, table'))
    headers = Charge._fields
    content = [gen_rand_charge(i) for i in range(5)]