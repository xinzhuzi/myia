// Ghidra inferred pseudocode; requested=0x4cbcb04
// entry=04cbcb04 end=04cbce07

undefined8 * FUN_04cbcb04(undefined8 *param_1,long param_2)

{
  uint uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined8 *puVar4;
  ulong uVar5;
  undefined8 *puVar6;
  undefined1 *local_68;
  undefined1 *local_60;
  undefined1 *local_58;
  
  *param_1 = &PTR_thunk_FUN_00ac6290_09eb04f0;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 2) = 0;
  param_1[4] = 0;
  param_1[3] = 0;
  param_1[0x16] = 0;
  param_1[0x15] = 0;
  param_1[0x14] = 0;
  param_1[0x13] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[10] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xd] = 0;
  param_1[0x10] = 0;
  param_1[0xf] = 0;
  *(undefined8 *)((long)param_1 + 0x8a) = 0;
  *(undefined8 *)((long)param_1 + 0x82) = 0;
  *(undefined4 *)(param_1 + 0x17) = 0x3f800000;
  param_1[0x1b] = 0;
  param_1[0x1a] = 0;
  param_1[0x1d] = 0;
  param_1[0x1c] = 0;
  *(undefined2 *)(param_1 + 0x1e) = 0;
  param_1[0x19] = 0;
  param_1[0x18] = 0;
  *(undefined8 *)((long)param_1 + 0xfc) = 0;
  *(undefined8 *)((long)param_1 + 0xf4) = 0;
  param_1[0x2d] = 0;
  param_1[0x2c] = 0;
  puVar6 = param_1 + 0x26;
  param_1[0x27] = 0;
  *puVar6 = 0;
  *(undefined8 *)((long)param_1 + 0x124) = 0;
  *(undefined8 *)((long)param_1 + 0x11c) = 0;
  *(undefined8 *)((long)param_1 + 0x114) = 0;
  *(undefined8 *)((long)param_1 + 0x10c) = 0;
  *(undefined8 *)((long)param_1 + 0x104) = 0;
  param_1[0x29] = 0;
  param_1[0x28] = 0;
  param_1[0x2b] = 0;
  param_1[0x2a] = 0;
  param_1[0x2f] = 0;
  param_1[0x2e] = 0;
  param_1[0x31] = 0;
  param_1[0x30] = 0;
  FUN_04ea6ba0(param_1 + 0x32);
  puVar4 = (undefined8 *)__Znwm(0x20);
  puVar4[2] = 0;
  puVar4[1] = 0;
  *puVar4 = &PTR_FUN_09c08428;
  puVar4[3] = 0;
  param_1[0x41] = puVar4 + 3;
  param_1[0x42] = puVar4;
  *(undefined1 *)(param_1 + 0x43) = 0;
  param_1[0x45] = 0;
  param_1[0x44] = 0;
  param_1[0x47] = 0;
  param_1[0x46] = 0;
  *(undefined1 *)(param_1 + 0x48) = 1;
  param_1[0x4c] = 0;
  param_1[0x4e] = 0;
  param_1[0x4d] = 0;
  *(undefined1 *)(param_1 + 0x4b) = 0;
  param_1[0x4a] = 0;
  param_1[0x49] = 0;
  param_1[0x1f] = *(undefined8 *)(param_2 + 8);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar6,param_2 + 0x18);
  uVar1 = *(uint *)(param_2 + 0x10);
  *(uint *)((long)param_1 + 0x114) = uVar1;
  param_1[0x20] = (ulong)uVar1 * 1000;
  *(undefined4 *)(param_1 + 0x23) = *(undefined4 *)(param_2 + 0x30);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x2c,param_2 + 0x40);
  *(undefined4 *)((long)param_1 + 0x124) = *(undefined4 *)(param_2 + 0x58);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 3,param_2 + 0xf0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 6,param_2 + 0x108);
  FUN_04cbbd20(param_1,*(undefined4 *)(param_2 + 0x34));
  FUN_04cbb728(param_1,*(undefined8 *)(param_2 + 0xa8));
  *(undefined4 *)(param_1 + 0x25) = 0xb;
  uVar5 = *(ulong *)(param_2 + 0x20);
  if (-1 < (char)*(byte *)(param_2 + 0x2f)) {
    uVar5 = (ulong)*(byte *)(param_2 + 0x2f);
  }
  if (uVar5 == 0) {
    uVar5 = *(ulong *)(param_2 + 0x68);
    if (-1 < (char)*(byte *)(param_2 + 0x77)) {
      uVar5 = (ulong)*(byte *)(param_2 + 0x77);
    }
    if (uVar5 != 0) {
      local_60 = &SUB_aaaaaaaaaaaaaaaa;
      local_58 = &SUB_aaaaaaaaaaaaaa;
      local_68 = &DAT_aaaaaaaaaaaaaa00;
      FUN_0471e584(param_2 + 0x60,&local_68);
      *(undefined1 *)(param_1 + 0x4b) = 0;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar6,&local_68);
      if ((long)local_58 < 0) {
        __ZdlPvm(local_68,(ulong)local_58 & 0x7fffffffffffffff);
      }
    }
  }
  if (*(int *)(param_2 + 0x34) == 0x31) {
    if (*(char *)((long)param_1 + 0x147) < '\0') {
      if (param_1[0x27] == 0) goto LAB_04cbcd38;
    }
    else if (*(char *)((long)param_1 + 0x147) == '\0') goto LAB_04cbcd38;
    uVar2 = FUN_04ccd978(puVar6);
  }
  else {
LAB_04cbcd38:
    uVar2 = 0;
  }
  *(undefined4 *)(param_1 + 2) = uVar2;
  param_1[0x21] = *(undefined8 *)((long)param_1 + 0xc);
  if ((param_1[0x44] != 0) && (iVar3 = FUN_04a29d84(param_1), iVar3 != 0)) {
    *(undefined4 *)(param_1[0x44] + 0xc) = uVar2;
  }
  uVar5 = FUN_04a29108(param_1);
  if (((((uVar5 & 1) != 0) || (uVar5 = FUN_04a291d0(param_1), (uVar5 & 1) != 0)) ||
      (uVar5 = FUN_04a28ef8(param_1), (uVar5 & 1) != 0)) ||
     (((uVar5 = FUN_04a28f24(param_1), (uVar5 & 1) != 0 ||
       (uVar5 = FUN_04a28ecc(param_1), (uVar5 & 1) != 0)) ||
      ((uVar5 = FUN_04a2a5c8(param_1), (uVar5 & 1) != 0 ||
       (iVar3 = FUN_04a28ae8(param_1), iVar3 != 0)))))) {
    FUN_04cbc3ac(param_1,1);
  }
  *(undefined1 *)(param_1 + 0x48) = 0;
  iVar3 = FUN_04a28ecc(param_1);
  if (iVar3 != 0) {
    *(undefined1 *)(param_1 + 0x48) = 1;
  }
  FUN_04cbc4c0(param_1,0);
  return param_1;
}


