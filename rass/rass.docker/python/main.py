import urllib
import urllib.request
import json
import os.path
import time

file = '/room-assistant/python/tags.json'
config = '/room-assistant/config/local.json'
interval = 6

def main():
  refresh_tags()
  #time.sleep(interval)

def refresh_tags():
  print('reloading tags.')
  tags = get_tags()
  if not os.path.isfile(file):
    print('local tags list does not exist. creating new one.')
    save_file(file, tags)
    edit_config(config, tags)
    reload_daemon()
    return
  file_tags = get_file(file)
  if file_tags != tags:
    print('tags list was changed')
    save_file(file, tags)
    edit_config(config, tags)
    reload_daemon()

def reload_daemon():
  print('reloading')

def edit_config(file, tags):
  config_data = get_file(file)
  config_data['ble']['whitelist'] = tags
  #config_data['ibeacon']['whitelist'] = tags
  save_file(config, config_data)

def get_tags():
  url = "https://home.yandex5.ru/api/appdaemon/tags"
  #url = "http://192.168.1.6:5000/api/appdaemon/tags"
  req = urllib.request.Request(url, data='{}'.encode('utf8'),
                           headers={'content-type': 'application/json'})
  r = urllib.request.urlopen(req)
  r_json = r.read().decode(r.info().get_param('charset') or 'utf-8')
  data = json.loads(r_json)
  return data

##################################################################################
def get_file(file):
  file = open(file, 'r')
  return json.loads(file.read())

def save_file(file, data):
  js = json.dumps(data, indent=4)
  print(js)
  with open(file, 'w') as file:
      file.write(js)
##################################################################################

if __name__ == "__main__":
  main()

