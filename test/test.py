from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice

def dump_logcat(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data)
    connection.close()

client = AdbClient(host="127.0.0.1", port=5037)

from test_host import test_list_devices
from test_device import test_get_properties
import json, os, sys

devices = client.devices()
serials = [device.serial for device in devices]
for device in devices:
    print(f'Device Serial: {device.serial}')
    print(f'Device Size: {device.wm_size()}')
    print(f'Device Density: {device.wm_density()}')
    print(f'Bettery Level: {device.get_battery_level()}%')
    # print(f'Top Activity: {device.get_top_activity()}')
    print(f'CPU counts: {device.cpu_count()}')
    
    device_feature_file = f'{device.serial}.features'    
    if os.path.exists(device_feature_file):
        features = json.loads(open(device_feature_file).read())
    else:
        features = device.list_features()
        open(device_feature_file, 'w').write(json.dumps(features))
    # for feature in features:
    #     print(f'{feature}: {features[feature]}')
    # device.shell('logcat', handler=dump_logcat)
    # test_list_devices(client, device.serial)
    # device_properties_file = f'{device.serial}.properties'
    # if os.path.exists(device_properties_file):
    #     properties = json.loads(open(device_properties_file).read())
    # else:
    properties = device.list_properties()
        # open(device_properties_file, 'w').write(json.dumps(properties))    
    # for prop in properties:
    #     print(f'{prop}: {properties[prop]}')

    print(f'model:', properties['ro.product.model'])
    print(f'manufacturer:', properties['ro.product.manufacturer'])

# for serial in serials:
#     print(serial, client.device(serial).serial)