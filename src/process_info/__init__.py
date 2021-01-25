import psutil

from collections import namedtuple

from src.logger import logger
from src.process_info.exceptions import GettingProcInfoException

Process = namedtuple('Process', ['name', 'connections'])


def _show_running_processes() -> list:
    pids = psutil.pids()
    return pids


def _get_process_info(pid: int) -> Process:

    process = psutil.Process(pid)
    try:
        return Process(process.name(), process.connections())

    except psutil.AccessDenied:
        raise GettingProcInfoException(
         f"Can't get info about process ID {pid}. Access Denied.")

    except psutil.NoSuchProcess:
        raise GettingProcInfoException(f"Process {pid} no longer exists")


def show_connections() -> dict:
    processes = _show_running_processes()
    connections = {}

    for process in processes:
        try:
            p_info = _get_process_info(process)

            if p_info and p_info.connections:
                ip_list = [
                    address.raddr.ip for address in p_info.connections
                    if address.raddr]
                ip_list = list(set(ip_list))
                connections[p_info.name] = ip_list

        except GettingProcInfoException as e:
            logger.warning(e)

    return connections
