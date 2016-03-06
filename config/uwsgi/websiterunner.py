import os
import sys
tracker_path = os.path.dirname(os.path.realpath(__file__))+'/../../albertyw.com/'
sys.path.append(tracker_path)

import monitor
monitor.start(interval=1.0)
#monitor.track(os.path.join(os.path.dirname(__file__), 'site.cf'))

from serve import *
