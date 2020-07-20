import archr
from driller import Driller
import rex

import os
import sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))

tt = archr.targets.LocalTarget(["./a.out"], target_arch='x86_64')

# gcc -shared -fPIC -o overwrite_stack_check_fail.o overwrite_stack_check_fail.so
# overwrite_stack_chk_so_path = os.path.join(SCRIPT_DIR, 'overwrite_stack_check_fail.o')
# env = [ k+"="+v for k,v in os.environ.items() ]
# env.append('LD_PRELOAD={}'.format(overwrite_stack_chk_so_path))
# tt = archr.targets.LocalTarget(["./a.out"], target_env=env, target_arch='x86_64')

tt.target_arch                                                               

d = Driller("./a.out", b"A" * 500, b"\xff" * 65535)                          
new_inputs = d.drill()                                                       

solution = next(iter(new_inputs))
crash = rex.Crash(tt, crash=solution[1])
