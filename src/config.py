from configparser import ConfigParser
from typing import List

CONFIG_FILE = 'config.ini'
VALID_WINDOW_SIZES = [1080, 900, 750, 600, 300]


class Config:
    def __init__(self):
        self.cp = None

    @classmethod
    def parse_keys(self, keys: str) -> List[int]:
        return [int(key) for key in keys.split(',')]

    def read(self):
        self.cp = ConfigParser()
        self.cp.read(CONFIG_FILE)

        general = self.cp['general']
        self.full_screen = general['full_screen'].lower() in ['true', 'yes']
        self.frames_per_second = int(general['frames_per_second'])
        self.window_size = int(general['window_size'])

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

        with open(CONFIG_FILE, 'r') as fp:
            self.cp = ConfigParser().write(fp)


CFG = Config()
CFG.read()
