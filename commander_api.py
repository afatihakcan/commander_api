from fastapi import FastAPI, Query
import rospy
import os
import re
from typing import List, Union
import subprocess
import psutil
import shlex
import json



def check_cmd_list():
    global cmd_list
    cmd_file = open('cmd_list.json', 'r')
    cmd_list = json.loads(cmd_file.read())
    print(cmd_list)


class Node:
    def __init__(self, name):
        self.is_running = False
        self.name = name
        self.process = None
        self.pid = None
        self.check_if_exist()
        
    def check_if_exist(self):
        for proc in psutil.process_iter():
            if proc.as_dict(attrs=['cmdline'])['cmdline']==shlex.split(cmd_list[f'{self.name}']['cmd']):
                cmd_list['cam']['pid']=proc.as_dict(attrs=['pid'])
                self.pid = proc.as_dict(attrs=['pid'])['pid']
                self.process = psutil.Process(self.pid)
                self.is_running=True
                break
                

    def start(self):
        self.check_if_exist()
        if not self.process:
            self.process = psutil.Popen(shlex.split(cmd_list[f'{self.name}']['exec']), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True,  close_fds=True, preexec_fn=os.setpgrp, shell=False)
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


app = FastAPI()
def node_get_builder(n):
    @app.get(f"/{n}/")
    async def f(q:Union[str,None] = Query(default=None)):
        ret = {f'{n}':{'running':globals()[f'{n}'].is_running,
                               'name':globals()[f'{n}'].name}}
        if q:
            if q=='start':
                if globals()[f'{n}'].is_running:
                    ret[f'{n}'].update({f'{q}':'failed! (already running)'})
                else:
                    print(f"started {n}")
                    globals()[f'{n}'].start()
                    ret[f'{n}'].update({f'{q}':'successful'})
            elif q=='kill':
                if globals()[f'{n}'].is_running:
            
                    print(f"killed {n}")
                    globals()[f'{n}'].kill()
                    ret[f'{n}'].update({f'{q}':'successful'})
                else:
                    ret[f'{n}'].update({f'{q}':'failed! (not yet started)'})

        if globals()[f'{n}'].pid != None:
            ret[f'{n}'].update({'pid':globals()[f'{n}'].pid})
        
        return ret
    return f

@app.get('/')
async def all_nodes_get():
    check_cmd_list()
    ret = dict()
    for n in cmd_list.keys():
        ret.update({f'{n}':{
            'running':globals()[f'{n}'].is_running,
            'name':globals()[f'{n}'].name,
        }})
        if globals()[f'{n}'].pid != None:
            ret[f'{n}'].update({'pid':globals()[f'{n}'].pid})   
            
    
    return ret
                 

check_cmd_list()
get_list = []
for n in cmd_list.keys():
    globals()[f'{n}'] = Node(n)
    get_list.append(node_get_builder(n))