"""
Sends data to xively whenever a new webcam images added to the directory (events represent motion detection when used along with YawCam on windows).
"""

SENSOR_PERIOD = 60*5  # [s] how often we check the directory and push data
MOTION_EVENT_FILE_DIR = '/temp'

from xively_config import XIVELY_API_KEY, XIVELY_FEED_ID

import xively
import datetime
import os
from threading import Timer
import sched

class MotionSensor(object):
    def __init__(self):
        self.api = xively.XivelyAPIClient(XIVELY_API_KEY)
        self.feed = self.api.feeds.get(XIVELY_FEED_ID)
        
        # store contents of the file dir
        self.n_files = len(os.listdir(MOTION_EVENT_FILE_DIR))
        
        # schedule first update
        self.update()
        
    def update(self):
        """
        checks if new data, and logs it if there is
        """
        new_file_count = len(os.listdir(MOTION_EVENT_FILE_DIR))
        
        if self.n_files < new_file_count:  # if there is a new file
            time = datetime.datetime.utcnow()  # TODO: read this from age of file?
            
            self.feed.datastreams = [
                xively.Datastream(id='motion', current_value=1, at=time),
            ]
            
            print 'new image detected'
            
            self.feed.update()
            self.n_files = new_file_count
        elif self.n_files > new_file_count:
            print 'files have been removed'
            
            # TODO: what should I do here?
            self.n_files = new_file_count
            
        else:  # no changes
            now = datetime.datetime.utcnow()

            self.feed.datastreams = [
                xively.Datastream(id='motion', current_value=0, at=now),
            ]
            
            print 'nothing new detected'
            
            self.feed.update()        

            
        # schedule next update
        Timer(SENSOR_PERIOD, self.update, ()).start()
        
my_sensor = MotionSensor()
