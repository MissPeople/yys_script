import struct

from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from PIL import Image
import io, time

# 连接 MuMu（默认5555端口；网易MuMu12是7555，看你自己设置）
device = AdbDeviceTcp("127.0.0.1", 5555, default_transport_timeout_s=5.)
device.connect()


def screenshot_raw():
    raw = device.shell("screencap", decode=False)      # 原始输出
    # 前 12 字节：width, height, format
    w, h, f = struct.unpack_from('<III', raw, 0)
    assert f == 1, "只支持 RGBA 格式"
    img = Image.frombuffer('RGBA', (w, h), raw[12:], 'raw', 'RGBA', 0, 1)
    return img

if __name__ == "__main__":
    img = screenshot_raw()
    img.save("mumu.png")

