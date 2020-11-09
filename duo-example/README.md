from https://duo.com/labs/tech-notes/writing-an-xdp-network-filter-with-ebpf

setup with the `nc` commands of section 03 first (you probably want many terminal windows, `vagrant ssh`in all of them)
send messages.

then, run via `sudo /vagrant/duo-example/main.py`, and send more messages.

doesn't really unload properly on quit, as python script would suggest.
however, loading the trivial filter (commenting out) works (i assume via `KBUILD_MODNAME`)
