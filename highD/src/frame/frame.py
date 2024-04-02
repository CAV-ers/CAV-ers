class Frame():
    """
        Frame contains all vehicle's id in one specifical frame
    """
    def __init__(self,id,vehicleIDs):
        self.id=id #帧号  25 frame/s
        self.vehicleIDs=vehicleIDs #当前帧所有交通工具id的集合

    def GetVehiles(self):
        return self.vehicleIDs
    
class FrameMgr():
    """
        Frame Manager contains all frames
    """

    def __init__(self):
        self.frames={}

    def AddFrame(self,frame_id,frame):
        if frame_id in self.frames:
            print("Frame:{} alread exist".format(frame_id))
            return
        self.frames[frame_id]=frame
    
    def GetFrame(self,frame_id):
        if frame_id in self.frames:
            print("Frame:{} not exist".format(frame_id))
            return None
        return self.frames[frame_id]
    
    def Clear(self):
        self.frames={}