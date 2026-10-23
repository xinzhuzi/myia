// Ghidra inferred pseudocode; requested=0x4f37b88
// entry=04f37b88 end=04f37c93

undefined8 FUN_04f37b88(long param_1,long param_2)

{
  char *pcVar1;
  char cVar2;
  uint uVar3;
  ulong uVar4;
  undefined8 uVar5;
  undefined8 *puVar6;
  
  do {
    while (pcVar1 = *(char **)(param_2 + 8), pcVar1 < *(char **)(param_2 + 0x10)) {
      cVar2 = *pcVar1;
      uVar3 = (uint)cVar2;
      if (cVar2 < 0) break;
      *(int *)(param_2 + 0x20) = (int)cVar2;
      *(char **)(param_2 + 8) = pcVar1 + 1;
      if (cVar2 != '\n') goto LAB_04f37bd0;
LAB_04f37c08:
      *(uint *)(param_1 + 0x14) = *(uint *)(param_1 + 0x14) | 1;
      puVar6 = *(undefined8 **)(param_1 + 8);
      if (puVar6 == &DAT_0a524ad0) {
        puVar6 = (undefined8 *)__Znwm(0x18);
        puVar6[1] = 0;
        puVar6[2] = 0;
        *puVar6 = 0;
        *(undefined8 **)(param_1 + 8) = puVar6;
      }
      uVar5 = FUN_05ab514c(param_2,puVar6);
      if ((int)uVar5 == 0) {
        return uVar5;
      }
      if ((*(long *)(param_2 + 8) == *(long *)(param_2 + 0x10)) &&
         ((*(int *)(param_2 + 0x2c) != 0 || (*(int *)(param_2 + 0x18) == *(int *)(param_2 + 0x28))))
         ) {
        *(undefined4 *)(param_2 + 0x20) = 0;
        *(undefined1 *)(param_2 + 0x24) = 1;
        return 1;
      }
    }
    uVar3 = FUN_05ab303c(param_2);
    *(uint *)(param_2 + 0x20) = uVar3;
    if (uVar3 == 10) goto LAB_04f37c08;
LAB_04f37bd0:
    if ((uVar3 == 0) || ((uVar3 & 7) == 4)) {
      return 1;
    }
    uVar4 = FUN_05ab4aac(param_2);
    if ((uVar4 & 1) == 0) {
      return 0;
    }
  } while( true );
}


