from argparse import ArgumentParser
import requests 
import sys
import os

def main(argv):
    parser = ArgumentParser()
    parser.add_argument("-i", "--ip", dest="slsIp", help="IP address of SLS gateway", default="192.168.1.2")
    parser.add_argument("-f", "--folder", dest="backupFolder", help="Name of backup folder", default="backup")
    args = parser.parse_args()

    slsIp = args.slsIp
    backupFolder = args.backupFolder

    print("slsIp: {}, folder: {}".format(slsIp, backupFolder))
    process_folder('/', slsIp, backupFolder)

def process_folder(path, slsIp, backupFolder):
    r = requests.get('http://{}/api/files?path={}'.format(slsIp, path))
    json = r.json()
    if json == None:
        print("Error while retrieving data, response is: {}".format(r.text))
        return
    
    if "success" not in json:
        print("Response was unsuccessfull.")
        return

    folderItems = json['result']
    for folderItem in folderItems:
        print("- {}".format(folderItem))
        name = folderItem["name"]
        folderRealPath = os.path.realpath(backupFolder)

        if folderItem['is_dir'] == True:
            process_folder("{}/{}".format(name), slsIp, backupFolder)
            continue
        else:
            cleanFolderPath = folderRealPath.replace("/", os.sep)
            filePath = cleanFolderPath + name.replace("/", os.sep)
            print(filePath)

            r = requests.get('http://{}/api/files?path={}'.format(slsIp, name))
            with open(filePath, 'w') as file:
                file.write(r.text)

if __name__ == '__main__':
    main(sys.argv)