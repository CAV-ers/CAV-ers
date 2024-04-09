import socket
import struct
import os
import sys

sys.path.append("/home/veins/src/veins/cmd/python_out")
sys.path.append("/home/veins/src/sumo/tools")
import traci
import time

from vehicle_pb2 import PV_GetVehicle
from vehicle_pb2 import VP_GetVehicle
from vehicle_pb2 import PV_GetNeigbours
from vehicle_pb2 import VP_GetNeigbours

CMD_NEW_STEP = 0x01
CMD_GET_VEHICLE = 0x02 # get info of vehicle x
CMD_GET_Neigbours = 0x03 # get neigbours of vehicle x
CMD_GET_SIM_TIME = 0x97
CMD_SIM_NEXT = 0x98 # python clietn finish, veins continue
CMD_SIM_END = 0x99 # sim end

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("set SUMO_HOME")


def Step(targetTime):
    print(traci.vehicle.getIDList())

# Send CMD to veins


def Send(socket, cmd):
    data = b""
    if cmd == 0x2:
        req = PV_GetVehicle()
        req.id = "flow0.0"  # todo: 整理命令
        data = req.SerializeToString()
    if cmd == 0x3 :
        req = PV_GetNeigbours()
        req.id = "flow0.0"
        data = req.SerializeToString()

    send_package_len = 0x5+len(data)  # 数据包长度, 4+1
    packed_data = struct.pack('>I', send_package_len)
    packed_data += struct.pack('>B', cmd)
    packed_data += data
    socket.send(packed_data)


def Recv(socket):
    PACKAGE_LENGTH_IN_HEAD = 4
    data = b''
    length = 0
    while True:
        tmp = s.recv(1024)
        if not tmp:
            return 0, data[:0]
        data += tmp
        if len(data) >= PACKAGE_LENGTH_IN_HEAD:
            length = struct.unpack('>I', data[:PACKAGE_LENGTH_IN_HEAD])[0]
            if len(data) >= length:
                break
    # package-len[4] + cmd[1] +  data
    cmd = struct.unpack(
        '>B', data[PACKAGE_LENGTH_IN_HEAD:PACKAGE_LENGTH_IN_HEAD+1])[0]  # CMD
    return cmd, data[PACKAGE_LENGTH_IN_HEAD+1:]


def StepFinish(socket):
    print("[python] step finish")
    Send(socket, CMD_SIM_NEXT)

# 执行python端算法逻辑


def PythonStep(socket):
    print(traci.vehicle.getIDList())

    Send(socket, CMD_GET_VEHICLE)
    HandleVeins(socket)

    Send(socket, CMD_GET_Neigbours)
    HandleVeins(socket)

    # Send(socket, 0x97)
    # HandleVeins(socket)

    StepFinish(socket)


def HandleVeins(socket):
    cmd, data = Recv(socket)
    if cmd == CMD_NEW_STEP:  # CMD_NEW_STEP  new round simulation
        print("New sim step")
        PythonStep(socket)
    elif cmd == CMD_GET_VEHICLE:
        v = VP_GetVehicle()
        v.ParseFromString(data)
        print("get vehicle data success:",v)
        return True
    elif cmd == CMD_GET_Neigbours:
        v = VP_GetNeigbours()
        v.ParseFromString(data)
        print("get neigbour data success:",v)
        return True
    elif cmd == CMD_GET_SIM_TIME:
        # print("Get SimTime Success:",data.decode())
        return True
    elif cmd == CMD_SIM_END or cmd == -1:
        return False
    # match cmd:
    #     case 0x01:# CMD_NEW_STEP  new round simulation
    #         print("New sim step")
    #         PythonStep(socket)
    #     case 0x02: #CMD_GET_VEHICLE, unmarshal vehicle data
    #         # print("Get Vehicle Success:",data.decode())
    #         v=VP_GetVehicle()
    #         v.ParseFromString(data)
    #         print(v)
    #         return True
    #     case 0x97: # CMD_GET_SIM_TIME
    #         # print("Get SimTime Success:",data.decode())
    #         return True
    #     case 0x99,-1:
    #         return False
    return True


def StartSim(socket):
    while HandleVeins(socket):
        pass
    print("Simulation End")


# 创建一个 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 定义veins地址和端口
host = '127.0.0.1'
port = 8888

# 连接veins服务器
s.connect((host, port))

# guarantee python-client be the second client connected to sumo-traci-server
time.sleep(1)
traci.init(9999, host=host)
# traci.connect(9999,label="default")
# traci.setOrder(1)
# traci.simulationStep(1)

# start sim
StartSim(s)
traci.close()
s.close()
