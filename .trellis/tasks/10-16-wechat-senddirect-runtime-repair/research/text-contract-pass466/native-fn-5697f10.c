// Ghidra inferred pseudocode; requested=0x5697f10
// entry=05697f10 end=0569807b

void FUN_05697f10(long param_1)

{
  long *plVar1;
  bool bVar2;
  long lVar3;
  undefined8 uVar4;
  long *plVar5;
  long *plVar6;
  undefined1 *local_70;
  undefined1 *puStack_68;
  undefined1 *puStack_60;
  long *local_58;
  long *local_50;
  
  FUN_05699df8(*(undefined8 *)(param_1 + 0x298));
  plVar5 = (long *)(param_1 + 0x38);
  (**(code **)(*plVar5 + 0x28))(plVar5,*(undefined8 *)(param_1 + 0x298));
  FUN_0562fcb4(&local_70);
  if ((*(byte *)(param_1 + 0x18) & 1) == 0) {
    uVar4 = FUN_05693108(plVar5,&local_70);
  }
  else {
    plVar5 = *(long **)(*(long *)(param_1 + 8) + 0x98);
    if (plVar5 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_0021eccc();
    }
    uVar4 = (**(code **)(*plVar5 + 0x30))(plVar5,&local_70);
  }
  *(undefined8 *)(param_1 + 0x298) = uVar4;
  FUN_0562fd84(&local_70);
  plVar5 = *(long **)(param_1 + 0x2a0);
  while (plVar5 != (long *)(param_1 + 0x2a8)) {
    local_50 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
    local_70 = &SUB_aaaaaaaaaaaaaaaa;
    local_58 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_60 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0562fd3c(&local_70,plVar5 + 4);
    local_58 = (long *)plVar5[7];
    local_50 = (long *)plVar5[8];
    if (local_50 != (long *)0x0) {
      local_50[1] = local_50[1] + 1;
    }
    (**(code **)(*local_58 + 0x10))();
    plVar1 = local_50;
    if (local_50 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_50[1];
      local_50[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_50 + 0x10))(local_50);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
    FUN_0562fd84(&local_70);
    plVar1 = (long *)plVar5[1];
    plVar6 = plVar5;
    if ((long *)plVar5[1] == (long *)0x0) {
      do {
        plVar5 = (long *)plVar6[2];
        bVar2 = (long *)*plVar5 != plVar6;
        plVar6 = plVar5;
      } while (bVar2);
    }
    else {
      do {
        plVar5 = plVar1;
        plVar1 = (long *)*plVar5;
      } while ((long *)*plVar5 != (long *)0x0);
    }
  }
  return;
}


