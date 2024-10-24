#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import Int32
from std_msgs.msg import Bool
#from example_interfaces.msg import Int64

class Detector(Node):
    def __init__(self):
        super().__init__('detector')


        topic_name = 'video_frames'
        self.publisher = self.create_publisher(Image, topic_name, 10)
        self.aruco_publisher = self.create_publisher(Int32, 'Aruco_ID', 10)  # Create ArUco ID publisher        
        self.timer = self.create_timer(0.1, self.timer_callback)


        self.cap = cv2.VideoCapture(0)
        self.br = CvBridge()

        self.subscription = self.create_subscription(Image, topic_name, self.img_callback, 10)
        self.subscription
        self.br = CvBridge()




    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            # Perform ArUco marker detection
            arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
            arucoParams = cv2.aruco.DetectorParameters_create()
            corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
            frame_with_markers = aruco_display(corners, ids, rejected, frame)



            if ids is not None and len(ids) > 0:
                aruco_id = int(ids[0][0])  # Convert to Python int
                aruco_msg = Int32()
                aruco_msg.data = aruco_id
                self.aruco_publisher.publish(aruco_msg)        



            # Publish the frame with detected markers
            self.publisher.publish(self.br.cv2_to_imgmsg(frame_with_markers))

        #self.get_logger().info('Publishing video frame with detected markers')

    def img_callback(self, data):
        self.get_logger().info('Receiving video frame')
        # current_frame = self.br.imgmsg_to_cv2(data)
        # cv2.imshow("camera", current_frame)
        # cv2.waitKey(1)
        


def aruco_display(corners, ids, rejected, image):
     

	if len(corners) > 0:
		
		ids = ids.flatten()
		
		for (markerCorner, markerID) in zip(corners, ids):
			
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners
			
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
			
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
			
			cv2.putText(image, str(markerID),(topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 255, 0), 2)
			print("[Inference] ArUco marker ID: {}".format(markerID))
			
	return image



def main(args=None):
    rclpy.init(args=args)
    simple_pub_sub = Detector()
    rclpy.spin(simple_pub_sub)
    simple_pub_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()