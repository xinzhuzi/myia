// Ghidra inferred pseudocode; requested=0x669440c
// entry=0669440c end=066944ab

void FUN_0669440c(void)

{
  undefined4 *puVar1;
  
  puVar1 = (undefined4 *)__Znwm(0xe8);
  *puVar1 = 0;
  *(undefined8 *)(puVar1 + 4) = 0;
  *(undefined8 *)(puVar1 + 2) = 0;
  *(undefined8 *)(puVar1 + 0xc) = 0x32aaaba7;
  *(undefined2 *)(puVar1 + 1) = 0;
  *(undefined8 *)(puVar1 + 8) = 0;
  *(undefined8 *)(puVar1 + 6) = 0;
  *(undefined8 *)(puVar1 + 10) = 0;
  *(undefined8 *)(puVar1 + 0x10) = 0;
  *(undefined8 *)(puVar1 + 0xe) = 0;
  *(undefined8 *)(puVar1 + 0x14) = 0;
  *(undefined8 *)(puVar1 + 0x12) = 0;
  *(undefined8 *)(puVar1 + 0x18) = 0;
  *(undefined8 *)(puVar1 + 0x16) = 0;
  *(undefined8 *)(puVar1 + 0x1c) = 0;
  *(undefined8 *)(puVar1 + 0x1a) = 0;
  *(undefined8 *)(puVar1 + 0x20) = 0;
  *(undefined8 *)(puVar1 + 0x1e) = 0;
  *(undefined4 **)(puVar1 + 0x22) = puVar1 + 0x22;
  *(undefined4 **)(puVar1 + 0x24) = puVar1 + 0x22;
  *(undefined8 *)(puVar1 + 0x26) = 0;
  __ZNSt3__115recursive_mutexC1Ev(puVar1 + 0x28);
  *(undefined8 *)(puVar1 + 0x38) = 0;
  *(undefined8 *)(puVar1 + 6) = 300000;
  DAT_0a518cb0 = puVar1;
  return;
}


