// Ghidra inferred pseudocode; requested=0x20ba10
// entry=0020ba10 end=0020baf7

void FUN_0020ba10(undefined8 *param_1)

{
  ulong uVar1;
  uint uVar2;
  int *piVar3;
  int iVar4;
  undefined8 *puVar5;
  ulong uVar6;
  ulong uVar7;
  int *local_48;
  
  FUN_06ef7df4(&local_48);
  piVar3 = local_48;
  uVar2 = local_48[1];
  uVar6 = (ulong)(int)uVar2;
  uVar7 = *(ulong *)(local_48 + 4);
  if (uVar2 != 0 && uVar7 < 0x18) {
    FUN_070d3ee0();
LAB_0020baf0:
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if ((int)uVar2 < 0) goto LAB_0020baf0;
  if (uVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)uVar2;
    puVar5 = param_1;
    if (uVar2 == 0) goto LAB_0020ba9c;
  }
  else {
    uVar1 = 0x19;
    if ((uVar6 | 7) != 0x17) {
      uVar1 = (uVar6 | 7) + 1;
    }
    puVar5 = (undefined8 *)__Znwm(uVar1);
    param_1[1] = uVar6;
    param_1[2] = uVar1 | 0x8000000000000000;
    *param_1 = puVar5;
  }
  _memmove(puVar5,(void *)(uVar7 + (long)piVar3),uVar6);
  param_1 = puVar5;
LAB_0020ba9c:
  *(undefined1 *)((long)param_1 + uVar6) = 0;
  if (*local_48 != -1) {
    if (*local_48 != 0) {
      LOAcquire();
      iVar4 = *local_48;
      *local_48 = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) {
        return;
      }
    }
    FUN_06ea14cc(local_48,1,8);
  }
  return;
}


