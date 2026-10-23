// Ghidra inferred pseudocode; requested=0x5ab3bc0
// entry=05ab3bc0 end=05ab3c8f

long FUN_05ab3bc0(long *param_1,long param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined1 uStack_a1;
  undefined1 auStack_a0 [48];
  undefined1 auStack_70 [24];
  byte local_58;
  undefined1 auStack_50 [32];
  
  uVar1 = (**(code **)(*param_1 + 0x60))();
  FUN_05ab3738(auStack_50,param_2,uVar1,0xffffffff);
  FUN_05ab3220(auStack_70,auStack_50);
  (**(code **)(*param_1 + 0x50))(param_1,auStack_70);
  if ((local_58 & 1) != 0) {
    FUN_05ab442c(auStack_a0,3,
                 "/Users/bkdevops/.wconan2/mmnet/e27341bb_1784873910/mars-private/mars/protobuf/google/protobuf/message_lite.cc"
                 ,0xe0);
    uVar2 = FUN_05ab4444(auStack_a0,"CHECK failed: !coded_out.HadError(): ");
    FUN_05ab4574(&uStack_a1,uVar2);
    FUN_05ab457c(auStack_a0);
  }
  FUN_05ab3254(auStack_70);
  thunk_FUN_0001accc(auStack_50);
  return param_2 + (int)uVar1;
}


