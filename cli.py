from common import Check
from stream import Stream, StreamCollection
from detdmgmt import DetdManager

import traceback
import os

class CLI:

    def __init__(self) -> None:
        pass

    def run_forever(self):
        while True:
            try:
                line = input(">>")
                cmd = self.parse(line)
                cmd.execute()
            except Exception as e:
                traceback.print_exc()
                continue

    def parse(self, string: str):
        tokens = string.split(" ")
        params = {}
        cmd = tokens[0]
        i = 0
        while i < len(tokens):
            if tokens[i].startswith("--"):
                key = tokens[i][2:]
                try:    
                    value = tokens[i + 1]
                except IndexError:
                    value = True
                params[key] = value
                i += 2
            else:
                i += 1
        return Command(cmd, params)
        
        
class Command:
    valid_commands = ["add", "remove", "list", "clear", "help", "exit", "rm", "reload", "load"]
    
    def __init__(self, cmd: str, params: dict) -> None:
        self.stream_collection = StreamCollection()
        if cmd not in self.valid_commands:
            raise ValueError("Invalid command")
        self.cmd = cmd
        self.params = {}
        if cmd == "add":
            if not Check.is_interface(params.get("if")):
                raise ValueError("Invalid interface")
            else:
                self.params["if"] = params.get("if")
            
            if not Check.is_valid_vlan_id(int(params.get("vid"))):
                raise ValueError("Invalid VLAN ID")
            else:
                self.params["vid"] = int(params.get("vid"))
            
            if not Check.is_valid_pcp(int(params.get("pcp"))):
                raise ValueError("Invalid PCP")
            else:
                self.params["pcp"] = int(params.get("pcp"))
            
            if not Check.is_mac_address(params.get("addr")):
                raise ValueError("Invalid MAC address")
            else:
                self.params["addr"] = params.get("addr")
            
            if not Check.is_natural(int(params.get("size"))):
                raise ValueError("Invalid size")
            else:
                self.params["size"] = int(params.get("size"))
            
            if not Check.is_natural(int(params.get("offset"))):
                raise ValueError("Invalid offset")
            else:
                self.params["offset"] = int(params.get("offset"))
                
            if not Check.is_natural(int(params.get("interval"))):
                raise ValueError("Invalid interval")
            else:
                self.params["interval"] = int(params.get("interval"))
        elif cmd == "remove" or cmd == "rm":
            if not Check.is_interface(params.get("if")):
                raise ValueError("Invalid interface")
            else:
                self.params["if"] = params.get("if")
            
            if not Check.is_natural(int(params.get("offset"))):
                raise ValueError("Invalid offset")
            else:
                self.params["offset"] = int(params.get("offset"))
        elif cmd == "list":
            pass
        elif cmd == "reload":
            pass
        elif cmd == "exit":
            self.params["nosave"] = params.get("nosave")
        elif cmd == "clear":
            pass
        elif cmd == "help":
            pass
        elif cmd == "load":
            defalut_file = "streams.txt"
            file = params.get("file")
            if file is None:
                file = defalut_file
            if not file.startswith("/"):
                file = f"{os.getcwd()}/{file}"
            if not Check.is_valid_file(file):
                raise ValueError("Invalid file")
            self.params["file"] = file
            
        else:
            print("Unrecognized command")
        

    def execute(self):
        if self.cmd == "add":
            stream = Stream(self.params.get("if"),  self.params.get("offset"), self.params.get("interval"), self.params.get("size"), self.params.get("addr"), self.params.get("vid"), self.params.get("pcp"))
            if(DetdManager.add_stream(stream)):
                self.stream_collection.add(stream)
            else:
                print("Failed to add stream")
        
        if self.cmd == "remove" or self.cmd == "rm":
            DetdManager.erase_configuration()
            stream = Stream(self.params.get("if"), self.params.get("offset"))
            self.stream_collection.remove(stream)
            DetdManager.remove_stream(stream)
        
        if self.cmd == "list":
            self.stream_collection.list()
            
        if self.cmd == "exit":
            if self.params.get("nosave") is not True:
                self.stream_collection.save()
            exit()
            
        if self.cmd == "reload":
            DetdManager.reload_configuration()
        
        if self.cmd == "clear":
            print("Are you sure you want to clear all streams? (y/n) ")
            inp = input()
            if inp == "y":
                DetdManager.erase_configuration()
                self.stream_collection.clear()
            else:
                print("Aborted")
            
        if self.cmd == "load":
            self.stream_collection.load(self.params.get("file"))
        
        if self.cmd == "help":
            print("Available commands: add, remove, list, clear, help, exit, reload")
            print("add --if <interface> --vid <vid> --pcp <pcp> --addr <address> --size <size> --offset <offset> --interval <interval>")
            print("remove --if <interface> --offset <offset>")
            print("list")
            print("clear")
            print("help")
            print("exit --nosave")
            print("reload")
            print("load --file <filename>")
            