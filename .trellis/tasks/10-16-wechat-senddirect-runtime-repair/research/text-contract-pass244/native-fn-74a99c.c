// Ghidra inferred pseudocode; requested=0x74a99c
// entry=0074a99c end=0074aa3f

void FUN_0074a99c(char *param_1,undefined8 param_2)

{
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [24];
  undefined8 local_38;
  
  if (*param_1 == '\x03') {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_2,*(undefined8 *)(param_1 + 8));
    return;
  }
  FUN_070dc3d8(auStack_50,auStack_58,param_1,&local_38);
  FUN_003b23fc(auStack_50,&DAT_0a29e364,auStack_58);
  FUN_003b2af0(local_38,0x12e,auStack_50,param_1);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(local_38,&PTR_DAT_09bf35b0,FUN_002283d8);
}


