#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import threading
import trollius as asyncio
import dynamixel_functions as dxl

__author__ = "Saburo Takahashi"
__copyright__ = "Copyright 2017, Saburo Takahashi"
__license__ = "MIT License"


class ControlTable():
    def __init__(self, address, byte):
        self.address = address
        self.byte = byte


class CraneX7Joint(object):
    # Control table address (Dynamixel-MX430/540)
    VELOCITY_LIMIT = ControlTable(44, 4)
    MAX_POSITION_LIMIT = ControlTable(48, 4)
    MIN_POSITION_LIMIT = ControlTable(52, 4)
    TORQUE_ENABLE = ControlTable(64, 1)
    HARDWARE_ERROR_STATUS = ControlTable(70, 1)
    POSITION_IGAIN = ControlTable(82, 2)
    POSITION_PGAIN = ControlTable(84, 2)
    PROFILE_ACCELERATION = ControlTable(108, 4)
    PROFILE_VELOCITY = ControlTable(112, 4)
    GOAL_POSITION = ControlTable(116, 4)
    MOVING = ControlTable(122, 1)
    PRESENT_CURRENT = ControlTable(126, 2)
    PRESENT_VELOCITY = ControlTable(128, 4)
    PRESENT_POSITION = ControlTable(132, 4)
    PRESENT_TEMPERATURE = ControlTable(146, 1)

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
        self._tmp = 0
        self._err = 0

        self._vlimit = self.vel_limit
        self._max_pos = self.max_pos
        self._min_pos = self.min_pos

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

    def _read_dxl(self, control_table):
        if control_table.byte == 4:
            val = dxl.read4ByteTxRx(self.port,
                                    self.PROTOCOL_VERSION,
                                    self.id,
                                    control_table.address)
        elif control_table.byte == 2:
            val = dxl.read2ByteTxRx(self.port,
                                    self.PROTOCOL_VERSION,
                                    self.id,
                                    control_table.address)
        else:
            val = dxl.read1ByteTxRx(self.port,
                                    self.PROTOCOL_VERSION,
                                    self.id,
                                    control_table.address)
        self._get_dxl_result()
        return val

    def _write_dxl(self, control_table, value):
        if control_table.byte == 4:
            dxl.write4ByteTxRx(self.port,
                               self.PROTOCOL_VERSION,
                               self.id,
                               control_table.address,
                               value)
        elif control_table.byte == 2:
            dxl.write2ByteTxRx(self.port,
                               self.PROTOCOL_VERSION,
                               self.id,
                               control_table.address,
                               value)
        else:
            dxl.write1ByteTxRx(self.port,
                               self.PROTOCOL_VERSION,
                               self.id,
                               control_table.address,
                               value)
        return self._get_dxl_result()

    def _torque(self, on_off):
        # Control Dynamixel Torque
        return self._write_dxl(self.TORQUE_ENABLE, on_off)

    def torque_on(self):
        # Enable Dynamixel Torque
        self._torque(1)
        # Default parameters
        if self._name == "hand":
            # hand settings
            self.pgain = 200
            self.igain = 20
            self.prof_acc = 10
            self.prof_vel = 20
        else:
            # joint settings
            self.pgain = 150
            self.igain = 20
            self.prof_acc = 50
            self.prof_vel = 200

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
            self._write_dxl(self.GOAL_POSITION, p)
            return True

    def pos2deg(self, pos):
        return int((pos * 360.0 / 4096.0) - 180.0)

    def deg2pos(self, deg):
        return int((deg + 180.0) / (360.0 / 4096.0))

    @property
    def torque(self):
        # Read torque on/off
        return self._read_dxl(self.TORQUE_ENABLE)

    @property
    def vel_limit(self):
        # Read velocity limit
        return self._read_dxl(self.VELOCITY_LIMIT)

    @property
    def pgain(self):
        # Read position P gain
        return self._read_dxl(self.POSITION_PGAIN)

    @pgain.setter
    def pgain(self, val):
        # Write position P gain
        self._write_dxl(self.POSITION_PGAIN, val)

    @property
    def igain(self):
        # Read position I gain
        return self._read_dxl(self.POSITION_IGAIN)

    @igain.setter
    def igain(self, val):
        # Write position I gain
        self._write_dxl(self.POSITION_IGAIN, val)

    @property
    def prof_acc(self):
        # Read acc profile
        return self._read_dxl(self.PROFILE_ACCELERATION)

    @prof_acc.setter
    def prof_acc(self, acc):
        # Write acc profile
        # 0-40 (unit=214.577[rev/min2])
        self._write_dxl(self.PROFILE_ACCELERATION, acc)

    @property
    def prof_vel(self):
        # Read velocity profile
        return self._read_dxl(self.PROFILE_VELOCITY)

    @prof_vel.setter
    def prof_vel(self, vel):
        # Write velocity profile
        # 0-44 (unit=0.229[RPM])
        self._write_dxl(self.PROFILE_VELOCITY, vel)

    @property
    def pos(self):
        # Read present position
        self._pos = self._read_dxl(self.PRESENT_POSITION)
        self._get_dxl_result()
        return self._pos

    @property
    def pos_in_deg(self):
        # Read present position
        self._pos = self._read_dxl(self.PRESENT_POSITION)
        self._get_dxl_result()
        return self.pos2deg(self._pos)

    @property
    def vel(self):
        # Read present velocity
        self._vel = self._read_dxl(self.PRESENT_VELOCITY)
        self._get_dxl_result()
        return self._vel

    @property
    def cur(self):
        # Read present current
        self._cur = self._read_dxl(self.PRESENT_CURRENT)
        self._get_dxl_result()
        return self._cur

    @property
    def tmp(self):
        # Read present temperature
        self._tmp = self._read_dxl(self.PRESENT_TEMPERATURE)
        self._get_dxl_result()
        return self._tmp

    @property
    def moving(self):
        # Read moving
        self._moving = self._read_dxl(self.MOVING)
        self._get_dxl_result()
        return self._moving

    @property
    def err(self):
        # Read hardware error status
        self._tmp = self._read_dxl(self.HARDWARE_ERROR_STATUS)
        self._get_dxl_result()
        return self._tmp

    @property
    def max_pos(self):
        # Read max position limit
        return self._read_dxl(self.MAX_POSITION_LIMIT)

    @property
    def min_pos(self):
        # Read min position limit
        return self._read_dxl(self.MIN_POSITION_LIMIT)

    @property
    def max_pos_in_deg(self):
        # Read max position limit
        return self.pos2deg(self._read_dxl(self.MAX_POSITION_LIMIT))

    @property
    def min_pos_in_deg(self):
        # Read min position limit
        return self.pos2deg(self._read_dxl(self.MIN_POSITION_LIMIT))


