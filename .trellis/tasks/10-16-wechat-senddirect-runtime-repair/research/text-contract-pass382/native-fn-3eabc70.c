// Ghidra inferred pseudocode; requested=0x3eabc70
// entry=03eabc70 end=03eabe7f

void FUN_03eabc70(long param_1)

{
  long lVar1;
  undefined1 local_a8;
  undefined7 uStack_a7;
  undefined7 local_98;
  char cStack_91;
  undefined8 local_90;
  long *local_88;
  undefined8 local_80;
  long *local_78;
  undefined8 local_70;
  long *local_68;
  undefined1 *local_60;
  undefined8 *puStack_58;
  undefined1 *puStack_50;
  undefined8 *local_48;
  undefined8 *local_40;
  undefined1 *puStack_38;
  undefined1 *puStack_30;
  undefined1 *local_28;
  
  puStack_38 = &SUB_aaaaaaaaaaaaaaaa;
  local_40 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_28 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_30 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_58 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  local_48 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0559f2a0(&local_60);
  if ((DAT_0a435a16 & 1) == 0) {
    DAT_0a435a08._0_1_ = s_JavaScrifunction_08572f98[8];
    DAT_0a435a08._1_1_ = s_JavaScrifunction_08572f98[9];
    DAT_0a435a08._2_1_ = s_JavaScrifunction_08572f98[10];
    DAT_0a435a08._3_1_ = s_JavaScrifunction_08572f98[0xb];
    DAT_0a435a08._4_1_ = s_JavaScrifunction_08572f98[0xc];
    DAT_0a435a08._5_1_ = s_JavaScrifunction_08572f98[0xd];
    DAT_0a435a08._6_1_ = s_JavaScrifunction_08572f98[0xe];
    DAT_0a435a08._7_1_ = s_JavaScrifunction_08572f98[0xf];
    DAT_0a435a10 = (undefined4)DAT_08760488;
    DAT_0a435a14 = 0x6c;
    DAT_0a435a16 = 1;
  }
  local_28 = (undefined1 *)((ulong)local_28 | 1);
  if (puStack_58 == DAT_0a523c00) {
    puStack_58 = (undefined8 *)__Znwm(0x18);
    *puStack_58 = 0;
    puStack_58[1] = 0;
    puStack_58[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (puStack_58,&DAT_0a435a08);
  local_28 = (undefined1 *)((ulong)local_28 | 4);
  if (local_48 == &DAT_0a524ad0) {
    local_48 = (undefined8 *)__Znwm(0x18);
    *local_48 = 0;
    local_48[1] = 0;
    local_48[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_48,param_1 + 8);
  local_28 = (undefined1 *)((ulong)local_28 | 8);
  if (local_40 == &DAT_0a524ad0) {
    local_40 = (undefined8 *)__Znwm(0x18);
    *local_40 = 0;
    local_40[1] = 0;
    local_40[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_40,param_1 + 0x20);
  FUN_0466aca8(&local_90);
  FUN_01205740(&local_80,local_90);
  FUN_026870f0(&local_70,local_80);
  cStack_91 = '\0';
  local_a8 = 0;
  FUN_02857ca4(local_70,&local_a8,&local_60);
  if (cStack_91 < '\0') {
    __ZdlPvm(CONCAT71(uStack_a7,local_a8),CONCAT17(cStack_91,local_98) & 0x7fffffffffffffff);
  }
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_68[1];
    local_68[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_68);
    }
  }
  if (local_78 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_78[1];
    local_78[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_78 + 0x10))(local_78);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_78);
    }
  }
  if (local_88 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_88[1];
    local_88[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_88 + 0x10))(local_88);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_88);
    }
  }
  FUN_055bebd4(&local_60);
  return;
}


