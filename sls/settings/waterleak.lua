print("Water leak sensor state changed to " .. Event.State.Value)
if Event.State.Value == "true" then
  mqtt.pub('home/watercontrol/bath/valve/set', 'close')
  audio.setvolume(100)
  audio.playurl("http://home-alt.yandex5.ru/local/sounds/sirena.mp3")
  mqtt.pub('home/watercontrol/bath/valve/set', 'close')
end