class CraneX7(object):
    # move end threshold in degree
    MOVE_THRESHOLD = 3

    # move offset for open/close gripper in degree
    GRIPPER_OFFSET = 5

    def __init__(self, device="/dev/ttyUSB0".encode('utf-8'),
                 baudrate=3000000):
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s',
                            level=logging.INFO)
        self._port = None
        self._device = device
        self._baudrate = baudrate
        self.j = None
        self.hand = None
        self._lock = threading.Lock()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._is_opened = False

        self._pos = None
        self._pos_hand = None
        self._vel = None
        self._cur = None
        self._tmp = None
        self._moving = None
        self._err = None
        self._all_prof_vel = None
        self._torque_enable = None

        # home position as 0
        self._home_pos_joints = [0 for x in range(7)]

        self._pause = False

    def loop_thread(self):
        self._loop.call_soon(self._open)
        self._loop.call_later(0.01, self._status_updater, self._loop)
        self._loop.run_forever()

    def open(self):
        if self._port:
            # already opened
            return True

        self._thread = threading.Thread(target=self.loop_thread)
        self._thread.setDaemon(True)
        self._thread.start()
        return True

    def _open(self):
        try:
            self._port = dxl.portHandler(self._device)
            dxl.packetHandler()
        except Exception as e:
            logging.error(e)
            self._port = None
            return False

        if not dxl.openPort(self._port):
            logging.error("Failed to open the port!")
            self._port = None
            return False

        # Set port baudrate
        if not dxl.setBaudRate(self._port, self._baudrate):
            logging.error("Failed to change the baudrate!")
            dxl.closePort(self._port)
            self._port = None
            return False

        # Initialize joint setting
        self.j = list()
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

        # get gripper piosition (offsets to prevent crash)
        self._close_pos_hand = self.hand.min_pos_in_deg + self.GRIPPER_OFFSET
        self._open_pos_hand = self.hand.max_pos_in_deg - self.GRIPPER_OFFSET

        self._is_opened = True

        return True

    def close(self):
        self._loop.call_soon(self._close)
        self._loop.stop()
        return True

    def _close(self):
        if self.j:
            for j in self.j:
                j.torque_off()
                del j
            self.j = None

        if self.hand:
            self.hand.torque_off()
            del self.hand
            self.hand = None

        if self._port:
            # Close port
            dxl.closePort(self._port)
            self._port = None

        self._is_opened = False
        return True

    def _wait_for_reach_joints(self, goals, count=20):
        # wait until reach goal or timeout (expire count)
        for i in range(count):
            match = 0
            for i, j in enumerate(self.j):
                if abs(goals[i] - self._pos[i]) < self.MOVE_THRESHOLD:
                    match += 1
                    if match == 7:
                        logging.info("Reach goal position")
                        return True
                time.sleep(0.01)
        logging.warn("timeout: not yet reach goal position " + str(self.pos))
        return False

    def _wait_for_reach_hand(self, goal, count=150):
        # wait until reach goal or timeout (expire count)
        for i in range(count):
            if abs(goal - self._pos_hand) < self.MOVE_THRESHOLD:
                logging.info("Reach goal position")
                return True
            time.sleep(0.01)
        logging.warn("timeout: not yet reach goal position " + str(self.hand.pos_in_deg))
        return False

    def home(self, sync=False):
        logging.info("move home")
        if not self.j:
            logging.error("move home: not yet initialized")
            return False
        self._loop.call_soon(self._home)
        if sync:
            # wait until reach goal or timeout (expire count)
            self._wait_for_reach_joints(self._home_pos_joints, count=100)
        return True

    def _home(self):
        with self._lock:
            for i, j in enumerate(self.j):
                if not j.move(self._home_pos_joints[i]):
                    logging.error("move j[" + str(i) + "]: cannot move")
                    return False
        return True

    def movej(self, pos, sync=False):
        logging.info("movej [deg]: " + str(pos))
        if not self.j:
            logging.error("movej: not yet initialized")
            return False
        if self._pause is True:
            logging.error("movej: now state is pause")
            return False
        self._loop.call_soon(self._movej, pos)
        if sync:
            # wait until reach goal or timeout (expire count)
            self._wait_for_reach_joints(pos)
        return True

    def _movej(self, pos):
        with self._lock:
            for i, j in enumerate(self.j):
                if not j.move(pos[i]):
                    logging.error("move j[" + str(i) + "]: cannot move")
                    return False
        return True

    def open_gripper(self, sync=False):
        logging.info("open gripper: sync=" + str(sync))
        if not self.hand:
            logging.error("gripper: not yet initialized")
            return False
        self._loop.call_soon(self._open_gripper, sync)
        if sync:
            # wait until reach goal or timeout (expire count)
            self._wait_for_reach_hand(self._open_pos_hand)
        return True

    def _open_gripper(self, sync=False):
        with self._lock:
            self.hand.move(self._open_pos_hand)
        return True

    def close_gripper(self, sync=False):
        logging.info("close gripper: sync=" + str(sync))
        if not self.hand:
            logging.error("gripper: not yet initialized")
            return False
        self._loop.call_soon(self._close_gripper)
        if sync:
            # wait until reach goal or timeout (expire count)
            self._wait_for_reach_hand(self._close_pos_hand)
        return True

    def _close_gripper(self):
        with self._lock:
            self.hand.move(self._close_pos_hand)
        return True

    def move_gripper(self, ratio=0, sync=False):
        logging.info("move gripper: sync=" + str(sync))
        if not self.hand:
            logging.error("gripper: not yet initialized")
            return False

        pos = self._open_pos_hand * ratio / 100.0

        self._loop.call_soon(self._move_gripper, pos)
        if sync:
            # wait until reach goal or timeout (expire count)
            self._wait_for_reach_hand(pos)
        return True

    def _move_gripper(self, pos=0):
        with self._lock:
            self.hand.move(pos)
        return True

    def servo_on(self):
        logging.info("servo on")
        if not self.j:
            logging.error("joint: not yet initialized")
            return False
        self._loop.call_soon(self._servo_on)
        return True

    def _servo_on(self):
        with self._lock:
            for i, j in enumerate(self.j):
                if not j._torque(1):
                    return False
            return True

    def servo_off(self):
        logging.info("servo off")
        if not self.j:
            logging.error("joint: not yet initialized")
            return False
        self._loop.call_soon(self._servo_off)
        return True

    def _servo_off(self):
        with self._lock:
            for i, j in enumerate(self.j):
                if not j._torque(0):
                    return False
            return True

    def set_prof_vel(self, ratio):
        logging.info("call set_prof_vel")
        if not self.j:
            logging.error("set_prof_vel: not yet initialized")
            return False
        self._loop.call_soon(self._set_prof_vel, ratio)
        return True

    def _set_prof_vel(self, ratio):
        with self._lock:
            for i, j in enumerate(self.j):
                j.prof_vel = int(j._vlimit * ratio / 100.0)
        return True

    def _status_updater(self, loop):
        if not self.j:
            return

        pos = list()
        with self._lock:
            for j in self.j:
                pos.append(j.pos_in_deg)
        self._pos = pos

        with self._lock:
            self._pos_hand = self.hand.pos_in_deg

        vel = list()
        with self._lock:
            for j in self.j:
                vel.append(j.vel)
        self._vel = vel

        cur = list()
        with self._lock:
            for j in self.j:
                cur.append(j.cur)
        self._cur = cur

        tmp = list()
        with self._lock:
            for j in self.j:
                tmp.append(j.tmp)
        self._tmp = tmp

        moving = False
        with self._lock:
            for j in self.j:
                moving |= j.moving
        if moving:
            self._moving = True
        else:
            self._moving = False

        err = 0
        with self._lock:
            for j in self.j:
                err |= j.err
        self._err = err

        prof_vel = list()
        with self._lock:
            for j in self.j:
                prof_vel.append(j.prof_vel)
        self._all_prof_vel = prof_vel

        torque_enable = list()
        with self._lock:
            for j in self.j:
                torque_enable.append(j.torque)
        self._torque_enable = torque_enable

        loop.call_later(0.01, self._status_updater, loop)

    @property
    def pos(self):
        return self._pos

    @property
    def vel(self):
        return self._vel

    @property
    def cur(self):
        return self._cur

    @property
    def tmp(self):
        return self._tmp

    @property
    def moving(self):
        return self._moving

    @property
    def err(self):
        return self._err

    @property
    def is_opened(self):
        return self._is_opened

    @property
    def all_prof_vel(self):
        return self._all_prof_vel

    @property
    def pause(self):
        return self._pause

    @pause.setter
    def pause(self, boolean):
        self._pause = boolean

if __name__ == '__main__':
    c = CraneX7()
    c.open()
    c.close()
    del c
