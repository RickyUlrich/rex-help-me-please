
## Introduction
I am trying to demonstrate [rex](https://github.com/angr/rex), an exploitation analysis
engine built on top of angr.

I created a simple exploitable program with a simple `strcmp` guard that needs
to be solved:
```
int main(void) {
	char buf[32];
	fgets(buf, 64, stdin);
	if (1 == 2) { return 0; }
	if (strncmp(buf, "hello there", strlen("hello there"))) { exit(1); }
	return 0;
}

```
`Driller` is able to find an input that bypasses the `strncmp`.  However,
when I pass that crashing input to `rex`'s `Crash` module, I get an `IndexError` in `rex`'s `crash.py`:647.
```
~/.virtualenvs/angr/lib/python3.6/site-packages/rex/crash.py in _trace(self, pov_file, format_infos)
    645         if 'crashed' in simgr.stashes:
    646             # the state at crash time
--> 647             self.state = simgr.crashed[0]
    648             # a path leading up to the crashing basic block
    649             self.prev = self._t.predecessors[-1]
```

## Steps to reproduce
```
cd /mnt
gcc -no-pie test.c
./install-driller.sh

ipython3 -i script.py
```

## Error output
There seems to be an error in the tracer module or how `rex` processes trace output:
```
(angr) angr@bbaa1745da8e:/mnt$ ipython3 -i script.py 
Python 3.6.9 (default, Nov  7 2019, 10:44:02) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.10.1 -- An enhanced Interactive Python. Type '?' for help.
WARNING | 2019-12-23 22:10:02,224 | angr.engines.successors | Exit state has over 256 possible solutions. Likely unconstrained; skipping. <BV64 0 .. file_0_stdin_3e_138_8{UNINITIALIZED} 
.. file_0_stdin_3d_137_8{UNINITIALIZED} .. file_0_stdin_3c_136_8{UNINITIALIZED} .. file_0_stdin_3b_135_8{UNINITIALIZED} .. file_0_stdin_3a_134_8{UNINITIALIZED} .. file_0_stdin_39_133_8{U
NINITIALIZED} .. file_0_stdin_38_132_8{UNINITIALIZED}>
WARNING | 2019-12-23 22:10:05,811 | cle.loader | <_io.BytesIO object at 0x7f31829e58e0>: base_addr was specified but the object is not PIC. specify force_rebase=True to override
WARNING | 2019-12-23 22:10:05,868 | cle.loader | <_io.BytesIO object at 0x7f3180145468>: base_addr was specified but the object is not PIC. specify force_rebase=True to override
WARNING | 2019-12-23 22:10:05,925 | cle.loader | <_io.BytesIO object at 0x7f317bea0620>: base_addr was specified but the object is not PIC. specify force_rebase=True to override
WARNING | 2019-12-23 22:10:05,982 | cle.loader | <_io.BytesIO object at 0x7f31801309e8>: base_addr was specified but the object is not PIC. specify force_rebase=True to override
WARNING | 2019-12-23 22:10:10,410 | archr.arsenal.qemu_tracer | setting LD_BIND_NOW=1. This will have an effect on the environment.
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
/mnt/script.py in <module>
     10 
     11 solution = next(iter(new_inputs))
---> 12 crash = rex.Crash(tt, crash=solution[1])

~/.virtualenvs/angr/lib/python3.6/site-packages/rex/crash.py in __init__(self, target, crash, pov_file, aslr, constrained_addrs, hooks, format_infos, tracer_bow, explore_steps, input_typ
e, port, use_crash_input, checkpoint_path, crash_state, prev_state, rop_cache_tuple, use_rop, fast_mode, angrop_object, rop_cache_path)
    117 
    118         # Work
--> 119         self._work(pov_file, format_infos)
    120 
    121     #

~/.virtualenvs/angr/lib/python3.6/site-packages/rex/crash.py in _work(self, pov_file, format_infos)
    563             self._has_preconstrained = False
    564             self._trace(pov_file=pov_file,
--> 565                         format_infos=format_infos,
    566                         )
    567 

~/.virtualenvs/angr/lib/python3.6/site-packages/rex/crash.py in _trace(self, pov_file, format_infos)
    645         if 'crashed' in simgr.stashes:
    646             # the state at crash time
--> 647             self.state = simgr.crashed[0]
    648             # a path leading up to the crashing basic block
    649             self.prev = self._t.predecessors[-1]

IndexError: list index out of range

```
