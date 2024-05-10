class Stream:
    def __init__(self, interface_name: str, txoffset: int, interval: int = None, size: int = None, addr: str = None, vid: int = None, pcp: int = None) -> None:
        self.interface_name = interface_name
        self.interval = interval
        self.size = size
        self.txoffset = txoffset
        self.addr = addr
        self.vid = vid
        self.pcp = pcp
        

class StreamCollection:
    _instance = None
    _collection = []

    def __new__(cls):
        if cls._instance is None:
            _collection = []
            cls._instance = super().__new__(cls)
        return cls._instance

    def add(self, stream: Stream):
        self._collection.append(stream)
        
    def remove(self, p_stream: Stream):
        for stream in self._collection:
            if stream.interface_name == p_stream.interface_name and stream.txoffset == p_stream.txoffset:
                print(f"Removing stream: Interface: {stream.interface_name}, Offset: {stream.txoffset}")
                self._collection.remove(stream)
                return
        print("Stream not found")
    
    def list(self):
        for stream in self._collection:
            print(f"Interface: {stream.interface_name}, Interval: {stream.interval}, Size: {stream.size}, Offset: {stream.txoffset}, MAC: {stream.addr}, VID: {stream.vid}, PCP: {stream.pcp}")
            
    def get_streams(self):
        return self._collection
    
    def get_interfaces_with_vid(self):
        interfaces = []
        for stream in self._collection:
            if [stream.interface_name, stream.vid] not in interfaces:
                interfaces.append([stream.interface_name, stream.vid])
        return interfaces
    
    def clear(self):
        self._collection = []