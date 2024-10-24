# Autonoumous-Aruco-Navigation-Competition-ROS2


<div align="center">
  <img src="https://github.com/HashikaChathubhashaka/Autonoumous-Aruco-Navigation-Competition-ROS2/blob/main/Images%20of%20Robot/1.jpeg?raw=true" alt="Robot Image" height="300" width="500"/>

  <h2> Autonoumous Navigation Robot using Aruco Marks </h2>
</div>






## Important
<p>To run the aruco detection node you need to install opencv-contrib-python 4.6.0.66

If already have other version
```bash
pip uninstall opencv-contrib-python opencv-python
```
Install required version
```bash
pip install opencv-contrib-python==4.6.0.66
```

</p>

## Installation
Clone the src/game file into your local directory and make ros2 package using colcon build.

```bash
colcon build --symlink-install 
```


  


source the workspace
```bash
source install/setup.bash
```

To run the full programme
```bash
ros2 launch game run.launch
```

To run only aruco marker detector

```bash
ros2 run game aruco_detection
```

To run only movement ( uncomment testing lines)

```bash
ros2 run game movements
```


