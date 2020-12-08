- start VM from instructions in root-level README
- load via `sudo /vagrant/coupon/main.py` (from inside VM)
- in separate `vagrant ssh` windows, run `nc -kul 127.0.0.1 7999` (server) and `nc -u 127.0.0.1 7999` (client) to test packets
- use `sendData.py` to run actual traces (spoofing source IP/ports)


(netcat based on https://duo.com/labs/tech-notes/writing-an-xdp-network-filter-with-ebpf)


