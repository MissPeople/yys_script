import subprocess
import os

def get_mumu_port():
    try:
        # 获取 MuMu 模拟器的 adb 端口
        result = subprocess.check_output(['netstat', '-ano'], text=True)
        lines = result.split('\n')
        
        # MuMu 模拟器默认使用 7555 端口，但可能被修改
        for line in lines:
            if '127.0.0.1' in line and 'LISTENING' in line:
                parts = line.split()
                port = parts[1].split(':')[-1]
                # 检查是否是 MuMu 相关进程
                pid = parts[-1]
                try:
                    process_info = subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'], text=True)
                    if 'Nemu' in process_info or 'MuMu' in process_info:
                        return int(port)
                except:
                    continue
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    



def check_mumu_connection(port=7555):
    try:
        # 1. 检查端口是否监听
        netstat = subprocess.check_output(['netstat', '-ano'], text=True)
        if f'127.0.0.1:{port}' not in netstat:
            print(f"错误：端口 {port} 未监听")
            return False
        
        # 2. 尝试连接ADB
        connect_result = subprocess.check_output(f'adb connect 127.0.0.1:{port}', shell=True, text=True)
        print(connect_result)
        
        # 3. 检查设备列表
        devices_result = subprocess.check_output('adb devices', shell=True, text=True)
        print(devices_result)
        
        if f'127.0.0.1:{port}' in devices_result:
            print("连接成功！")
            return True
        else:
            print("连接失败，设备未出现在列表中")
            return False
            
    except Exception as e:
        print(f"调试过程中出错: {e}")
        return False

# 使用示例
check_mumu_connection(5557)  # 先尝试默认端口7555

# port = get_mumu_port()
# print(f"MuMu 模拟器端口号: {port}")
