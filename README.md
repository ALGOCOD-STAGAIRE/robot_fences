# Implementation fence_model on  ROS
## 1.Creating Ros_package:rosbot_fences
```
$ catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
$ catkin_make
$~/catkin_ws/devel/setup.bash
```
* create folder script neer src (catkin_ws/src/rosbot_fences):
add your scripts 
* go to Cmakelist in src (vscode) and add this : 
```
catkin_install_python(PROGRAMS
scripts/name.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```
* Put your model .h5 in : `home/fedy/ubecome/config model.h5 `

* compile : `catkin_make`+`source devel/setup.bash `
## 2. Adding launch file

* add a launch folder neer input etc ... 

* put the **file :name.launch** in the  launch folder 

* Modify file :

```
<?xml version="1.0"?>

<launch>
  <node name="rosbot_fences" pkg="rosbot_fences" type="model_fence.py" output="screen">
  </node>
</launch>
```
* compile 

* source devel

* put this command : 

`roslaunch "name of your package" "name of launch file.launch " `

.Note 
=== 
* If you want to run script python :

`rosrun "name package""name .py"`
## 3. Creating node_Ros
* First Let's see our  librairis in the script:
 ```
 from keras.models import load_model
 from PIL import Image, ImageOps
 import numpy as np
 import os
 import rospy
 import ros_numpy
 from sensor_msgs.msg import Image as SensorImage
import numpy as np
from PIL import Image
from std_msgs.msg import Bool
from std_msgs.msg import String
```
* Now you have to install for your python3
 **Tensorflow** : `pip3  install tensorflow==2.6.2`
 **kers **: `pip3  install tensorflow==2.6.0`
  if this is missing :
   `rossudo apt-get install -y python-rospy`
* The rest are already installed in ros python 2.7 
* compile My following script:model_fences.py 

* Open 3 windows on the terminator 

* compile My following scripts : 
[model_fences.py](https://trello.com/1/cards/621f5a2ff22f9e08343b5b70/attachments/62209ce90b4db62a3adf70c0/download/model_fences.py) 

*  source devel the 3 windows 

* open roscore  in the first window 
* write this command in the second  window : 
`roslaunch rosbot_fences rosbot_fences.launch `
* write this command in the  third window :
`roslaunch video_stream_opencv all_stream.launch`

* Result : 
**Our Model works without errors! ** 
* we can see the pourcentage of class 1 and 2 !
[Capture d’écran de 2022-03-03 11-42-21.png](https://trello.com/1/cards/621f5a2ff22f9e08343b5b70/attachments/62209bdafa833a25cc751695/download/Capture_d%E2%80%99%C3%A9cran_de_2022-03-03_11-42-21.png)

* **We succeeded to make a model .h5 works with Ros!!!!!!!!!!!!!!**



Useful links for Errors 
===
* ** link1 :fail to use function in cv_bridge : **
 https://github.com/ros-perception/vision_opencv/issues/207

* ** link2 : nd_array to img error ! : **https://stackoverflow.com/questions/49271913/convert-numpy-array-to-rgb-image

* **Note:**  
Other errors are easy to find in google, such as setting up libraries.

## 4-Build topics for ros

* **Topic 1**: bool return True or False  :fence ripped or not 
[Capture d’écran de 2022-03-03 15-51-56.png](https://trello.com/1/cards/621f5a2ff22f9e08343b5b70/attachments/6220d8cbea050f221bd971ab/download/Capture_d%E2%80%99%C3%A9cran_de_2022-03-03_15-51-56.png) 

* **Topic 2**: String retrun predection of  "Fence not Ripped"
[Capture d’écran de 2022-03-03 15-56-57.png](https://trello.com/1/cards/621f5a2ff22f9e08343b5b70/attachments/6220d92ca9d9e98ea1aa2430/download/Capture_d%E2%80%99%C3%A9cran_de_2022-03-03_15-56-57.png)  

* **Topic 3 **String retrun predection of  "Fence  Ripped"
[Capture d’écran de 2022-03-03 15-59-50.png](https://trello.com/1/cards/621f5a2ff22f9e08343b5b70/attachments/6220d955ce45d95232907ffa/download/Capture_d%E2%80%99%C3%A9cran_de_2022-03-03_15-59-50.png) 
**Note**: we can see that in subject 3 there is no data because most of the images are not ripped.



