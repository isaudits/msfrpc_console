import sys
import os
import modules

modules_dir = os.path.dirname(modules.__file__)

for module in os.listdir(modules_dir):
    sys.path.insert(0, os.path.join(modules_dir, module))

#These arent true standalone modules - add subdirectories to path
sys.path.insert(0, os.path.join(modules_dir, "pymetasploit", "src"))