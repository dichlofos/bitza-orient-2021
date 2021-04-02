# coding: utf-8

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
        for punch in item['punches']:
            punch_id = punch[0]
            punch_ts = int(punch[1])
            print(
                "    {:04d}: {}".format(
                    punch_id,
                    datetime.utcfromtimestamp(punch_ts).strftime('%Y-%m-%d %H:%M:%S'),
                )
            )
            if len(punch) == 2:  # old format
                punch.append('{:04d}'.format(punch_id))
                punch.append(datetime.utcfromtimestamp(punch_ts).strftime('%Y-%m-%d %H:%M:%S'))

    if file_name is not None:
        with open('{}_formatted.json'.format(file_name), 'w') as out:
            out.write(json.dumps(dump, indent=4, sort_keys=True))
    else:
        print(json.dumps(dump, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
