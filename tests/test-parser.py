#!/usr/bin/env python3

from sys import argv
from collections import defaultdict

if len(argv) < 2:
    print("Usage:", argv[0], "INPUT [INPUT2 ...]")
    exit(1)

SEPERATOR = ";"

PAGES = [
    "many-images",
    "many-js",
    "simple-tiny",
    "simple-small",
    "simple-medium",
    "simple-large",
    "multiple-small",
    "multiple-large"
]

SERVERS = [
    "quic",
    "http1",
    "http2"
]

total_result = ""

for file in argv[1:]:
    results = []

    with open(file) as f:
        i = 0
        test_run = {}
        for server in SERVERS:
            test_run[server] = {}
        for line in f:
            line = line.strip()
            server = "quic"
            if "7000" in line:
                server = "http2"
            elif "8000" in line:
                server = "http1"

            page = line.split("/")[-1].split(".html")[0]
            result = line.split(" - ")[1]

            test_run[server][page] = result
            i += 1
            if i == len(PAGES) * len(SERVERS):
                i = 0
                results.append(test_run)
                test_run = {}
                for server in SERVERS:
                    test_run[server] = {}

    name = "".join(file.split(".")[:-1])
    with open(name + ".csv", "w") as f:
        print(SEPERATOR + SEPERATOR.join(PAGES), file=f)

        avg = defaultdict(lambda: defaultdict(lambda: 0))
        avg_percent = defaultdict(lambda: defaultdict(lambda: 0.0))

        for run in results:
            for server in SERVERS:
                line = server
                for page in PAGES:
                    line += SEPERATOR + run[server][page]
                print(line, file=f)
            for page in PAGES:
                value_quic = int(run["quic"][page])
                for server in ("http1", "http2"):
                    value_server = int(run[server][page])
                    avg[server][page] += (value_server - value_quic)
                    avg_percent[server][page] += (value_server - value_quic) / value_server
            print(file=f)

        print(file=f)
        print("Average", file=f)
        print(SEPERATOR + SEPERATOR.join(PAGES), file=f)

        total_result += name + "\n"

        for server in ("http1", "http2"):
            line = server
            for page in PAGES:
                line += SEPERATOR + str(round(avg[server][page] / len(results)))
            print(line, file=f)
            total_result += line + "\n"

        print("Average percent", file=f)
        total_result += "Average percent\n"
        for server in ("http1", "http2"):
            line = server
            for page in PAGES:
                line += SEPERATOR + str(round(100 * avg_percent[server][page] / len(results))) + "%"
            print(line, file=f)
            total_result += line + "\n"
        
        total_result += "\n"

with open("total.csv", "w") as f:
    f.write(total_result)
