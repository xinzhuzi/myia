// Ghidra inferred pseudocode; requested=0x597d418
// entry=0597d418 end=0597d477

undefined8 FUN_0597d418(undefined8 param_1)

{
  undefined8 uVar1;
  undefined8 local_38 [2];
  char local_21;
  
  FUN_05941fe8(local_38,(ulong)PTR_s_N4mars7account14AccountManagerE_09f460a8 & 0x7fffffffffffffff);
  uVar1 = FUN_05941f18(param_1,local_38);
  if (local_21 < '\0') {
    __ZdlPv(local_38[0]);
  }
  return uVar1;
}


