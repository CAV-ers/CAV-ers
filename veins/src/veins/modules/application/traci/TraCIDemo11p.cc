//
// Copyright (C) 2006-2011 Christoph Sommer <christoph.sommer@uibk.ac.at>
//
// Documentation for these modules is at http://veins.car2x.org/
//
// SPDX-License-Identifier: GPL-2.0-or-later
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//

#include "veins/modules/application/traci/TraCIDemo11p.h"

#include "veins/modules/application/traci/TraCIDemo11pMessage_m.h"
#include "veins/modules/utility/Consts80211p.h"
using namespace veins;

Define_Module(veins::TraCIDemo11p);

void TraCIDemo11p::initialize(int stage)
{
    DemoBaseApplLayer::initialize(stage);
    if (stage == 0) {
        sentMessage = false;
        lastDroveAt = simTime();
        currentSubscribedServiceId = -1;
    }
}

void TraCIDemo11p::onWSA(DemoServiceAdvertisment* wsa)
{
    if (currentSubscribedServiceId == -1) {
        mac->changeServiceChannel(static_cast<Channel>(wsa->getTargetChannel()));
        currentSubscribedServiceId = wsa->getPsid();
        if (currentOfferedServiceId != wsa->getPsid()) {
            stopService();
            startService(static_cast<Channel>(wsa->getTargetChannel()), wsa->getPsid(), "Mirrored Traffic Service");
        }
    }
}

void TraCIDemo11p::onWSM(BaseFrame1609_4* frame)
{
    TraCIDemo11pMessage* wsm = check_and_cast<TraCIDemo11pMessage*>(frame);

    findHost()->getDisplayString().setTagArg("i", 1, "green");

    if (mobility->getRoadId()[0] != ':') traciVehicle->changeRoute(wsm->getDemoData(), 9999);
    if (!sentMessage) {
        sentMessage = true;
        // repeat the received traffic update once in 2 seconds plus some random delay
        wsm->setSenderAddress(myId);
        wsm->setSerial(3);
        scheduleAt(simTime() + 2 + uniform(0.01, 0.2), wsm->dup());
    }
}

void TraCIDemo11p::onRM(ReportMessage* frame){
    ReportMessage* rm = check_and_cast<ReportMessage*>(frame);
    auto distance = rm->getSenderPos().distance(curPosition);
    std::cout << "self:"<< myId << " position "<<curPosition<<std::endl;
    std::cout << "remote:" << rm->getSenderAddress() << " reported from position " << rm->getSenderPos() << std::endl;
    std::cout << "distance:" << distance << std::endl<<std::endl;
    auto vi = VehicleInfo();
    vi.id = rm->getSenderAddress();
    vi.pos = rm->getSenderPos();
    vi.speed = rm->getSenderSpeed();

    // this neigbour is in the front of me or not?
    double headDot = (rm->getSenderPos()-curPosition)*curSpeed;
    if (headDot > 0.0f){
       vi.isForward = true;
    }else{
       vi.isForward = false;
    }

    // the neigbout is at the same direction of me or not?
    double directionDot = curSpeed * rm->getSenderSpeed();
    if (directionDot > 0.0f){// same direction
        vi.isSameDirection = true;
    }else{
        vi.isSameDirection = false;
    }

    if (distance < 50.0){ // neibours within the range of 50 meters
        if (connectedNodes.find(rm->getSenderAddress()) == connectedNodes.end()){
            std::cout << "add:"<<rm->getSenderAddress()<<std::endl;
        }else{
            std::cout << "update:"<<rm->getSenderAddress()<<std::endl;
        }
        connectedNodes[rm->getSenderAddress()]=vi;
    }else{
        std::cout << "delete:"<<rm->getSenderAddress()<<std::endl;
        connectedNodes.erase(rm->getSenderAddress());
        // connectedNodes(rm->getSenderAddress());
    }

    ProcessNeigbour(); // 邻居的信息整理
}

void TraCIDemo11p::ProcessNeigbour(){
    this->f_nei.id = 0;
    this->b_nei.id = 0;
    // 最近的邻居
    double f_min_dis = 9999999999.f;
    double b_min_dis = 9999999999.f;
    for(auto n: this->connectedNodes){
        auto nei_address = n.first;
        auto nei_info = n.second;

        auto distance = nei_info.pos.distance(curPosition);
        if (nei_info.isForward){
            if ( distance < f_min_dis){
                this->f_nei = nei_info;
            }
        }else{
            if (distance < b_min_dis){
                this->b_nei = nei_info;
            }
        }
    }
}

void TraCIDemo11p::handleSelfMsg(cMessage* msg)
{
    if (TraCIDemo11pMessage* wsm = dynamic_cast<TraCIDemo11pMessage*>(msg)) {
        // send this message on the service channel until the counter is 3 or higher.
        // this code only runs when channel switching is enabled
        sendDown(wsm->dup());
        wsm->setSerial(wsm->getSerial() + 1);
        if (wsm->getSerial() >= 3) {
            // stop service advertisements
            stopService();
            delete (wsm);
        }
        else {
            scheduleAt(simTime() + 1, wsm);
        }
    }
    else {
        DemoBaseApplLayer::handleSelfMsg(msg);
    }
}

void TraCIDemo11p::handlePositionUpdate(cObject* obj)
{
    DemoBaseApplLayer::handlePositionUpdate(obj);

    ReportMessage* rm = new ReportMessage();
    populateWSM(rm);
    rm->setSenderAddress(myId);
    rm->setSenderPos(curPosition);

    std::cout<< getFullName()<<std::endl;
    std::cout<< getFullPath()<<std::endl;
    std::cout<< getClassName()<<std::endl;
    std::cout<< getId()<<std::endl;
    std::cout<< getIndex()<<std::endl;

    std::cout<< getModuleType()<<std::endl;
    sendDown(rm);

    findHost()->getDisplayString().setTagArg("i", 1, "green");

    // stopped for for at least 10s?
    if (mobility->getSpeed() < 1) {
        if (simTime() - lastDroveAt >= 10 && sentMessage == false) {
            findHost()->getDisplayString().setTagArg("i", 1, "red");
            sentMessage = true;

            TraCIDemo11pMessage* wsm = new TraCIDemo11pMessage();
            populateWSM(wsm);
            wsm->setDemoData(mobility->getRoadId().c_str());

            // host is standing still due to crash
            if (dataOnSch) {
                startService(Channel::sch2, 42, "Traffic Information Service");
                // started service and server advertising, schedule message to self to send later
                scheduleAt(computeAsynchronousSendingTime(1, ChannelType::service), wsm);
            }
            else {
                // send right away on CCH, because channel switching is disabled
                sendDown(wsm);
            }
        }
    }
    else {
        lastDroveAt = simTime();
    }
}
