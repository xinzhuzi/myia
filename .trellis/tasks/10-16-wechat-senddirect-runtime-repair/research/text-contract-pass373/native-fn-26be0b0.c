// Ghidra inferred pseudocode; requested=0x26be0b0
// entry=026be0b0 end=026be187

void FUN_026be0b0(undefined8 *param_1)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  long *plVar4;
  
  plVar3 = (long *)__Znwm(0x80);
  plVar3[2] = 0;
  plVar4 = plVar3 + 3;
  *plVar4 = (long)&PTR_thunk_FUN_02877a18_09db21d0;
  *plVar3 = (long)&PTR_FUN_09da1880;
  plVar3[1] = 0;
  plVar3[5] = 0;
  plVar3[4] = 0;
  plVar3[7] = 0;
  plVar3[6] = 0;
  plVar3[9] = 0;
  plVar3[8] = 0;
  plVar3[0xb] = 0;
  plVar3[10] = 0;
  plVar3[0xd] = 0;
  plVar3[0xc] = 0;
  plVar3[0xf] = 0;
  plVar3[0xe] = 0;
  plVar3[10] = 0;
  plVar3[9] = 0;
  plVar3[8] = 0;
  plVar3[7] = 0;
  *(undefined4 *)(plVar3 + 0xb) = 0x3f800000;
  plVar3[0xc] = 0;
  plVar3[0xd] = 0;
  *(undefined1 *)(plVar3 + 0xf) = 0;
  plVar3[0xe] = 0;
  if (plVar4 != (long *)0x0) {
    if (plVar3 == (long *)0x0) {
      segment_command_00000020.cmd = 0x18;
      segment_command_00000020.cmdsize = 0;
    }
    else {
      plVar1 = plVar3 + 1;
      *plVar1 = *plVar1 + 1;
      plVar3[2] = plVar3[2] + 1;
      plVar3[4] = (long)plVar4;
      plVar3[5] = (long)plVar3;
      LOAcquire();
      lVar2 = *plVar1;
      *plVar1 = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar3 + 0x10))();
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      }
    }
  }
  *param_1 = plVar4;
  param_1[1] = plVar3;
  return;
}


