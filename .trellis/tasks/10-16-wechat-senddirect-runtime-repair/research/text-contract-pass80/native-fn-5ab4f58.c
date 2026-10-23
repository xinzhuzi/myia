// Ghidra inferred pseudocode; requested=0x5ab4f58
// entry=05ab4f58 end=05ab5023

void FUN_05ab4f58(int param_1,long *param_2,undefined8 param_3)

{
  uint uVar1;
  long *plVar2;
  undefined8 uVar3;
  byte bVar4;
  undefined1 uStack_51;
  undefined1 auStack_50 [48];
  
  FUN_05ab33f0(param_3,param_1 << 3 | 2);
  bVar4 = *(byte *)((long)param_2 + 0x17);
  if (((char)bVar4 < '\0') && ((ulong)param_2[1] >> 0x1f != 0)) {
    FUN_05ab442c(auStack_50,3,
                 "/Users/bkdevops/.wconan2/mmnet/e27341bb_1784873910/mars-private/mars/protobuf/google/protobuf/wire_format_lite.cc"
                 ,0x11c);
    uVar3 = FUN_05ab4444(auStack_50,"CHECK failed: value.size() <= kint32max: ");
    FUN_05ab4574(&uStack_51,uVar3);
    FUN_05ab457c(auStack_50);
    bVar4 = *(byte *)((long)param_2 + 0x17);
  }
  uVar1 = *(uint *)(param_2 + 1);
  if (-1 < (char)bVar4) {
    uVar1 = (uint)bVar4;
  }
  FUN_05ab33f0(param_3,uVar1);
  plVar2 = (long *)*param_2;
  uVar1 = *(uint *)(param_2 + 1);
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    plVar2 = param_2;
    uVar1 = (uint)*(byte *)((long)param_2 + 0x17);
  }
  FUN_05ab3290(param_3,plVar2,uVar1);
  return;
}


