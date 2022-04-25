Commands to get the Arduino IDE working under Ubuntu (21.10)

```shell
# install IDE
sudo apt install arduino
# add user to needed groups
sudo usermod -aG dialout $USER
sudo usermod -aG tty $USER
# start a new login shell to dodge logging out
sudo -u $USER -i
# hack around broken Ubuntu package https://bugs.launchpad.net/ubuntu/+source/arduino/+bug/1916278
sudo apt install libserialport0 patchelf
sudo patchelf --add-needed /usr/lib/x86_64-linux-gnu/libserialport.so.0 /usr/lib/x86_64-linux-gnu/liblistSerialsj.so.1.4.0
# now IDE can be started
arduino
```

In the future, it would be nice to bundle a container and [crossdev](https://wiki.gentoo.org/wiki/Arduino#Recommended:_Install_the_toolchain_using_crossdev) which worked for Teensy 3.x too years ago
