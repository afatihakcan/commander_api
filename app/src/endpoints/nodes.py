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


from fastapi import APIRouter, Query, HTTPException
from typing import List, Union
from ..models.nodes import Node
from ..models.cmdList import CmdDb, CmdItem

router_cmd = APIRouter(
    prefix='/cmd',
    tags=['Cmd'],
)

router_list = APIRouter(
    prefix='/list',
    tags=['List'],
)


NodeList = {}
CmdList = CmdDb()
CmdList.read_cmd()


def check_if_running():
    for node_name in NodeList:
        cmd_check = getattr(NodeList[f'{node_name}'], 'check_if_exist')
        cmd_check()


def create_node_list():
    for cmd_name in CmdList.cmd_list:
        new_item = CmdItem
        new_item.name = cmd_name
        new_item.exec = CmdList.cmd_list[f'{cmd_name}']['exec']
        new_item.cmd = CmdList.cmd_list[f'{cmd_name}']['cmd']
        new_item.cwd = CmdList.cmd_list[f'{cmd_name}'].get('cwd')
        NodeList.update({f'{cmd_name}':Node(new_item)})
        
create_node_list()

@router_cmd.get("/")
async def get_all_nodes():
    check_if_running()
    #ret = dict()
    ret = []
    for idx, node_name in enumerate(NodeList ):
        cmd_info = getattr(NodeList[f'{node_name}'], 'info')
        #ret.update({f'{idx+1}':cmd_info()})
        ret.append(cmd_info())
    return ret
        
@router_cmd.get("/{node}/")
async def node_controller(node:str, action:Union[str,None]=None):
    check_if_running()
    try:
        if action==None:
            cmd_info = getattr(NodeList[f'{node}'], 'info')
            ret = cmd_info()
            return ret
        else:
            if(NodeList[f'{node}'].is_running and action=='start'):
                postfix = 'already running!'
            elif(not NodeList[f'{node}'].is_running and action=='kill'):
                postfix = 'not yet started!' 
            else:
                # postfix = 'successful!' 
                if action=='start':
                    postfix = 'started!'
                elif action=='kill':
                    postfix = 'killed!'
                else:
                    # raise HTTPException(status_code=404, detail="there is no action like this")
                    raise Exception('no such action')
                
            cmd_action = getattr(NodeList[f'{node}'], f'{action}')
            cmd_action()
            cmd_info = getattr(NodeList[f'{node}'], 'info')
            ret = cmd_info()
            ret.update({'response':postfix})
            return ret
    except FileNotFoundError:
        cmd_info = getattr(NodeList[f'{node}'], 'info')
        ret = cmd_info()
        ret.update({'response':'Not Found!'})
        return ret
    except Exception as e:
        raise HTTPException(status_code=404, detail="Node or action doesn't exist!")
    

@router_list.get('/')
async def get_list():
    return CmdList.read_cmd()

# @router_list.post('/add/')
# async def add_to_list(item:CmdItem):
#     CmdList.add_cmd({f'{item.name}':{'exec':item.exec, 'cmd':item.cmd}})
#     NodeList.update({f'{item.name}':Node(item)})

#     return {'status':'successful!', 
#             'added':item.dict()}
    
# @router_list.post('/add_multiple/')
# async def add_to_list_multiple(new_items:List[CmdItem]):
#     for item in new_items:
#         CmdList.add_cmd({f'{item.name}':{'exec':item.exec, 'cmd':item.cmd}})
#         NodeList.update({f'{item.name}':Node(item)})
#     return {'status':'successful!', 
#             'added':new_items.dict()}

    
@router_list.post('/update/')
async def update_list(new_list:List[CmdItem]):
    new_dict = dict()
    for new_item in new_list:
        new_dict.update({f'{new_item.name}':{'exec':new_item.exec, 'cmd':new_item.cmd, 'cwd':new_item.cwd if new_item.cwd!='' else None}})
    
    CmdList.write_all(new_dict)
    
    NodeList.clear()
    create_node_list()
    # return {'status':'successful!', 'cmdList':CmdList.cmd_list}
    return CmdList.cmd_list
