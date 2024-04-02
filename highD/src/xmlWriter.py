
class XML_Writer():
    def Edge(self,length,*lanes):
        numLane=0
        for lane in lanes:
            numLane+=len(lane)

        str="""    <edge id="e_{}" from="J0" to="J1" numLanes="{}" function="internal">\n""".format(0,numLane)

        last=0
        for lane in lanes:
            for i in range(len(lane)):
                lane_id=i+last
                str+="""        <lane id="{}" index="{}" speed="100" length="{}" shape="{}"/>\n""".format("Lane_{}".format(lane_id),lane_id,length,"{},{} {},{}".format(0.00,lane[i],length,lane[i]))
            last+=len(lane)
        
        str+="""    </edge>\n""" 
        str="""    <junction id="J0" type="dead_end" x="0" y="62.20" incLanes="" intLanes="" shape="-11.20,62.20 -11.20,43.00"/>
    <junction id="J1" type="dead_end" x="{}" y="62.20" incLanes="E0_0 E0_1 E0_2 E0_3 E0_4 E0_5" intLanes="" shape="100.62,43.00 100.62,62.20"/>
""".format(length)
        return str