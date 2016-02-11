#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import requests
import json
import sys
import math
from Queue import PriorityQueue

def main():
    filename = sys.argv[1]
    delivery = parse_file(filename)
    max_turns = delivery['turns']
    warehousePrice = []
    for warehouse in delivery['warehouses']:
        warehouse['price'] = PriceW(warehouse, delivery['orders'], delivery['product_weights'], delivery['payload'])
    
    pqueue = PriorityQueue()
    for x in range(0, delivery['drones']):
        drone = {}
        drone['number'] = x
        drone['location'] = delivery['warehouses'][0]['location']
        drone['inventory'] = []
        drone['turn'] = 0
        pqueue.put((0, drone))
    
    turn = 0
    
    while turn < max_turns:
        while pqueue.queue[0] == turn:
            drone = pqueue.get()
            bestPoints = sys.maxint
            bestWarehouse = delivery['warehouses'][0]
            for warehouse in delivery['warehouses']:
                if eucledianDistance(drone['location'], warehouse['location']) + warehouse['price'][0][0][0] < bestPoints:
                    bestWarehouse = warehouse
                    bestPoints = eucledianDistance(drone['location'], warehouse['location']) + warehouse['price'][0][0][0]
            
        turn = turn + 1
    
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
        order['products'] = {}
        raw_products = to_int_list(lines[index])
        for j in range(0, order['num_items']):
            if raw_products[j] in order['products']:
                order['products'][raw_products[j]] = order['products'][raw_products[j]] + 1
            else:
                order['products'][raw_products[j]] = 1
        index = index + 1
        orders.append(order)
    parsed['num_orders'] = num_orders
    parsed['orders'] = orders

    return parsed

def to_int_list(line):
    return map(int, line.split(" "))

def PriceW(warehouse, orderList, product_weights, payload):
    price = sys.maxint
    correctOrder = orderList[0]
    done = PriorityQueue()
    notDone = PriorityQueue()
    for order in orderList:
        canDo = True
        canDoPartially = False
        priceTemp = 0
        weight = 0
        for product,number in order['products'].items():
            weight = weight + product_weights[product]*number
            if(warehouse['inventory'][product] < number):
                canDo = False
            else:
                canDoPartially = True
                priceTemp = priceTemp + 2  
        if payload >= weight:
            if canDo:
                done.put((priceTemp + eucledianDistance(warehouse['location'], order['location']), order))
            elif canDoPartially:
                notDone.put((priceTemp + eucledianDistance(warehouse['location'], order['location']), order))
    return done, notDone
    
def eucledianDistance(location1, location2):
    return math.hypot(location1[0] - location2[0], location1[1] - location2[1])
    
if __name__ == '__main__':
    main()
