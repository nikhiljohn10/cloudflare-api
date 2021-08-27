#!/usr/bin/env python3

import os
import json
import pathlib
from typing import Dict, List, Optional, Union
from cloudflare import Cloudflare


class Worker:
    def __init__(self, cf: Cloudflare) -> None:
        self.cf = cf
        self.base_url = f"{self.cf.base_url}/accounts/{self.cf.account_id}/workers/scripts"

    # def list(self, detailed: bool = False) -> List:
    #     workers = self.cf.get(self.base_url)
    #     if detailed:
    #         wlist = [
    #             {
    #                 worker["id"]: [
    #                     {item["script"]: item["pattern"]} for item in worker["routes"]
    #                 ]
    #             }
    #             if worker["routes"] is not None
    #             else {worker["id"]: "No routes"}
    #             for worker in workers
    #         ]
    #         wlist = sorted(wlist, key=lambda worker: worker.keys())
    #     else:
    #         wlist = [worker["id"] for worker in workers]
    #     return wlist

    def download(self, name: str, directory: str = "./workers") -> None:
        data = self.cf.get(f"{self.base_url}/{name}")
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        with open(f"{directory}/{name}.js", "w") as fd:
            fd.write(data)
        print(f"Worker script written in to {directory}/{name}.js")

    def upload(self, name: str, file: str, bindings: Optional[Union[List[Dict[str, str]], Dict[str, str]]] = None) -> None:
        if bindings is None:
            with open(file, 'r') as f:
                data = f.read()
            done = self.cf.put(f"{self.base_url}/{name}", data=data)
        else:
            bindings = [bindings] if isinstance(bindings, dict) else bindings
            metadata = {
                'body_part': 'script',
                'bindings': [
                    {
                        'name': binding['name'].upper(),
                        'type': 'kv_namespace',
                        'namespace_id': binding['id']
                    }
                    for binding in bindings
                ]
            }
            miltipart_data = {
                'metadata': (
                    None,
                    json.dumps(metadata),
                    'application/json'
                ),
                'script': (
                    os.path.basename(file),
                    open(file, 'rb'),
                    'application/javascript'
                )
            }
            done = self.cf.put(f"{self.base_url}/{name}", files=miltipart_data)
        if done:
            print(f"Worker script {name} is uploaded to cloudflare")
        else:
            print(f"Unkown error while uploading worker script {name}")

    def delete(self, name: str) -> None:
        if self.cf.delete(f"{self.base_url}/{name}"):
            print(f"Worker script {name} is deleted from cloudflare")
        else:
            print(f"Unkown error while deleting worker script {name}")
