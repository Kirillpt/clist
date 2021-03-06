#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from pprint import pprint

from ranking.management.modules.common import REQ, BaseModule


class Statistic(BaseModule):
    API_RANKING_URL_FORMAT_ = 'https://leetcode.com/contest/api/ranking/{key}/?pagination={{}}'
    RANKING_URL_FORMAT_ = '{url}/ranking'

    def __init__(self, **kwargs):
        super(Statistic, self).__init__(**kwargs)

    def get_standings(self, users=None):
        standings_url = self.standings_url or self.RANKING_URL_FORMAT_.format(**self.__dict__)

        api_ranking_url_format = self.API_RANKING_URL_FORMAT_.format(**self.__dict__)
        url = api_ranking_url_format.format(1)
        content = REQ.get(url)
        data = json.loads(content)
        if not data:
            return {'result': {}, 'url': standings_url}
        n_page = (data['user_num'] - 1) // len(data['total_rank']) + 1

        problems_info = [{'short': f'Q{i + 1}', 'name': p['title']} for i, p in enumerate(data['questions'])]

        def fetch_page(page):
            url = api_ranking_url_format.format(page + 1)
            content = REQ.get(url)
            return json.loads(content)

        start_time = self.start_time.replace(tzinfo=None)
        result = {}
        with PoolExecutor(max_workers=8) as executor:
            for data in executor.map(fetch_page, range(n_page)):
                for row, submissions in zip(data['total_rank'], data['submissions']):
                    if not submissions:
                        continue
                    handle = row.pop('username')
                    if users and handle not in users:
                        continue
                    row.pop('contest_id')
                    row.pop('user_slug')
                    row.pop('global_ranking')

                    r = result.setdefault(handle, {})
                    r['member'] = handle
                    r['place'] = row.pop('rank')
                    r['solving'] = row.pop('score')

                    data_region = row.pop('data_region').lower()
                    r['info'] = {'profile_url': {'_data_region': '' if data_region == 'us' else f'-{data_region}'}}

                    country = None
                    for field in 'country_code', 'country_name':
                        country = country or row.pop(field, None)
                    if country:
                        r['country'] = country

                    solved = 0
                    problems = r.setdefault('problems', {})
                    for i, (k, s) in enumerate(submissions.items()):
                        p = problems.setdefault(f'Q{i + 1}', {})
                        p['time'] = self.to_time(datetime.fromtimestamp(s['date']) - start_time)
                        if s['status'] == 10:
                            solved += 1
                            p['result'] = '+' + str(s['fail_count'] or '')
                        else:
                            p['result'] = f'-{s["fail_count"]}'
                    r['solved'] = {'solving': solved}
                    finish_time = datetime.fromtimestamp(row.pop('finish_time')) - start_time
                    r['penalty'] = self.to_time(finish_time)
                    r.update(row)

        standings = {
            'result': result,
            'url': standings_url,
            'problems': problems_info,
        }
        return standings


if __name__ == "__main__":
    statictic = Statistic(
        name='Biweekly Contest 18',
        url='https://leetcode.com/contest/biweekly-contest-18/',
        key='biweekly-contest-18',
        start_time=datetime.now(),
        standings_url=None,
    )
    pprint(next(iter(statictic.get_standings()['result'].values())))
