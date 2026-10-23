// Ghidra inferred pseudocode; requested=0x3c7534c
// entry=03c7534c end=03c756c7

/* WARNING: Removing unreachable block (ram,0x03c75694) */
/* WARNING: Removing unreachable block (ram,0x03c75428) */
/* WARNING: Removing unreachable block (ram,0x03c75668) */
/* WARNING: Removing unreachable block (ram,0x03c75640) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_03c7534c(undefined8 param_1)

{
  size_t sVar1;
  undefined8 ***pppuVar2;
  ulong uVar3;
  undefined1 local_b8;
  undefined7 uStack_b7;
  undefined7 local_a8;
  char cStack_a1;
  undefined1 local_a0;
  undefined7 uStack_9f;
  undefined7 local_90;
  char cStack_89;
  undefined1 local_88;
  undefined7 uStack_87;
  undefined7 local_78;
  char cStack_71;
  undefined1 *local_70;
  undefined1 *puStack_68;
  undefined8 **local_60;
  size_t sStack_58;
  undefined8 local_50;
  undefined1 *local_48;
  undefined1 *local_40;
  undefined1 *local_38;
  
  local_40 = &SUB_aaaaaaaaaaaaaaaa;
  local_38 = &SUB_aaaaaaaaaaaaaaaa;
  local_48 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a426711 & 1) == 0) {
    uRam000000000a426708 = s_4jn_t3er5ger_g1tInitSilentRestar_0897cf20._8_8_;
    _DAT_0a426700 = s_4jn_t3er5ger_g1tInitSilentRestar_0897cf20._0_8_;
    DAT_0a426710 = 0;
    DAT_0a426711 = 1;
  }
  sVar1 = _strlen(&DAT_0a426700);
  if (0x7ffffffffffffff7 < sVar1) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_60);
  }
  if (sVar1 < 0x17) {
    local_50 = CONCAT17((char)sVar1,(undefined7)local_50);
    pppuVar2 = &local_60;
    if (sVar1 == 0) goto LAB_03c7540c;
  }
  else {
    uVar3 = 0x19;
    if ((sVar1 | 7) != 0x17) {
      uVar3 = (sVar1 | 7) + 1;
    }
    pppuVar2 = (undefined8 ***)__Znwm(uVar3);
    local_50 = uVar3 | 0x8000000000000000;
    local_60 = pppuVar2;
    sStack_58 = sVar1;
  }
  _memcpy(pppuVar2,&DAT_0a426700,sVar1);
LAB_03c7540c:
  *(undefined1 *)((long)pppuVar2 + sVar1) = 0;
  FUN_04756024(&local_48,param_1,&local_60);
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_04878be8(&local_70,&local_48);
  uVar3 = (ulong)local_70 & 0xff;
  if (((char)local_70 != '\0') && ((char)local_70 != '\t')) {
    cStack_71 = '\0';
    local_88 = 0;
    if ((DAT_0a4266e7 & 1) == 0) {
      DAT_0a4266e5 = 0x31;
      DAT_0a4266e7 = 1;
    }
    FUN_0487929c(&local_60,&local_70,&DAT_0a4266e5,&local_88);
    pppuVar2 = (undefined8 ***)local_60;
    if (-1 < (long)local_50._7_1_) {
      pppuVar2 = &local_60;
    }
    sVar1 = sStack_58;
    if (-1 < (long)local_50) {
      sVar1 = (long)local_50._7_1_;
    }
    FUN_000206bc(pppuVar2,sVar1,&DAT_0a426690);
    if (cStack_71 < '\0') {
      __ZdlPvm(CONCAT71(uStack_87,local_88),CONCAT17(cStack_71,local_78) & 0x7fffffffffffffff);
    }
    cStack_89 = '\0';
    local_a0 = 0;
    if ((DAT_0a4266ea & 1) == 0) {
      DAT_0a4266e8 = 0x32;
      DAT_0a4266ea = 1;
    }
    FUN_0487929c(&local_60,&local_70,&DAT_0a4266e8,&local_a0);
    pppuVar2 = (undefined8 ***)local_60;
    if (-1 < (long)local_50._7_1_) {
      pppuVar2 = &local_60;
    }
    sVar1 = sStack_58;
    if (-1 < (long)local_50) {
      sVar1 = (long)local_50._7_1_;
    }
    FUN_000206bc(pppuVar2,sVar1,&DAT_0a4266a8);
    if (cStack_89 < '\0') {
      __ZdlPvm(CONCAT71(uStack_9f,local_a0),CONCAT17(cStack_89,local_90) & 0x7fffffffffffffff);
    }
    cStack_a1 = '\0';
    local_b8 = 0;
    if ((DAT_0a4266ed & 1) == 0) {
      DAT_0a4266eb = 0x33;
      DAT_0a4266ed = 1;
    }
    FUN_0487929c(&local_60,&local_70,&DAT_0a4266eb,&local_b8);
    if ((long)DAT_0a4266d0 < 0) {
      __ZdlPvm(DAT_0a4266c0,DAT_0a4266d0 & 0x7fffffffffffffff);
    }
    DAT_0a4266c8 = sStack_58;
    DAT_0a4266c0 = (undefined8 ***)local_60;
    DAT_0a4266d0 = local_50;
    local_50 = local_50 & 0xffffffffffffff;
    local_60 = (undefined8 **)((ulong)local_60 & 0xffffffffffffff00);
    if (cStack_a1 < '\0') {
      __ZdlPvm(CONCAT71(uStack_b7,local_b8),CONCAT17(cStack_a1,local_a8) & 0x7fffffffffffffff);
    }
    if ((DAT_0a4266f0 & 1) == 0) {
      DAT_0a4266ee = 0x34;
      DAT_0a4266f0 = 1;
    }
    DAT_0a4266d8 = FUN_04879214(&local_70,&DAT_0a4266ee,0);
    uVar3 = (ulong)local_70 & 0xff;
  }
  FUN_001fa1c8(&puStack_68,uVar3);
  return 1;
}


