// Ghidra inferred pseudocode; requested=0x2ab8e14
// entry=02ab8e14 end=02ab8f4f

void FUN_02ab8e14(undefined8 param_1,long param_2)

{
  ulong uVar1;
  long lVar2;
  int iVar3;
  char *pcVar4;
  long *plVar5;
  long **pplVar6;
  long **pplVar7;
  long *local_60;
  long *local_58;
  undefined8 local_50;
  undefined4 local_44;
  
  pplVar6 = &local_60;
  pplVar7 = &local_60;
  iVar3 = FUN_04bb4dc0(param_2 + 8);
  if (iVar3 == 0) {
    return;
  }
  FUN_0466aca8(&local_60);
  (**(code **)(*local_60 + 8))();
  plVar5 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_58[1];
    local_58[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  local_44 = *(undefined4 *)(param_2 + 0x54);
  FUN_047231e0(&local_44);
  *(undefined4 *)(param_2 + 0x54) = local_44;
  pcVar4 = (char *)FUN_04e2102c();
  plVar5 = (long *)_strlen(pcVar4);
  if ((long *)0x7ffffffffffffff7 < plVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_60);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar5) {
    uVar1 = 0x19;
    if (((ulong)plVar5 | 7) != 0x17) {
      uVar1 = ((ulong)plVar5 | 7) + 1;
    }
    pplVar6 = (long **)__Znwm(uVar1);
    local_50 = uVar1 | 0x8000000000000000;
    local_60 = (long *)pplVar6;
    local_58 = plVar5;
  }
  else {
    local_50 = CONCAT17((char)plVar5,(undefined7)local_50);
    if (plVar5 == (long *)0x0) goto LAB_02ab8f08;
  }
  _memmove(pplVar6,pcVar4,(size_t)plVar5);
  pplVar7 = pplVar6;
LAB_02ab8f08:
  *(undefined1 *)((long)pplVar7 + (long)plVar5) = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_2 + 0xa8,&local_60)
  ;
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  return;
}


