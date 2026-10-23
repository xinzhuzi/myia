// Ghidra inferred pseudocode; requested=0x594c390
// entry=0594c390 end=0594c3ef

undefined8 FUN_0594c390(undefined8 param_1)

{
  undefined8 uVar1;
  undefined8 local_38 [2];
  char local_21;
  
  FUN_05941fe8(local_38,(ulong)PTR_s_N4mars3stn12MMStnManagerE_09f2e408 & 0x7fffffffffffffff);
  uVar1 = FUN_05941f18(param_1,local_38);
  if (local_21 < '\0') {
    __ZdlPv(local_38[0]);
  }
  return uVar1;
}


