# -*- coding: utf-8 -*-

import json
import re
from pprint import pprint
from collections import OrderedDict
from datetime import datetime

from ranking.management.modules.common import BaseModule, requester


class Statistic(BaseModule):
    CONTEST_STATE_ = '{0.url}'
    STANDING_URL_ = '{0.url}scoreboard/'
    SCOREBOARD_STATE_URL_ = 'https://csacademy.com/contest/scoreboard_state/?contestId={0.cid}'

    def __init__(self, **kwargs):
        super(Statistic, self).__init__(**kwargs)

    def get_standings(self, users=None):
        if not self.key.isdigit():
            return {'action': 'delete'}

        self.cid = int(self.key)

        req = requester(headers=[('X-Requested-With', 'XMLHttpRequest')])
        req.caching = None
        req.time_out = 17

        url = self.CONTEST_STATE_.format(self)
        state = json.loads(req.get(url))['state']
        tasks = {}
        problems_info = OrderedDict()
        for task in state['contesttask']:
            if task.get('contestId') != self.cid:
                continue
            tasks[task['id']] = task

            d = {'short': task['name'], 'name': task['longName']}
            if 'pointsWorth' in task:
                d['full_score'] = task['pointsWorth']
            problems_info[task['id']] = d

        url = self.SCOREBOARD_STATE_URL_.format(self)
        state = json.loads(req.get(url))['state']
        handles = {}
        for user in state['publicuser']:
            handles[user['id']] = user

        result = {}
        n_total = 0
        rows = state['contestuser']
        start_time = datetime.timestamp(self.start_time)
        for row in rows:
            if row['contestId'] != self.cid or 'rank' not in row:
                continue
            u = handles[row['userId']]
            handle = u['username']
            if not handle or users and handle not in users:
                continue
            n_total += 1
            r = result.setdefault(handle, OrderedDict())
            r['member'] = handle
            r['place'] = row.pop('rank')
            r['penalty'] = round(row.pop('penalty'))
            r['solving'] = row.pop('totalScore')
            problems = r.setdefault('problems', {})
            solving = 0
            for k, v in row.pop('scores').items():
                k = int(k)
                if k not in tasks:
                    continue
                task = tasks[k]
                p = problems.setdefault(task['name'], {})
                p['result'] = v['score']
                if v['score'] > 0:
                    solving += 1

                n = v.get('numSubmissions')
                if task.get('scoreTypeName', '').lower() == 'acm-style' and n:
                    if v['score'] > 0:
                        p['result'] = f'+{"" if n == 1 else n - 1}'
                    else:
                        p['result'] = f'-{n}'
                if 'scoreTime' in v:
                    time = int((v['scoreTime'] - start_time) / 60)
                    p['time'] = f'{time // 60:02}:{time % 60:02}'

            r['solved'] = {'solving': solving}

            for f in ('userId', 'timeRegistered', 'numSubmissions', 'contestId', 'id'):
                row.pop(f, None)
            for f in ('oldRating', 'rating'):
                if f in row:
                    r[re.sub('[A-Z]', lambda m: '_' + m.group(0).lower(), f)] = round(row.pop(f))
            if 'old_rating' in r and 'rating' in r:
                r['delta'] = r['rating'] - r['old_rating']

            for k, v in row.items():
                if k not in r:
                    r[k] = v

        standings = {
            'result': result,
            'url': self.STANDING_URL_.format(self),
            'problems': list(problems_info.values()),
        }
        return standings


if __name__ == '__main__':
    statistic = Statistic(
        url='https://csacademy.com/contest/round-67/',
        key='33089',
        start_time=datetime.strptime('31.01.2018 18:35', '%d.%m.%Y %H:%M'),
    )
    pprint(statistic.get_result('Aeon'))
    # pprint(statistic.get_standings()['problems'])
