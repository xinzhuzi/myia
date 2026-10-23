// Ghidra inferred pseudocode; requested=0x3bda648
// entry=03bda648 end=03bda74f

void FUN_03bda648(long *param_1,undefined8 param_2,int param_3,undefined8 param_4)

{
  undefined1 *puVar1;
  long *plVar2;
  long lVar3;
  undefined8 uVar4;
  long lVar5;
  undefined1 *local_30;
  long *local_28;
  
  local_30 = &SUB_aaaaaaaaaaaaaaaa;
  local_28 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  if (param_3 == 1) {
    uVar4 = FUN_03343580(param_2,param_4,0);
    FUN_0334a774(&local_30,param_2,uVar4);
    puVar1 = local_30;
joined_r0x03bda6c4:
    local_30 = puVar1;
    if (((puVar1 != (undefined1 *)0x0) && (*(long *)(puVar1 + 8) != 0)) &&
       (lVar3 = ___dynamic_cast(*(long *)(puVar1 + 8),&PTR_DAT_09e227a0,&PTR_DAT_09df14c0,0),
       lVar3 != 0)) {
      lVar5 = *(long *)(puVar1 + 0x10);
      *param_1 = lVar3;
      param_1[1] = lVar5;
      if (lVar5 != 0) {
        *(long *)(lVar5 + 8) = *(long *)(lVar5 + 8) + 1;
      }
      goto LAB_03bda710;
    }
  }
  else {
    if (param_3 == 2) {
      uVar4 = FUN_0334f98c(param_2,param_4,0);
      FUN_03355090(&local_30,param_2,uVar4);
      puVar1 = local_30;
      goto joined_r0x03bda6c4;
    }
    local_30 = (undefined1 *)0x0;
    local_28 = (long *)0x0;
  }
  *param_1 = 0;
  param_1[1] = 0;
LAB_03bda710:
  plVar2 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_28[1];
    local_28[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  return;
}


