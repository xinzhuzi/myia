// Ghidra inferred pseudocode; requested=0x46687e8
// entry=046687e8 end=0466891f

void FUN_046687e8(long param_1)

{
  ulong uVar1;
  undefined *puVar2;
  long lVar3;
  uint uVar4;
  uint uVar5;
  size_t sVar6;
  undefined8 ***pppuVar7;
  undefined8 **local_68;
  size_t local_60;
  undefined8 local_58;
  long *local_50;
  long *local_48;
  
  FUN_04a447f4(*(undefined8 *)(param_1 + 0xb0));
  FUN_04a7a29c(&local_50);
  puVar2 = PTR_s_upgradeToV4_kHasScanAllBetaUserK_0a05ac40;
  sVar6 = _strlen(PTR_s_upgradeToV4_kHasScanAllBetaUserK_0a05ac40);
  if (0x7ffffffffffffff7 < sVar6) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_68);
  }
  if (sVar6 < 0x17) {
    local_58 = CONCAT17((char)sVar6,(undefined7)local_58);
    pppuVar7 = &local_68;
    if (sVar6 == 0) goto LAB_04668888;
  }
  else {
    uVar1 = 0x19;
    if ((sVar6 | 7) != 0x17) {
      uVar1 = (sVar6 | 7) + 1;
    }
    pppuVar7 = (undefined8 ***)__Znwm(uVar1);
    local_58 = uVar1 | 0x8000000000000000;
    local_68 = pppuVar7;
    local_60 = sVar6;
  }
  _memmove(pppuVar7,puVar2,sVar6);
LAB_04668888:
  *(undefined1 *)((long)pppuVar7 + sVar6) = 0;
  uVar4 = (**(code **)(*local_50 + 0x58))(local_50,&local_68,0);
  if ((long)local_58 < 0) {
    __ZdlPvm(local_68,local_58 & 0x7fffffffffffffff);
  }
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_48[1];
    local_48[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_48);
    }
  }
  uVar5 = FUN_04a6e044();
  if (((uVar4 | uVar5) & 1) == 0) {
    FUN_04a46240();
  }
  return;
}


