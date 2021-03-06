"""
main.py
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


from fastapi import Depends, FastAPI
from src.endpoints import nodes, search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(nodes.router_cmd)
app.include_router(nodes.router_list)
app.include_router(search.router)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
