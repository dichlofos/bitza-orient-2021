#!/usr/bin/env python
# coding: utf-8

"""
Translate SportIduino station output format into Ctrl-F-friendly format
that is easy to edit via text editor (manual check points insertion/etc.

Author: Mikhail Veltishchev <dichlofos-mv@yandex.ru>
"""


from __future__ import print_function

import sys
import json

from datetime import datetime


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
        print("Card: {}".format(item['card_number']))
        item['card_number'] = '{:04d}n'.format(item['card_number'])
        for punch in item['punches']:
            punch_id = punch[0]
            punch_ts = int(punch[1])
            print(
                "    {:04d}: {}".format(
                    punch_id,
                    datetime.utcfromtimestamp(punch_ts).strftime('%Y-%m-%d %H:%M:%S'),
                )
            )
            punch[0] = '{:04d}'.format(punch_id)
            punch[1] = datetime.utcfromtimestamp(punch_ts).strftime('%Y-%m-%d %H:%M:%S')

    if file_name is not None:
        output_file_name = '{}_pretty.json'.format(file_name.replace('.json', ''))
        with open(output_file_name, 'w') as out:
            out.write(json.dumps(dump, indent=4, sort_keys=True))

        print()
        print('Output is written into `{}`'.format(output_file_name))
    else:
        print(json.dumps(dump, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
