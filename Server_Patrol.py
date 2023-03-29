#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2023/3/28 18:20
# file: 巡检脚本.py
# author: qinxi
# email: 1023495336@qq.com
import os
import subprocess
import re
import datetime


# 获取 CPU 使用率
def get_cpu_usage():
    cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'"
    output = subprocess.check_output(cmd, shell=True)
    return float(output)


# 获取内存使用率
def get_memory_usage():
    cmd = "free | awk '/Mem/{printf(\"%d\", ($2-$7)/$2*100)}'"
    output = subprocess.check_output(cmd, shell=True)
    return float(output)


# 获取硬盘使用率
def get_disk_usage():
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d\", $5}'"
    output = subprocess.check_output(cmd, shell=True)
    return float(output)


# 获取危险进程
def get_dangerous_processes():
    cmd = "ps -eo pid,user,%cpu,%mem,command --sort=-%cpu | head -n 11"
    output = subprocess.check_output(cmd, shell=True)
    return output


# 获取登录日志
def get_login_log():
    cmd = "cat /var/log/auth.log | grep 'Accepted password' | tail -n 10"
    output = subprocess.check_output(cmd, shell=True)
    return output


if __name__ == "__main__":
    # 获取当前时间
    now = datetime.datetime.now().strftime('%Y-%m-%d')

    # 创建以当日时间为名的文件夹
    if not os.path.exists(now):
        os.mkdir(now)

    # 设置保存文件路径
    file_path = os.path.join(now, "inspection_result.txt")

    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    dangerous_processes = get_dangerous_processes()
    login_log = get_login_log()

    # 打印巡检结果
    with open(file_path, 'w') as f:
        f.write("CPU 使用率: {}%\n".format(cpu_usage))
        f.write("内存使用率: {}%\n".format(memory_usage))
        f.write("硬盘使用率: {}%\n".format(disk_usage))
        f.write("危险进程:\n{}\n".format(dangerous_processes))
        f.write("登录日志:\n{}\n".format(login_log))

        # 进行优化建议
        if cpu_usage > 80:
            f.write("CPU 使用率过高，建议检查是否存在大量 CPU 占用的进程。\n")
        if memory_usage > 80:
            f.write("内存使用率过高，建议检查是否存在内存泄漏的进程。\n")
        if disk_usage > 80:
            f.write("硬盘使用率过高，建议清理不必要的文件和日志。\n")

    print("巡检结果已保存到文件：{}".format(file_path))
