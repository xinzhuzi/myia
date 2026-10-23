// Ghidra inferred pseudocode; requested=0x28544e4
// entry=028544e4 end=02854713

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_028544e4(undefined8 param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 ***pppuVar3;
  undefined8 *local_88;
  undefined8 *local_80;
  undefined8 *local_78;
  undefined8 **local_70;
  size_t local_68;
  undefined8 local_60;
  undefined8 **local_58;
  size_t local_50;
  undefined8 local_48;
  
  if ((DAT_0a39ea92 & 1) == 0) {
    _DAT_0a39ea7c = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
    uRam000000000a39ea84 = CONCAT44((int)DAT_08567f40,(int)DAT_088050f0);
    DAT_0a39ea8c = (undefined4)DAT_084a8110;
    DAT_0a39ea90 = 0x65;
    DAT_0a39ea92 = 1;
  }
  sVar2 = _strlen(&DAT_0a39ea7c);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_58);
  }
  if (sVar2 < 0x17) {
    local_48 = CONCAT17((char)sVar2,(undefined7)local_48);
    pppuVar3 = &local_58;
    if (sVar2 != 0) goto LAB_028545c0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    pppuVar3 = (undefined8 ***)__Znwm(uVar1);
    local_48 = uVar1 | 0x8000000000000000;
    local_58 = pppuVar3;
    local_50 = sVar2;
LAB_028545c0:
    _memcpy(pppuVar3,&DAT_0a39ea7c,sVar2);
  }
  *(undefined1 *)((long)pppuVar3 + sVar2) = 0;
  if ((DAT_0a39e948 & 1) == 0) {
    DAT_0a39e940._0_1_ = s_search_imessage_085b1d58[8];
    DAT_0a39e940._1_1_ = s_search_imessage_085b1d58[9];
    DAT_0a39e940._2_1_ = s_search_imessage_085b1d58[10];
    DAT_0a39e940._3_1_ = s_search_imessage_085b1d58[0xb];
    DAT_0a39e940._4_1_ = s_search_imessage_085b1d58[0xc];
    DAT_0a39e940._5_1_ = s_search_imessage_085b1d58[0xd];
    DAT_0a39e940._6_1_ = s_search_imessage_085b1d58[0xe];
    DAT_0a39e940._7_1_ = s_search_imessage_085b1d58[0xf];
    DAT_0a39e948 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a39e940);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_70);
  }
  if (sVar2 < 0x17) {
    local_60 = CONCAT17((char)sVar2,(undefined7)local_60);
    pppuVar3 = &local_70;
    if (sVar2 == 0) goto LAB_02854668;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    pppuVar3 = (undefined8 ***)__Znwm(uVar1);
    local_60 = uVar1 | 0x8000000000000000;
    local_70 = pppuVar3;
    local_68 = sVar2;
  }
  _memcpy(pppuVar3,&DAT_0a39e940,sVar2);
LAB_02854668:
  *(undefined1 *)((long)pppuVar3 + sVar2) = 0;
  local_88 = (undefined8 *)__Znwm(8);
  local_80 = local_88 + 1;
  *local_88 = 0x100000000;
  local_78 = local_80;
  FUN_0286f9c8(param_1,&local_58,&local_70,&local_88);
  if (local_88 != (undefined8 *)0x0) {
    local_80 = local_88;
    __ZdlPvm(local_88,(long)local_78 - (long)local_88);
  }
  if ((long)local_60 < 0) {
    __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
  }
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  return;
}


