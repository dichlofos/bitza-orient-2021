#!/usr/bin/env bash

./pretty_print_station.py station_log.json
./convert_to_si.py station_log_pretty.json
# out `station_log_machine.json`
cp station_log_pretty.json back_station_log_pretty.json
./pretty_print_station.py station_log_machine.json
if diff back_station_log_pretty.json station_log_machine_pretty.json ; then
    echo "OK"
else
    echo "FAIL"
fi
