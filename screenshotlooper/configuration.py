import configobj
import os
import sys
import validate

def check_exists(file_in):
    if not os.path.isfile(file_in):
        print('ERROR! ' + file_in + ' was not found. Abort.')
        sys.exit(1)

def check_dir_exists(dir_in):
    if not os.path.isdir(dir_in):
        print('ERROR! ' + dir_in + ' was not found or is not a directory. Abort.')
        sys.exit(1)

class Configuration(object):

    def __init__(self, ini_file):
        self.config = configobj.ConfigObj(ini_file)

        # expand any relative file paths
        if self.config['config']['output_dir'].startswith('~'):
            self.config['config']['output_dir'] = os.path.expanduser(self.config['config']['output_dir'])

        # check that output directory exists
        check_dir_exists(self.config['config']['output_dir'])

        self.output_dir = self.config['config']['output_dir']
        self.monitor = self.config['config']['monitor']
        self.low_image_quality = int(self.config['config']['low_image_quality'])
        self.low_image_interval = int(self.config['config']['low_image_interval'])
        self.high_image_interval = int(self.config['config']['high_image_interval'])

if __name__ == '__main__':
    pass