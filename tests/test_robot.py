#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append(".")
sys.path.append("..")

from CraneX7Controller import CraneX7 as robot


__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "MIT License"


class TestRobot(unittest.TestCase):

    def setUp(self):
        self._r = robot()
        self._r.open()

    def tearDown(self):
        self._r.close()
        del self._r

    def test_home(self):
        self.assertTrue(self._r.home(sync=True))

    def test_pos(self):
        pos = self._r.pos()
        self.assertIsNotNone(pos)
        print("joints: " + str(pos))

    def test_moving(self):
        moving = self._r.moving()
        self.assertFalse(moving)
        print("joints: " + str(moving))

    def test_cur(self):
        cur = self._r.cur()
        self.assertIsNotNone(cur)
        print("current: " + str(cur))

    def test_vel(self):
        vel = self._r.vel()
        self.assertIsNotNone(vel)
        print("current: " + str(vel))

    def test_movej(self):
        ret = self._r.movej([-58.2, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6], sync=True)
        self.assertTrue(ret)
        ret = self._r.movej([-58.2, -13.1, 4.5, -140.5, -4.3, -21.8, -74.6], sync=True)
        self.assertTrue(ret)
        ret = self._r.movej([39.7, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6], sync=True)
        self.assertTrue(ret)
        ret = self._r.movej([-4.3, -15.1, 4.5, -140.5, -4.3, -21.8, -74.6], sync=True)
        self.assertTrue(ret)

    def test_open_gripper(self):
        ret = self._r.open_gripper(sync=True)
        self.assertTrue(ret)

    def test_close_gripper(self):
        ret = self._r.close_gripper(sync=True)
        self.assertTrue(ret)


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
