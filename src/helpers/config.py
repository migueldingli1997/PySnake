from configparser import ConfigParser
from typing import List

VALID_WINDOW_SIZES = [1080, 900, 750, 600, 300]


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.cp = None

    @classmethod
    def parse_keys(cls, keys: str) -> List[int]:
        return [int(key) for key in keys.split(',')]

    @classmethod
    def keys_to_str(cls, keys: List[int]) -> str:
        return ','.join([str(key) for key in keys])

    def read(self):
        self.cp = ConfigParser()
        self.cp.read(self.config_file)

        player = self.cp['player']
        self.player_name = player['name']

        video = self.cp['video']
        self.full_screen = video['full_screen'].lower() in ['true', 'yes']
        self.frames_per_second = int(video['frames_per_second'])
        self.window_size = self.height_px = self.width_px = \
            int(video['window_size'])
        self.font = video['font']

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

    def write(self):
        if self.cp is None:
            raise Exception('Tried to save None config')

        self.cp['controls']['up'] = self.keys_to_str(self.ctrl_up)
        self.cp['controls']['down'] = self.keys_to_str(self.ctrl_down)
        self.cp['controls']['left'] = self.keys_to_str(self.ctrl_left)
        self.cp['controls']['right'] = self.keys_to_str(self.ctrl_right)
        self.cp['controls']['pause'] = self.keys_to_str(self.ctrl_pause)
        self.cp['controls']['boost'] = self.keys_to_str(self.ctrl_boost)
        self.cp['controls']['shoot'] = self.keys_to_str(self.ctrl_shoot)

        with open(self.config_file, 'w') as fp:
            self.cp.write(fp)
