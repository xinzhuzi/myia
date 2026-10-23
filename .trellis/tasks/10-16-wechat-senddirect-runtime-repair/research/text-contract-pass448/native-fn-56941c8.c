// Ghidra inferred pseudocode; requested=0x56941c8
// entry=056941c8 end=056942a3

void FUN_056941c8(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined8 uVar1;
  undefined1 auStack_160 [88];
  undefined1 auStack_108 [72];
  undefined1 auStack_c0 [64];
  undefined **local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *puStack_50;
  undefined1 *puStack_48;
  
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_056d6d10(auStack_c0);
  FUN_056d0028(auStack_108);
  uVar1 = FUN_056d6d4c(auStack_c0,auStack_108);
  uVar1 = FUN_056d10a0(uVar1,param_3);
  thunk_FUN_056cf36c(auStack_160,param_4);
  uVar1 = FUN_056d6e08(uVar1,auStack_160);
  FUN_056c2744(&local_80,uVar1);
  local_80 = &PTR_thunk_FUN_056c2628_09f216e8;
  FUN_056cef1c(auStack_160);
  FUN_056cf890(auStack_108);
  thunk_FUN_056c2628(auStack_c0);
  FUN_056942e8(param_1,param_2,&local_80,1);
  thunk_FUN_056c2628(&local_80);
  return;
}


