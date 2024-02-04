## Usage inside SONiC

```
# Download a matching libsai for your kernel driver
wget https://sonicstorage.blob.core.windows.net/public/sai/sai-broadcom/SAI_8.4.0_GA/8.4.0.2/xgs/libsaibcm_8.4.0.2_amd64.deb
wget https://sonicstorage.blob.core.windows.net/public/sai/sai-broadcom/SAI_8.4.0_GA/8.4.0.2/xgs/libsaibcm-dev_8.4.0.2_amd64.deb

sudo apt install g++ libthrift-dev make thrift-compiler libboost1.74-dev lz4 \
  ./libsaibcm*.deb
make

sudo mknod /dev/linux-user-bde c 126 0
sudo rmmod linux_knet_cb
sudo rmmod psample

# copy broadcom config to config.bcm and/or modifiy sai.profile to match
sudo ./saiserver -p sai.profile
```
