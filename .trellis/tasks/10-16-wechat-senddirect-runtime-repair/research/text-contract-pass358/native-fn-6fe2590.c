// Ghidra inferred pseudocode; requested=0x6fe2590
// entry=06fe2590 end=06fe266f

void FUN_06fe2590(undefined8 *param_1,undefined8 *param_2)

{
  long lVar1;
  long lVar2;
  uint uVar3;
  undefined8 *puVar4;
  ulong uVar5;
  uint uVar6;
  int *piVar7;
  
  uVar3 = *(uint *)(param_2 + 1);
  uVar6 = uVar3 & 0x3fffffff;
  if (uVar6 == 10) {
    piVar7 = (int *)*param_2;
    *param_1 = piVar7;
    if (*piVar7 - 1U < 0xfffffffe) {
      LOAcquire();
      *piVar7 = *piVar7 + 1;
      LORelease();
      return;
    }
  }
  else {
    *param_1 = &DAT_0a2320b0;
    if ((uVar3 & 0x3ffffc00) != 0) {
      puVar4 = param_2;
      if ((uVar3 >> 0x1e & 1) != 0) {
        puVar4 = *(undefined8 **)*param_2;
      }
      uVar5 = FUN_06fc976c(puVar4,uVar6,param_1,10);
      if ((uVar5 & 1) != 0) {
        return;
      }
      uVar6 = *(uint *)(param_2 + 1) & 0x3fffffff;
    }
    lVar1 = 2;
    if (uVar6 != 0x79) {
      lVar1 = 3;
    }
    lVar2 = 1;
    if (0x17 < uVar6 - 0x40) {
      lVar2 = lVar1;
    }
    lVar1 = 0;
    if (0x37 < uVar6) {
      lVar1 = lVar2;
    }
    (**(code **)((&PTR_PTR_0a24b0a8)[lVar1] + 0x30))(param_2,10,param_1,0);
  }
  return;
}


