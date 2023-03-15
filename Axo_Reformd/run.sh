#!/usr/bin/env bash
python divide_eu.py
python divide_us.py 
wait

detox -r US
detox -r EU
wait

# python clean_city.py 5 5 2 EU
# python clean_city.py 5 5 2 US
# wait