// Ghidra inferred pseudocode; requested=0x206bc
// entry=000206bc end=000207c7

bool FUN_000206bc(undefined8 param_1,ulong param_2,long *param_3)

{
  ulong uVar1;
  ulong uVar2;
  undefined8 ****ppppuVar3;
  uint uVar4;
  ulong uVar5;
  undefined8 ***local_48;
  ulong uStack_40;
  undefined8 local_38;
  
  local_48 = (undefined8 ****)0x0;
  uStack_40 = 0;
  local_38 = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEmc
            (&local_48,(param_2 >> 2) * 3 + 2,0);
  ppppuVar3 = (undefined8 ****)local_48;
  if (-1 < (long)local_38) {
    ppppuVar3 = &local_48;
  }
  uVar1 = FUN_000abf6c(ppppuVar3,param_1,param_2);
  uVar2 = (ulong)local_38._7_1_;
  uVar4 = (uint)(char)local_38._7_1_;
  if (uVar1 == 0xffffffffffffffff) goto LAB_00020798;
  if ((int)uVar4 < 0) {
    ppppuVar3 = (undefined8 ****)local_48;
    uVar2 = uStack_40;
    uVar5 = uVar1;
    if (uVar1 <= uStack_40) goto LAB_00020770;
LAB_00020754:
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEmc
              (&local_48,uVar1 - uVar2,0);
  }
  else {
    if (uVar2 < uVar1) goto LAB_00020754;
    local_38 = CONCAT17((char)uVar1,(undefined7)local_38);
    ppppuVar3 = &local_48;
    uVar5 = uStack_40;
LAB_00020770:
    uStack_40 = uVar5;
    *(undefined1 *)((long)ppppuVar3 + uVar1) = 0;
  }
  ppppuVar3 = (undefined8 ****)*param_3;
  uVar2 = param_3[1];
  uVar5 = param_3[2];
  param_3[1] = uStack_40;
  *param_3 = (long)local_48;
  param_3[2] = local_38;
  uVar4 = (uint)(byte)(uVar5 >> 0x38);
  local_48 = ppppuVar3;
  uStack_40 = uVar2;
  local_38 = uVar5;
LAB_00020798:
  if ((uVar4 >> 7 & 1) != 0) {
    __ZdlPvm(local_48,local_38 & 0x7fffffffffffffff);
  }
  return uVar1 != 0xffffffffffffffff;
}


