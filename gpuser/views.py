import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

import paramiko
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from paramiko.ssh_exception import SSHException

from .models import Server


def execute_command(hostname: str) -> Union[str, None]:
    ssh = paramiko.SSHClient()
    try:
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
        ssh.connect(hostname=hostname, timeout=20)
        stdin, stdout, stderr = ssh.exec_command(
            "join -t, -a 1 -1 2 -2 2 -e NULL -o '1.1,2.1' \
            <(nvidia-smi --query-gpu=index,serial --format=csv,nounits,noheader | sort -t , -b -k2n) \
            <(nvidia-smi --query-compute-apps=pid,gpu_serial --format=csv,nounits,noheader | sort -t , -b -k2n) | sort -t , -b -k1,1n -k2,2n | \
            xargs -I {} bash -c 'row={}; columns=(${row//,/ }); \
            if [ ${columns[1]} != \"NULL\" ]; \
            then echo ${columns[0]},${columns[1]},$(ps -p ${columns[1]} -o user=); \
            else echo ${columns[0]},NULL,NULL; fi'",
            timeout=20,
        )
        output = stdout.read().decode("utf-8")
    except SSHException:
        return None
    except socket.gaierror:
        return None
    finally:
        ssh.close()

    return output


def update_gpu_status():
    servers = Server.objects.all()
    with ThreadPoolExecutor() as executor:
        future_to_server = {
            executor.submit(execute_command, server.name): server for server in servers
        }
        for future in as_completed(future_to_server):
            server = future_to_server[future]
            output = future.result()
            if output is None:
                continue
            with transaction.atomic():
                fetch_time = server.fetchtime_set.create()
                for line in output.splitlines():
                    columns = line.split(",")
                    assert len(columns) == 3
                    fetch_time.gpuinfo_set.create(
                        device_id=columns[0],
                        pid=columns[1] if columns[1] != "NULL" else None,
                        username=columns[2] if columns[2] != "NULL" else None,
                    )


def get_gpu_status(add_extra_info=False):
    servers = Server.objects.all()
    gpu_infos = []
    for server in servers:
        fetch_time = server.fetchtime_set.order_by("-fetch_time").first()
        if fetch_time is None:
            continue
        item = {
            "hostname": server.name,
            "gpu_info": [],
            "fetch_time": fetch_time.fetch_time,
        }
        for gpu in fetch_time.gpuinfo_set.all():
            item["gpu_info"].append(
                {
                    "index": gpu.device_id,
                    "pid": gpu.pid,
                    "user": gpu.username,
                }
            )
        if add_extra_info:
            gpus = set()
            empty_gpus = set()
            for gpu in item["gpu_info"]:
                gpus.add(gpu["index"])
                if gpu["pid"] is None:
                    empty_gpus.add(gpu["index"])
            item["empty_gpus"] = sorted(empty_gpus)
            item["gpus"] = sorted(gpus)
        gpu_infos.append(item)
    return gpu_infos


def update(request: HttpRequest):
    update_gpu_status()
    return HttpResponse("OK")


def get(request: HttpRequest):
    gpu_infos = get_gpu_status()
    return JsonResponse(gpu_infos, safe=False)


def gpu(request: HttpRequest):
    auto_reload = request.GET.get("auto_reload", "true") == "true"
    gpu_infos = get_gpu_status(add_extra_info=True)
    return render(
        request,
        "gpu_status.html",
        context={"result": gpu_infos, "auto_reload": auto_reload},
    )
