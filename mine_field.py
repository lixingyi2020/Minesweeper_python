import random
from enum import Enum


class MineStatus(Enum):
    INITIAL = 1
    OPENED = 2
    MINE = 3
    FLAGGED = 4  # flagged as mine
    QUESTION_MARK = 5
    BOOMED = 6
    HINTING = 7  # left and right button down
    BOTH_BUTTON_CLICKING = 8


class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._around_mine_count = -1
        self._status = MineStatus.INITIAL
        self.set_value(value)

    def __repr__(self):
        return str(self._value)
        # return f'({self._x},{self._y})={self._value}, status={self.status}'

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    x = property(fget=get_x, fset=set_x)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    y = property(fget=get_y, fset=set_y)

    def get_value(self):
        return self._value

    def set_value(self, value):
        if value:
            self._value = 1
        else:
            self._value = 0

    value = property(fget=get_value, fset=set_value, doc="0:NO MINE 1:MINE")

    def get_around_mine_count(self):
        return self._around_mine_count

    def set_around_mine_count(self, around_mine_count):
        self._around_mine_count = around_mine_count

    around_mine_count = property(
        fget=get_around_mine_count, fset=set_around_mine_count, doc="mine count around"
    )

    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value

    status = property(fget=get_status, fset=set_status, doc="BlockStatus")

    def toggle_status(self):
        if self.status == MineStatus.INITIAL:
            self.status = MineStatus.FLAGGED
        elif self.status == MineStatus.FLAGGED:
            self.status = MineStatus.QUESTION_MARK
        elif self.status == MineStatus.QUESTION_MARK:
            self.status = MineStatus.INITIAL


class MineField:
    def __init__(self, width=30, height=16, mine_count=99):
        self.width = width
        self.height = height
        self.mine_count = mine_count

        self._block = [[Mine(i, j) for i in range(width)] for j in range(height)]

        # set mine
        for i in random.sample(range(width * height), mine_count):
            self._block[i // width][i % width].value = 1

    def get_block(self):
        return self._block

    block = property(fget=get_block)

    def get_mine(self, x, y):
        return self._block[y][x]

    def open_mine(self, x, y):
        # clicked on mine
        if self._block[y][
            x
        ].value:  # and self._block[y][x].status != BlockStatus.FLAGGED:
            self._block[y][x].status = MineStatus.BOOMED
            return False

        # opened
        self._block[y][x].status = MineStatus.OPENED

        around = _get_around(x, y, self.width, self.height)

        _sum = 0
        for i, j in around:
            if self._block[j][i].value:
                _sum += 1

        self._block[y][x].around_mine_count = _sum

        # if no mine around, then open around 8 un-opened blocks recursively
        # thus to implment the effect of opening a whole area
        if _sum == 0:
            for i, j in around:
                if self._block[j][i].around_mine_count == -1:
                    self.open_mine(i, j)

        return True

    def double_mouse_button_down(self, x, y):
        if self._block[y][x].around_mine_count == 0:
            return True

        self._block[y][x].status = MineStatus.BOTH_BUTTON_CLICKING

        around = _get_around(x, y, self.width, self.height)

        sumflag = 0  # around mine count of marked
        for i, j in around:
            if self._block[j][i].status == MineStatus.FLAGGED:
                sumflag += 1

        # all mines around are marked
        result = True
        if sumflag == self._block[y][x].around_mine_count:
            for i, j in around:
                if self._block[j][i].status == MineStatus.INITIAL:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._block[j][i].status == MineStatus.INITIAL:
                    self._block[j][i].status = MineStatus.HINTING
        return result

    def double_mouse_button_up(self, x, y):
        self._block[y][x].status = MineStatus.OPENED
        around = _get_around(x, y, self.width, self.height)
        for i, j in around:
            if self._block[j][i].status == MineStatus.HINTING:
                self._block[j][i].status = MineStatus.INITIAL


def _get_around(x, y, width=30, height=16):
    """return all coordinates around (x, y)"""
    # note: range end is open interval, so add 1
    if x < 0 or y < 0 or x >= width or y >= height:
        return []

    return [
        (i, j)
        for i in range(max(0, x - 1), min(width - 1, x + 1) + 1)
        for j in range(max(0, y - 1), min(height - 1, y + 1) + 1)
        if i != x or j != y
    ]
