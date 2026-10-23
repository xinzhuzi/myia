// Ghidra inferred pseudocode; requested=0x56cb228
// entry=056cb228 end=056cb35b

void FUN_056cb228(undefined8 param_1,byte *param_2)

{
  byte bVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined4 *puVar4;
  
  bVar1 = *param_2;
  if (bVar1 < 2) {
    if (bVar1 == 0) {
      FUN_0562fcb4(param_1);
      return;
    }
    if ((DAT_0a4d8aad & 1) == 0) {
      DAT_0a4d8aa8 = (undefined4)DAT_08482ff8;
      DAT_0a4d8aac = 0;
      DAT_0a4d8aad = 1;
    }
    puVar4 = &DAT_0a4d8aa8;
  }
  else {
    if (bVar1 != 2) {
      if (bVar1 == 3) {
        FUN_0562fd3c(param_1,param_2 + 8);
        return;
      }
      uVar2 = FUN_05632b8c(param_2 + 8);
      uVar3 = FUN_009ce4a8(param_2 + 8);
      FUN_05630794(param_1,uVar2,uVar3);
      return;
    }
    if ((DAT_0a4d8ab1 & 1) == 0) {
      DAT_0a4d8aae = 0x6625;
      DAT_0a4d8ab0 = 0;
      DAT_0a4d8ab1 = 1;
    }
    puVar4 = (undefined4 *)&DAT_0a4d8aae;
  }
  FUN_05630c8c(puVar4);
  return;
}


