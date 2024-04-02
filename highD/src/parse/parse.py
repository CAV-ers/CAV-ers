import sys
sys.path.append("../")
sys.path.append("../csvReader")
# sys.path.append("../frame")

from vehicle import Vehicle,VehicleMgr,VehicleState,Vehicle_XMLWriter
from frame import Frame,FrameMgr
from .csvReader import *
from xmlWriter import *
import os
import time
import subprocess

class MyVehicle(Vehicle):
    """
        self define velhicle class
    """
    pass

def Parse(created_arguments):

    if not os.path.exists(created_arguments["input_path"]):
        print("input file {} not found".format(created_arguments["input_path"]))
        sys.exit(1)
    if not os.path.exists(created_arguments["input_static_path"]):
        print("input static file {} not found".format(created_arguments["input_static_path"]))
        sys.exit(1)
    if not os.path.exists(created_arguments["input_meta_path"]):
        print("input meta file {} not found".format(created_arguments["input_meta_path"]))
        sys.exit(1)
    
    print("Parsing {} ".format(created_arguments["input_path"]))
    print("Parsing {} ".format(created_arguments["input_static_path"]))
    print("Parsing {} ".format(created_arguments["input_meta_path"]))

    
    TR = TrackReader(created_arguments["input_path"],created_arguments["input_static_path"],created_arguments["input_meta_path"])
    xml_writer=XML_Writer()

    # 读取每帧
    frameMgr = FrameMgr()
    for frame, rows in TR.GetGroupedFrame():
        frame_id = frame[0]
        new_frame = Frame(frame_id,list(rows[TRACK_ID].values))
        frameMgr.AddFrame(frame_id,new_frame)

    vehicleMgr = VehicleMgr()
    tracks,length = TR.ReadTrack()
    track_meta = TR.ReadTrackMeta()
    recording_meta = TR.ReadRecordingMeta()
    upperLaneNum=len(recording_meta[UPPER_LANE_MARKINGS])
    lowerLaneNum=len(recording_meta[LOWER_LANE_MARKINGS])

    outpath = created_arguments["output_path"]
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    with open(outpath+"\out.nod.xml",'w') as nod_f:
        nod_f.write("""<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">\n""")
        nod_f.write("""     <node id="n_{}" x="{}" y="{}" type="priority"/>\n""".format(0,-100,0))
        nod_f.write("""     <node id="n_{}" x="{}" y="{}" type="priority"/>\n""".format(1,length+100,0))
        nod_f.write("""</nodes>\n""")

    with open(outpath+"\out.edg.xml",'w') as nod_f:
        nod_f.write("""<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">\n""")
        nod_f.write("""     <edge id="e_{}" from="n_{}" to="n_{}" priority="1" numLanes="{}" speed="100" />\n""".format(0,0,1,upperLaneNum))
        nod_f.write("""     <edge id="e_{}" from="n_{}" to="n_{}" priority="1" numLanes="{}" speed="100" />\n""".format(1,1,0,lowerLaneNum))
        nod_f.write("""</edges>\n""")

    subprocess.check_output(["netconvert","--node-files="+outpath+"\out.nod.xml","--edge-files="+outpath+"\out.edg.xml","--output-file="+outpath+"\out.net.xml","--no-turnarounds=true"])

    # with open(outpath+"\out.net.xml",'w') as net_f:
    #     net_f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
    #     net_f.write("""<net version="1.16" junctionCornerDetail="5" limitTurnSpeed="5.50" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/net_file.xsd">\n""")
    #     net_f.write(xml_writer.Edge(length,list(recording_meta[UPPER_LANE_MARKINGS]),list(recording_meta[LOWER_LANE_MARKINGS])))
    #     net_f.write("""</net>""")


    for track in tracks.values():
        track_meta_info = track_meta[track[TRACK_ID]]
        
        vehicle = MyVehicle(track[TRACK_ID])
        vehicle.InitFrameInfo(track_meta_info[INITIAL_FRAME],track_meta_info[FINAL_FRAME])
        vehicle.SetShape(track[BBOX][0],track[BBOX][1],track_meta_info[CLASS])

        for i in range(len(track[FRAME])):
            vs = VehicleState(track[FRAME][i],track[LANE_ID][i],track_meta_info[DRIVING_DIRECTION])
            vs.SetPosition(track[X][i]
                           ,track[Y][i])
            vs.SetVelocity(track[X_VELOCITY][i]
                               ,track[Y_VELOCITY][i])
            vs.SetAcceleration(track[X_ACCELERATION][i]
                               ,track[Y_ACCELERATION][i])
            vs.SetNeighbour(track[PRECEDING_ID][i]
                            ,track[FOLLOWING_ID][i]
                            ,track[LEFT_PRECEDING_ID][i]
                            ,track[RIGHT_PRECEDING_ID][i]
                            ,track[LEFT_FOLLOWING_ID][i]
                            ,track[RIGHT_FOLLOWING_ID][i]
                            ,track[LEFT_ALONGSIDE_ID][i]
                            ,track[RIGHT_ALONGSIDE_ID][i])
            vehicle.AddState(vs)

        vehicleMgr.AddVehicle(vehicle)

    #获取vehicle_x在第N帧的状态
    # SSS=vehicleMgr.GetVehicle(1).GetStateAtFrame(4)


    now = int(round(time.time()*1000))
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
    vw=Vehicle_XMLWriter()
    with open(outpath+"\out.rou.xml",'w') as rou_f:
        rou_f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
        rou_f.write("""<!-- generated on {} by Eclipse SUMO netedit Version 1.16.0\n""".format(time_stamp))
        rou_f.write("""-->\n""")
        rou_f.write("""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n""")
        rou_f.write("""    <!-- Routes -->\n""")
        rou_f.write("""    <route id="r_0" edges="e_0"/>\n""")
        rou_f.write("""    <route id="r_1" edges="e_1"/>\n""")
        rou_f.write("""    <!-- Vehicles, persons and containers (sorted by depart) -->\n""")
        rou_f.write("""    <vType accel="3.0" decel="6.0" id="CarA" length="5.0" minGap="2.5" maxSpeed="50.0" sigma="0.5" />\n""")
        # ff.write("""    <vehicle id="v_0" depart="0.00" color="0,255,224" route="r_0" type="CarA"/>\n""")
        for  k,v in vehicleMgr.GetAllVehicle().items():
            rou_f.write(vw.getVehicleXML(v,upperLaneNum,length))

        rou_f.write("""</routes>\n""")
