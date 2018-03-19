#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import dynamixel_functions as dxl

__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "MIT License"


class CraneX7Joint(object):
    # Control table address (Dynamixel-MX430/540)
    ADDR_MAX_POSITION_LIMIT = 48
    ADDR_MIN_POSITION_LIMIT = 52
    ADDR_TORQUE_ENABLE = 64
    ADDR_POSITION_IGAIN = 82
    ADDR_POSITION_PGAIN = 84
    ADDR_PROFILE_ACCELERATION = 108
    ADDR_PROFILE_VELOCITY = 112
    ADDR_GOAL_POSITION = 116
    ADDR_MOVING = 122
    ADDR_PRESENT_CURRENT = 126
    ADDR_PRESENT_VELOCITY = 128
    ADDR_PRESENT_POSITION = 132

    # Communication definitions
    PROTOCOL_VERSION = 2

    def __init__(self, name, mid, port):
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)
        self.id = mid
        self.port = port
        self._name = name
        self._moving = False
        self._pos = 0
        self._cur = 0
        self._vel = 0

    def _get_dxl_result(self):
        COMM_SUCCESS = 0
        result = dxl.getLastTxRxResult(self.port,
                                       self.PROTOCOL_VERSION)
        err = dxl.getLastRxPacketError(self.port,
                                       self.PROTOCOL_VERSION)
        if result != COMM_SUCCESS:
            logging.error(dxl.getTxRxResult(self.PROTOCOL_VERSION, result))
            return False
        elif err != 0:
            logging.error(dxl.getRxPacketError(self.PROTOCOL_VERSION, err))
            return False
        else:
            return True

    def _read_dxl(self, byte, address):
        if byte == 4:
            val = dxl.read4ByteTxRx(self.port,
                                    self.PROTOCOL_VERSION,
                                    self.id,
                                    address)
        elif byte == 2:
            val = dxl.read2ByteTxRx(self.port,
                                    self.PROTOCOL_VERSION,
                                    self.id,
                                    address)
        else:
            val = dxl.read1ByteTxRx(self.port,
                                    self.PROTOCOL_VERSION,
                                    self.id,
                                    address)
        self._get_dxl_result()
        return val

    def _write_dxl(self, byte, address, value):
        if byte == 4:
            dxl.write4ByteTxRx(self.port,
                               self.PROTOCOL_VERSION,
                               self.id,
                               address,
                               value)
        elif byte == 2:
            dxl.write2ByteTxRx(self.port,
                               self.PROTOCOL_VERSION,
                               self.id,
                               address,
                               value)
        else:
            dxl.write1ByteTxRx(self.port,
                               self.PROTOCOL_VERSION,
                               self.id,
                               address,
                               value)
        return self._get_dxl_result()

    def _torque(self, on_off):
        # Control Dynamixel Torque
        return self._write_dxl(1,
                               self.ADDR_TORQUE_ENABLE,
                               on_off)

    def torque_on(self):
        # Enable Dynamixel Torque
        self._torque(1)
        # Default parameters
        self.pgain = 100
        self.igain = 20
        self.prof_acc = 10
        self.prof_vel = 30

    def torque_off(self):
        # Disable Dynamixel Torque
        self._torque(0)

    def move(self, pos):
        p = self.deg2pos(pos)
        if p > self.max_pos:
            logging.error("joint[" + str(self._name) + "] cannot move: " + str(pos))
            return False
        elif p <= self.min_pos:
            logging.error("joint[" + str(self._name) + "] cannot move: " + str(pos))
            return False
        else:
            # Write goal position
            logging.info("joint[" + str(self._name) + "] move: " + str(p))
            self._write_dxl(4, self.ADDR_GOAL_POSITION, p)
            return True

    def pos2deg(self, pos):
        return int((pos * 360.0 / 4096.0) - 180.0)

    def deg2pos(self, deg):
        return int((deg + 180.0) / (360.0 / 4096.0))

    @property
    def pgain(self):
        # Read position P gain
        return self._read_dxl(2, self.ADDR_POSITION_PGAIN)

    @pgain.setter
    def pgain(self, val):
        # Write position P gain
        self._write_dxl(2, self.ADDR_POSITION_PGAIN, val)

    @property
    def igain(self):
        # Read position I gain
        return self._read_dxl(2, self.ADDR_POSITION_IGAIN)

    @igain.setter
    def igain(self, val):
        # Write position I gain
        self._write_dxl(2, self.ADDR_POSITION_IGAIN, val)

    @property
    def prof_acc(self):
        # Read acc profile
        return self._read_dxl(4, self.ADDR_PROFILE_ACCELERATION)

    @prof_acc.setter
    def prof_acc(self, acc):
        # Write acc profile
        # 0-40 (unit=214.577[rev/min2])
        self._write_dxl(4, self.ADDR_PROFILE_ACCELERATION, acc)

    @property
    def prof_vel(self):
        # Read velocity profile
        return self._read_dxl(4, self.ADDR_PROFILE_VELOCITY)

    @prof_vel.setter
    def prof_vel(self, vel):
        # Write velocity profile
        # 0-44 (unit=0.229[RPM])
        self._write_dxl(4, self.ADDR_PROFILE_ACCELERATION, vel)

    @property
    def pos(self):
        # Read present position
        self._pos = self._read_dxl(4, self.ADDR_PRESENT_POSITION)
        self._get_dxl_result()
        return self._pos

    @property
    def pos_in_deg(self):
        # Read present position
        self._pos = self._read_dxl(4, self.ADDR_PRESENT_POSITION)
        self._get_dxl_result()
        return self.pos2deg(self._pos)

    @property
    def vel(self):
        # Read present velocity
        self._vel = self._read_dxl(4, self.ADDR_PRESENT_VELOCITY)
        self._get_dxl_result()
        return self._vel

    @property
    def cur(self):
        # Read present current
        self._cur = self._read_dxl(4, self.ADDR_PRESENT_CURRENT)
        self._get_dxl_result()
        return self._cur

    @property
    def moving(self):
        # Read moving
        self._moving = self._read_dxl(1, self.ADDR_MOVING)
        self._get_dxl_result()
        return self._moving

    @property
    def max_pos(self):
        # Read max position limit
        return self._read_dxl(4, self.ADDR_MAX_POSITION_LIMIT)

    @property
    def min_pos(self):
        # Read min position limit
        return self._read_dxl(4, self.ADDR_MIN_POSITION_LIMIT)

    @property
    def max_pos_in_deg(self):
        # Read max position limit
        return self.pos2deg(self._read_dxl(4, self.ADDR_MAX_POSITION_LIMIT))

    @property
    def min_pos_in_deg(self):
        # Read min position limit
        return self.pos2deg(self._read_dxl(4, self.ADDR_MIN_POSITION_LIMIT))


