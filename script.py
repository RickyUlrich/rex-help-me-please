import archr
from driller import Driller
import rex

tt = archr.targets.LocalTarget(["./a.out"], target_arch='x86_64')
tt.target_arch                                                               

d = Driller("./a.out", b"A" * 500, b"\xff" * 65535)                          
new_inputs = d.drill()                                                       

solution = next(iter(new_inputs))
crash = rex.Crash(tt, crash=solution[1])
