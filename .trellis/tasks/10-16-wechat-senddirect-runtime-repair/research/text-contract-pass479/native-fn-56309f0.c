// Ghidra inferred pseudocode; requested=0x56309f0
// entry=056309f0 end=05630abb

void FUN_056309f0(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  char *pcVar2;
  undefined8 uVar3;
  size_t sVar4;
  long lVar5;
  char *pcVar6;
  
  lVar5 = param_2[2];
  if (lVar5 != 0) {
    uVar1 = *param_2;
    uVar3 = param_2[1];
    param_2[1] = 0;
    param_2[2] = 0;
    *param_2 = "";
    *param_1 = uVar1;
    param_1[1] = uVar3;
    param_1[2] = lVar5;
    return;
  }
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = "";
  pcVar2 = (char *)*param_2;
  sVar4 = param_2[1];
  if (pcVar2 != (char *)0x0 && sVar4 == 0) {
    sVar4 = _strlen(pcVar2);
  }
  FUN_056305e0(param_1,sVar4);
  pcVar6 = "";
  if (((pcVar2 != (char *)0x0) && (pcVar6 = "", sVar4 != 0)) && (param_1[2] != 0)) {
    pcVar6 = (char *)(param_1[2] + 4);
    _memcpy(pcVar6,pcVar2,sVar4);
    pcVar6[sVar4] = '\0';
  }
  *param_1 = pcVar6;
  return;
}


