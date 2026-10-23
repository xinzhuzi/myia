// Ghidra inferred pseudocode; requested=0x305cdec
// entry=0305cdec end=0305cee7

void FUN_0305cdec(long *param_1)

{
  long lVar1;
  long *plVar2;
  undefined8 *puVar3;
  undefined8 local_60;
  undefined8 local_58 [2];
  undefined7 local_48;
  char cStack_41;
  undefined8 local_40;
  long *local_38;
  
  FUN_0305cefc(&local_60,param_1 + 4);
  puVar3 = (undefined8 *)*param_1;
  *puVar3 = local_60;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar3 + 1,local_58);
  if (local_38 != (long *)0x0) {
    local_38[1] = local_38[1] + 1;
  }
  plVar2 = (long *)puVar3[5];
  puVar3[4] = local_40;
  puVar3[5] = local_38;
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
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_38[1];
    local_38[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
    }
  }
  if (cStack_41 < '\0') {
    __ZdlPvm(local_58[0],CONCAT17(cStack_41,local_48) & 0x7fffffffffffffff);
  }
  *(undefined4 *)param_1[2] = 1;
  return;
}


