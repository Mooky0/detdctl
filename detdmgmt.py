from detd import StreamConfiguration
from detd import TrafficSpecification
from detd import Interface
from detd import Configuration
from detd import ServiceProxy

from stream import Stream, StreamCollection
import subprocess
import traceback

class DetdManager:
    stream_collection = StreamCollection()
    proxy = ServiceProxy()
    
    @staticmethod
    def add_stream(stream: Stream):
        print(f"Adding stream: Interface: {stream.interface_name}, Offset: {stream.txoffset}")
        try:
            interface = Interface(stream.interface_name)
            print(f"Interface set up")
            stream_conf = StreamConfiguration(stream.addr, stream.vid, stream.pcp, stream.txoffset)
            print(f"Stream Configuration done")
            traffic = TrafficSpecification(stream.interval, stream.size)
            print(f"Traffic Specification done")
            config = Configuration(interface, stream_conf, traffic)
            print(f"Configuration done")
            DetdManager.proxy.add_talker(config)
            print(f"Talker added")
            return True
        except Exception as e:
            traceback.print_exc()
            return False
            
    
    @staticmethod
    def remove_stream(stream: Stream):
        DetdManager.reload_configuration()
    
    @staticmethod
    def reload_configuration():
        # stop detd and delete configuration, then restart detd
        DetdManager.erase_configuration()
        streams = DetdManager.stream_collection.get_streams()
        for stream in streams:
            DetdManager.add_stream(stream)
            
    @staticmethod
    def erase_configuration():
        commands = ["sudo systemctl stop detd",
                    "sudo rmdir /var/tmp/detd/"]
        
        interfaces_vid = DetdManager.stream_collection.get_interfaces_with_vid()
        interfaces = [i[0] for i in interfaces_vid]
        interfaces = list(set(interfaces))
        for interface in interfaces:
            commands.append(f"sudo tc qdisc del dev {interface} root")
            
        for interface, vid in interfaces_vid:
            commands.append(f"sudo ip link delete {interface}.{vid}")
            commands.append(f"sudo ip link del link {interface} name {interface}.{vid} type vlan")

        commands.append("sudo systemctl force-reload detd")
        commands.append("sudo systemctl start detd")
        commands.append("detd")
        commands.append("sudo systemctl status detd")
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Command failed:")
                print(result.stderr)
            else:
                print(f"Command executed successfully: ")
                print(result.stdout)