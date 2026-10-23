// Ghidra inferred pseudocode; requested=0x30251cc
// entry=030251cc end=0302534b

void FUN_030251cc(undefined8 *param_1,undefined8 param_2)

{
  ulong uVar1;
  undefined1 **ppuVar2;
  size_t sVar3;
  undefined8 ***pppuVar4;
  undefined8 *puVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined1 *local_70;
  ulong uStack_68;
  undefined7 local_60;
  byte bStack_59;
  undefined8 **local_58;
  size_t local_50;
  undefined8 local_48;
  
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a3d4499 & 1) == 0) {
    DAT_0a3d4494 = (undefined4)DAT_0857cfa0;
    DAT_0a3d4498 = 0;
    DAT_0a3d4499 = 1;
  }
  sVar3 = _strlen((char *)&DAT_0a3d4494);
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_58);
  }
  if (sVar3 < 0x17) {
    local_48 = CONCAT17((char)sVar3,(undefined7)local_48);
    pppuVar4 = &local_58;
    if (sVar3 == 0) goto LAB_03025294;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppuVar4 = (undefined8 ***)__Znwm(uVar1);
    local_48 = uVar1 | 0x8000000000000000;
    local_58 = pppuVar4;
    local_50 = sVar3;
  }
  _memcpy(pppuVar4,&DAT_0a3d4494,sVar3);
LAB_03025294:
  *(undefined1 *)((long)pppuVar4 + sVar3) = 0;
  FUN_06686dd8(&local_70,param_2);
  ppuVar2 = (undefined1 **)local_70;
  if (-1 < (char)bStack_59) {
    uStack_68 = (ulong)bStack_59;
    ppuVar2 = &local_70;
  }
  puVar5 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                     (&local_58,ppuVar2,uStack_68);
  if (*(char *)((long)puVar5 + 0x17) < '\0') {
    FUN_00018d20(param_1,*puVar5,puVar5[1]);
  }
  else {
    uVar7 = puVar5[1];
    uVar6 = *puVar5;
    param_1[2] = puVar5[2];
    param_1[1] = uVar7;
    *param_1 = uVar6;
  }
  if ((char)bStack_59 < '\0') {
    __ZdlPvm(local_70,CONCAT17(bStack_59,local_60) & 0x7fffffffffffffff);
  }
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  return;
}


