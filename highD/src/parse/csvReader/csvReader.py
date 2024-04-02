import pandas
import numpy as np
import warnings
import os
import pickle
# TRACK FILE
BBOX = "bbox"
FRAMES = "frames"
FRAME = "frame"
TRACK_ID = "id"
X = "x"
Y = "y"
WIDTH = "width"
HEIGHT = "height"
X_VELOCITY = "xVelocity"
Y_VELOCITY = "yVelocity"
X_ACCELERATION = "xAcceleration"
Y_ACCELERATION = "yAcceleration"
FRONT_SIGHT_DISTANCE = "frontSightDistance"
BACK_SIGHT_DISTANCE = "backSightDistance"
DHW = "dhw"
THW = "thw"
TTC = "ttc"
PRECEDING_X_VELOCITY = "precedingXVelocity"
PRECEDING_ID = "precedingId"
FOLLOWING_ID = "followingId"
LEFT_PRECEDING_ID = "leftPrecedingId"
LEFT_ALONGSIDE_ID = "leftAlongsideId"
LEFT_FOLLOWING_ID = "leftFollowingId"
RIGHT_PRECEDING_ID = "rightPrecedingId"
RIGHT_ALONGSIDE_ID = "rightAlongsideId"
RIGHT_FOLLOWING_ID = "rightFollowingId"
LANE_ID = "laneId"

# STATIC FILE
INITIAL_FRAME = "initialFrame"
FINAL_FRAME = "finalFrame"
NUM_FRAMES = "numFrames"
CLASS = "class"
DRIVING_DIRECTION = "drivingDirection"
TRAVELED_DISTANCE = "traveledDistance"
MIN_X_VELOCITY = "minXVelocity"
MAX_X_VELOCITY = "maxXVelocity"
MEAN_X_VELOCITY = "meanXVelocity"
MIN_DHW = "minDHW"
MIN_THW = "minTHW"
MIN_TTC = "minTTC"
NUMBER_LANE_CHANGES = "numLaneChanges"

# VIDEO META
ID = "id"
FRAME_RATE = "frameRate"
LOCATION_ID = "locationId"
SPEED_LIMIT = "speedLimit"
MONTH = "month"
WEEKDAY = "weekDay"
START_TIME = "startTime"
DURATION = "duration"
TOTAL_DRIVEN_DISTANCE = "totalDrivenDistance"
TOTAL_DRIVEN_TIME = "totalDrivenTime"
N_VEHICLES = "numVehicles"
N_CARS = "numCars"
N_TRUCKS = "numTrucks"
UPPER_LANE_MARKINGS = "upperLaneMarkings"
LOWER_LANE_MARKINGS = "lowerLaneMarkings"

