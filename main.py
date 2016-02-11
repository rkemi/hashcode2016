#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import requests
import json
import sys

def main():
    filename = sys.argv[1]
    delivery = parse_file(filename)
    print delivery

def parse_file(filename):
    f = open(filename, 'rU')
    parsed = {}
    lines = f.readlines()
    index = 0

    # settings
    settings = lines[index].split(" ")
    parsed['rows'] = int(settings[0])
    parsed['columns'] = int(settings[1])
    parsed['drones'] = int(settings[2])
    parsed['turns'] = int(settings[3])
    parsed['payload'] = int(settings[4])
    index = index + 1

    # products
    parsed['num_products'] = int(lines[index])
    index = index + 1
    parsed['product_weights'] = to_int_list(lines[index])
    index = index + 1

    # warehouses
    num_warehouses = int(lines[index])
    index = index + 1
    warehouses = []
    for i in range(0, num_warehouses):
        warehouse = {}
        warehouse['location'] = to_int_list(lines[index])
        index = index + 1
        warehouse['inventory'] = to_int_list(lines[index])
        index = index + 1
        warehouses.append(warehouse)
    parsed['num_warehouses'] = num_warehouses
    parsed['warehouses'] = warehouses

    # orders
    num_orders = int(lines[index])
    index = index + 1
    orders = []
    for i in range(0, num_orders):
        order = {}
        order['location'] = to_int_list(lines[index])
        index = index + 1
        order['num_items'] = int(lines[index])
        index = index + 1
        order['product_types'] = to_int_list(lines[index])
        index = index + 1
        orders.append(order)
    parsed['num_orders'] = num_orders
    parsed['orders'] = orders

    return parsed

def to_int_list(line):
    return map(int, line.split(" "))


if __name__ == '__main__':
    main()
