// Ghidra inferred pseudocode; requested=0x666ab58
// entry=0666ab58 end=0666ac4b

void FUN_0666ab58(undefined8 *param_1,long param_2)

{
  long lVar1;
  long *plVar2;
  undefined1 *local_48;
  long *local_40;
  undefined1 *local_38;
  long *local_30;
  undefined1 uStack_21;
  
  local_38 = &SUB_aaaaaaaaaaaaaaaa;
  local_30 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_021efaf0(&local_38,&uStack_21);
  local_48 = local_38;
  local_40 = local_30;
  lVar1 = 0;
  if (local_30 != (long *)0x0) {
    lVar1 = local_30[1];
    local_30[1] = lVar1 + 1;
  }
  plVar2 = *(long **)(param_2 + 0x18);
  if (plVar2 != (long *)0x0) {
    (**(code **)(*plVar2 + 0x30))(plVar2,&local_48);
    plVar2 = local_40;
    if (local_40 != (long *)0x0) {
      LOAcquire();
      lVar1 = local_40[1];
      local_40[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*local_40 + 0x10))(local_40);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
    plVar2 = local_30;
    *param_1 = local_38;
    param_1[1] = local_30;
    if (local_30 == (long *)0x0) {
      param_1[2] = 0;
    }
    else {
      local_30[1] = local_30[1] + 1;
      param_1[2] = 0;
      if (local_30 != (long *)0x0) {
        LOAcquire();
        lVar1 = local_30[1];
        local_30[1] = lVar1 + -1;
        LORelease();
        if (lVar1 == 0) {
          (**(code **)(*local_30 + 0x10))(local_30);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
    }
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc(lVar1);
}


