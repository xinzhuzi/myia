// Ghidra inferred pseudocode; requested=0x667e734
// entry=0667e734 end=0667e8af

void FUN_0667e734(long param_1)

{
  byte bVar1;
  undefined8 *puVar2;
  long lVar3;
  undefined8 uVar4;
  char cVar5;
  ulong uVar6;
  long *plVar7;
  undefined8 local_50;
  long *plStack_48;
  undefined8 local_40;
  
  LOAcquire();
  bVar1 = *(byte *)(param_1 + 0x140);
  *(byte *)(param_1 + 0x140) = 1;
  LORelease();
  if ((bVar1 & 1) != 0) {
    return;
  }
  puVar2 = (undefined8 *)__Znwm(0x10);
  lVar3 = *(long *)(param_1 + 0xa0);
  *puVar2 = *(undefined8 *)(param_1 + 0x98);
  if (lVar3 == 0) {
    puVar2[1] = 0;
LAB_0667e8ac:
                    /* WARNING: Subroutine does not return */
    FUN_00283500();
  }
  lVar3 = __ZNSt3__119__shared_weak_count4lockEv();
  puVar2[1] = lVar3;
  if (lVar3 == 0) goto LAB_0667e8ac;
  FUN_0667378c(&local_50,FUN_0667f4c8,puVar2,FUN_0667f4d8,param_1 + 0xe0);
  plVar7 = *(long **)(param_1 + 0xb0);
  puVar2 = (undefined8 *)(param_1 + 0xa8);
  *(long **)(param_1 + 0xb0) = plStack_48;
  *puVar2 = local_50;
  local_50 = 0;
  plStack_48 = (long *)0x0;
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar7[1];
    plVar7[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  plVar7 = plStack_48;
  if (plStack_48 == (long *)0x0) {
LAB_0667e7f8:
    if (-1 < *(char *)(param_1 + 0x97)) goto LAB_0667e800;
LAB_0667e87c:
    FUN_00018d20(&local_50,*(undefined8 *)(param_1 + 0x80),*(undefined8 *)(param_1 + 0x88));
    cVar5 = local_40._7_1_;
    if ((long)local_40 < 0) goto LAB_0667e890;
LAB_0667e818:
    if (cVar5 != '\0') goto LAB_0667e830;
  }
  else {
    LOAcquire();
    lVar3 = plStack_48[1];
    plStack_48[1] = lVar3 + -1;
    LORelease();
    if (lVar3 != 0) goto LAB_0667e7f8;
    (**(code **)(*plStack_48 + 0x10))(plStack_48);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    if (*(char *)(param_1 + 0x97) < '\0') goto LAB_0667e87c;
LAB_0667e800:
    plStack_48 = *(long **)(param_1 + 0x88);
    local_50 = *(undefined8 *)(param_1 + 0x80);
    uVar6 = *(ulong *)(param_1 + 0x90);
    local_40._7_1_ = (char)(uVar6 >> 0x38);
    cVar5 = local_40._7_1_;
    local_40 = uVar6;
    if (-1 < (long)uVar6) goto LAB_0667e818;
LAB_0667e890:
    plVar7 = plStack_48;
    __ZdlPvm(local_50,local_40 & 0x7fffffffffffffff);
    if (plVar7 != (long *)0x0) goto LAB_0667e830;
  }
  uVar4 = FUN_06674180(puVar2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x80,uVar4);
LAB_0667e830:
  FUN_066738d4(puVar2,0);
  *(undefined1 *)(param_1 + 0x141) = 1;
  return;
}


