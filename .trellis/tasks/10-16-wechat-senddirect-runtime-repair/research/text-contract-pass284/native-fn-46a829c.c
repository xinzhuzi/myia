// Ghidra inferred pseudocode; requested=0x46a829c
// entry=046a829c end=046a84af

undefined8 FUN_046a829c(undefined8 param_1,undefined8 *param_2)

{
  undefined1 uVar1;
  ulong uVar2;
  undefined8 ***pppuVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  undefined1 *puVar7;
  undefined8 *puVar8;
  undefined1 *local_88;
  undefined1 *local_80;
  undefined1 *local_78;
  undefined8 **local_70;
  undefined1 *puStack_68;
  undefined8 local_60;
  
  uVar2 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE5rfindEcm
                    (param_2,0x2f,0xffffffffffffffff);
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  local_70 = (undefined8 **)&SUB_aaaaaaaaaaaaaaaa;
  if (uVar2 == 0xffffffffffffffff) {
    if (*(char *)((long)param_2 + 0x17) < '\0') {
      FUN_00018d20(&local_70,*param_2,param_2[1]);
    }
    else {
      puStack_68 = (undefined1 *)param_2[1];
      local_70 = (undefined8 **)*param_2;
      local_60 = (undefined1 *)param_2[2];
    }
    goto LAB_046a8394;
  }
  uVar6 = (ulong)*(char *)((long)param_2 + 0x17);
  if ((long)uVar6 < 0) {
    uVar6 = param_2[1];
    if (uVar6 <= uVar2) goto LAB_046a84a0;
    puVar8 = (undefined8 *)*param_2;
  }
  else {
    puVar8 = param_2;
    if (uVar6 <= uVar2) {
LAB_046a84a0:
                    /* WARNING: Subroutine does not return */
      FUN_0020edd0(&local_70);
    }
  }
  uVar2 = uVar2 + 1;
  puVar7 = (undefined1 *)(uVar6 - uVar2);
  if ((undefined1 *)0x7ffffffffffffff7 < puVar7) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_70);
  }
  if (puVar7 < (undefined1 *)0x17) {
    local_60 = (undefined1 *)CONCAT17((char)puVar7,0xaaaaaaaaaaaaaa);
    pppuVar3 = &local_70;
    if (uVar6 != uVar2) goto LAB_046a8380;
  }
  else {
    uVar6 = 0x19;
    if (((ulong)puVar7 | 7) != 0x17) {
      uVar6 = ((ulong)puVar7 | 7) + 1;
    }
    pppuVar3 = (undefined8 ***)__Znwm(uVar6);
    local_60 = (undefined1 *)(uVar6 | 0x8000000000000000);
    local_70 = pppuVar3;
    puStack_68 = puVar7;
LAB_046a8380:
    _memmove(pppuVar3,(void *)((long)puVar8 + uVar2),(size_t)puVar7);
  }
  *(undefined1 *)((long)pppuVar3 + (long)puVar7) = 0;
LAB_046a8394:
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_88 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a460721 & 1) == 0) {
    DAT_0a46071c = (undefined4)DAT_08531628;
    DAT_0a460720 = 0;
    DAT_0a460721 = 1;
  }
  __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
            (&local_88,&DAT_0a46071c,&local_70);
  lVar4 = FUN_003e8c8c(&DAT_0a460278,param_2);
  if (lVar4 == 0) {
    lVar4 = FUN_003e8c8c(&DAT_0a4602a0,param_2);
    uVar1 = lVar4 != 0;
  }
  else {
    uVar1 = 2;
  }
  uVar5 = FUN_046a850c(param_1,&local_88,uVar1);
  if ((long)local_78 < 0) {
    __ZdlPvm(local_88,(ulong)local_78 & 0x7fffffffffffffff);
  }
  if ((long)local_60 < 0) {
    __ZdlPvm(local_70,(ulong)local_60 & 0x7fffffffffffffff);
  }
  return uVar5;
}