class TrackReader():
    trackFileName = ""
    trackMetaFileName = ""
    trackRecordFileName = ""

    track_f=None
    trackMeta_f=None
    recordingMeta_f=None

    def __init__(self,track,tracksMeta,recordingMeta):
        self.trackFileName = track
        self.trackMetaFileName = tracksMeta
        self.trackRecordFileName = recordingMeta
        self.track_f = self.ReadFile(track)
        self.trackMeta_f = self.ReadFile(tracksMeta)
        self.recordingMeta_f = self.ReadFile(recordingMeta)


    def ReadFile(self,filePath):
        try:
            return pandas.read_csv(filePath)
        except FileNotFoundError:
            warnings.warn("{} is not Exist !".format(filePath))
            return None
        
    def GetGroupedTrack(self):
        if self.track_f is None:
            return None
        return self.track_f.groupby([TRACK_ID], sort=False)
    
    def GetGroupedFrame(self):
        if self.track_f is None:
            return None
        return self.track_f.groupby([FRAME], sort=True)
    
    def ReadTrack(self):
        fn,_ = os.path.splitext(self.trackFileName)
        pickle_name=fn +".pickle"
        if os.path.isfile(pickle_name): ##直接读缓存
            with open(pickle_name,"rb") as f:
                return pickle.load(f)
            
        if self.track_f is None:
            return None,0
        track_grouped = self.GetGroupedTrack()
        tracks = {}
        length=0
        for group_id, rows in track_grouped:
            max_length=rows[X].max()
            if max_length>length:
                length=max_length
            current_track = np.int64(group_id[0])
            bounding_boxes = np.transpose(np.array([rows[WIDTH].values,
                                                    rows[HEIGHT].values]))
            tracks[current_track] = {TRACK_ID: current_track,
                                     FRAME: rows[FRAME].values,
                                     BBOX: bounding_boxes,
                                     X:rows[X].values,
                                     Y:rows[Y].values,
                                     X_VELOCITY: rows[X_VELOCITY].values,
                                     Y_VELOCITY: rows[Y_VELOCITY].values,
                                     X_ACCELERATION: rows[X_ACCELERATION].values,
                                     Y_ACCELERATION: rows[Y_ACCELERATION].values,
                                     FRONT_SIGHT_DISTANCE: rows[FRONT_SIGHT_DISTANCE].values,
                                     BACK_SIGHT_DISTANCE: rows[BACK_SIGHT_DISTANCE].values,
                                     THW: rows[THW].values,
                                     TTC: rows[TTC].values,
                                     DHW: rows[DHW].values,
                                     PRECEDING_X_VELOCITY: rows[PRECEDING_X_VELOCITY].values,
                                     PRECEDING_ID: rows[PRECEDING_ID].values,
                                     FOLLOWING_ID: rows[FOLLOWING_ID].values,
                                     LEFT_FOLLOWING_ID: rows[LEFT_FOLLOWING_ID].values,
                                     LEFT_ALONGSIDE_ID: rows[LEFT_ALONGSIDE_ID].values,
                                     LEFT_PRECEDING_ID: rows[LEFT_PRECEDING_ID].values,
                                     RIGHT_FOLLOWING_ID: rows[RIGHT_FOLLOWING_ID].values,
                                     RIGHT_ALONGSIDE_ID: rows[RIGHT_ALONGSIDE_ID].values,
                                     RIGHT_PRECEDING_ID: rows[RIGHT_PRECEDING_ID].values,
                                     LANE_ID: rows[LANE_ID].values
                                     }
        data=(tracks,length)
        with open(pickle_name,"wb") as f:## 缓存到文件
            pickle.dump(data,f) 
        return tracks,length


    def ReadTrackMeta(self):
        fn,_ = os.path.splitext(self.trackMetaFileName)
        pickle_name=fn +".pickle"
        if os.path.isfile(pickle_name): ##直接读缓存
            with open(pickle_name,"rb") as f:
                return pickle.load(f)
            
        if self.trackMeta_f is None:
            return None
        track_meta = {}
        for i_row in range(self.trackMeta_f.shape[0]):
            track_id = int(self.trackMeta_f[TRACK_ID][i_row])
            track_meta[track_id] = {TRACK_ID: track_id,
                                           WIDTH: int(self.trackMeta_f[WIDTH][i_row]),
                                           HEIGHT: int(self.trackMeta_f[HEIGHT][i_row]),
                                           INITIAL_FRAME: int(self.trackMeta_f[INITIAL_FRAME][i_row]),
                                           FINAL_FRAME: int(self.trackMeta_f[FINAL_FRAME][i_row]),
                                           NUM_FRAMES: int(self.trackMeta_f[NUM_FRAMES][i_row]),
                                           CLASS: str(self.trackMeta_f[CLASS][i_row]),
                                           DRIVING_DIRECTION: float(self.trackMeta_f[DRIVING_DIRECTION][i_row]),
                                           TRAVELED_DISTANCE: float(self.trackMeta_f[TRAVELED_DISTANCE][i_row]),
                                           MIN_X_VELOCITY: float(self.trackMeta_f[MIN_X_VELOCITY][i_row]),
                                           MAX_X_VELOCITY: float(self.trackMeta_f[MAX_X_VELOCITY][i_row]),
                                           MEAN_X_VELOCITY: float(self.trackMeta_f[MEAN_X_VELOCITY][i_row]),
                                           MIN_TTC: float(self.trackMeta_f[MIN_TTC][i_row]),
                                           MIN_THW: float(self.trackMeta_f[MIN_THW][i_row]),
                                           MIN_DHW: float(self.trackMeta_f[MIN_DHW][i_row]),
                                           NUMBER_LANE_CHANGES: int(self.trackMeta_f[NUMBER_LANE_CHANGES][i_row])
                                           }
        with open(pickle_name,"wb") as f:## 缓存到文件
            pickle.dump(track_meta,f) 
        return track_meta

    def ReadRecordingMeta(self):
        fn,_ = os.path.splitext(self.trackRecordFileName)
        pickle_name=fn +".pickle"
        if os.path.isfile(pickle_name): ##直接读缓存
            with open(pickle_name,"rb") as f:
                return pickle.load(f)
            
        if self.recordingMeta_f is None:
            return None
        recording_meta_dictionary = {ID: int(self.recordingMeta_f[ID][0]),
                                     FRAME_RATE: int(self.recordingMeta_f[FRAME_RATE][0]),
                                     LOCATION_ID: int(self.recordingMeta_f[LOCATION_ID][0]),
                                     SPEED_LIMIT: float(self.recordingMeta_f[SPEED_LIMIT][0]),
                                     MONTH: str(self.recordingMeta_f[MONTH][0]),
                                     WEEKDAY: str(self.recordingMeta_f[WEEKDAY][0]),
                                     START_TIME: str(self.recordingMeta_f[START_TIME][0]),
                                     DURATION: float(self.recordingMeta_f[DURATION][0]),
                                     TOTAL_DRIVEN_DISTANCE: float(self.recordingMeta_f[TOTAL_DRIVEN_DISTANCE][0]),
                                     TOTAL_DRIVEN_TIME: float(self.recordingMeta_f[TOTAL_DRIVEN_TIME][0]),
                                     N_VEHICLES: int(self.recordingMeta_f[N_VEHICLES][0]),
                                     N_CARS: int(self.recordingMeta_f[N_CARS][0]),
                                     N_TRUCKS: int(self.recordingMeta_f[N_TRUCKS][0]),
                                     UPPER_LANE_MARKINGS: np.fromstring(self.recordingMeta_f[UPPER_LANE_MARKINGS][0], sep=";"),
                                     LOWER_LANE_MARKINGS: np.fromstring(self.recordingMeta_f[LOWER_LANE_MARKINGS][0], sep=";")}
        with open(pickle_name,"wb") as f:## 缓存到文件
            pickle.dump(recording_meta_dictionary,f) 
        return recording_meta_dictionary