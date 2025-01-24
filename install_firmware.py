import usb.core
import time

from hexdump import hexdump


dev = usb.core.find(idVendor=0x18d1, idProduct=0x9302)
if dev is None:
  # download firmware
  dev = usb.core.find(idVendor=0x1a6e, idProduct=0x089a)
  if dev is None:
    raise Exception("U NEED TO BUY GOOGLE CORAL NO FREE BANANA FOR U")
  print("doing download firmware bro")
  fw = open("apex_latest_single_ep.bin", "rb").read()
  cnt = 0
  for i in range(0, len(fw), 0x100):
    dev.ctrl_transfer(0x21, 1, cnt, 0, fw[i:i+0x100])
    ret = dev.ctrl_transfer(0xa1, 3, 0, 0, 6)
    hexdump(ret)
    cnt += 1
  dev.ctrl_transfer(0x21, 1, cnt, 0, "")
  ret = dev.ctrl_transfer(0xa1, 3, 0, 0, 6)
  hexdump(ret)

  for i in range(0, 0x81):
    ret = dev.ctrl_transfer(0xa1, 2, i, 0, 0x100)
  try: 
    dev.reset()
  except usb.core.USBError:
    print("okay exception")
  print("downloaded, napping quick bro")
  time.sleep(3)
  dev = usb.core.find(idVendor=0x18d1, idProduct=0x9302)

else:
  print("Already installed")

dev.reset()
time.sleep(0.6)
usb.util.claim_interface(dev, 0)
dev.set_configuration(1)