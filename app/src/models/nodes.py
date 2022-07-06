"""
nodes.py
Copyright (C) 2022  Ahmet Fatih Akcan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import psutil
import os
import subprocess
import shlex
from .cmdList import CmdDb, CmdItem
from pathlib import Path


class Node:
    def __init__(self, item: CmdItem, process=None, pid=None, check_flag=True):
        self.is_running = False
        self.name = item.name
        self.exec = item.exec
        self.cmd = item.cmd
        self.process = process
        self.pid = pid
        self.cwd = item.cwd if item.cwd and item.cwd!= '' else Path.home()
        self.db = CmdDb()
        if check_flag:
            self.check_if_exist()

    def check_if_exist(self):
        cmd_list = self.db.read_cmd()
        for proc in psutil.process_iter():
            if proc.as_dict(attrs=['cmdline'])['cmdline'] == shlex.split(self.cmd):
                self.pid = proc.as_dict(attrs=['pid'])['pid']
                self.process = psutil.Process(self.pid)
                try:
                    self.cwd = proc.cwd()
                except psutil.AccessDenied:
                    self.cwd = None
                self.is_running = True
                return

        self.is_running = False
        self.pid = None
        self.process = None

    def start(self):
        self.check_if_exist()
        if not self.process:
            self.process = psutil.Popen(shlex.split(self.exec), stdin=subprocess.PIPE,
                                        stdout=subprocess.DEVNULL, cwd=self.cwd, text=True,  close_fds=True, preexec_fn=os.setpgrp, shell=False)
            while not self.pid:
                self.pid = self.process.pid
                print(self.process.pid)
            self.is_running = True

    def kill(self):
        self.check_if_exist()
        if self.process:
            self.process.terminate()
            self.is_running = False
            self.process = None
            self.pid = None

    def info(self):
        ret_info = {'name': self.name,
                    'status': self.is_running,
                    'pid': None,
                    'cwd': self.cwd}
        if self.is_running:
            ret_info.update({'pid': self.pid})
        return ret_info
    
    def info_for_search(self):
        ret_info = {'name':self.name, 
                    'cmd':self.cmd,
                    'pid':self.pid,
                    'cwd':self.cwd}
        return ret_info


def search(name_list, search_list):
    for proc in psutil.process_iter():
        if len(proc.cmdline()):
            if(proc.name() in name_list):
                item = CmdItem
                item.name = proc.name()
                item.exec = " ".join(proc.cmdline())
                item.cmd = item.exec
                search_list.append(
                    Node(item=item, process=proc, pid=proc.pid, check_flag=False))
    return