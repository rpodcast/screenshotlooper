"""Console script for screenshotlooper."""
import os
import pwd
import sys
import argh
from argh.decorators import arg
import platform
from mss import mss
import mss.tools
from screenshotlooper import configuration

from timeloop import Timeloop

from datetime import timedelta, datetime
from PIL import Image, ImageOps
import logging

# utility functions
def check_exists(file_in):
    if not os.path.isfile(file_in):
        print('ERROR! ' + file_in + ' was not found. Abort.')
        sys.exit(1)

def say_hello(name):
    print("hello %s" % (name))

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def py_minor():
    return sys.version_info[1]

def platform_is_osx():
    return sys.platform == "darwin"

def platform_is_win():
    return sys.platform == "win32"

def platform_is_linux():
    return sys.platform.startswith("linux")

def use_x_display():
    if platform_is_win():
        return False
    if platform_is_osx():
        return False
    DISPLAY = os.environ.get("DISPLAY")
    XDG_SESSION_TYPE = os.environ.get("XDG_SESSION_TYPE")
    # Xwayland can not be used for screenshot
    return DISPLAY and XDG_SESSION_TYPE != "wayland"

def using_multiple_displays():
    with mss.mss() as mss_instance:
        #print(mss_instance.monitors)
        return len(mss_instance.monitors) > 2

def res_gt_1080p(monitor_dict):
    width = monitor_dict['width']
    height = monitor_dict['height']
    #print(f"width is {width}")
    #print(f"height is {height}")
    return width > 1920 or height > 1080

def linux_term_check():
    if platform_is_linux():
        print("running under linux")

        # if in a tty session (i.e. not in an actual graphical desktop), exit script
        if os.environ.get("XDG_SESSION_TYPE") == "tty":
            print("screenshots cannot be taken in a terminal (tty) session!  Please run inside a graphical session")
            sys.exit()
        else:
            if use_x_display():
                print("Running under X11: Proceeding as normal")
            else:
                print("Running under Wayland needs more work")
                sys.exit()
    else:
        print("not running under linux")

@arg('-f', '--filename', help='Screenshotlooper configuration file (ini format)')
@arg('-d', '--dryrun', help='Conduct a dry run of the screenshot looper', default=False)
def cmd(**kwargs):
    if kwargs['filename'] == None:
        print('no config file specified')
    else:
        check_exists(kwargs['filename'])
        config = configuration.Configuration(kwargs['filename'])
        #print('config file output dir: ', config.output_dir)
        #print('config file monitor index: ', config.monitor)

    # check if running under a real terminal / X11 in linux
    linux_term_check()

    if kwargs['dryrun']:
        print("I am in dry run mode")
        # monitors[0] is all monitors together
        # monitors[N] is monitor N (where N is greater than 0)
        with mss.mss() as mss_instance:
            # obtain number of monitors
            n_monitors = len(mss_instance.monitors)

        sys.exit()

    # obtain metadata on host
    user_id = get_username()
    host = platform.node()
    op_system = platform.system()

    # check if multiple displays are being used
    if using_multiple_displays():
        print("using multiple displays")
    else:
        print("using a single display")

    # obtain constants from config file
    low_img_quality = config.low_image_quality
    low_img_interval = config.low_image_interval
    high_img_interval = config.high_image_interval

    # establish time loop
    tl = Timeloop()

    # define jobs to obtain screenshots
    with mss.mss() as mss_instance:
        # low quality image job
        @tl.job(interval=timedelta(seconds=low_img_interval))
        def low_image_screenshot():
            #print("Begin compressed picture saving : {}".format(time.ctime()))
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            output_filename = user_id + "_" + host + "_" + dt_string + ".jpg"
            monitor_1 = mss_instance.monitors[1]
            screenshot1 = mss_instance.grab(monitor_1)
            img1 = Image.frombytes("RGB", screenshot1.size, screenshot1.bgra, "raw", "BGRX")  # Convert to PIL.Image

            if res_gt_1080p(monitor_1):
                #print("resizing screenshot to 1080p")
                img1 = img1.resize((1920, 1080))
            
            output_path = os.path.join(config.output_dir, output_filename)
            img1.save(output_path, quality = low_img_quality)

        # high quality image job
        @tl.job(interval=timedelta(seconds=high_img_interval))
        def high_image_screenshot():
            #print("Begin compressed picture saving : {}".format(time.ctime()))
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            output_filename = user_id + "_" + host + "_" + dt_string + ".png"
            monitor_1 = mss_instance.monitors[1]
            screenshot1 = mss_instance.grab(monitor_1)
            img1 = Image.frombytes("RGB", screenshot1.size, screenshot1.bgra, "raw", "BGRX")  # Convert to PIL.Image

            if res_gt_1080p(monitor_1):
                #print("resizing screenshot to 1080p")
                img1 = img1.resize((1920, 1080))
            
            output_path = os.path.join(config.output_dir, output_filename)
            img1.save(output_path)
    
    tl.start(block=True)

@arg('-m', '--myarg', help='Test arg.', default=True)
@arg('--output_dir', help='Directory to store screenshot files. If not specified, the current working directory where the tool is being executed will be used.')
def dryrun(**kwargs):
    print('my arg: ', kwargs['myarg'])

