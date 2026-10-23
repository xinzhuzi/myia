// Ghidra inferred pseudocode; requested=0x56a1bec
// entry=056a1bec end=056a1e53

void FUN_056a1bec(long param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  uint uVar2;
  undefined1 uVar3;
  int iVar4;
  undefined4 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  size_t sVar8;
  long *plVar9;
  ulong uVar10;
  long lVar11;
  long lVar12;
  long lVar13;
  undefined8 uVar14;
  undefined1 auStack_58 [8];
  
  uVar14 = *(undefined8 *)(param_1 + 0x10);
  uVar6 = FUN_05632b8c(param_2);
  uVar7 = FUN_009ce4a8(param_2);
  uVar6 = FUN_0591eaac(uVar14,param_3,uVar6,uVar7,0xffffffffffffffff);
  iVar4 = FUN_0569fba0(param_1,uVar6);
  if (iVar4 == 0) {
    return;
  }
  if (*(char *)(param_1 + 0x70) != '\x01') {
    return;
  }
  plVar1 = (long *)(param_1 + 0x78);
  uVar6 = __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi(plVar1,param_3);
  if ((DAT_0a4d7a5c & 1) == 0) {
    DAT_0a4d7a5a = 0x3a;
    DAT_0a4d7a5c = 1;
  }
  sVar8 = _strlen((char *)&DAT_0a4d7a5a);
  FUN_003b1afc(uVar6,&DAT_0a4d7a5a,sVar8);
  lVar12 = *plVar1;
  lVar13 = *(long *)(lVar12 + -0x18);
  uVar2 = *(uint *)((long)plVar1 + lVar13 + 8);
  *(uint *)((long)plVar1 + lVar13 + 8) = uVar2 & 0xffffffb5 | 8;
  lVar12 = (long)plVar1 + *(long *)(lVar12 + -0x18);
  if (*(int *)(lVar12 + 0x90) == -1) {
    __ZNKSt3__18ios_base6getlocEv(auStack_58,lVar12);
    plVar9 = (long *)__ZNKSt3__16locale9use_facetERNS0_2idE
                               (auStack_58,PTR___ZNSt3__15ctypeIcE2idE_09b367c8);
    uVar5 = (**(code **)(*plVar9 + 0x38))(plVar9,0x20);
    __ZNSt3__16localeD1Ev(auStack_58);
    *(undefined4 *)(lVar12 + 0x90) = uVar5;
  }
  *(undefined4 *)(lVar12 + 0x90) = 0x30;
  uVar10 = FUN_009ce4a8(param_2);
  if (uVar10 < 0xb) {
    lVar12 = FUN_009ce4a8(param_2);
    if (lVar12 == 0) goto LAB_056a1d90;
  }
  else {
    lVar12 = 10;
  }
  lVar13 = 0;
  do {
    lVar11 = FUN_05632b8c(param_2);
    uVar3 = *(undefined1 *)(lVar11 + lVar13);
    *(undefined8 *)(param_1 + 0x90 + *(long *)(*plVar1 + -0x18)) = 2;
    __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEi(plVar1,uVar3);
    lVar13 = lVar13 + 1;
  } while (lVar12 != lVar13);
LAB_056a1d90:
  *(uint *)((long)plVar1 + *(long *)(*plVar1 + -0x18) + 8) = uVar2;
  uVar10 = FUN_009ce4a8(param_2);
  if (10 < uVar10) {
    if ((DAT_0a4d7a64 & 1) == 0) {
      DAT_0a4d7a60 = (undefined4)DAT_084cf428;
      DAT_0a4d7a64 = 1;
    }
    sVar8 = _strlen((char *)&DAT_0a4d7a60);
    FUN_003b1afc(plVar1,&DAT_0a4d7a60,sVar8);
  }
  if ((DAT_0a4d7a5f & 1) == 0) {
    DAT_0a4d7a5d = 0x3b;
    DAT_0a4d7a5f = 1;
  }
  sVar8 = _strlen((char *)&DAT_0a4d7a5d);
  FUN_003b1afc(plVar1,&DAT_0a4d7a5d,sVar8);
  return;
}


