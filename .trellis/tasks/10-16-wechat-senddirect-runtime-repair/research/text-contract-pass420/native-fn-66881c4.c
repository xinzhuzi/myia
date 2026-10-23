// Ghidra inferred pseudocode; requested=0x66881c4
// entry=066881c4 end=06688273

bool FUN_066881c4(undefined8 *param_1,undefined8 *param_2)

{
  ulong uVar1;
  undefined8 *puVar2;
  byte bVar3;
  byte bVar4;
  ulong uVar5;
  bool bVar6;
  int iVar7;
  ulong uVar8;
  ulong uVar9;
  ulong uVar10;
  
  bVar3 = *(byte *)((long)param_1 + 0x17);
  uVar9 = (ulong)bVar3;
  uVar8 = param_1[1];
  uVar10 = uVar8;
  if (-1 < (char)bVar3) {
    uVar10 = uVar9;
  }
  bVar4 = *(byte *)((long)param_2 + 0x17);
  uVar1 = param_2[1];
  if (-1 < (char)bVar4) {
    uVar1 = (ulong)bVar4;
  }
  uVar5 = uVar10 - uVar1;
  if (uVar10 < uVar1) {
    bVar6 = false;
  }
  else {
    if ((char)bVar3 < '\0') {
      if (uVar1 == 0xffffffffffffffff || uVar8 < uVar5) goto LAB_06688270;
      uVar10 = uVar8 - uVar5;
      if (uVar1 <= uVar8 - uVar5) {
        uVar10 = uVar1;
      }
      param_1 = (undefined8 *)*param_1;
    }
    else {
      if (uVar9 < uVar5 || uVar1 == 0xffffffffffffffff) {
LAB_06688270:
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0();
      }
      uVar10 = uVar9 - uVar5;
      if (uVar1 <= uVar9 - uVar5) {
        uVar10 = uVar1;
      }
    }
    puVar2 = (void *)*param_2;
    if (-1 < (char)bVar4) {
      puVar2 = param_2;
    }
    iVar7 = _memcmp((void *)((long)param_1 + uVar5),puVar2,uVar10);
    bVar6 = iVar7 == 0 && uVar10 == uVar1;
  }
  return bVar6;
}


