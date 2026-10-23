// Ghidra inferred pseudocode; requested=0x4663a3c
// entry=04663a3c end=04663b33

void FUN_04663a3c(long *param_1,long *param_2)

{
  int iVar1;
  long lVar2;
  undefined8 *puVar3;
  int iVar4;
  undefined8 uVar5;
  long lVar6;
  
  FUN_05ab4038(param_1,(int)param_2[1] + (int)param_1[1]);
  if (0 < (int)param_2[1]) {
    lVar6 = 0;
    do {
      uVar5 = *(undefined8 *)(*param_2 + lVar6 * 8);
      iVar1 = (int)param_1[1];
      iVar4 = *(int *)((long)param_1 + 0xc);
      if (iVar1 < iVar4) {
        *(int *)(param_1 + 1) = iVar1 + 1;
        puVar3 = *(undefined8 **)(*param_1 + (long)iVar1 * 8);
      }
      else {
        if (iVar4 == (int)param_1[2]) {
          FUN_05ab4038(param_1,iVar4 + 1);
          iVar4 = *(int *)((long)param_1 + 0xc);
        }
        *(int *)((long)param_1 + 0xc) = iVar4 + 1;
        puVar3 = (undefined8 *)__Znwm(0x38);
        *puVar3 = &PTR_FUN_09e91d80;
        puVar3[1] = 0;
        puVar3[2] = &DAT_0a524ad0;
        puVar3[3] = 0;
        puVar3[4] = &DAT_0a524ad0;
        puVar3[5] = 0;
        puVar3[6] = 0;
        lVar2 = param_1[1];
        *(int *)(param_1 + 1) = (int)lVar2 + 1;
        *(undefined8 **)(*param_1 + (long)(int)lVar2 * 8) = puVar3;
      }
      FUN_0465c668(puVar3,uVar5);
      lVar6 = lVar6 + 1;
    } while (lVar6 < (int)param_2[1]);
  }
  return;
}


