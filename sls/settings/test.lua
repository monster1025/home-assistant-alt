-- mqtt.pub('home/yandexStation/say', 'Здрасьте!')
if Event.State.Value == "single" then
   zigbee.set("0x00158D0001A4CFB4", "state", "toggle")
end