class CraneX7(object):
    # gap threshold in move
    MOVE_THRESHOLD = 3

    def __init__(self, device="/dev/ttyUSB0".encode('utf-8'),
                 baudrate=3000000):
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)
        self._port = None
        self._device = device
        self._baudrate = baudrate
        self.j = list()
        self.hand = None

    def open(self):
        self._port = dxl.portHandler(self._device)
        dxl.packetHandler()
        if not dxl.openPort(self._port):
            logging.error("Failed to open the port!")
            return False

        # Set port baudrate
        if not dxl.setBaudRate(self._port, self._baudrate):
            logging.error("Failed to change the baudrate!")
            return False

        # Initialize joint setting
        self.j.append(CraneX7Joint("link1", 2, self._port))
        self.j.append(CraneX7Joint("link2", 3, self._port))
        self.j.append(CraneX7Joint("link3", 4, self._port))
        self.j.append(CraneX7Joint("link4", 5, self._port))
        self.j.append(CraneX7Joint("link5", 6, self._port))
        self.j.append(CraneX7Joint("link6", 7, self._port))
        self.j.append(CraneX7Joint("link7", 8, self._port))
        self.hand = CraneX7Joint("hand", 9, self._port)

        for j in self.j:
            j.torque_on()
        self.hand.torque_on()
        self.hand.pgain = 200
        return True

    def close(self):
        for j in self.j:
            j.torque_off()
        self.hand.torque_off()

        if self._port:
            # Close port
            for j in self.j:
                del j
            del self.hand
            dxl.closePort(self._port)
            self._port = None

    def home(self, sync=False):
        pos = 0
        logging.info("move home")
        for i, j in enumerate(self.j):
            if not j.move(pos):
                logging.error("move j[" + str(i) + "]: cannot move")
                return False
        if sync:
            for i in range(100):
                match = 0
                for i, j in enumerate(self.j):
                    if abs(pos - j.pos_in_deg) < self.MOVE_THRESHOLD:
                        match += 1
                if match == 7:
                    logging.info("Reach goal position")
                    return True
            logging.warn("timeout: not yet reach goal position " + str(self.pos))
        return True

    def movej(self, pos, sync=False):
        logging.info("movej [deg]: " + str(pos))
        for i, j in enumerate(self.j):
            if not j.move(pos[i]):
                logging.error("move j[" + str(i) + "]: cannot move")
                return False
        if sync:
            for i in range(20):
                match = 0
                for i, j in enumerate(self.j):
                    if abs(pos[i] - j.pos_in_deg) < self.MOVE_THRESHOLD:
                        match += 1
                if match == 7:
                    logging.info("Reach goal position")
                    return True
            logging.warn("timeout: not yet reach goal position " + str(self.pos))
        return True

    def open_gripper(self, sync=False):
        logging.info("open gripper")
        open_pos = self.hand.max_pos_in_deg - 5
        self.hand.move(open_pos)
        if sync:
            for i in range(150):
                if abs(open_pos - self.hand.pos_in_deg) < self.MOVE_THRESHOLD:
                    logging.info("Reach goal position")
                    return True
            logging.warn("timeout: not yet reach goal position " + str(open_pos))
        return True

    def close_gripper(self, sync=False):
        logging.info("close gripper")
        close_pos = self.hand.min_pos_in_deg + 5
        self.hand.move(close_pos)
        if sync:
            for i in range(100):
                if abs(close_pos - self.hand.pos_in_deg) < self.MOVE_THRESHOLD:
                    logging.info("Reach goal position")
                    return True
            logging.warn("timeout: not yet reach goal position " + str(close_pos))
        return True

    @property
    def pos(self):
        self._pos = list()
        for j in self.j:
            self._pos.append(j.pos_in_deg)
        return self._pos

    @property
    def vel(self):
        self._vel = list()
        for j in self.j:
            self._vel.append(j.vel)
        return self._vel

    @property
    def cur(self):
        self._cur = list()
        for j in self.j:
            self._cur.append(j.cur)
        return self._cur

    @property
    def moving(self):
        for j in self.j:
            if j.moving:
                return True
        return False


