#!/usr/bin/env python3
""" h5_model_detector_node
    Detect fence  in the incoming image stream /quad1/image_raw and publish result into topic.
"""
from ast import Str
#from tokenize import String
import numpy
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os
import rospy
import ros_numpy
from sensor_msgs.msg import Image as SensorImage
#from cv_bridge import CvBridge
import numpy as np
from PIL import Image
from std_msgs.msg import Bool
from std_msgs.msg import String

"""
    TO DO REAd the doc
    h5_detector listen to topic:={/quad1/image_raw} from video_stream_opencv package
        - upon data received, store the data in a local variable
        - Call detction process function dnn_detector_node,
"""
class FenceDetectorNode(object):
    """
    This is the constructor of the class FenceDetectorNode
    this is called ONCE in the beginning
    """
    def __init__(self):
        #rospy.init_node('FenceDetectorNode', anonymous=True)

        """
        Initialize local topics value with empty data values = 0
        and store them
        """
        # PARAMETERS
        self.path_model= os.path.join(os.path.expanduser('~'),"ubecome","config","keras_model.h5")
        self.model               = load_model(self.path_model)
        self.camera_quad_one     = SensorImage  ()
        self.image_message       = SensorImage  ()
        self.camera_one          = SensorImage  ()
        self.predcition_bool     = Bool()
        self.predection_Value_c0    = String()
        self.predection_Value_c1    = String()
        """Params
        """
        """Publisher
        """
        self.pub_predection_bool = rospy.Publisher('rosbot/fences/ripped', Bool, queue_size=5)
        self.pub_predection_c0      = rospy.Publisher('rosbot/fences/notripped/prediction', String, queue_size=5)
        self.pub_predection_c1      = rospy.Publisher('rosbot/fences/ripped/prediction', String, queue_size=5)
        #std_msgs.msg.String
        #self.pub_detect_images     =rospy.Publisher('/detect/Fence/images', SensorImage, queue_size=5)
        #affiche le resultas 
        # self.rec_timer             = rospy.Timer(rospy.Duration(rospy.get_param('~detect/duration'   , 0.5  )), self.detect_object)

        """Subscriber
        """
        self.sub_camera_quad_one = rospy.Subscriber('/quad1/image_raw'    , SensorImage   , self.listen_camera_quad_one)

    def detect_fence_array(self,ros_image):
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        #image = Image.open('/home/fedy/Documents/test3.jpeg')
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image_arry = ros_numpy.numpify(ros_image)
        image = self.numpy2pil(image_arry)

        #color_image = self.bridge.imgmsg_to_cv2(ros_image, "bgr8")

        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image.show()
        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array
        # run the inference
        prediction = self.model.predict(data)
        rospy.logwarn(prediction)
        if (prediction[0][0]>=0.85):
             a=self.predcition_bool.data=False 
             self.pub_predection_bool.publish(a)
             b=self.predection_Value_c0.data =str(prediction[0][0])
             self.pub_predection_c0 .publish(b)  
             rospy.loginfo('Grillage non coupé')
        elif(prediction[0][1]>=0.85):
             a=self.predcition_bool.data=True
             self.pub_predection_bool.publish(a)
             b=self.predection_Value_c1 .data =str(prediction[0][1])
             self.pub_predection_c1.publish(b) 
             rospy.loginfo("Grillage coupé")
        else: 
             rospy.loginfo ("None")

    def listen_camera_quad_one(self,camera_quad):
        self.camera_quad_one = camera_quad
        self.detect_fence_array(self.camera_quad_one)

    # def unsubscribe(self):
    #     # use the saved subscriber object to unregister the subscriber
    #     self.sub_camera_quad_one.unregister()

    def numpy2pil(self,numpyy):
        assert_msg = 'Input shall be a HxWx3 ndarray'
        assert isinstance(numpyy, np.ndarray), assert_msg
        assert len(numpyy.shape) == 3, assert_msg
        assert numpyy.shape[2] == 3, assert_msg
        img = Image.fromarray(numpyy, 'RGB')
        return img

    def shutdown(self):
        rospy.loginfo("Stopping the Fence_Detector_Node...")
        #rospy.sleep(2)


if __name__ == '__main__':
    rospy.init_node('Fence_Detector_Node', anonymous=True)
    try:
        fence_detector_node = FenceDetectorNode()
        rospy.on_shutdown(fence_detector_node.shutdown)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("{0} node finished.".format(rospy.get_name()))

