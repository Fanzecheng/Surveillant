import os
import platform

home_dir = os.path.expanduser("~")
target_dir = os.path.join(home_dir, ".Surveillant")
if os.path.exists(target_dir) and os.path.isdir(target_dir):
    pass
else:
    os.makedirs(target_dir, exist_ok=True)