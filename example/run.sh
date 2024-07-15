set -x
mkdir /artifacts

ip4=`curl -4 ipconfig.io`
echo $ip4
nslookup $ip4

traceroute 1.1.1.1

grpcurl -plaintext -d {\"get_status\":{}} 192.168.100.1:9200 SpaceX.API.Device.Device/Handle

chmod +x /leotest/leotest/bin/irtt
ping -D -i 0.01 -c 12000 100.64.0.1 > /artifacts/ping-gw-`date "+%y%m%d-%H%M%S"`.txt
