#!/bin/bash

DISK="$1"

if [ ! -n "$DISK" ]
then
   echo "you must input block dev"
   exit
else
   echo "are you sure to clean device: $DISK ? yes/no"
   read ANSWER
   case $ANSWER in
     [Yy]*)
     echo " you input is y or Y !"
     ;;
     [Nn]*)
     echo " you input a "$ANSWER
     exit
     ;;
   esac
fi

echo "clean /var/lib/rook"
rm -rf /var/lib/rook


echo "clean block dev"

# Zap the disk to a fresh, usable state (zap-all is important, b/c MBR has to be clean)
# You will have to run this step for all disks.
sgdisk --zap-all $DISK
# Clean hdds with dd
dd if=/dev/zero of="$DISK" bs=1M count=100 oflag=direct,dsync
# Clean disks such as ssd with blkdiscard instead of dd
blkdiscard $DISK

# These steps only have to be run once on each node
# If rook sets up osds using ceph-volume, teardown leaves some devices mapped that lock the disks.
ls /dev/mapper/ceph-* | xargs -I% -- dmsetup remove %
# ceph-volume setup can leave ceph-<UUID> directories in /dev (unnecessary clutter)
rm -rf /dev/ceph-*

