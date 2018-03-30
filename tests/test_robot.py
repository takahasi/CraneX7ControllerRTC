#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import time
sys.path.append(".")
sys.path.append("..")

from CraneX7Controller import CraneX7 as robot


__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "MIT License"


class TestRobot(unittest.TestCase):
    up_pos = [-58.2, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6]
    down_pos = [-4.3, -15.1, 4.5, -140.5, -4.3, -21.8, -74.6]
    right_pos = [-58.2, -13.1, 4.5, -140.5, -4.3, -21.8, -74.6]
    left_pos = [39.7, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6]

    def setUp(self):
        self._r = robot()
        if not self._r.open():
            self._r = None
        time.sleep(1.5)

    def tearDown(self):
        if self._r:
            self._r.close()
            time.sleep(1.5)
            del self._r
            self._r = None

    def test_home(self):
        ret = self._r.movej(self.right_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.home(sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.right_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.down_pos, sync=True)
        self.assertTrue(ret)

    def test_pos(self):
        pos = self._r.pos
        self.assertTrue(len(pos) == 7)
        print("joints: " + str(pos))

    def test_moving(self):
        moving = self._r.moving
        self.assertFalse(moving)
        print("moving: " + str(moving))

    def test_cur(self):
        cur = self._r.cur
        self.assertTrue(len(cur) == 7)
        print("current: " + str(cur))

    def test_vel(self):
        vel = self._r.vel
        self.assertTrue(len(vel) == 7)
        print("velocity: " + str(vel))

    def test_tmp(self):
        tmp = self._r.tmp
        self.assertTrue(len(tmp) == 7)
        print("temperature: " + str(tmp))

    def test_err(self):
        err = self._r.err
        self.assertIsNotNone(err)
        print("error: " + str(err))

    def test_pickplace(self):
        ret = self._r.movej(self.up_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.open_gripper(sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.right_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.close_gripper(sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.left_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.open_gripper(sync=True)
        self.assertTrue(ret)
        ret = self._r.close_gripper(sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.down_pos, sync=True)
        self.assertTrue(ret)

    def test_movej(self):
        ret = self._r.movej(self.up_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.right_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.left_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.down_pos, sync=True)
        self.assertTrue(ret)

    def test_gripper(self):
        ret = self._r.movej(self.up_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.open_gripper(sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.right_pos, sync=True)
        self.assertTrue(ret)
        ret = self._r.close_gripper(sync=True)
        self.assertTrue(ret)
        ret = self._r.movej(self.down_pos, sync=True)
        self.assertTrue(ret)


def test():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    test()
