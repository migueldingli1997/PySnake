from configparser import ConfigParser
from typing import List

VALID_WINDOW_SIZES = [1080, 900, 750, 600, 300]


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.cp = None

    @classmethod
    def parse_keys(self, keys: str) -> List[int]:
        return [int(key) for key in keys.split(',')]

    def read(self):
        self.cp = ConfigParser()
        self.cp.read(self.config_file)

        video = self.cp['video']
        self.full_screen = video['full_screen'].lower() in ['true', 'yes']
        self.frames_per_second = int(video['frames_per_second'])
        self.window_size = self.height_px = self.width_px = \
            int(video['window_size'])
        self.center_px = int(self.width_px / 2), int(self.height_px / 2)

        if self.window_size not in VALID_WINDOW_SIZES:
            raise Exception('Invalid window size; Valid sizes: {}'
                            ''.format(VALID_WINDOW_SIZES))

        controls = self.cp['controls']
        self.ctrl_up = self.parse_keys(controls['up'])
        self.ctrl_down = self.parse_keys(controls['down'])
        self.ctrl_left = self.parse_keys(controls['left'])
        self.ctrl_right = self.parse_keys(controls['right'])
        self.ctrl_pause = self.parse_keys(controls['pause'])
        self.ctrl_boost = self.parse_keys(controls['boost'])
        self.ctrl_shoot = self.parse_keys(controls['shoot'])

        self.all_keys = \
            self.ctrl_up + self.ctrl_down + self.ctrl_left + self.ctrl_right + \
            self.ctrl_pause + self.ctrl_boost + self.ctrl_shoot

        print()

    def write(self):
        if self.cp is None:
            raise Exception('Tried to save None config')

        with open(self.config_file, 'r') as fp:
            self.cp = ConfigParser().write(fp)
