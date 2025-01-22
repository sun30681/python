
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import psutil

def print_system_info():
    # CPU信息
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU信息: {cpu_usage}%")

    # 内存信息
    memory = psutil.virtual_memory()
    print(f"内存信息使用: {memory.percent}%")

    # 磁盘信息
    disk = psutil.disk_usage('/')
    print(f"磁盘使用: {disk.percent}%")

    # 网络信息
    net_io = psutil.net_io_counters()
    print(f"网络上传速度: {net_io.bytes_sent} bytes")
    print(f"网路下载速度: {net_io.bytes_recv} bytes")

print_system_info()