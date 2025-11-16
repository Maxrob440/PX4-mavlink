from pymavlink import mavutil
from expandingBox import ExpandingBox
from sectorSearch import SectorSearch
import time
class Controller:
    def __init__(self):
        self.master = mavutil.mavlink_connection("udp:127.0.0.1:14540")
        self.expandingBox = None
        self.sectorSearch = None
        print("Waiting for heartbeat...")

        #Connect to correct instance - avoids connecting to QGroundControl
        while True:
            hb = self.master.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
            if hb is None:
                print("No heartbeat yet...")
                continue

            sysid = hb.get_srcSystem()
            compid = hb.get_srcComponent()
            print(f"Heartbeat from sysid={sysid}, compid={compid}, type={hb.type}")
            if sysid == 1:     
                print("CONNECTED to PX4")
                break
        self.displayHeartBeat(hb)
    
    def arm(self):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0  # param1 = 1 → arm
        )
        print("Arming...")
        response = self.master.recv_match(type="COMMAND_ACK",blocking=True,timeout=5)
        if response.result ==1:
            raise Exception("Failed to arm")
        print(response)

    def takeOff(self,alt:int):
        self.master.mav.command_long_send(
            self.master.target_system,
            self.master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,0,0,0,
            float('nan'),float('nan'),
            alt
        )
        response = self.master.recv_match(type="COMMAND_ACK",blocking=True,timeout=5)
        print(response)
        print("Waiting to reach 2m...")
        while(True):
            response = self.master.recv_match(
                type="LOCAL_POSITION_NED",
                blocking=True,
                timeout=5)
            if response.z<-2:
                print('height reached')
                break

    def getHeartBeat(self,debug:str=''):
        while True:
            hb = self.master.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
            if hb is None:
                print("No heartbeat yet...")
                continue

            sysid = hb.get_srcSystem()
            compid = hb.get_srcComponent()
            if sysid == 1:     
                break
        self.displayHeartBeat(hb,debug)
        return hb

    def displayHeartBeat(self,hb,debug:str=''):
        final = f"{debug}Heartbeat -> "
        if hb.type ==2:
            final+=f"Type: Quadrotor"
        elif hb.type ==6:
            final+="WARNING Type: GCS"
        else:
            final += "WARNING Type: Unknown"

        if hb.autopilot ==12:
            final+=", Autopilot: PX4"
        system_statuses={4:"Active",3:"Startup",5:"Critical"}
        
        final+=f", System Status: {system_statuses[hb.system_status]}"

        final+=f", Custom mode : {(hb.custom_mode>>16)&0xFF}"
        final+=f".{(hb.custom_mode>>24)&0xFF}"
        print(final)

    def moveTo(self,x:float,y:float,z:float):
        hb=self.getHeartBeat()
        if (hb.custom_mode >>16)&0xFF !=6:
            print("Not in offboard mode, updating now")
        # Initial point
            self.master.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
                10,
                self.master.target_system, 
                self.master.target_component,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                int(0b110111111000),
                x,y,-z,
                0,0,0,
                0,0,0,
                0,0
            ))
            self.master.mav.command_long_send(
                self.master.target_system,
                self.master.target_component,
                mavutil.mavlink.MAV_CMD_DO_SET_MODE,
                0,
                mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # base_mode
                6, 
                0, 0, 0, 0, 0
            )

            hb=self.getHeartBeat() 

            if (hb.custom_mode >>16)&0xFF !=6:
                print("Failed to change mode...")

        while(True):

            self.master.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
                10,
                self.master.target_system, 
                self.master.target_component,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                int(0b110111111000),
                x,y,-z,
                0,0,0,
                0,0,0,
                0,0
            ))
            response = self.master.recv_match(type="LOCAL_POSITION_NED",blocking=True,timeout=0.1)
            if not response:
                print("NO RESPONSE FROM DRONE")
            else:
                if abs(response.x-x)<1 and abs(response.y-y)<1 and abs(response.z--z)<1:
                    break
        self.setHover()

    def setHover(self):
        self.setMode(4,2)
    
    def setRTL(self):
        self.setMode(4,5)

    def setMode(self,main_mode,sub_mode):
        custom_mode = (sub_mode << 24) | (main_mode << 16)
        base_mode = mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
        self.master.mav.set_mode_send(
            self.master.target_system,
            base_mode,
            custom_mode
        )
        hb= self.getHeartBeat()

        if (hb.custom_mode >>16)&0xFF!=main_mode:
            print("Error setting main mode")

        if (hb.custom_mode >>24)&0xFF!=sub_mode:
            print("Error setting sub mode")    
    def createExpandingBox(self,x,y,z,direction=0):
        self.expandingBox = ExpandingBox(x,y,z,direction)

    def expandingExpandingBox(self):
        if not self.expandingBox:
            print("Expanding box has not been created... ")
        x,y,z = self.expandingBox.step()
        self.moveTo(x,y,z)
    
    def createSectorSearch(self,x,y,z):
        self.sectorSearch=SectorSearch(x,y,z)

    def nextSectorSearch(self):
        if not self.sectorSearch:
            print("Sector Search hasn't been created yet... ")
        x,y,z=self.sectorSearch.step()
        self.moveTo(x,y,z)
controller = Controller()
controller.arm()
time.sleep(1)
controller.takeOff(5)
x,y,z=-100,750,10
controller.moveTo(x,y,z)
# controller.createSectorSearch(x,y,z)
# for x in range(25):
#     controller.nextSectorSearch()
controller.createExpandingBox(x,y,z,45)
for x in range(25):
    controller.expandingExpandingBox()
controller.setRTL()
