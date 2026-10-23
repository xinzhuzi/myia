// Ghidra inferred pseudocode; requested=0x56456ec
// entry=056456ec end=0564595b

void FUN_056456ec(long param_1,int param_2)

{
  undefined1 auStack_b8 [24];
  undefined1 local_a0 [8];
  undefined1 auStack_98 [96];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (param_2 < 0x404) {
    if (param_2 == 0x101) {
      local_a0[0] = 3;
      FUN_056c9128(auStack_b8,&DAT_0a524420);
      FUN_056309f0(auStack_98,auStack_b8);
      FUN_0562fd84(auStack_b8);
      FUN_05626090(param_1 + 0x28,&DAT_0a5242d0,local_a0);
    }
    else {
      if (param_2 != 0x201) {
        if (param_2 != 0x301) goto LAB_05645880;
        goto LAB_05645798;
      }
      local_a0[0] = 3;
      FUN_056c9128(auStack_b8,&DAT_0a524438);
      FUN_056309f0(auStack_98,auStack_b8);
      FUN_0562fd84(auStack_b8);
      FUN_05626090(param_1 + 0x28,&DAT_0a5242d0,local_a0);
    }
  }
  else if (param_2 < 0x601) {
    if (param_2 == 0x404) {
LAB_05645798:
      local_a0[0] = 3;
      FUN_056c9128(auStack_b8,&DAT_0a524480);
      FUN_056309f0(auStack_98,auStack_b8);
      FUN_0562fd84(auStack_b8);
      FUN_05626090(param_1 + 0x28,&DAT_0a5242d0,local_a0);
    }
    else {
      if (param_2 != 0x501) {
LAB_05645880:
        FUN_05634db4(param_1 + 0x28,&DAT_0a5242d0);
        goto LAB_05645928;
      }
      local_a0[0] = 3;
      FUN_056c9128(auStack_b8,&DAT_0a524450);
      FUN_056309f0(auStack_98,auStack_b8);
      FUN_0562fd84(auStack_b8);
      FUN_05626090(param_1 + 0x28,&DAT_0a5242d0,local_a0);
    }
  }
  else if (param_2 == 0x601) {
    local_a0[0] = 3;
    FUN_056c9128(auStack_b8,&DAT_0a524468);
    FUN_056309f0(auStack_98,auStack_b8);
    FUN_0562fd84(auStack_b8);
    FUN_05626090(param_1 + 0x28,&DAT_0a5242d0,local_a0);
  }
  else {
    if (param_2 != 0x701) goto LAB_05645880;
    local_a0[0] = 3;
    FUN_056c9128(auStack_b8,&DAT_0a524498);
    FUN_056309f0(auStack_98,auStack_b8);
    FUN_0562fd84(auStack_b8);
    FUN_05626090(param_1 + 0x28,&DAT_0a5242d0,local_a0);
  }
  FUN_056caefc(local_a0);
LAB_05645928:
  *(int *)(param_1 + 0x218) = param_2;
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


