// Ghidra inferred pseudocode; requested=0x2e86b60
// entry=02e86b60 end=02e86cf7

long FUN_02e86b60(long *param_1,undefined8 param_2)

{
  ulong uVar1;
  undefined8 *puVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  long lVar6;
  ulong uVar7;
  undefined8 *puVar8;
  long lVar9;
  
  lVar6 = param_1[1] - *param_1 >> 3;
  uVar1 = lVar6 * -0x6474a8819ec8e951 + 1;
  if (uVar1 < 0x67b23a5440cf65) {
    lVar5 = param_1[2] - *param_1 >> 3;
    uVar7 = lVar5 * 0x3716aefcc26e2d5e;
    if (uVar7 < uVar1 || uVar7 - uVar1 == 0) {
      uVar7 = uVar1;
    }
    if (0x33d91d2a2067b1 < (ulong)(lVar5 * -0x6474a8819ec8e951)) {
      uVar7 = 0x67b23a5440cf64;
    }
    if (uVar7 == 0) {
      lVar5 = 0;
    }
    else {
      if (0x67b23a5440cf64 < uVar7) goto LAB_02e86cf4;
      lVar5 = __Znwm(uVar7 * 0x278);
    }
    lVar4 = lVar5 + lVar6 * 8;
    FUN_00f57630(lVar4,param_2);
    lVar9 = 0;
    lVar6 = *param_1;
    lVar3 = param_1[1];
    while (lVar3 + lVar9 != lVar6) {
      lVar9 = lVar9 + -0x278;
      FUN_00f57630(lVar9 + lVar4,lVar9 + lVar3);
    }
    puVar2 = (undefined8 *)*param_1;
    puVar8 = (undefined8 *)param_1[1];
    *param_1 = lVar4 + lVar9;
    lVar6 = param_1[2];
    param_1[2] = lVar5 + uVar7 * 0x278;
    param_1[1] = lVar4 + 0x278;
    while (puVar8 != puVar2) {
      puVar8 = puVar8 + -0x4f;
      (**(code **)*puVar8)(puVar8);
    }
    if (puVar2 != (undefined8 *)0x0) {
      __ZdlPvm(puVar2,lVar6 - (long)puVar2);
    }
    return lVar4 + 0x278;
  }
  FUN_02e83288(param_1);
LAB_02e86cf4:
                    /* WARNING: Subroutine does not return */
  FUN_001e96c0();
}


