#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ManipulatorCommonInterface_Common_idl_examplefile.py
 @brief Python example implementations generated from ManipulatorCommonInterface_Common.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import JARA_ARM
import JARA_ARM__POA

import ManipulatorCommonInterface_DataTypes_idl as DATATYPES_IDL
import ManipulatorCommonInterface_Common_idl as COMMON_IDL

class ManipulatorCommonInterface_Common_i (JARA_ARM__POA.ManipulatorCommonInterface_Common):
    """
    @class ManipulatorCommonInterface_Common_i
    Example class implementing IDL interface JARA_ARM.ManipulatorCommonInterface_Common
    """

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self._robot = None
        self._axisnum = 7
        self._middle = None
        pass

    def set_robot(self, robot):
        self._robot = robot

    def unset_robot(self):
        self._robot = None
        
    def _make_alarm(self, code, alarm_type, alarm_val):
        if alarm_type == "FAULT":
            alarm = COMMON_IDL._0_JARA_ARM.FAULT
        elif alarm_type == "WARNING":
            alarm = COMMON_IDL._0_JARA_ARM.WARNING
        else:
            alarm = COMMON_IDL._0_JARA_ARM.UNKNOWN

        if alarm_val is None:
            comment = '{:X}'.format(0)
        else:
            comment = '{:X}'.format(alarm_val)

        return COMMON_IDL._0_JARA_ARM.Alarm(code, alarm, comment)

    def _make_manipInfo(self, manu, name, num, cycle, isgripper):
        return COMMON_IDL._0_JARA_ARM.ManipInfo(manu, name, num, cycle, isgripper)

    def _make_limitValue(self, upper, lower):
        return DATATYPES_IDL._0_JARA_ARM.LimitValue(upper, lower)

    # RETURN_ID clearAlarms()
    def clearAlarms(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID getActiveAlarm(out AlarmSeq alarms)
    def getActiveAlarm(self):
        if self._robot:
            return DATATYPES_IDL.make_return_id('OK', ''),\
                [self._make_alarm(0xFFFFFFFF, 'WARNING', self._robot.err)]
        else:
            return DATATYPES_IDL.make_return_id('NG', ''), []

    # RETURN_ID getFeedbackPosJoint(out JointPos pos)
    def getFeedbackPosJoint(self):
        if self._robot:
            return DATATYPES_IDL.make_return_id('OK', ''), self._robot.pos
        else:
            return DATATYEPS_IDL.make_return_id('NG', ''), []

    # RETURN_ID getManipInfo(out ManipInfo mInfo)
    def getManipInfo(self):
        return DATATYPES_IDL.make_return_id('OK', ''),\
            self._make_manipInfo('RT CORPORATION',
                                 'Crane-X7',
                                 self._axisnum,
                                 1,
                                 True)

    # RETURN_ID getSoftLimitJoint(out LimitSeq softLimit)
    def getSoftLimitJoint(self):
        limit = []
        if self._robot and self._robot.j:
            for j in self._robot.j:
                limit.append(self._make_limitValue(j._max_pos, j._min_pos))
            return DATATYPES_IDL.make_return_id('OK', ''), limit
        else:
            return DATATYPES_IDL.make_return_id('NG', ''), limit

    # RETURN_ID getState(out ULONG state)
    def getState(self):
        if self._robot:
            state = 0x01
            # check toruqe enable
            for i in self._robot._torque_enable:
                if i is False:
                    state = 0x00
                    break
            # check moving
            if self._robot._moving:
                state |= 0x02

            # check alarm
            if self._robot._err != 0:
                state |= 0x04

            # buffer is not available

            # check pause
            if self._robot.pause is True:
                state |= 0x10

            return DATATYPES_IDL.make_return_id('OK', ''), state
        else:
            return DATATYPES_IDL.make_return_id('NG', ''), 0

    # RETURN_ID servoOFF()
    def servoOFF(self):
        if self._robot:
            if self._robot.servo_off():
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID servoON()
    def servoON(self):
        if self._robot:
            if self._robot.servo_on():
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID setSoftLimitJoint(in LimitSeq softLimit)
    def setSoftLimitJoint(self, softLimit):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result


if __name__ == "__main__":
    import sys

    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)

    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = ManipulatorCommonInterface_Common_i()

    # Activate it in the Root POA
    poa.activate_object(servant)

    # Get the object reference to the object
    objref = servant._this()

    # Print a stringified IOR for it
    print(orb.object_to_string(objref))

    # Activate the Root POA's manager
    poa._get_the_POAManager().activate()

    # Run the ORB, blocking this thread
    orb.run()
