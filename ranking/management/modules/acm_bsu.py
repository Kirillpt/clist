#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from ranking.management.modules.common import REQ, DOT
from ranking.management.modules.common import BaseModule, parsed_table
from ranking.management.modules.excepts import InitModuleException


class Statistic(BaseModule):

    def __init__(self, **kwargs):
        super(Statistic, self).__init__(**kwargs)
        if not self.standings_url:
            raise InitModuleException('Not set standings url for %s' % self.name)

    def get_standings(self, users=None):
        season = self.key.split()[0]

        result = {}

        page = REQ.get(self.standings_url)
        table = parsed_table.ParsedTable(html=page, xpath="//table[@class='ir-contest-standings']//tr")
        problems_info = collections.OrderedDict()
        for r in table:
            row = {}
            problems = row.setdefault('problems', {})
            for k, v in list(r.items()):
                classes = v.attrs['class'].split()
                if 'ir-column-contestant' in classes:
                    row['member'] = v.value + ' ' + season
                    row['name'] = v.value
                elif 'ir-column-place' in classes:
                    row['place'] = v.value
                elif 'ir-column-penalty' in classes:
                    row['penalty'] = int(v.value)
                elif 'ir-problem-count' in classes:
                    row['solving'] = int(v.value)
                else:
                    letter = k.split()[0]
                    problems_info[letter] = {'short': letter}
                    if v.value == DOT:
                        continue
                    p = problems.setdefault(letter, {})
                    values = v.value.replace('−', '-').split(' ')
                    p['result'] = values[0]
                    if len(values) > 1:
                        p['time'] = values[1]
            result[row['member']] = row
        standings = {
            'result': result,
            'url': self.standings_url,
            'problems': list(problems_info.values()),
        }
        return standings


if __name__ == "__main__":
    statictic = Statistic(
        name='42', standings_url='https://acm.bsu.by/contests/40/standings/wide/', key='2017-2018 Олимпиада БГУ')
    from pprint import pprint
    pprint(statictic.get_standings('BelarusianSUIR #2 (Волчек, Соболь, Вистяж) 2017-2018'))
