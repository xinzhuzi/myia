// Ghidra inferred pseudocode; requested=0x30c2ed8
// entry=030c2ed8 end=030c2f5b

undefined8 FUN_030c2ed8(long param_1,undefined8 param_2,undefined8 param_3,undefined1 *param_4)

{
  undefined8 ***pppuVar1;
  uint uVar2;
  undefined8 **local_38;
  undefined1 *local_30;
  undefined8 local_28;
  
  *param_4 = 0;
  local_30 = &SUB_aaaaaaaaaaaaaaaa;
  local_28 = &SUB_aaaaaaaaaaaaaaaa;
  local_38 = (undefined8 **)&SUB_aaaaaaaaaaaaaaaa;
  FUN_05ab4028(&local_38,param_1 + 0x78);
  pppuVar1 = (undefined8 ***)local_38;
  uVar2 = (uint)local_30;
  if (-1 < (long)local_28) {
    pppuVar1 = &local_38;
    uVar2 = (uint)local_28._7_1_;
  }
  FUN_04659f18(param_2,pppuVar1,uVar2);
  if ((long)local_28 < 0) {
    __ZdlPvm(local_38,(ulong)local_28 & 0x7fffffffffffffff);
  }
  return 1;
}


