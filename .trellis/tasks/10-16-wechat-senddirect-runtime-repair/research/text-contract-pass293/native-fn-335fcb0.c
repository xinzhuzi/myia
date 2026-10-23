// Ghidra inferred pseudocode; requested=0x335fcb0
// entry=0335fcb0 end=0335fda7

void FUN_0335fcb0(undefined8 *param_1)

{
  long *plVar1;
  long lVar2;
  undefined1 *local_2d0;
  long *local_2c8;
  undefined1 *local_2c0;
  long *local_2b8;
  undefined1 local_2b0 [632];
  char local_38;
  
  local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2b8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_021efaf0(&local_2c0,local_2b0);
  local_2d0 = local_2c0;
  local_2c8 = local_2b8;
  lVar2 = 0;
  if (local_2b8 != (long *)0x0) {
    lVar2 = local_2b8[1];
    local_2b8[1] = lVar2 + 1;
  }
  local_2b0[0] = 0;
  local_38 = '\0';
  FUN_0335fdd8(lVar2,&local_2d0,local_2b0);
  if (local_38 == '\x01') {
    FUN_00ac6290(local_2b0);
  }
  plVar1 = local_2c8;
  if (local_2c8 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_2c8[1];
    local_2c8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_2c8 + 0x10))(local_2c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_2b8;
  *param_1 = local_2c0;
  param_1[1] = local_2b8;
  if (local_2b8 != (long *)0x0) {
    local_2b8[1] = local_2b8[1] + 1;
    if (local_2b8 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_2b8[1];
      local_2b8[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_2b8 + 0x10))(local_2b8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
  }
  return;
}


