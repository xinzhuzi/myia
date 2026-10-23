// Ghidra inferred pseudocode; requested=0x5ab3ab8
// entry=05ab3ab8 end=05ab3bbf

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_05ab3ab8(long *param_1,long param_2,int param_3)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  byte bVar4;
  undefined8 local_c0;
  long lStack_b8;
  long local_b0;
  int local_a8;
  undefined8 local_a4;
  undefined2 local_9c;
  int local_98;
  undefined8 local_94;
  undefined8 uStack_8c;
  undefined4 local_84;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined1 uStack_69;
  undefined8 local_68 [2];
  char local_51;
  undefined1 auStack_50 [48];
  
  local_c0 = 0;
  local_b0 = param_2 + param_3;
  local_a4 = 0;
  local_9c = 0;
  uStack_8c = _UNK_08b8c9c8;
  local_94 = _DAT_08b8c9c0;
  local_84 = DAT_0a123fc0;
  local_80 = 0;
  uStack_78 = 0;
  lStack_b8 = param_2;
  local_a8 = param_3;
  local_98 = param_3;
  (**(code **)(*param_1 + 0x20))();
  iVar1 = (**(code **)(*param_1 + 0x40))(param_1,&local_c0);
  bVar4 = 0;
  if (iVar1 != 0) {
    uVar2 = (**(code **)(*param_1 + 0x28))(param_1);
    if ((uVar2 & 1) == 0) {
      FUN_05ab442c(auStack_50,2,
                   "/Users/bkdevops/.wconan2/mmnet/e27341bb_1784873910/mars-private/mars/protobuf/google/protobuf/message_lite.cc"
                   ,0x7b);
      FUN_05ab3c90(local_68,param_1);
      uVar3 = FUN_05ab446c(auStack_50,local_68);
      FUN_05ab4574(&uStack_69,uVar3);
      if (local_51 < '\0') {
        __ZdlPv(local_68[0]);
      }
      FUN_05ab457c(auStack_50);
      bVar4 = 0;
    }
    else {
      bVar4 = (byte)local_9c;
    }
  }
  thunk_FUN_05ab25ec(&local_c0);
  return bVar4 & 1;
}


