import random
class VehicleState():
    def __init__(self,frame_id,lane,direction):
        self.frame_id=frame_id
        self.lane=lane
        self.direction=1
        if direction==1:
            self.direction=-1
        # position
        self.x=0.0
        self.y=0.0
        # motion states
        self.xVelocity=0.0
        self.yVelocity=0.0
        self.xAcceleration=0.0
        self.yAcceleration=0.0
        # neighbours
        self.PrecedingID=0
        self.FollowingID=0
        self.PrecedingID_L=0
        self.PrecedingID_R=0
        self.FollowingID_L=0
        self.FollowingID_R=0
        self.AlongSideID_L=0
        self.AlongSideID_R=0

    def SetPosition(self,x,y):
        self.x=x
        self.y=y
    
    def SetVelocity(self,xVelocity,yVelocity):
        self.xVelocity=xVelocity
        self.yVelocity=yVelocity  
    
    def GetXVelocity(self):
        return self.xVelocity/self.direction
    
    def GetDirection(self):
        return self.direction
    
    def SetAcceleration(self,xAcceleration,yAcceleration):
        self.xAcceleration=xAcceleration
        self.yAcceleration=yAcceleration

    def SetNeighbour(self,PrecedingID
                     ,FollowingID
                     ,PrecedingID_L
                     ,PrecedingID_R
                     ,FollowingID_L
                     ,FollowingID_R
                     ,AlongSideID_L
                     ,AlongSideID_R):
        self.PrecedingID=PrecedingID
        self.FollowingID=FollowingID
        self.PrecedingID_L=PrecedingID_L
        self.PrecedingID_R=PrecedingID_R
        self.FollowingID_L=FollowingID_L
        self.FollowingID_R=FollowingID_R
        self.AlongSideID_L=AlongSideID_L
        self.AlongSideID_R=AlongSideID_R


class Vehicle:
    """
        Base Class of a Vehicle
    """
    def __init__(self,id):
        # identification
        self.id=id
        #  vehicle type  #Car #Truck
        self.type = "Car"
        # shape
        self.width = 0.0
        self.height= 0.0
        # frame
        self.initialFrame=0
        self.finalFrame=0
        # frame_id ==> vehicleState
        self.states={}

    def InitFrameInfo(self,initialFrame,finalFrame):
        self.initialFrame=initialFrame
        self.finalFrame=finalFrame

    def SetShape(self,width,height,vehicle_type):
        self.width=width
        self.height=height
        self.type=vehicle_type
    
    def  AddState(self,state):
        if state.frame_id in self.states:
            print("frame_id:{} already added to state set".format(state.frame_id))
            return
        self.states[state.frame_id]=state

    def GetStateAtFrame(self,frame_id) -> VehicleState:
        if frame_id in self.states:
            return self.states[frame_id]
        return None
    
    def GetDepartInfo(self):
        initFrame=self.GetStateAtFrame(self.initialFrame)
        if initFrame:
            return self.initialFrame/25,initFrame.lane,initFrame.x,initFrame.GetXVelocity(),initFrame.GetDirection()

class VehicleMgr():
    def __init__(self):
        self.vehicles={}

    def AddVehicle(self,vehicle):
        if vehicle.id in self.vehicles:
            print("vehicle:{} alread exist".format(vehicle.id))
            return
        self.vehicles[vehicle.id]=vehicle
    
    def GetAllVehicle(self):
        return self.vehicles
    
    def GetVehicle(self,vehicle_id):
        if  vehicle_id not in self.vehicles:
            print("vehicle:{} not exist".format(vehicle_id))
            return None
        return self.vehicles[vehicle_id]
    
    def Clear(self):
        self.frames={}


class Vehicle_XMLWriter():
    """
        writer for vehicle xml format
    """
    def __init__(self):
        pass
    
    def getVehicleTypeXML(self,vehicle:Vehicle):
        return """<vType accel="{}" decel="{}" id="{}" length="5.0" minGap="2.5" maxSpeed="50.0" sigma="0.5" />\n""".format(vehicle.GetStateAtFrame(vehicle.initialFrame).xAcceleration,vehicle.GetStateAtFrame(vehicle.initialFrame).xVelocity,"CarType_{}".format(vehicle.id))
    
    def getVehicleXML(self,vehicle:Vehicle,upperLaneNum,length):
        depart,departLane,departPos,departSpeed,direction=vehicle.GetDepartInfo()
        # return """<vehicle id="{}" depart="{}" departLane="{}" departPos="{}" departSpeed="{}" color="0,255,224" route="{}" type="{}"/>\n""".format(vehicle.id,depart,departLane,departPos,departSpeed,"r_0","CarType_{}".format(vehicle.id))
        route="r_0"
        if direction==-1:
            route="r_1"
            departPos=length-departPos
        departLane-=1
        if departLane>=upperLaneNum:
            departLane-=upperLaneNum
        color="{},{},{}".format(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        return """<vehicle id="{}" depart="{}" departLane="{}" departPos="{}" departSpeed="{}" color="{}" route="{}"/>\n""".format(vehicle.id,depart,departLane,departPos,departSpeed,color,route)
