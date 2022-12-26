#!/usr/bin/env python

'''
Advent of Code 2022 - Day 16: Proboscidea Volcanium (Part 1)
https://adventofcode.com/2022/day/16
'''
import time
import re

# Initialize globals
graph = {}
flow = {}
flow_codes = {}
shortest_path = {}


def find_shortest_path(current: str, state: int, remaining_time: int, pressure_flow: int, flow_per_path: dict) -> dict:
    flow_per_path[state] = max(flow_per_path.get(state, 0), pressure_flow)

    for dest in flow:
        time_after_dest = remaining_time - shortest_path[current][dest] - 1
        if flow_codes[dest] & state or time_after_dest <= 0:
            continue

        find_shortest_path(current=dest, remaining_time=time_after_dest, state=state |
                           flow_codes[dest], pressure_flow=pressure_flow + time_after_dest * flow[dest], flow_per_path=flow_per_path)

    return flow_per_path


def main():

    global shortest_path

    filename = input("What is the input file name? ")

    try:

        with open(filename, "r") as file:

            start = time.time()

            flow_count = 0

            # Read the scan output
            for line in file:
                line = line.strip()

                match = re.findall(r"[A-Z][A-Z]|\d+", line)
                valve = match[0]
                flow_rate = int(match[1])
                tunnel_valves = [x for x in match[2:]]
                graph[valve] = tunnel_valves
                if flow_rate != 0:
                    flow[valve] = flow_rate

                    # Encode the valves with a flow rate to use in a bitmap to maintain state
                    flow_codes[valve] = 1 << flow_count

                    flow_count += 1

            shortest_path = {x: {y: 1 if y in graph[x] else float(
                "+inf") for y in graph} for x in graph}
            for mid in shortest_path:
                for dst in shortest_path:
                    for src in shortest_path:
                        shortest_path[src][dst] = min(
                            shortest_path[src][dst], shortest_path[src][mid] + shortest_path[mid][dst])

            flows_per_path = find_shortest_path(
                current='AA', state=0, remaining_time=30, pressure_flow=0, flow_per_path={})
            print(
                f"The most pressure that can be released in 30 minutes: {max(flows_per_path.values())}")

        end = time.time()
        print(f"Execution time in seconds: {end - start}\n")

    except FileNotFoundError:
        print(f"No such file or directory: '{filename}'")


if __name__ == "__main__":
    main()
