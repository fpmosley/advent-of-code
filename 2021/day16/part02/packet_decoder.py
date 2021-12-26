#!/usr/bin/env python

'''
Advent of Code 2021 - Day 16: Packet Decoder (Part 2)
https://adventofcode.com/2021/day/16
'''

import math
from enum import Enum


PACKET_HEADER_SIZE = 6
LENGTH_TYPE_ID_SIZE = 1
LENGTH_TYPE_ID_0_SIZE = 15
LENGTH_TYPE_ID_1_SIZE = 11


class TYPE(Enum):
    LITERAL = 4
    TOTAL_LENGTH = 0
    NUM_SUBS = 1


def hex_to_binary(hex_str: str) -> str:
    bin_list = [str(bin(int(char, base=16)))[2:].zfill(4) for char in hex_str]
    return ''.join(bin_list)


def binary_to_decimal(bin_str: str) -> int:
    try:
        return int(bin_str, 2)
    except ValueError as e:
        print(e)


def packet_header(message: str):
    return binary_to_decimal(message[:3]), binary_to_decimal(message[3:6]), message[6:]


def literal_value_packet(packet: str) -> int:
    n = 5  # Length of bit values
    split_bits = [packet[index: index + n]
                  for index in range(0, len(packet), n)]
    bin_str = ''
    length = 0
    for bits in split_bits:
        length += len(bits)
        bin_str = bin_str + bits[1:]
        if bits[0] == '0':
            break

    return {
        'value': binary_to_decimal(bin_str),
        'length': length + PACKET_HEADER_SIZE,
    }


def int_list_to_string_list(values) -> list:
    return [str(x) for x in values]


def sum_operation(values: list) -> int:
    total = sum(values)
    strings = int_list_to_string_list(values)
    print(f"\tSum of {' + '.join(strings)} = {total}")
    return total


def prod_operation(values: list) -> int:
    product = math.prod(values)
    strings = int_list_to_string_list(values)
    print(f"\tProduct of {' x '.join(strings)} = {product}")
    return product


def min_operation(values: list) -> int:
    minimum = min(values)
    strings = int_list_to_string_list(values)
    print(f"\tThe minimum value of {', '.join(strings)} = {minimum}")
    return minimum


def max_operation(values: list) -> int:
    maximum = max(values)
    strings = int_list_to_string_list(values)
    print(f"\tThe maximum value of {', '.join(strings)} = {maximum}")
    return maximum


def greater_than_operation(values: list) -> int:
    if len(values) != 2:
        return 0

    result = 1 if values[0] > values[1] else 0

    print(f"\tThe value of {values[0]} is greater than {values[1]}: {result}")

    return result


def less_than_operation(values: list) -> int:
    if len(values) != 2:
        return 0

    result = 1 if values[0] < values[1] else 0

    print(f"\tThe value of {values[0]} is less than {values[1]}: {result}")

    return result


def equal_to_operation(values: list) -> int:
    if len(values) != 2:
        return 0

    result = 1 if values[0] == values[1] else 0

    print(f"\tThe value of {values[0]} is equal to {values[1]}: {result}")

    return result


def operation(type_id: int, values: list) -> int:

    switcher = {
        0: lambda: sum_operation(values),
        1: lambda: prod_operation(values),
        2: lambda: min_operation(values),
        3: lambda: max_operation(values),
        5: lambda: greater_than_operation(values),
        6: lambda: less_than_operation(values),
        7: lambda: equal_to_operation(values),
    }

    func = switcher.get(type_id, lambda: 'Invalid')

    return func()


def operator_packet(type_id: int, packet):
    sub_packet_versions = 0
    packet_size = PACKET_HEADER_SIZE + LENGTH_TYPE_ID_SIZE

    length_type_id = binary_to_decimal(
        packet[0])  # Bit 1 is the length type ID
    if length_type_id == TYPE.TOTAL_LENGTH.value:
        packet_size += LENGTH_TYPE_ID_0_SIZE
        number_of_bits_in_subs = binary_to_decimal(packet[1:16])  # 15-bits
        limit = number_of_bits_in_subs
        index = 16  # Index of where to start processing sub packets
    else:
        packet_size += LENGTH_TYPE_ID_1_SIZE
        number_of_sub_packets = binary_to_decimal(packet[1:12])  # 11-bits
        limit = number_of_sub_packets
        index = 12  # Index of where to start processing sub packets

    counter = 0
    sub_packet_count = 0
    processed_sub_packet_bits = 0
    values = []
    while counter < limit:
        result = decode(packet[index:])
        sub_packet_count += 1
        values.append(result['value'])
        processed_sub_packet_bits += result['length']
        sub_packet_versions += result['version']
        index += result['length']
        counter = processed_sub_packet_bits if length_type_id == TYPE.TOTAL_LENGTH.value else sub_packet_count

    return {
        'length': packet_size + processed_sub_packet_bits,
        'version': sub_packet_versions,
        'type': type_id,
        'value': operation(type_id, values=values)
    }


def decode(message):
    version, type_id, packet = packet_header(message)

    if type_id == TYPE.LITERAL.value:
        result = literal_value_packet(packet)
        result['version'] = version
    else:
        result = operator_packet(type_id, packet)
        result['version'] += version

    return result


def main():
    filename = input("What is the input file name? ")
    try:
        with open(filename, "r") as file:

            # Read the messages
            hex_messages = file.read().splitlines()
            for hex_message in hex_messages:
                binary_message = hex_to_binary(hex_message)
                print(f"\nDecoding message: {hex_message}")
                result = decode(binary_message)
                print(
                    f"Message: {hex_message} -> sum of all version numbers in packets: {result['version']}")
    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
