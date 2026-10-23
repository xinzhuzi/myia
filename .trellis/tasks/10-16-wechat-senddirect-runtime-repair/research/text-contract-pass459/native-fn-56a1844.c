// Ghidra inferred pseudocode; requested=0x56a1844
// entry=056a1844 end=056a19f7

void FUN_056a1844(long param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  size_t sVar4;
  ulong uVar5;
  undefined8 uVar6;
  undefined1 auStack_58 [24];
  
  uVar6 = *(undefined8 *)(param_1 + 0x10);
  uVar2 = FUN_0008a8b8(param_2);
  uVar3 = FUN_009abfd4(param_2);
  uVar2 = FUN_0591f0b8(uVar6,param_3,uVar2,uVar3,0xffffffffffffffff);
  iVar1 = FUN_0569fba0(param_1,uVar2);
  if ((iVar1 != 0) && (*(char *)(param_1 + 0x70) == '\x01')) {
    uVar2 = __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi(param_1 + 0x78,param_3);
    if ((DAT_0a4d7a5c & 1) == 0) {
      DAT_0a4d7a5a = 0x3a;
      DAT_0a4d7a5c = 1;
    }
    sVar4 = _strlen((char *)&DAT_0a4d7a5a);
    FUN_003b1afc(uVar2,&DAT_0a4d7a5a,sVar4);
    uVar5 = FUN_009abfd4(param_2);
    if (uVar5 < 0x14) {
      FUN_05631328(param_1 + 0x78,param_2);
    }
    else {
      uVar2 = FUN_0008a8b8(param_2);
      FUN_0562fd20(auStack_58,uVar2,0x14);
      uVar2 = FUN_05631328(param_1 + 0x78,auStack_58);
      if ((DAT_0a4d7a64 & 1) == 0) {
        DAT_0a4d7a60 = (undefined4)DAT_084cf428;
        DAT_0a4d7a64 = 1;
      }
      sVar4 = _strlen((char *)&DAT_0a4d7a60);
      FUN_003b1afc(uVar2,&DAT_0a4d7a60,sVar4);
      FUN_0562fd84(auStack_58);
    }
    if ((DAT_0a4d7a5f & 1) == 0) {
      DAT_0a4d7a5d = 0x3b;
      DAT_0a4d7a5f = 1;
    }
    sVar4 = _strlen((char *)&DAT_0a4d7a5d);
    FUN_003b1afc(param_1 + 0x78,&DAT_0a4d7a5d,sVar4);
  }
  return;
}


