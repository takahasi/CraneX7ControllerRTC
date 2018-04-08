CraneX7ControllerRTC
====================

This is RT-Component(RTC) for CRANE-X7 (RT Corporation)

- RT Corporation製ロボットアーム CRANE-X7 を RTC 経由で操作することが可能
-- http://www.rt-net.jp/crane-x7/
-- 各関節は RBOTIS 製 Dynamixel モータがデイジーチェーン接続で利用されているため，PCからはUSBシリアルを通じて制御を行う

[![VIDEO](http://img.youtube.com/vi/UohZ_0gL7BM/0.jpg)](http://www.youtube.com/watch?v=UohZ_0gL7BM)
[![VIDEO](http://img.youtube.com/vi/qaLNA0zFO4k/0.jpg)](http://www.youtube.com/watch?v=qaLNA0zFO4k)

In Port
-------

|Name|Type|Note|
----|----|----
|joints | TimeFloatSeq [7] | 各Jointの値を入力することでアームを操作できる．関節J0~J6を順番に格納する．|
|grip | TimeOctet | グリッパの操作．(0: open, 1: close)|

Out Port
--------

|Name|Type|Note|
----|----|----
|status | TimedOctet | ロボットアームの動作モードを出力する (0: normal)．|
|out_joints |TimedFloatSeq [7] |  アクチュエータから取得できる関節の現在位置(deg)．関節J0~J6が順番に格納される．|
|out_vel | TimedFloatSeq [7] |   アクチュエータから取得できる関節の現在速度(deg/s)．関節J0~J6が順番に格納される．|
|out_cur | TimedFloatSeq [7] |  アクチュエータから取得できる現在電流値．関節J0~J6が順番に格納される．|
|out_tmp |TimedFloatSeq [7]  | アクチュエータら取得できるモータドライバの温度(℃)．関節J0~J6が順番に格納される．|
|is_moving| TimedBoolean|  アームが動作中情報が出力される． (動作中: True，停止状態: False)|

Configuration
-------------

|Name|Type|Default value|Note|
----|----|-------------|----
|device | string | /dev/ttyUSB0 | device file name of USB serial port |

Service Port
------------
ManipulatorCommonInterfaceIDL
- ManipulatorCommonInterface

|InterfaceName|Support|
----|----
|clearAlarms||
|getActiveAlarm|○|
|getFeedbackPosJoint|○|
|getManipInfo|○|
|getSoftLimitJoint|○|
|getState|○|
|servoOFF|○|
|servoON|○|
|setSoftLimitJoint||

- ManipulatorMiddleInterface

|InterfaceName|Support|
----|----
|closeGripper|○|
|getBaseOffset||
|getFeedBackPosCartesian||
|getMaxSpeedCartesian||
|getMaxSpeedJoint|○|
|getMinAccelTimeCartesian||
|getMinAccelTimeJoint||
|getSoftLimitCartesian||
|moveGripper|○|
|moveLinearCartesianAbs||
|moveLinearCartesianRel||
|movePTPJointAbs|○|
|movePTPJointRel|○|
|openGripper|○|
|pause|○|
|resume|○|
|stop|○|
|setAccelTimeJoint||
|setBaseOffset||
|setControlPointOffset||
|setMaxSpeedCartesian||
|setMaxSpeedJoint||
|setMinAccelTimeCartesian||
|setMinAccelTimeJoint||
|setSoftLimitCartesian||
|setSpeedCartesian||
|setSpeedJoint|○|
|moveCircularCartesianAbs||
|moveCircularCartesianRel||
|setHome|○|
|getHome|○|
|goHome|○|


Usage
=====

Preparation
-----------
- DynamixelSDK
```
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
```

Run
------
```
$ python CraneX7ControllerRTC.py
```

Unit Test
-----------
Connects actual URx robot via usb-serial
```
$ python test/test_robot.py
```
