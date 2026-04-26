from pprint import pprint as print
import subprocess

# rssi for each router measured at 1 meter
P = -57 # to be caliberated

# environmental constant (2 to 4)
n = 3

# getting all available network info
r = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=bssid']).decode('ascii', errors='ignore').split("\r\n\r\n")

# cleaning up
networks = [{} for _ in range(0, len(r))]
for ctr in range(0, len(r)):
	r[ctr] = r[ctr].replace('\r', '').split('\n')
	for ctr2 in range(0, len(r[ctr])):
		r[ctr][ctr2] = r[ctr][ctr2].replace('\t', '').split(':')
		for ctr3 in range(0, len(r[ctr][ctr2])):
			r[ctr][ctr2][ctr3] = r[ctr][ctr2][ctr3].strip()
		try:
			networks[ctr][r[ctr][ctr2][0]] = r[ctr][ctr2][1]
		except Exception as e:
			pass

# calculating the rssi and distance
for wifi in networks:
	if wifi == {} or wifi == {'Interface name': 'Wi-Fi'}:
		continue
	wifi['RSSI'] = (int(wifi['Signal'].replace('%', ''))/2)-100
	wifi['DISTANCE'] = 10**((P-wifi['RSSI'])/(10*n))


print(networks)