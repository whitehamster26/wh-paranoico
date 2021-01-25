import os
import json

from src import ip_whois
from src import process_info

from src.logger import logger


def show_connections():
    report = {}
    processes = process_info.show_connections()
    print(f"Found {len(processes)} applications that use the connection")
    for p_name, p_connections in processes.items():
        print(f"Checking out {p_name}")
        report[p_name] = []
        for address in p_connections:
            print(f"    Found connection: {address}")
            try:
                report[p_name].append(
                    {address: ip_whois.show_whois(address)}
                )
            except Exception as e:
                logger.error(e)
        if not report[p_name]:
            # May be there's no active connections but app listens a port
            del report[p_name]

    with open('paranoico-report.json', 'w') as file:
        json.dump(report, file, indent=4)

    print(f"Done! The report and execution log are available at {os.getcwd()}")
