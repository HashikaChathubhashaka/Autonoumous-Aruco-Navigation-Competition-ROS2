
    def turn_left_90(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer                
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,9300,-10000,9300,1)

    def turn_right_90(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,-10000,9300,10000,9300,1)

    
    def rotation_forward(self):
        self.roboclaw.ResetEncoders(self.address)

                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,13000,10000,13000,1)

    def small_forward(self):
        self.roboclaw.ResetEncoders(self.address)

                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,16000,10000,16000,1)


    def right_90_forward(self): #turn right and go forward
        self.rotation_forward()
        sleep(2)
        self.turn_right_90()
        sleep(2)
        self.small_forward()


    def left_90_forward(self): #turn left and go forward
        self.rotation_forward()
        sleep(2)
        self.turn_left_90()
        sleep(2)
        self.small_forward()



    #diagonal
        
    def turn_left_45(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer                
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,3200,-10000,3200,1)

    def turn_right_45(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,-10000,3200,10000,3200,1)

        
    def turn_left_135(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer                
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,15000,-10000,15000,1)

    def turn_right_135(self):
        self.roboclaw.ResetEncoders(self.address)
                
                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,-10000,15000,10000,15000,1)

    def diagonal_forward(self):
        self.roboclaw.ResetEncoders(self.address)

                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,27000,10000,27000,1)
    
    def diagonal_rotation_forward(self):
        self.roboclaw.ResetEncoders(self.address)

                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,13000,10000,13000,1)

    def diagonal_small_forward(self):
        self.roboclaw.ResetEncoders(self.address)

                #address, speedM1 , distanceM1 , speedM2 , distanceM2 , buffer
        self.roboclaw.SpeedDistanceM1M2(self.address,10000,16000,10000,16000,1)
    
    

    ##########
    def right_45_forward(self):
        self.diagonal_rotation_forward()    
        sleep(2)
        self.turn_right_45()
        sleep(2)
        self.diagonal_small_forward()    

    def left_45_forward(self):
        self.diagonal_rotation_forward()    
        sleep(2)
        self.turn_left_45()
        sleep(2)
        self.diagonal_small_forward()    

    def right_135_forward(self):
        self.diagonal_rotation_forward()    
        sleep(2)
        self.turn_right_135()
        sleep(2)
        self.diagonal_small_forward()  
    
    def left_135_forward(self):
        self.diagonal_rotation_forward()    
        sleep(2)
        self.turn_left_135()
        sleep(2)
        self.diagonal_small_forward()  




if aruco_id == 0:  # Stop the robot
            self.get_logger().info('Received ArUco ID 0: Stop ')
            self.stop()
        
        else: 
            if self.current_forward_direction =="E":  # current Direction --> East
                if aruco_id == 3:
                    self.get_logger().info('Robot going in East Direction :next move - 90 right ')
                    self.right_90_forward()
                        
                    self.current_forward_direction= "S"

                elif aruco_id == 7:
                    self.get_logger().info('Robot going in East Direction :next move - 90 left ')
                    self.left_90_forward()
                    self.current_forward_direction= "N"
                
                elif aruco_id == 1 or aruco_id == 2 or aruco_id == 8:
                    self.get_logger().info('Robot going in East Direction :next move - forward ')
                    self.forward()

                else:
                    self.stop()

            elif self.current_forward_direction =="S": # current Direction --> South
                if aruco_id == 5:
                    self.get_logger().info('Robot going in South Direction :next move - 90 right ')
                    self.right_90_forward()
                    self.current_forward_direction= "W"


                elif aruco_id == 1:
                    self.get_logger().info('Robot going in South Direction :next move - 90 left ')
                    self.left_90_forward()
                    self.current_forward_direction= "E"
                
                elif aruco_id == 3 or aruco_id == 4 or aruco_id == 2:
                    self.get_logger().info('Robot going in South Direction :next move - forward ')
                    self.forward()
                
                else:
                    self.stop()



            elif self.current_forward_direction =="W": # current Direction --> West
                if aruco_id == 7:
                    self.get_logger().info('Robot going in West Direction :next move - 90 right ')
                    self.right_90_forward()
                    self.current_forward_direction= "N"

                elif aruco_id == 3:
                    self.get_logger().info('Robot going in West Direction :next move - 90 left ')
                    self.left_90_forward()
                    self.current_forward_direction= "S"

                elif aruco_id == 5 or aruco_id == 4 or aruco_id == 6:
                    self.get_logger().info('Robot going in West Direction :next move - forward ')
                    self.forward()
                    
                else:
                    self.stop()


            elif self.current_forward_direction =="N": # current Direction --> North
                if aruco_id == 1:
                    self.get_logger().info('Robot going in North Direction :next move - 90 right ')
                    self.r_f()
                    self.current_forward_direction= "E"

                elif aruco_id == 5:
                    self.get_logger().info('Robot going in North Direction :next move - 90 left ')
                    self.l_f()
                    self.current_forward_direction= "W"
                
                elif aruco_id == 7:
                    self.get_logger().info('Robot going in North Direction :next move - forward ')
                    self.forward()
                
                else:
                    self.stop()

            
