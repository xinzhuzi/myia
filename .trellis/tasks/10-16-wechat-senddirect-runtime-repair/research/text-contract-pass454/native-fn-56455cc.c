// Ghidra inferred pseudocode; requested=0x56455cc
// entry=056455cc end=0564566f

long * FUN_056455cc(long *param_1)

{
  undefined8 *puVar1;
  long lVar2;
  undefined1 auStack_38 [24];
  
  puVar1 = (undefined8 *)FUN_056927b4();
  *puVar1 = &PTR____cxa_pure_virtual_09f18c30;
  *(undefined4 *)(puVar1 + 0x43) = 0;
  *(undefined1 *)((long)puVar1 + 0x21c) = 0;
  puVar1[0x45] = puVar1 + 0x45;
  puVar1[0x46] = puVar1 + 0x45;
  puVar1[0x47] = 0;
  puVar1[0x44] = &PTR_FUN_09f1a798;
  puVar1[0x49] = puVar1 + 0x49;
  puVar1[0x4a] = puVar1 + 0x49;
  puVar1[0x4c] = 0;
  puVar1[0x4b] = 0;
  puVar1[0x48] = &PTR_FUN_09f1a798;
  FUN_0562fcb4(auStack_38);
  lVar2 = (**(code **)(*param_1 + 0x20))(param_1,auStack_38);
  param_1[0x4c] = lVar2;
  FUN_0562fd84(auStack_38);
  return param_1;
}


