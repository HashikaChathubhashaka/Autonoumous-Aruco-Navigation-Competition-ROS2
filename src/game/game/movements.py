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
        self.current_forward_direction= "E"

        #config the PID for both motors
        p_M1 = 1.56562;
        i_M1 = 0.29137;
        d_M1 = 0.0;
        qpps_M1 = 10500;

        p_M2 = 1.53399;
        i_M2 = 0.27342;
        d_M2 = 0.0;
        qpps_M2 = 10687;
    
        self.p_M1 = p_M1
        self.i_M1 = i_M1
        self.d_M1 = d_M1
        self.qpps_M1 = qpps_M1

        self.p_M2 = p_M2
        self.i_M2 = i_M2
        self.d_M2 = d_M2
        self.qpps_M2 = qpps_M2



        # subscription for taking aruco ID.
        self.subscription = self.create_subscription(
            Int32,
            'Aruco_ID',
            self.aruco_id_callback,
            10
        )

    #---Movement Functions-----#
    def turn_left_90(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer                
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,13550,-10000,13550,1)

    def turn_right_90(self):
                
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,-10000,13550,10000,13550,1)

    def forward(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,20000,10000,20000,1)
          
    def r_f(self):
        sleep(2)
        self.turn_right_90()
        sleep(2)
        self.forward()
        sleep(2)

    def l_f(self):
        sleep(2)
        self.turn_left_90()
        sleep(2)
        self.forward()
        sleep(2)

    def f(self):
        sleep(2)
        self.forward()
        sleep(2)


    def aruco_id_callback(self, msg):
        aruco_id = msg.data


# 1= East , 2 =South-East , 3=South ,  4=South-West , 5=West , 6=North-West , 7=North , 8=North-East , 0=Stop


        if aruco_id == 0:  # Stop the robot
            self.get_logger().info('Received ArUco ID 0: Stop ')

            return 
        
        if self.current_forward_direction =="E":  # current Direction --> East
            if aruco_id == 3:
                self.get_logger().info('Robot going in East Direction :next move - 90 right ')
                self.r_f()
                    
                self.current_forward_direction= "S"

            elif aruco_id == 7:
                self.get_logger().info('Robot going in East Direction :next move - 90 left ')
                self.l_f()
                self.current_forward_direction= "N"
            
            else:
                self.get_logger().info('Robot going in East Direction :next move - forward ')
                #self.f()


        elif self.current_forward_direction =="S": # current Direction --> South
            if aruco_id == 5:
                self.get_logger().info('Robot going in South Direction :next move - 90 right ')
                self.r_f()
                self.current_forward_direction= "E"


            elif aruco_id == 1:
                self.get_logger().info('Robot going in South Direction :next move - 90 left ')
                self.l_f()
                self.current_forward_direction= "W"
            
            else:
                self.get_logger().info('Robot going in South Direction :next move - forward ')
                #self.f()



        elif self.current_forward_direction =="W": # current Direction --> West
            if aruco_id == 7:
                self.get_logger().info('Robot going in West Direction :next move - 90 right ')
                self.current_forward_direction= "N"

            elif aruco_id == 3:
                self.get_logger().info('Robot going in West Direction :next move - 90 left ')
                self.l_f()
                self.current_forward_direction= "S"
            
            else:
                self.get_logger().info('Robot going in West Direction :next move - forward ')
                #self.f()


        elif self.current_forward_direction =="N": # current Direction --> North
            if aruco_id == 1:
                self.get_logger().info('Robot going in North Direction :next move - 90 right ')
                self.r_f()
                self.current_forward_direction= "E"

            elif aruco_id == 5:
                self.get_logger().info('Robot going in North Direction :next move - 90 left ')
                self.l_f()
                self.current_forward_direction= "W"
            
            else:
                self.get_logger().info('Robot going in North Direction :next move - forward ')
                #self.f()




def main(args=None):
    rclpy.init(args=args)
    aruco_id_subscriber = Movements()
    rclpy.spin(aruco_id_subscriber)
    aruco_id_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()