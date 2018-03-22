#!/bin/bash

context="/localhost/takahashi-Parallels-Virtual-Platform.host_cxt"
rtc="CraneX7ControllerRTC0.rtc"
joints="$context/$rtc:joints"
grip="$context/$rtc:grip"

j0="[-58.2, 4.5, 4.5, -118.5, -4.3, -21.8, -74.6]"
j1="[-4.3, -15.1, 4.5, -140.5, -4.3, -21.8, -74.6]"
j2="[-58.2, -13.1, 4.5, -140.5, -4.3, -21.8, -74.6]"
g0=0
g1=1


echo "joints: $j0"
rtinject $joints -c "RTC.TimedFloatSeq({time}, $j0)"
echo "joints: $j1"
rtinject $joints -c "RTC.TimedFloatSeq({time}, $j1)"
echo "joints: $j2"
rtinject $joints -c "RTC.TimedFloatSeq({time}, $j2)"

echo "grip: $g0"
rtinject $grip -c "RTC.TimedOctet({time}, $g0)"
echo "grip: $g1"
rtinject $grip -c "RTC.TimedOctet({time}, $g1)"

exit 0
