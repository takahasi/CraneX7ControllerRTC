#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file CraneX7ControllerRTC.py
 @brief RTC for CRANE-X7
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import ManipulatorCommonInterface_Common_idl
import ManipulatorCommonInterface_Middle_idl

# Import Service implementation class
# <rtc-template block="service_impl">
from ManipulatorCommonInterface_Common_idl_example import *
from ManipulatorCommonInterface_Middle_idl_example import *

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
cranex7controllerrtc_spec = ["implementation_id", "CraneX7ControllerRTC", 
		 "type_name",         "CraneX7ControllerRTC", 
		 "description",       "RTC for CRANE-X7", 
		 "version",           "1.0.0", 
		 "vendor",            "takahasi", 
		 "category",          "Manipulation", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class CraneX7ControllerRTC
# @brief RTC for CRANE-X7
# 
# 
class CraneX7ControllerRTC(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		joints_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_joints = RTC.TimedFloatSeq(*joints_arg)
		"""
		"""
		self._jointsIn = OpenRTM_aist.InPort("joints", self._d_joints)
		grip_arg = [None] * ((len(RTC._d_TimedOctet) - 4) / 2)
		self._d_grip = RTC.TimedOctet(*grip_arg)
		"""
		"""
		self._gripIn = OpenRTM_aist.InPort("grip", self._d_grip)
		is_moving_arg = [None] * ((len(RTC._d_TimedChar) - 4) / 2)
		self._d_is_moving = RTC.TimedChar(*is_moving_arg)
		"""
		"""
		self._is_movingOut = OpenRTM_aist.OutPort("is_moving", self._d_is_moving)
		out_joints_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_out_joints = RTC.TimedFloatSeq(*out_joints_arg)
		"""
		"""
		self._out_jointsOut = OpenRTM_aist.OutPort("out_joints", self._d_out_joints)
		out_velocity_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_out_velocity = RTC.TimedFloatSeq(*out_velocity_arg)
		"""
		"""
		self._out_velocityOut = OpenRTM_aist.OutPort("out_velocity", self._d_out_velocity)
		out_current_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_out_current = RTC.TimedFloatSeq(*out_current_arg)
		"""
		"""
		self._out_currentOut = OpenRTM_aist.OutPort("out_current", self._d_out_current)
		status_arg = [None] * ((len(RTC._d_TimedOctet) - 4) / 2)
		self._d_status = RTC.TimedOctet(*status_arg)
		"""
		"""
		self._statusOut = OpenRTM_aist.OutPort("status", self._d_status)

		"""
		"""
		self._sv_namePort = OpenRTM_aist.CorbaPort("sv_name")

		"""
		"""
		self._common = ManipulatorCommonInterface_Common_i()
		"""
		"""
		self._middle = ManipulatorCommonInterface_Middle_i()
		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("joints",self._jointsIn)
		self.addInPort("grip",self._gripIn)
		
		# Set OutPort buffers
		self.addOutPort("is_moving",self._is_movingOut)
		self.addOutPort("out_joints",self._out_jointsOut)
		self.addOutPort("out_velocity",self._out_velocityOut)
		self.addOutPort("out_current",self._out_currentOut)
		self.addOutPort("status",self._statusOut)
		
		# Set service provider to Ports
		self._sv_namePort.registerProvider("common", "JARA_ARM::ManipulatorCommonInterface_Common", self._common)
		self._sv_namePort.registerProvider("middle", "JARA_ARM::ManipulatorCommonInterface_Middle", self._middle)
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		self.addPort(self._sv_namePort)
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def CraneX7ControllerRTCInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=cranex7controllerrtc_spec)
    manager.registerFactory(profile,
                            CraneX7ControllerRTC,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    CraneX7ControllerRTCInit(manager)

    # Create a component
    comp = manager.createComponent("CraneX7ControllerRTC")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

