// Ghidra inferred pseudocode; requested=0x56c9dac
// entry=056c9dac end=056c9ed7

void FUN_056c9dac(undefined8 *param_1,long *param_2,undefined8 param_3)

{
  long lVar1;
  undefined1 local_199;
  undefined1 local_198 [288];
  undefined1 auStack_78 [64];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar1 = FUN_056c25d4(param_3);
  if (*(char *)(lVar1 + 0xe8) == '\x01') {
    lVar1 = FUN_056c25d4(param_3);
    lVar1 = FUN_056db3a0(lVar1 + 8);
    if (*(char *)(lVar1 + 8) == '\x02') {
      (**(code **)(*(long *)((long)param_2 + *(long *)(*param_2 + -0x28)) + 0x10))
                (local_198,(long)param_2 + *(long *)(*param_2 + -0x28));
      param_1[0x29] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x28] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x2b] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x2a] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x25] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x24] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x27] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x26] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x21] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x20] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x23] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x22] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x1d] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x1c] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x1f] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x1e] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x19] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x18] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x1b] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x1a] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x15] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x14] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x17] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x16] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x11] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x10] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x13] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x12] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xd] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xc] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xf] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xe] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[9] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[8] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xb] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[10] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[7] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[6] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
      *param_1 = &SUB_aaaaaaaaaaaaaaaa;
      param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
      local_199 = 5;
      FUN_056c98ec(param_1,auStack_78,&local_199);
      lVar1 = FUN_056c252c(param_1);
      *(undefined1 *)(lVar1 + 0xee) = 0;
      FUN_056cd5a8(local_198);
      goto LAB_056c9ea8;
    }
  }
  local_198[0] = 0xf;
  FUN_056c9b48(param_1,param_2,param_3,local_198);
LAB_056c9ea8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


