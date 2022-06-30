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


class Node:
    def __init__(self, item:CmdItem):
        self.is_running = False
        self.name = item.name
        self.exec = item.exec
        self.cmd = item.cmd
        self.process = None
        self.pid = None
        self.db = CmdDb()
        self.check_if_exist()
        
    def check_if_exist(self):
        cmd_list = self.db.read_cmd()
        for proc in psutil.process_iter():
            if proc.as_dict(attrs=['cmdline'])['cmdline']==shlex.split(self.cmd):
                self.pid = proc.as_dict(attrs=['pid'])['pid']
                self.process = psutil.Process(self.pid)
                self.is_running=True
                return
            
        self.is_running = False
        self.pid = None
        self.process = None
                
    def start(self):
        self.check_if_exist()
        if not self.process:
            self.process = psutil.Popen(shlex.split(self.exec), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True,  close_fds=True, preexec_fn=os.setpgrp, shell=False)
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
        ret_info = {'name':self.name, 
                'status':self.is_running,
                'pid':None}
        if self.is_running:
            ret_info.update({'pid':self.pid})
        return ret_info