if __name__ == '__main__':
    c = CraneX7()
    c.open()
    c.home(sync=True)
    time.sleep(1)
    print("joints: " + str(c.pos))
    print("joints: " + str(c.pos))
    print("move: " + str(c.moving))
    print("current: " + str(c.cur))
    print("velocity: " + str(c.vel))
    c.movej([-58.2, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6], sync=True)
    c.open_gripper(sync=True)
    c.close_gripper(sync=True)
    c.movej([-58.2, -13.1, 4.5, -140.5, -4.3, -21.8, -74.6], sync=True)
    print("joints: " + str(c.pos))
    print("joints: " + str(c.pos))
    print("move: " + str(c.moving))
    print("current: " + str(c.cur))
    print("velocity: " + str(c.vel))
    c.movej([39.7, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6])
    print("joints: " + str(c.pos))
    print("move: " + str(c.moving))
    print("current: " + str(c.cur))
    print("velocity: " + str(c.vel))
    time.sleep(3)
    c.open_gripper(sync=False)
    time.sleep(2)
    c.close_gripper(sync=False)
    time.sleep(2)
    c.movej([-4.3, -15.1, 4.5, -140.5, -4.3, -21.8, -74.6], sync=True)
    print("joints: " + str(c.pos))
    print("move: " + str(c.moving))
    print("current: " + str(c.cur))
    print("velocity: " + str(c.vel))
    time.sleep(2)
    print("joints: " + str(c.pos))
    print("move: " + str(c.moving))
    print("current: " + str(c.cur))
    print("velocity: " + str(c.vel))
    print("joints: " + str(c.pos))
    time.sleep(1)
    c.close()
