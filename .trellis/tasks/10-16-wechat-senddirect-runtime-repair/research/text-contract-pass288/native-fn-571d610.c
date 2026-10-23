// Ghidra inferred pseudocode; requested=0x571d610
// entry=0571d610 end=0571d73f

ulong * FUN_0571d610(ulong *param_1,char *param_2)

{
  undefined *puVar1;
  size_t sVar2;
  ulong *puVar3;
  undefined8 *puVar4;
  ulong *puVar5;
  ulong uVar6;
  undefined1 *local_28;
  
  puVar3 = (ulong *)*param_1;
  if (puVar3 == (ulong *)0x0) {
    return (ulong *)0x0;
  }
  if (0xfffffffd < ((uint)*puVar3 & 0xf) - 3) {
    puVar4 = *(undefined8 **)((long)puVar3 - (*puVar3 >> 8));
    local_28 = &SUB_aaaaaaaaaaaaaaaa;
    puVar1 = (undefined *)(puVar4[1] + 0x40);
    if (&DAT_00007fd8 < puVar1) {
      puVar3 = (ulong *)FUN_057220f8(puVar4,0x40,&local_28);
    }
    else {
      local_28 = (undefined1 *)*puVar4;
      puVar3 = (ulong *)(local_28 + puVar4[1] + 0x28);
      puVar4[1] = puVar1;
    }
    if (puVar3 != (ulong *)0x0) {
      puVar3[2] = 0;
      puVar3[1] = 0;
      puVar3[4] = 0;
      puVar3[3] = 0;
      puVar3[6] = 0;
      puVar3[5] = 0;
      puVar3[7] = 0;
      *puVar3 = ((long)puVar3 - (long)local_28) * 0x100 | 2;
      uVar6 = *param_1;
      puVar3[3] = uVar6;
      if (*(long *)(uVar6 + 0x20) == 0) {
        *(ulong **)(uVar6 + 0x20) = puVar3;
        puVar5 = puVar3 + 5;
      }
      else {
        puVar5 = (ulong *)(*(long *)(uVar6 + 0x20) + 0x28);
        uVar6 = *puVar5;
        *(ulong **)(uVar6 + 0x30) = puVar3;
        puVar3[5] = uVar6;
      }
      *puVar5 = (ulong)puVar3;
      sVar2 = _strlen(param_2);
      FUN_0571cb24(puVar3 + 1,puVar3,0x20,param_2,sVar2);
      return puVar3;
    }
  }
  return (ulong *)0x0;
}


