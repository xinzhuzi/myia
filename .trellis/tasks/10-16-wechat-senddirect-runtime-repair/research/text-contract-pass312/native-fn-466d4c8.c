// Ghidra inferred pseudocode; requested=0x466d4c8
// entry=0466d4c8 end=0466d5fb

void FUN_0466d4c8(undefined8 *param_1,long param_2)

{
  long lVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long local_40;
  long *local_38;
  
  (**(code **)(*DAT_0a45df38 + 0x68))(&local_40);
  if ((local_38 != (long *)0x0) && (local_38[1] = local_38[1] + 1, local_38 != (long *)0x0)) {
    LOAcquire();
    lVar1 = local_38[1];
    local_38[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
    }
  }
  if (local_40 != 0) {
    puVar2 = (undefined8 *)FUN_04553f74(local_40);
    if (*(char *)((long)puVar2 + 0x17) < '\0') {
      FUN_00018d20(param_1,*puVar2,puVar2[1]);
    }
    else {
      uVar4 = puVar2[1];
      uVar3 = *puVar2;
      param_1[2] = puVar2[2];
      param_1[1] = uVar4;
      *param_1 = uVar3;
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
  if (local_40 == 0) {
    if (*(char *)(param_2 + 0x28f) < '\0') {
      FUN_00018d20(param_1,*(undefined8 *)(param_2 + 0x278),*(undefined8 *)(param_2 + 0x280));
    }
    else {
      uVar3 = *(undefined8 *)(param_2 + 0x278);
      param_1[1] = *(undefined8 *)(param_2 + 0x280);
      *param_1 = uVar3;
      param_1[2] = *(undefined8 *)(param_2 + 0x288);
    }
  }
  return;
}


