from detd import StreamConfiguration
from detd import TrafficSpecification
from detd import Interface
from detd import Configuration
from detd import ServiceProxy

from stream import Stream, StreamCollection
import subprocess

class DetdManager:
    stream_collection = StreamCollection()
    proxy = ServiceProxy()
    
    @staticmethod
    def add_stream(stream: Stream):
        try:
            interface = Interface(stream.interface_name)
            stream_conf = StreamConfiguration(stream.addr, stream.vid, stream.pcp, stream.txoffset)
            traffic = TrafficSpecification(stream.interval, stream.size)
            config = Configuration(interface, stream_conf, traffic)
            DetdManager.proxy.add_talker(config)
            return True
        except Exception as e:
            print(e)
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
        
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Command failed: {cmd}")
                print(result.stderr)