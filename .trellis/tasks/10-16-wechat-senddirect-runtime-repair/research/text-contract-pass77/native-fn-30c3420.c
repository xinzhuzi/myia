// Ghidra inferred pseudocode; requested=0x30c3420
// entry=030c3420 end=030c3573

undefined8 FUN_030c3420(long param_1,long *param_2,undefined4 param_3,int param_4)

{
  long *plVar1;
  undefined8 uVar2;
  long lVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 local_70;
  undefined1 *puStack_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *local_50;
  long *local_48;
  
  uVar5 = *(undefined8 *)(param_1 + 0x18);
  __ZNSt3__15mutex4lockEv(uVar5);
  uVar2 = (**(code **)(*param_2 + 0x28))(param_2);
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  local_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_50 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_030c15b8(&local_70,0,0);
  FUN_0465f460(local_50,uVar2);
  lVar3 = *(long *)(local_50 + 8);
  if (lVar3 == 0) {
    lVar3 = *(long *)(DAT_0a51ea50 + 8);
  }
  lVar4 = *(long *)(lVar3 + 8);
  if (lVar4 == 0) {
    lVar4 = *(long *)(DAT_0a51ea28 + 8);
  }
  local_70._4_4_ = *(int *)(lVar3 + 0x10);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            ((ulong)&local_70 | 8,*(undefined8 *)(lVar4 + 8));
  local_70 = (undefined1 *)CONCAT44(local_70._4_4_,param_3);
  if ((param_4 != 0) && (local_70._4_4_ == 0)) {
    local_70 = (undefined1 *)CONCAT44(param_4,param_3);
  }
  FUN_030c35a0(param_1,&local_70);
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_48[1];
    local_48[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if ((long)puStack_58 < 0) {
    __ZdlPvm(puStack_68,(ulong)puStack_58 & 0x7fffffffffffffff);
  }
  __ZNSt3__15mutex6unlockEv(uVar5);
  return 1;
}


