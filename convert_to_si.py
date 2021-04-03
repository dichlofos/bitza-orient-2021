#!/usr/bin/env python
# coding: utf-8

"""
Translate pretty-printed file back to SportIduino station output format
after manual editing.

Author: Mikhail Veltishchev <dichlofos-mv@yandex.ru>
"""


from __future__ import print_function

import re
import sys
import json
import time

from datetime import datetime


def _decode(s):
    # assume 0 is not a valid station/punch number
    return int(re.sub(r'^0+', '', s.replace('n', '')))


def main():
    input_stream = None
    file_name = None
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        input_stream = open(file_name)
    else:
        input_stream = sys.stdin

    contents = input_stream.read()
    dump = json.loads(contents)

    for item in dump:
        card_number = str(item['card_number'])
        if 'n' not in card_number:
            print('This file is not an pretty-printed one, please check your input')
            sys.exit(1)

        card_number = _decode(card_number)
        item['card_number'] = card_number
        print("Card: {}".format(card_number))
        for punch in item['punches']:
            punch[0] = _decode(punch[0])
            punch[1] = time.mktime(datetime.strptime(punch[1], '%Y-%m-%d %H:%M:%S').timetuple())

    if file_name is not None:
        output_file_name = '{}_machine.json'.format(file_name.replace('_pretty.json', ''))
        with open(output_file_name, 'w') as out:
            out.write(json.dumps(dump, indent=4, sort_keys=True))

        print()
        print('Output is written into `{}`'.format(output_file_name))
    else:
        print(json.dumps(dump, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
