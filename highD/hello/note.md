# note
---

# 路网文件
--remote-port 111

--num-clients

# data
## file type
 - xx_highway.jpg
 - xx_recordingMeta.csv
 - xx_tracksMeta.csv
 - xx_tracks.csv

## xx_recordingMeta.csv 记录的总体信息
 - id 
 - frameRate帧率
 - locationId
 - ...

## xx_tracksMeta.csv


## xx_tracks.csv



<NETWORK_FILE>: a SUMO network file as built by netgenerate or netconvert
<ROUTES_FILE>: a SUMO routes file as built by duarouter or jtrrouter or by hand
<TYPE_FILE>: a SUMO edge type file, built by hand or downloaded
<OSM_FILE>: a OpenStreetMap file as exported from OpenStreetMap

<SUMO_HOME> is the path you have saved your SUMO-package into.


# Vehicle
## 属性[https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html]
- id
- type
- route
- color
- depart
- departLane
- departPos
- departSpeed
- departEdge

## Route
  - id
  - edges
  - color
  - repeat
  - cycleTime


## vType
- id
- imgFile