// Ghidra inferred pseudocode; requested=0x56c28e4
// entry=056c28e4 end=056c29d3

undefined8 FUN_056c28e4(undefined8 *param_1)

{
  long lVar1;
  long *plVar2;
  undefined1 *local_30;
  long *local_28;
  
  if ((*(byte *)(param_1 + 2) & 1) == 0) {
    if ((param_1[1] != 0) && (0 < *(long *)(param_1[1] + 8))) {
      local_30 = &SUB_aaaaaaaaaaaaaaaa;
      local_28 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_056e06f0(&local_30,*param_1);
      if (local_28 != (long *)0x0) {
        local_28[1] = local_28[1] + 1;
      }
      plVar2 = (long *)param_1[1];
      *param_1 = local_30;
      param_1[1] = local_28;
      if (plVar2 != (long *)0x0) {
        LOAcquire();
        lVar1 = plVar2[1];
        plVar2[1] = lVar1 + -1;
        LORelease();
        if (lVar1 == 0) {
          (**(code **)(*plVar2 + 0x10))(plVar2);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
      plVar2 = local_28;
      *(undefined1 *)(param_1 + 2) = 1;
      if (local_28 != (long *)0x0) {
        LOAcquire();
        lVar1 = local_28[1];
        local_28[1] = lVar1 + -1;
        LORelease();
        if (lVar1 == 0) {
          (**(code **)(*local_28 + 0x10))(local_28);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
      return *param_1;
    }
    *(undefined1 *)(param_1 + 2) = 0;
  }
  return *param_1;
}


