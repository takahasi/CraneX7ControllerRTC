#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ManipulatorCommonInterface_Middle_idl_examplefile.py
 @brief Python example implementations generated from ManipulatorCommonInterface_Middle.idl
 @date $Date$


"""

import omniORB
from omniORB import CORBA, PortableServer
import JARA_ARM
import JARA_ARM__POA

import ManipulatorCommonInterface_DataTypes_idl as DATATYPES_IDL
import ManipulatorCommonInterface_Common_idl as COMMON_IDL
import math

class ManipulatorCommonInterface_Middle_i (JARA_ARM__POA.ManipulatorCommonInterface_Middle):
    """
    @class ManipulatorCommonInterface_Middle_i
    Example class implementing IDL interface JARA_ARM.ManipulatorCommonInterface_Middle
    """

    def __init__(self):
        """
        @brief standard constructor
        Initialise member variables here
        """
        self._robot = None
        self._common = None
        self._home = [0.0 for i in range(7)]

        self.MIDDLE_IDL_STATE_NORMAL = 0
        self.MIDDLE_IDL_STATE_PAUSE = 1
        self.MIDDLE_IDL_STATE_STOP = 2
        self._middle_idl_state = self.MIDDLE_IDL_STATE_NORMAL
        pass

    def set_robot(self, robot):
        self._robot = robot

    def unset_robot(self):
        self._robot = None

    def set_common(self, common):
        self._common = common

    def unset_common(self):
        self._common = None

    # RETURN_ID closeGripper()
    def closeGripper(self):
        if self._robot:
            ret = self._robot.close_gripper()
            if ret is True:
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID getBaseOffset(out HgMatrix offset)
    def getBaseOffset(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, offset

    # RETURN_ID getFeedbackPosCartesian(out CarPosWithElbow pos)
    def getFeedbackPosCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, pos

    # RETURN_ID getMaxSpeedCartesian(out CartesianSpeed speed)
    def getMaxSpeedCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, speed

    # RETURN_ID getMaxSpeedJoint(out DoubleSeq speed)
    def getMaxSpeedJoint(self):
        max_speed = []
        if self._robot:
            for j in self._robot.j:
                max_speed.append(j._vlimit)
            return DATATYPES_IDL.make_return_id('OK', ''), max_speed
        else:
            return DATATYPES_IDL.make_return_id('NG', ''), max_speed

    # RETURN_ID getMinAccelTimeCartesian(out double aclTime)
    def getMinAccelTimeCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, aclTime

    # RETURN_ID getMinAccelTimeJoint(out double aclTime)
    def getMinAccelTimeJoint(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, aclTime

    # RETURN_ID getSoftLimitCartesian(out LimitValue xLimit, out LimitValue yLimit, out LimitValue zLimit)
    def getSoftLimitCartesian(self):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result, xLimit, yLimit, zLimit

    # RETURN_ID moveGripper(in ULONG angleRatio)
    def moveGripper(self, angleRatio):
        if self._robot:
            ret = self._robot.move_gripper(angleRatio)
            if ret is True:
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID moveLinearCartesianAbs(in CarPosWithElbow carPoint)
    def moveLinearCartesianAbs(self, carPoint):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID moveLinearCartesianRel(in CarPosWithElbow carPoint)
    def moveLinearCartesianRel(self, carPoint):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID movePTPCartesianAbs(in CarPosWithElbow carPoint)
    def movePTPCartesianAbs(self, carPoint):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID movePTPCartesianRel(in CarPosWithElbow carPoint)
    def movePTPCartesianRel(self, carPoint):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID movePTPJointAbs(in JointPos jointPoints)
    def movePTPJointAbs(self, jointPoints):
        if self._robot:
            ret = self._robot.movej(jointPoints)
            if ret is True:
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', 'invalid value')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID movePTPJointRel(in JointPos jointPoints)
    def movePTPJointRel(self, jointPoints):
        if self._robot:
            return DATATYPES_IDL.make_return_id('OK', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID openGripper()
    def openGripper(self):
        if self._robot:
            ret = self._robot.open_gripper()
            if ret is True:
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID pause()
    def pause(self):
        if self._middle_idl_state > 0:
            msg = 'robot is already pause or stop'
            return DATATYPES_IDL.make_return_id('OK', msg)

        if self._common:
            __, state = self._common.getState()

            if state & 0x01 == 0x00:
                return DATATYPES_IDL.make_return_id('NOT_SV_ON_ERR',
                                                    'Now Servo OFF')
            if state & 0x04 == 0x04:
                return DATATYPES_IDL.make_return_id('STATUS_ERROR',
                                                    'Now Alarm Occur')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

        if self._robot:
            # update state for robot
            self._robot.pause = True
            # update state
            self._middle_idl_state = self.MIDDLE_IDL_STATE_PAUSE
            return DATATYPES_IDL.make_return_id('OK', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID resume()
    def resume(self):
        if self._robot and \
           self._middle_idl_state == self.MIDDLE_IDL_STATE_PAUSE:
            self._robot.pause = False
            self._middle_idl_state = self.MIDDLE_IDL_STATE_NORMAL
            return DATATYPES_IDL.make_return_id('OK', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID stop()
    def stop(self):
        if self._common:
            __, state = self._common.getState()

            if state & 0x01 == 0x00:
                return DATATYPES_IDL.make_return_id('NOT_SV_ON_ERR',
                                                    'Now Servo OFF')
            if state & 0x04 == 0x04:
                return DATATYPES_IDL.make_return_id('STATUS_ERROR',
                                                    'Now Alarm Occur')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

        if self._robot:
            self._robot.pause = False
            self._middle_idl_state = self.MIDDLE_IDL_STATE_NORMAL
            return DATATYPES_IDL.make_return_id('OK', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID setAccelTimeCartesian(in double aclTime)
    def setAccelTimeCartesian(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setAccelTimeJoint(in double aclTime)
    def setAccelTimeJoint(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setBaseOffset(in HgMatrix offset)
    def setBaseOffset(self, offset):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setControlPointOffset(in HgMatrix offset)
    def setControlPointOffset(self, offset):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMaxSpeedCartesian(in CartesianSpeed speed)
    def setMaxSpeedCartesian(self, speed):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMaxSpeedJoint(in DoubleSeq speed)
    def setMaxSpeedJoint(self, speed):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMinAccelTimeCartesian(in double aclTime)
    def setMinAccelTimeCartesian(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setMinAccelTimeJoint(in double aclTime)
    def setMinAccelTimeJoint(self, aclTime):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSoftLimitCartesian(in LimitValue xLimit, in LimitValue yLimit, in LimitValue zLimit)
    def setSoftLimitCartesian(self, xLimit, yLimit, zLimit):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSpeedCartesian(in ULONG spdRatio)
    def setSpeedCartesian(self, spdRatio):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setSpeedJoint(in ULONG spdRatio)
    def setSpeedJoint(self, spdRatio):
        if self._robot:
            self._robot.set_prof_vel(spdRatio)
            return DATATYPES_IDL.make_return_id('OK', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')

    # RETURN_ID moveCircularCartesianAbs(in CarPosWithElbow carPointR, in CarPosWithElbow carPointT)
    def moveCircularCartesianAbs(self, carPointR, carPointT):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID moveCircularCartesianRel(in CarPosWithElbow carPointR, in CarPosWithElbow carPointT)
    def moveCircularCartesianRel(self, carPointR, carPointT):
        raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
        # *** Implement me
        # Must return: result

    # RETURN_ID setHome(in JointPos jointPoint)
    def setHome(self, jointPoint):
        self._home = jointPoint
        return DATATYPES_IDL.make_return_id('OK', '')

    # RETURN_ID getHome(out JointPos jointPoint)
    def getHome(self):
        return DATATYPES_IDL.make_return_id('OK', ''), self._home

    # RETURN_ID goHome()
    def goHome(self):
        if self._robot:
            ret = self._robot.movej(self._home)
            if ret is True:
                return DATATYPES_IDL.make_return_id('OK', '')
            else:
                return DATATYPES_IDL.make_return_id('NG', '')
        else:
            return DATATYPES_IDL.make_return_id('NG', '')


if __name__ == "__main__":
    import sys

    # Initialise the ORB
    orb = CORBA.ORB_init(sys.argv)

    # As an example, we activate an object in the Root POA
    poa = orb.resolve_initial_references("RootPOA")

    # Create an instance of a servant class
    servant = ManipulatorCommonInterface_Middle_i()

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
