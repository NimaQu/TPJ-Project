import socket
import fcntl
import struct
import Image
import screen
import Global

# This function allows us to grab any of our IP addresses
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack("256s", str.encode(ifname[:15])),
        )[20:24]
    )

def show():
    ip_addr = ""
    port = Global.var.cf.get('web', 'flask_port')
    # This sets TEXT equal to whatever your IP address is, or isn't
    try:
        ip_addr = get_ip_address("wlan0")  # WiFi address of WiFi adapter. NOT ETHERNET
    except IOError:
        try:
            ip_addr = get_ip_address("eth0")  # WiFi address of Ethernet cable. NOT ADAPTER
        except IOError:
            ip_addr = "NO INTERNET!"

    # Create blank image for drawing.
    image = Image.status(ip_addr, port)
    screen.display(image)


if __name__ == "__main__":
    from configparser import ConfigParser
    cf = ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    Global.init(cf)
    show()