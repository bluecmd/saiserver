# Usage inside SONiC

```
# Download a matching libsai for your kernel driver
wget https://sonicstorage.blob.core.windows.net/public/sai/sai-broadcom/SAI_8.4.0_GA/8.4.0.2/xgs/libsaibcm_8.4.0.2_amd64.deb
wget https://sonicstorage.blob.core.windows.net/public/sai/sai-broadcom/SAI_8.4.0_GA/8.4.0.2/xgs/libsaibcm-dev_8.4.0.2_amd64.deb

sudo apt install g++ libthrift-dev make thrift-compiler libboost1.74-dev lz4 \
  ./libsaibcm*.deb
make

sudo systemctl stop syncd
sudo mknod /dev/linux-user-bde c 126 0
sudo rmmod linux_knet_cb
sudo rmmod psample

# copy broadcom config to config.bcm and/or modifiy sai.profile to match
sudo ./saiserver -p sai.profile
```

## Example run

```
admin@sonic:~/saiserver$ sudo ./saiserver -p sai.profile 
profile map file: sai.profile
insert: SAI_INIT_CONFIG_FILE:config.bcm
resetting profile map iteratorkey: SAI_INIT_CONFIG_FILE:config.bcmiterator reached endFound 0 devices.
linux-user-bde:new probed device unit 0 dev_no 0 _ndevices 1
DMA pool size: 33554432 bytes.
BDE dev 0 (PCI), Dev 0xb873, Rev 0x01, Chip BCM56873_A0, Driver BCM56870_A0
SOC unit 0 attached to PCI device BCM56873_A0
rc: unit 0 device BCM56873_A0
0:soc_trident3_chip_reset: TS_PLL locked on unit 0 using 50.0MHz external reference clock
Recommended to add "ptp_ts_pll_fref=50000000" config variable
0:soc_trident3_chip_reset: BS_PLL0 locked on unit 0 using 50.0MHz external reference clock
Recommended to add "ptp_bs_fref_0=50000000" config variable
0:soc_trident3_chip_reset: BS_PLL1 locked on unit 0 using 50.0MHz external reference clock
Recommended to add "ptp_bs_fref_1=50000000" config variable
UNIT0 CANCUN: 
        CIH: LOADED
        Ver: 06.04.01
        Bug fix rev: 1

        CMH: LOADED
        Ver: 06.04.01
        Bug fix rev: 1
        SDK Ver: 06.05.27

        CCH: LOADED
        Ver: 06.04.01
        Bug fix rev: 1
        SDK Ver: 06.05.27

        CEH: LOADED
        Ver: 06.04.01
        Bug fix rev: 1
        SDK Ver: 06.05.27

rc: MMU initialized
*** unit 0: ports capable of limited speed range cut-thru
ALPM Distributed HITBIT thread enabled (interval 1000000 us)
*** unit 0: alpm forwarding level 2 loaded: 4 banks in combined-128 
0:bcmi_xgs5_bfd_init: uKernel BFD application not available
0:bcm_xgs5_telemetry_eapp_init: uKernel Telemetry application not available
0:bcm_esw_ifa_init: uKernel IFA application not available
rc: L2 Table shadowing enabled
rc: Port modes initialized
rc: platform SDK init complete
Starting SAI RPC server on port Hit enter to get drivshell prompt..
9092
create pthread switch_sai_thrift_rpc_server_thread result 0
detach switch_sai_thrift_rpc_server_thread rc0

Enter 'quit' to exit the application.
drivshell>
drivshell>ps
                 ena/        speed/ link auto    STP                  lrn  inter   max   cut   loop        
           port  link  Lns   duplex scan neg?   state   pause  discrd ops   face frame  thru?  back   encap
       xe0( 49)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe1( 50)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe2( 51)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe3( 52)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe4( 57)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe5( 58)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe6( 59)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe7( 60)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe8( 61)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       xe9( 62)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe10( 63)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe11( 64)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe12( 79)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe13( 80)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe14( 81)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe15( 82)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe16( 87)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe17( 88)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe18( 89)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe19( 90)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe20( 95)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe21( 96)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe22( 97)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe23( 98)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe24( 13)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe25( 14)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe26( 15)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe27( 16)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe28( 21)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe29( 22)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe30( 23)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe31( 24)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe32( 29)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe33( 30)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe34( 31)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe35( 32)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe36( 99)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe37(100)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe38(101)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe39(102)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe40(107)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe41(108)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe42(109)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe43(110)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe44(115)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe45(116)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe46(117)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
      xe47(118)  !ena   1   25G  FD   SW  No   Forward          None   FA     CR  9412    No          IEEE
       ce0( 67)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce1( 71)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce2(123)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce3(127)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce4(  1)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce5( 33)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce6(  5)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
       ce7( 41)  !ena   4  100G  FD   SW  No   Forward          None   FA    CR4  9412    No          IEEE
drivshell>
```
