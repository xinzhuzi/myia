// Ghidra inferred pseudocode; requested=0x50e0d54
// entry=050e0d54 end=050e0df3

void FUN_050e0d54(undefined8 *param_1)

{
  *param_1 = &PTR_FUN_09edc360;
  if (DAT_0a520ca0 != param_1) {
    if ((long *)param_1[1] != (long *)0x0) {
      (**(code **)(*(long *)param_1[1] + 8))();
    }
    if ((long *)param_1[2] != (long *)0x0) {
      (**(code **)(*(long *)param_1[2] + 8))();
    }
    if ((long *)param_1[3] != (long *)0x0) {
      (**(code **)(*(long *)param_1[3] + 8))();
    }
    if ((long *)param_1[4] != (long *)0x0) {
      (**(code **)(*(long *)param_1[4] + 8))();
    }
    if ((long *)param_1[5] != (long *)0x0) {
      (**(code **)(*(long *)param_1[5] + 8))();
    }
  }
  FUN_0001accc(param_1);
  return;
}


