from configparser import ConfigParser
from typing import Set

VALID_WINDOW_SIZES = [1080, 900, 750, 600, 300]
Keys = Set[int]


class Player:
    def __init__(self, name: str, ctrl_up: Keys, ctrl_down: Keys,
                 ctrl_left: Keys, ctrl_right: Keys, ctrl_pause: Keys,
                 ctrl_boost: Keys, ctrl_shoot: Keys):
        self.name = name

        self.ctrl_up = ctrl_up
        self.ctrl_down = ctrl_down
        self.ctrl_left = ctrl_left
        self.ctrl_right = ctrl_right
        self.ctrl_pause = ctrl_pause
        self.ctrl_boost = ctrl_boost
        self.ctrl_shoot = ctrl_shoot

        all_sets = [ctrl_up, ctrl_down, ctrl_left, ctrl_right,
                    ctrl_pause, ctrl_boost, ctrl_shoot]
        self.all_keys = set().union(*all_sets)


class Config:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.cp = None

    @classmethod
    def parse_keys(cls, keys: str) -> Keys:
        return {int(key) for key in keys.split(',')}

    @classmethod
    def keys_to_str(cls, keys: Keys) -> str:
        return ','.join([str(key) for key in keys])

    def read(self):
        self.cp = ConfigParser()
        self.cp.read(self.config_file)

        # Video settings
        video = self.cp['video']
        self.full_screen = video['full_screen'].lower() in ['true', 'yes']
        self.frames_per_second = int(video['frames_per_second'])
        self.window_size = self.height_px = self.width_px = \
            int(video['window_size'])
        self.font = video['font']
        self.draw_fps = video['draw_fps'].lower() in ['true', 'yes']

        if self.window_size not in VALID_WINDOW_SIZES:
            raise Exception('Invalid window size; Valid sizes: {}'
                            ''.format(VALID_WINDOW_SIZES))

        # Players
        self.players = []
        player_sections = [s for s in self.cp if s.startswith('player_')]
        for ps in player_sections:
            player_name = self.cp[ps]['name']
            ctrl_up = self.parse_keys(self.cp[ps]['ctrl_up'])
            ctrl_down = self.parse_keys(self.cp[ps]['ctrl_down'])
            ctrl_left = self.parse_keys(self.cp[ps]['ctrl_left'])
            ctrl_right = self.parse_keys(self.cp[ps]['ctrl_right'])
            ctrl_pause = self.parse_keys(self.cp[ps]['ctrl_pause'])
            ctrl_boost = self.parse_keys(self.cp[ps]['ctrl_boost'])
            ctrl_shoot = self.parse_keys(self.cp[ps]['ctrl_shoot'])
            self.players.append(Player(
                player_name, ctrl_up, ctrl_down, ctrl_left,
                ctrl_right, ctrl_pause, ctrl_boost, ctrl_shoot))

        self.all_keys = set()
        for p in self.players:
            self.all_keys = self.all_keys.union(p.all_keys)

        if len(self.players) == 0:
            raise Exception('Invalid config: zero players')

    def write(self):
        if self.cp is None:
            raise Exception('Tried to save None config')
        elif len(self.players) == 0:
            raise Exception('Tried to save config with zero players')

        # Clear previous config
        self.cp.clear()

        # Video settings
        section = 'video'
        self.cp.add_section(section)
        self.cp[section]['full_screen'] = str(self.full_screen)
        self.cp[section]['frames_per_second'] = str(self.frames_per_second)
        self.cp[section]['window_size'] = str(self.window_size)
        self.cp[section]['font'] = self.font
        self.cp[section]['draw_fps'] = str(self.draw_fps)

        if self.window_size not in VALID_WINDOW_SIZES:
            raise Exception('Invalid window size; Valid sizes: {}'
                            ''.format(VALID_WINDOW_SIZES))

        # Players
        for i, p in enumerate(self.players):
            section = "player_" + str(i)
            self.cp.add_section(section)
            self.cp[section]['name'] = p.name
            self.cp[section]['ctrl_up'] = self.keys_to_str(p.ctrl_up)
            self.cp[section]['ctrl_down'] = self.keys_to_str(p.ctrl_down)
            self.cp[section]['ctrl_left'] = self.keys_to_str(p.ctrl_left)
            self.cp[section]['ctrl_right'] = self.keys_to_str(p.ctrl_right)
            self.cp[section]['ctrl_pause'] = self.keys_to_str(p.ctrl_pause)
            self.cp[section]['ctrl_boost'] = self.keys_to_str(p.ctrl_boost)
            self.cp[section]['ctrl_shoot'] = self.keys_to_str(p.ctrl_shoot)

        with open(self.config_file, 'w') as fp:
            self.cp.write(fp)

    def add_player(self, player: Player):
        self.players.append(player)
