// Ghidra inferred pseudocode; requested=0x5626ae8
// entry=05626ae8 end=05626cff

void FUN_05626ae8(long param_1,void *param_2,size_t param_3,long *param_4)

{
  void *pvVar1;
  long *plVar2;
  undefined8 uVar3;
  code *pcVar4;
  undefined1 auStack_c8 [24];
  undefined **local_b0;
  long lStack_a8;
  long local_a0;
  undefined ***local_98;
  undefined **local_90;
  undefined8 auStack_88 [3];
  undefined1 auStack_70 [8];
  long local_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (param_3 == 0) {
    local_90 = (undefined **)0x0;
    FUN_0562e288(param_1 + 0x18,&local_90);
    FUN_000404d0(&local_90,0);
    *(undefined8 *)(param_1 + 0x38) = auStack_88[0];
    *(undefined ***)(param_1 + 0x30) = local_90;
    plVar2 = *(long **)(param_1 + 0x58);
    *(undefined8 *)(param_1 + 0x58) = 0;
    if (plVar2 == (long *)(param_1 + 0x40)) {
      pcVar4 = *(code **)(*plVar2 + 0x20);
LAB_05626cc4:
      (*pcVar4)();
    }
    else if (plVar2 != (long *)0x0) {
      pcVar4 = *(code **)(*plVar2 + 0x28);
      goto LAB_05626cc4;
    }
  }
  else {
    pvVar1 = _malloc(param_3);
    if (pvVar1 == (void *)0x0) {
      FUN_0562fcb4(auStack_c8);
      FUN_05632e9c(&local_90,7,5,auStack_c8);
      FUN_0562fc90(&local_90);
      FUN_03b35c00(auStack_70,local_68[0]);
      FUN_0562fd84(auStack_88);
      FUN_0562fd84(auStack_c8);
      uVar3 = 0;
      goto LAB_05626ccc;
    }
    if (*param_4 != 0) {
      FUN_0562a9d0(*param_4,param_3);
    }
    if (param_2 != (void *)0x0) {
      _memcpy(pvVar1,param_2,param_3);
    }
    lStack_a8 = *param_4;
    local_a0 = param_4[1];
    if (local_a0 != 0) {
      *(long *)(local_a0 + 8) = *(long *)(local_a0 + 8) + 1;
    }
    local_b0 = &PTR_FUN_09f17180;
    local_98 = &local_b0;
    FUN_056327dc(&local_90,pvVar1,param_3,&local_b0);
    FUN_05627270(param_1 + 0x18,&local_90);
    local_90 = &PTR_FUN_09da5788;
    FUN_0562e260(&local_90);
    if (local_50 == local_68) {
      pcVar4 = *(code **)(*local_50 + 0x20);
LAB_05626c78:
      (*pcVar4)();
    }
    else if (local_50 != (long *)0x0) {
      pcVar4 = *(code **)(*local_50 + 0x28);
      goto LAB_05626c78;
    }
    FUN_0562e140(&local_90);
    if (local_98 == &local_b0) {
      pcVar4 = (code *)(*local_98)[4];
LAB_05626cac:
      (*pcVar4)();
    }
    else if (local_98 != (undefined ***)0x0) {
      pcVar4 = (code *)(*local_98)[5];
      goto LAB_05626cac;
    }
    *(undefined8 *)(param_1 + 8) = *(undefined8 *)(param_1 + 0x30);
    *(size_t *)(param_1 + 0x10) = param_3;
  }
  uVar3 = 1;
LAB_05626ccc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar3);
}


