#pragma once
#include "veins/base/utils/Coord.h"
namespace veins{

    struct VehicleInfo
    {
        LAddress::L2Type id;
        Coord pos;
        Coord speed;
        double heading;
        double accelaration;

        bool isForward;
        bool isSameDirection;
    };
    
}
