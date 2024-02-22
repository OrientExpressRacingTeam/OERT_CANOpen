import can
import canopen
from PCANBasic import *
import time


manufacturer = {373: "Peak System Technik GmbH", 994: "BlinkMarine"}

baudrates = {
    "10000k": (0x00, 1000000),
    "800k": (0x01, 800000),
    "500k": (0x02, 500000),
    "250k": (0x03, 250000),
    "125k": (0x04, 125000),
    "50k": (0x06, 50000),
    "20k": (0x07, 20000),
}


class OERT_CANopen:
    def __init__(self, baudrate):
        self.devices = {}
        self.autodetect_channel()
        self.network = canopen.Network()
        self.baudrate = baudrate
        self.network.connect(
            bustype="pcan", channel=self.channel, bitrate=self.baudrate
        )
        self.list_canopen_devices()

    def autodetect_channel(self):
        pcan = PCANBasic()

        channel_names = [
            (PCAN_USBBUS1, "PCAN_USBBUS1"),
            (PCAN_USBBUS2, "PCAN_USBBUS2"),
            (PCAN_USBBUS3, "PCAN_USBBUS3"),
            (PCAN_USBBUS4, "PCAN_USBBUS4"),
        ]

        for channel in channel_names:
            result = pcan.GetValue(channel[0], PCAN_CHANNEL_CONDITION)
            if result[0] == PCAN_ERROR_OK:
                if result[1] & PCAN_CHANNEL_AVAILABLE:
                    print(f"Channel {channel[1]} is available")
                    self.channel = channel[1]
                    return channel[1]

    def autodetect_baudrate(self):
        pcan = PCANBasic()

        baudrates = [
            (PCAN_BAUD_1M, 1000000),
            (PCAN_BAUD_500K, 500000),
            (PCAN_BAUD_250K, 250000),
            (PCAN_BAUD_125K, 125000),
            (PCAN_BAUD_100K, 100000),
            (PCAN_BAUD_50K, 50000),
            (PCAN_BAUD_20K, 20000),
            (PCAN_BAUD_10K, 10000),
            (PCAN_BAUD_5K, 5000),
        ]

        for baudrate in baudrates:
            result = pcan.SetValue(self.channel, PCAN_BITRATE_INFO, baudrate[1])
            time.sleep(0.05)
            if result == PCAN_ERROR_OK:
                print(f"Baudrate {baudrate[0]} is available")
                return baudrate[1]
            else:
                print(result)
                continue

    def list_canopen_devices(self):
        # Create a network representing one CAN bus
        self.network.scanner.search()
        time.sleep(0.05)
        self.devices = {}
        try:
            for node_id in self.network.scanner.nodes:
                node = self.network.add_node(node_id)
                manufacturer_code = node.sdo.upload(
                    0x1018, 1
                )  # assuming manufacturer code is at index 0x1018, subindex 1
                manufacturer_code = int.from_bytes(
                    manufacturer_code, byteorder="little"
                )
                if manufacturer_code in manufacturer:
                    print(
                        f"Node #{node_id} is a {manufacturer[manufacturer_code]} device"
                    )
                    self.devices[node_id] = {"manufacturer_code": manufacturer_code}
        except:
            pass
        return
        network.disconnect()

    def change_baudrate(self, node_id=None, new_baudrate=None):
        node_id = input_node_id(node_id)
        # Send Canopen message to change baudrate
        baudrate = input_baudrate(new_baudrate)
        # get manufacturer code
        manufacturer_code = self.devices[node_id]["manufacturer_code"]
        if manufacturer_code == 373:
            data = [0x23, 0x50, 0x1F, 0x03, ord("B"), ord("P"), ord("S"), baudrate]
            print(data)
        elif manufacturer_code == 994:
            data = [0x2F, 0x20, 0x10, 0x00, baudrate, 0x00, 0x00, 0x00]
        else:
            print("Manufacturer code not supported")
        self.network.send_message(0x600 + node_id, bytes(data))
        time.sleep(1)
        if manufacturer_code == 373:
            data = [0x23, 0x10, 0x10, 0x01, ord("s"), ord("a"), ord("v"), ord("e")]
            self.network.send_message(0x600 + node_id, bytes(data))
        time.sleep(1)


def input_node_id(node_id=None):
    if node_id is None:
        node_id = -1
    while node_id < 1 or node_id > 0x7F:
        node_id = int(input("Enter node id : "))
        # Check if node id is valid, hence between 1 and 15
        if node_id < 1 or node_id > 0x7F:
            print("Invalid node id, try again")
    return node_id


def input_baudrate(baudrate=None):
    while baudrate not in baudrates:
        baudrate = input(
            'Enter baudrate to change to: ["1000k","800k" "500k", "250k", "125k", "50k", "20k"]:'
        )
    else:
        return baudrates[baudrate][0]


# main
if __name__ == "__main__":
    print(
        """\
   ____    _    _   _                        
  / ___|  / \  | \ | | ___  _ __   ___ _ __  
 | |     / _ \ |  \| |/ _ \| '_ \ / _ \ '_ \ 
 | |___ / ___ \| |\  | (_) | |_) |  __/ | | |
  \____/_/   \_\_| \_|\___/| .__/ \___|_| |_|
                           |_|               """
    )

    my_can = OERT_CANopen(125000)

    # Create a CAN bus interface (replace 'socketcan' and 'can0' with your setup)

    while True:
        print("1. Monitor Input")
        print("2. Change Baudrate")

        # while True:
        #     print("1. Monitor Input")
        #     print("2. Change Baudrate")
        #     print("3. Monitor startup status")
        #     print("4. Change node id")
        #     print("5. Transmit info")
        #     print("6. Check heartbeat cycle")
        #     print("7. Start Canopen device")
        #     print("8. Change background brightness")
        #     print("9. Read device info")
        #     print("10. Default reset")
        #     print("11. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            print("Monitoring CAN bus")
            # can_monitor(bus)
            break
        elif choice == "2":
            my_can.change_baudrate()
            break

        print(
            "Invalid choice, try again"
        )  # Create a CLI menu with various options to choose the task to perform
