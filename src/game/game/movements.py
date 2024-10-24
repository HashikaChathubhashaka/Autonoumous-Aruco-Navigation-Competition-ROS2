import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from game.roboclaw import Roboclaw
from time import sleep


class Movements(Node):
    def __init__(self):

        super().__init__('Movements_of_robot')

        address = 0x80
        roboclaw = Roboclaw("/dev/ttyS0", 38400)
        #roboclaw = Roboclaw("/dev/ttyAMA0", 38400)
        roboclaw.Open()
        
        self.address = address
        self.roboclaw = roboclaw
    


        # In the start the robot always go in East Direction
        self.current_forward_direction= "East"


        self.directions = ["East","South_East","South","South_West","West","North_West","North","North_East"]
        
        self.numbering_of_directions = { "East":    (1,2,3,4,5,6,7,8)
                                     ,"South_East":(2,3,4,5,6,7,8,1)
                                     ,"South":     (3,4,5,6,7,8,1,2)
                                     ,"South_West":(4,5,6,7,8,1,2,3)
                                     ,"West":      (5,6,7,8,1,2,3,4)
                                     ,"North_West":(6,7,8,1,2,3,4,5)
                                     ,"North":     (7,8,1,2,3,4,5,6)
                                     ,"North_East":(8,1,2,3,4,5,6,7) }
        


        # subscription for taking aruco ID.
        self.subscription = self.create_subscription(
            Int32,
            'Aruco_ID',
            self.aruco_id_callback,
            10
        )

        degree_90 = 14000
        degree_45 = 3100
        degree_135 = 15000

        forward_before_rotation = 13000
        forward_after_rotation =  18000

        self.roboclaw.ResetEncoders(self.address)

        while(self.roboclaw.ReadEncM2(self.address)[1] < 34000):
            speed_m1 = abs(self.roboclaw.ReadSpeedM1(self.address)[1])
            speed_m2 = abs(self.roboclaw.ReadSpeedM2(self.address)[1])

        # Calculate error (difference in speeds)
            error = speed_m1 - speed_m2

        # Compute PID output
            pid_output = int(error * 0.054)

            self.roboclaw.ForwardM1(self.address,abs(100 - pid_output))
            self.roboclaw.ForwardM2(self.address,abs(100 + pid_output))
            
        
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0) 

        ##########################

        rotation_direction = "right"

        self.roboclaw.ResetEncoders(self.address)
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,forward_before_rotation,10000,forward_before_rotation,1) 
        while(self.roboclaw.ReadEncM2(self.address)[1] < forward_before_rotation):
            speed_m1 = abs(self.roboclaw.ReadSpeedM1(self.address)[1])
            speed_m2 = abs(self.roboclaw.ReadSpeedM2(self.address)[1])

            error = speed_m1 - speed_m2

            pid_output = int(error * 0.054)

            self.roboclaw.ForwardM1(self.address,abs(100 - pid_output))
            self.roboclaw.ForwardM2(self.address,abs(100 + pid_output))
        
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0) 


        if rotation_direction == "right":
            self.roboclaw.ResetEncoders(self.address)        
                    #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
            # self.roboclaw.SpeedDistanceM1M2(self.address,-10000,rotation,10000,rotation,1) 
            while(self.roboclaw.ReadEncM2(self.address)[1] < degree_45):
                self.roboclaw.BackwardM1(self.address,abs(100 ))
                self.roboclaw.ForwardM2(self.address,abs(100))
            
            self.roboclaw.ForwardM1(self.address, 0)
            self.roboclaw.ForwardM2(self.address, 0) 

        else:
            self.roboclaw.ResetEncoders(self.address)        
                    #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
            # self.roboclaw.SpeedDistanceM1M2(self.address,10000,rotation,-10000,rotation,1)     
            while(self.roboclaw.ReadEncM2(self.address)[1] < degree_90):
                self.roboclaw.BackwardM2(self.address,abs(100 ))
                self.roboclaw.ForwardM1(self.address,abs(100))
            
            self.roboclaw.ForwardM1(self.address, 0)
            self.roboclaw.ForwardM2(self.address, 0)        



        self.roboclaw.ResetEncoders(self.address)
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,forward_after_rotation,10000,forward_after_rotation,1) 
        while(self.roboclaw.ReadEncM2(self.address)[1] < forward_after_rotation):
            speed_m1 = abs(self.roboclaw.ReadSpeedM1(self.address)[1])
            speed_m2 = abs(self.roboclaw.ReadSpeedM2(self.address)[1])

            error = speed_m1 - speed_m2

            pid_output = int(error * 0.054)

            self.roboclaw.ForwardM1(self.address,abs(100 - pid_output))
            self.roboclaw.ForwardM2(self.address,abs(100 + pid_output))
            
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0)

        

        # ##----For testing Motors----
        # print(self.roboclaw.ReadEncM1(self.address))
        # print(self.roboclaw.ReadEncM2(self.address)) 

        # self.roboclaw.ForwardM1(self.address, 100)
        # self.roboclaw.ForwardM2(self.address, 100)
        # sleep(15)

        # print(self.roboclaw.ReadEncM1(self.address)) 
        # print(self.roboclaw.ReadEncM2(self.address)) 

        # self.roboclaw.ForwardM1(self.address, 0)
        # self.roboclaw.ForwardM2(self.address, 0)


        # self.roboclaw.ResetEncoders(self.address)
                
        #         #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,15000,10000,15000,1)

        # sleep(5)
        # # self.stop()


        # self.roboclaw.ResetEncoders(self.address)
                
        #         #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,15000,10000,15000,1)

        # sleep(5)
        # self.stop()


        # sleep(2)


        # self.roboclaw.ResetEncoders(self.address)

        #         #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,40000,8800,40000,1)

    #---Basic Movement Functions-----#
        
    #Straight Movements

    # tune parameters
        


    def forward(self):
        self.roboclaw.ResetEncoders(self.address)

                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,28000,10000,28000,1) 
        # while (self.roboclaw.ReadEncM1(self.address)[1] < 28000  and self.roboclaw.ReadEncM2(self.address)[1] < 28000):
        #     pass

        while(self.roboclaw.ReadEncM2(self.address)[1] < 18000):
            self.roboclaw.ForwardM1(self.address,abs(100 ))
            self.roboclaw.ForwardM2(self.address,abs(100))
            
        
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0) 



    def movement(self,forward_before_rotation ,rotation_direction ,  rotation , forward_after_rotation):

        self.roboclaw.ResetEncoders(self.address)
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,forward_before_rotation,10000,forward_before_rotation,1) 
        while(self.roboclaw.ReadEncM2(self.address)[1] < forward_before_rotation):
            self.roboclaw.ForwardM1(self.address,abs(100 ))
            self.roboclaw.ForwardM2(self.address,abs(100))
            
        
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0) 

        sleep(4)

        if rotation_direction == "right":
            self.roboclaw.ResetEncoders(self.address)        
                    #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
            # self.roboclaw.SpeedDistanceM1M2(self.address,-10000,rotation,10000,rotation,1) 
            while(self.roboclaw.ReadEncM2(self.address)[1] < rotation):
                self.roboclaw.BackwardM1(self.address,abs(100 ))
                self.roboclaw.ForwardM2(self.address,abs(100))
            
            self.roboclaw.ForwardM1(self.address, 0)
            self.roboclaw.ForwardM2(self.address, 0) 

        else:
            self.roboclaw.ResetEncoders(self.address)        
                    #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
            # self.roboclaw.SpeedDistanceM1M2(self.address,10000,rotation,-10000,rotation,1)     
            while(self.roboclaw.ReadEncM2(self.address)[1] < rotation):
                self.roboclaw.BackwardM2(self.address,abs(100 ))
                self.roboclaw.ForwardM1(self.address,abs(100))
            
            self.roboclaw.ForwardM1(self.address, 0)
            self.roboclaw.ForwardM2(self.address, 0)        

        sleep(4)

        self.roboclaw.ResetEncoders(self.address)
        # self.roboclaw.SpeedDistanceM1M2(self.address,10000,forward_after_rotation,10000,forward_after_rotation,1) 
        while(self.roboclaw.ReadEncM2(self.address)[1] < forward_after_rotation):
                self.roboclaw.ForwardM1(self.address,abs(100 ))
                self.roboclaw.ForwardM2(self.address,abs(100))
            
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0)

    def stop(self):
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0)   


        
    def aruco_id_callback(self, msg):
        aruco_id = msg.data

    # 1= East , 2 =South-East , 3=South ,  4=South-West , 5=West , 6=North-West , 7=North , 8=North-East , 0=Stop

        # ---Stop at End --- 
        if aruco_id == 0: 
            self.get_logger().info('Stop')
            self.stop()

        else:
            current_set = self.numbering_of_directions[self.current_forward_direction]

            # ---forward---
            if  aruco_id == current_set[0]:
                self.forward()
                self.current_forward_direction= self.directions[current_set[0]-1]

            # ---90 turns---
            elif aruco_id == current_set[2]:
                #self.right_90_forward()
                self.movement(self.forward_before_rotation ,"right", self.degree_90, self.forward_after_rotation)
                self.current_forward_direction = self.directions[current_set[2]-1]

            elif aruco_id == current_set[6]:
                #self.left_90_forward()
                self.movement(self.forward_before_rotation ,"left", self.degree_90, self.forward_after_rotation)
                self.current_forward_direction= self.directions[current_set[6]-1]
            
            # ---45 turns---   
            elif aruco_id == current_set[1]:
                #self.right_45_forward()
                self.movement(self.forward_before_rotation ,"right", self.degree_45, self.forward_after_rotation)
                self.current_forward_direction= self.directions[current_set[1]-1]
            
            elif aruco_id == current_set[7]:
                #self.left_45_forward()
                self.movement(self.forward_before_rotation ,"left", self.degree_45, self.forward_after_rotation)
                self.current_forward_direction= self.directions[current_set[7]-1]
            
            # ---135 turns---
            elif aruco_id == current_set[3]:
                #self.right_135_forward()
                self.movement(self.forward_before_rotation ,"right", self.degree_135, self.forward_after_rotation)
                self.current_forward_direction= self.directions[current_set[3]-1]
            
            elif aruco_id == current_set[5]:
                #self.left_135_forward()
                self.movement(self.forward_before_rotation ,"left", self.degree_135, self.forward_after_rotation)
                self.current_forward_direction= self.directions[current_set[5]-1]

            else:
                self.stop()
            
        
def main(args=None):
    rclpy.init(args=args)
    aruco_id_subscriber = Movements()
    rclpy.spin(aruco_id_subscriber)
    aruco_id_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
