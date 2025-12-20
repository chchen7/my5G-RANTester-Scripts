# root@f0c386730537:/workspace/my5G-RANTester/cmd# iperf -c iperf 
# ------------------------------------------------------------
# Client connecting to iperf, TCP port 5001
# TCP window size: 16.0 KByte (default)
# ------------------------------------------------------------
# [  1] local 10.100.200.13 port 34392 connected with 10.100.200.14 port 5001 (icwnd/mss/irtt=14/1448/151)
# ^C[ ID] Interval       Transfer     Bandwidth
# [  1] 0.0000-1.7015 sec  4.48 GBytes  22.6 Gbits/sec
# root@f0c386730537:/workspace/my5G-RANTester/cmd# iperf -c iperf --bind 10.60.0.1
# ------------------------------------------------------------
# Client connecting to iperf, TCP port 5001
# TCP window size: 16.0 KByte (default)
# ------------------------------------------------------------
# tcp connect failed: No route to host
# [  1] local 10.60.0.1 port 0 connected with 10.100.200.14 port 5001
# root@f0c386730537:/workspace/my5G-RANTester/cmd# ip route
# default dev uetun1 scope link 
# 10.100.200.0/24 dev eth0 proto kernel scope link src 10.100.200.13 
# 10.100.200.200 dev eth0 scope link 

UPF_PID=$(docker inspect -f '{{.State.Pid}}' upf)
sudo nsenter -t $UPF_PID -n tcpdump -i upfgtp icmp -n
sudo nsenter -t $UPF_PID -n tcpdump -i eth0 icmp -n
# 看 UPF 的實體介面有沒有把封包「包好」並從它自己的 eth0 送出去
sudo nsenter -t $UPF_PID -n tcpdump -i eth0 udp port 2152 -n

UE_PID=$(docker inspect -f '{{.State.Pid}}' my5grantester0)

# 看 UE 的實體介面有沒有收到這些封裝過的封包
sudo nsenter -t $UE_PID -n tcpdump -i eth0 udp -n
# 看 UE 的虛擬介面有沒有收到解風過的封包
sudo nsenter -t $UE_PID -n tcpdump -i uetun1 icmp -n

ping -I uetun1 1.1.1.1