// Ghidra inferred pseudocode; requested=0x2b2110
// entry=002b2110 end=002b2263

uint * FUN_002b2110(undefined8 *param_1,undefined8 param_2)

{
  long lVar1;
  uint *puVar2;
  int iVar3;
  uint uVar4;
  ulong uVar5;
  uint *puVar6;
  uint *puVar7;
  undefined8 local_50;
  undefined4 local_48;
  
  puVar6 = (uint *)*param_1;
  if (1 < *puVar6) {
    FUN_002b2284(param_1);
    puVar6 = (uint *)*param_1;
  }
  puVar6 = *(uint **)(puVar6 + 4);
  if (puVar6 != (uint *)0x0) {
    puVar7 = (uint *)0x0;
    do {
      iVar3 = FUN_06ef30ec(puVar6 + 6,param_2);
      lVar1 = 0x10;
      if (iVar3 == 0) {
        lVar1 = 8;
        puVar7 = puVar6;
      }
      puVar6 = *(uint **)((long)puVar6 + lVar1);
    } while (puVar6 != (uint *)0x0);
    if ((puVar7 != (uint *)0x0) && (iVar3 = FUN_06ef30ec(param_2,puVar7 + 6), iVar3 == 0))
    goto LAB_002b2248;
  }
  local_48 = 0x80000000;
  local_50 = 0;
  puVar6 = (uint *)*param_1;
  if (1 < *puVar6) {
    FUN_002b2284(param_1);
    puVar6 = (uint *)*param_1;
  }
  if (*(uint **)(puVar6 + 4) == (uint *)0x0) {
    puVar6 = puVar6 + 2;
    uVar4 = 1;
LAB_002b2224:
    puVar7 = (uint *)FUN_002a3414(*param_1,param_2,&local_50,puVar6,uVar4);
  }
  else {
    puVar7 = (uint *)0x0;
    puVar2 = *(uint **)(puVar6 + 4);
    do {
      puVar6 = puVar2;
      uVar4 = FUN_06ef30ec(puVar6 + 6,param_2);
      if (uVar4 == 0) {
        puVar7 = puVar6;
      }
      lVar1 = 0x10;
      if (uVar4 == 0) {
        lVar1 = 8;
      }
      puVar2 = *(uint **)((long)puVar6 + lVar1);
    } while (*(uint **)((long)puVar6 + lVar1) != (uint *)0x0);
    uVar4 = uVar4 ^ 1;
    if ((puVar7 == (uint *)0x0) || (uVar5 = FUN_06ef30ec(param_2,puVar7 + 6), (uVar5 & 1) != 0))
    goto LAB_002b2224;
    FUN_06fe18f4(puVar7 + 8,&local_50);
  }
  FUN_06fe0f68(&local_50);
LAB_002b2248:
  return puVar7 + 8;
}


