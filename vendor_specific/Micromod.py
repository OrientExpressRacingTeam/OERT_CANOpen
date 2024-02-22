import canopen



class Node_Micromod:

    # init
    def __init__(self, node_id, network):
        self.node_id = node_id
        self.network = network
        self.node = self.network.add_node(self.node_id)
        self.manufacturer_code = self.node.sdo.upload(0x1018, 1)
        self.manufacturer_code = int.from_bytes(self.manufacturer_code, byteorder="little")
        self.manufacturer = {373: "Micromod"}
        self.baudrate = {1: "10 kbit/s", 2: "20 kbit/s", 3: "50 kbit/s", 4: "125 kbit/s", 5: "250 kbit/s", 6: "500 kbit/s", 7: "800 kbit/s", 8: "1000 kbit/s"}
        self.baudrate_code = {1: 0x00, 2: 0x01, 3: 0x02, 4: 0x03, 5: 0x04, 6: 0x05, 7: 0x06, 8: 0x07}
