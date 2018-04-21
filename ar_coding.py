# arithmetic coding for text implementation
# Université de Fribourg, Suisse
# AUTHOR: Noé Zufferey - noe.zufferey@gmail.com
# CREATION: april 2018 
# USAGE: python3 ar_coding.py '<string to encode>'
# OUTPUT: an interval of floating value and a binary code

import sys
from decimal import *

"""this function compute the distribution of each character in the text. The algorithm assume that each character is genrated independently"""
def compute_ditribution(data):
    dist = {}
    nbr_char = 0
    for char in data:
        nbr_char += 1
        if char in dist:
            dist[char] += 1
        else:
            dist[char] = 1
    getcontext().prec = 4
    for nbr in dist:
        dist[nbr] = Decimal(dist[nbr]) / Decimal(nbr_char)
    getcontext().prec = 100000
    return dist

def compute_endpoint(dist, key, lower_bound):
    endpoint = lower_bound
    for tup in dist:
        endpoint += tup[1]
        if tup[0] == key:
            break
    return endpoint

def compress(data):
    comp_data = [Decimal('0'), Decimal('1')]
    dist = compute_ditribution(data)
    for char in data:
        interval = comp_data[1] - comp_data[0]
        new_dist = []
        for key in dist:
            new_dist.append((key, dist[key] * interval))
        new_dist = sorted(new_dist)
        comp_data[1] = compute_endpoint(new_dist, char, comp_data[0])
        comp_data[0] = compute_endpoint(new_dist, char, comp_data[0]) - (dist[char] * interval)
    return comp_data

def to_bits(data):
    result = ''
    nbr = Decimal('0')
    while nbr <= data[0]:
        temp = Decimal('0')
        i = -1
        for n in result + '1':
            if n == '1':
                temp += Decimal(2 ** i)
            i -= 1
        if temp < data[1]:
            result += '1'
            nbr += Decimal(2 ** (len(result) * -1))
        else:
            result += '0'
    return result

if __name__ == '__main__':
    data = sys.argv[1]
    getcontext().prec = 100000
    comp_data = compress(data)
    print(comp_data)
    print(to_bits(comp_data))
