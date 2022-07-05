from fastapi import APIRouter, Query
from ..models.nodes import Node, search
# from ..models.cmdList import CmdDb, CmdItem
from typing import Union, List


router = APIRouter(
    prefix='/search',
    tags=['Search'],
)

SearchList = []


@router.get("/")
async def search_by_name(name: Union[List[str], None] = Query()):
    global SearchList
    SearchList.clear()
    search(name, SearchList)

    ret = []
    for idx, node_name in enumerate(SearchList):
        cmd_info = getattr(SearchList[idx], 'info_for_search')
        ret.append(cmd_info())
    return ret


@router.get('/kill/')
async def kill_from_search(pid: Union[List[str], None] = Query()):
    global SearchList
    for idx, node in enumerate(SearchList):
        if(str(node.pid) in pid):
            kill = getattr(SearchList[idx], 'kill')
            kill()
            del SearchList[idx]
            del node
    ret = []
    for idx, node_name in enumerate(SearchList):
        cmd_info = getattr(SearchList[idx], 'info_for_search')
        ret.append(cmd_info())
    return ret
