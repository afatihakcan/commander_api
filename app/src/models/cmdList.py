"""
cmdList.py
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


from pydantic import BaseModel
import json
from typing import Union


class CmdItem(BaseModel):
    name: str
    exec:str
    cmd: str
    cwd: str = None
    
class CmdDb:
    def __init__(self):
        self.cmd_list = None
        self.read_cmd()
    
    def read_cmd(self):
        f = open(f'cmd_list.json', 'r')
        self.cmd_list = json.loads(f.read())
        f.close()
        return self.cmd_list
    
    def write(self, new_cmd):
        f = open('cmd_list.json', 'w')
        f.write(json.dumps(new_cmd))
        f.close()
        
    def write_all(self, new_list):
        self.cmd_list = new_list
        self.write(self.cmd_list)
        
    def add_cmd(self, new_line):
        self.cmd_list.update(new_line)
        self.write(self.cmd_list)
