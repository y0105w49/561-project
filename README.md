
## BPF

### running VM
- needs vagrant and virtualbox installed
- run `vagrant up` to build and start, `vagrant ssh` to login.
- the `suspend`, `halt`, `destroy` commands might also be helpful.
- files sync from this directory to VM at `/vagrant`

### logs
from the vm, to see log output written with `bpf_trace_printk` (without taking over the python thread with `trace_print`), in another shell run:
``` sh
sudo cat /sys/kernel/debug/tracing/trace_pipe
```

