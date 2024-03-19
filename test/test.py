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

devices = client.devices()
serials = [device.serial for device in devices]
for device in devices:
    print(f'Device Serial: {device.serial}')
    print(f'Device Size: {device.wm_size()}')
    print(f'Device Density: {device.wm_density()}')
    print(f'Bettery Level: {device.get_battery_level()}%')
    print(f'Top Activity: {device.get_top_activity()}')
    print(f'CPU counts: {device.cpu_count()}')
    features = device.list_features()
    for feature in features:
        print(f'{feature}: {features[feature]}')
    device.shell('logcat', handler=dump_logcat)

for serial in serials:
    print(serial, client.device(serial).serial)