// Ghidra inferred pseudocode; requested=0x27d4348
// entry=027d4348 end=027d4407

/* WARNING: Removing unreachable block (ram,0x027d43c4) */
/* WARNING: Removing unreachable block (ram,0x027d43a8) */
/* WARNING: Removing unreachable block (ram,0x027d43dc) */

void FUN_027d4348(long param_1)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  
  FUN_0668272c(param_1 + 0x48);
  FUN_066823c4(param_1 + 0x48);
  puVar1 = *(undefined8 **)(param_1 + 0x20);
  if (*(undefined8 **)(param_1 + 0x28) != puVar1) {
    puVar3 = *(undefined8 **)(param_1 + 0x28) + -6;
    do {
      if (*(char *)((long)puVar3 + 0x17) < '\0') {
        __ZdlPvm(*puVar3,puVar3[2] & 0x7fffffffffffffff);
      }
      puVar2 = puVar3 + -7;
      puVar3 = puVar3 + -0xd;
    } while (puVar2 != puVar1);
  }
  *(undefined8 **)(param_1 + 0x28) = puVar1;
  FUN_015e49ec(param_1 + 0x38);
  return;
}


