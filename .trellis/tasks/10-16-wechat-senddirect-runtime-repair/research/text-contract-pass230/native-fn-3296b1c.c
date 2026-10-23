// Ghidra inferred pseudocode; requested=0x3296b1c
// entry=03296b1c end=03296d63

undefined8 FUN_03296b1c(undefined8 param_1,long *param_2,undefined8 param_3,long param_4)

{
  undefined8 ****ppppuVar1;
  undefined8 uVar2;
  undefined **local_208 [11];
  undefined1 auStack_1b0 [64];
  undefined1 auStack_170 [8];
  undefined1 auStack_168 [8];
  undefined1 *local_160;
  undefined1 local_150;
  undefined7 uStack_14f;
  long *plStack_148;
  undefined **local_140;
  undefined1 *puStack_138;
  undefined1 *puStack_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *puStack_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *puStack_f0;
  undefined **local_e8;
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *puStack_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined **local_a8;
  undefined8 ***local_a0;
  undefined8 ***pppuStack_98;
  undefined1 *local_90;
  undefined1 *local_88;
  long *plStack_80;
  
  if (param_2[1] == *param_2) {
    uVar2 = 1;
  }
  else {
    plStack_80 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    pppuStack_98 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
    local_a0 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
    local_88 = &SUB_aaaaaaaaaaaaaaaa;
    local_90 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_c0 = &SUB_aaaaaaaaaaaaaaaa;
    local_a8 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_e0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
    local_100 = &SUB_aaaaaaaaaaaaaaaa;
    local_e8 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    puStack_f0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
    local_120 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_110 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
    local_140 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_130 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_03296ddc(local_208);
    FUN_056d6250(auStack_1b0,param_3);
    local_150 = 2;
    plStack_148 = param_2;
    FUN_056f5490(&local_140,local_208);
    local_140 = &PTR_FUN_09da6390;
    FUN_056c2744(&local_e8,auStack_1b0);
    local_e8 = &PTR_thunk_FUN_056c2628_09f215f8;
    local_140 = &PTR_FUN_09df1c00;
    local_90 = (undefined1 *)0x0;
    local_a0 = &local_a0;
    pppuStack_98 = &local_a0;
    for (; local_160 != auStack_168; local_160 = *(undefined1 **)(local_160 + 8)) {
      ppppuVar1 = (undefined8 ****)__Znwm(0x108);
      ppppuVar1[0x18] = (undefined8 ***)&PTR____cxa_pure_virtual_09da57d8;
      *ppppuVar1 = (undefined8 ***)0x0;
      ppppuVar1[1] = (undefined8 ***)0x0;
      FUN_02703c98(ppppuVar1 + 2,&PTR_PTR_09f24220,local_160 + 0x10);
      ppppuVar1[2] = (undefined8 ***)&PTR_FUN_09f23fe8;
      ppppuVar1[0x18] = (undefined8 ***)&PTR_FUN_09f24040;
      ppppuVar1[0x19] = (undefined8 ***)&PTR_FUN_09f24080;
      ppppuVar1[0x1a] = (undefined8 ***)&PTR_FUN_09f240c0;
      ppppuVar1[0x1b] = (undefined8 ***)&PTR_FUN_09f24100;
      ppppuVar1[0x1c] = (undefined8 ***)&PTR_FUN_09f24140;
      ppppuVar1[0x1d] = (undefined8 ***)&PTR_FUN_09f24180;
      ppppuVar1[0x1e] = (undefined8 ***)&PTR_FUN_09f241c0;
      ppppuVar1[0x1f] = (undefined8 ***)&PTR_FUN_09f24200;
      ppppuVar1[0x20] = *(undefined8 ****)(local_160 + 0x100);
      *ppppuVar1 = local_a0;
      ppppuVar1[1] = &local_a0;
      local_a0[1] = ppppuVar1;
      local_90 = (undefined1 *)((long)local_90 + 1);
      local_a0 = ppppuVar1;
    }
    local_a8 = &PTR_FUN_09f24930;
    local_88 = (undefined1 *)CONCAT71(uStack_14f,local_150);
    plStack_80 = plStack_148;
    FUN_056fa768(auStack_170);
    local_208[0] = &PTR_FUN_09da6390;
    thunk_FUN_056c2628(auStack_1b0);
    FUN_056f54fc(local_208);
    if (*(long *)(param_4 + 0x18) != 0) {
      FUN_03296ee8(&local_140,param_4);
    }
    uVar2 = FUN_032970cc(&local_140);
    FUN_056fa768(&local_a8);
    local_140 = &PTR_FUN_09da6390;
    thunk_FUN_056c2628(&local_e8);
    FUN_056f54fc(&local_140);
  }
  return uVar2;
}


