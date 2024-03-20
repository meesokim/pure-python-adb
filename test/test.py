from ppadb.client import Client as AdbClient
from ppadb.device import Device as AdbDevice
from ppadb import InstallError

def dump_logcat(connection):
    while True:
        data = connection.read(1024)
        if not data:
            break
        print(data)
    connection.close()

import os, sys
MUSCAT_ROOT = 'MUSCAT_ROOT'
def path(local_path):
    if MUSCAT_ROOT in os.environ:
        root = os.environ[MUSCAT_ROOT]
    else:
        root = f'{os.environ["HOME"]}/muscat/muscat_client/'
    return f'{root}/{local_path}'

client = AdbClient(host="127.0.0.1", port=5037)

from test_host import test_list_devices
from test_device import test_get_properties

devices = client.devices()
serials = [device.serial for device in devices]
for device in devices:
    features = device.list_features()
    properties = device.list_properties()
    print(f'Device Serial: {device.serial}')
    print(f'Device Size: {device.wm_size()}')
    print(f'Device Density: {device.wm_density()}')
    print(f'Bettery Level: {device.get_battery_level()}%')
    # print(f'Top Activity: {device.get_top_activity()}')
    print(f'CPU counts: {device.cpu_count()}')
    print(f'model:', properties['ro.product.model'])
    print(f'manufacturer:', properties['ro.product.manufacturer'])

    print('[Features]')
    for ix, feature in enumerate(features):
        print(f'[F{ix:04d}] {feature}: {features[feature]}')
    # device.shell('logcat', handler=dump_logcat)
    print('[Properties]')
    for ix, prop in enumerate(properties):
        print(f'[P{ix:04d}] {prop}: {properties[prop]}')

    device.set_apk_path(path('.'))
    if device.install('game/genshin/ACT_eng.apk', test=True) != True:
        print('Install Failed')
    device.shell('input keyevent 26')
    device.shell('settings put global package_verifier_user_consent -1')
    device.uninstall('com.sec.android.spa_automation')
    device.uninstall('com.sec.android.spa_automation.test')
    device.install('/auto_apk/spa-testcase.apk')
# for serial in serials:
#     print(serial, client.device(serial).serial)