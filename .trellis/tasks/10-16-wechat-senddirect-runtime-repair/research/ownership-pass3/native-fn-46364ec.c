// Ghidra inferred pseudocode; requested=0x46364ec
// entry=046364ec end=046367eb

/* WARNING: Removing unreachable block (ram,0x046366d0) */
/* WARNING: Removing unreachable block (ram,0x04636620) */
/* WARNING: Removing unreachable block (ram,0x046365c8) */
/* WARNING: Removing unreachable block (ram,0x04636678) */
/* WARNING: Removing unreachable block (ram,0x04636728) */
/* WARNING: Type propagation algorithm not settling */

long FUN_046364ec(long param_1)

{
  char cVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  
  FUN_05ded188(param_1 + 0x1f0);
  FUN_05ded188(param_1 + 0x1c8);
  if (*(char *)(param_1 + 0x1bf) < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x1a8),*(ulong *)(param_1 + 0x1b8) & 0x7fffffffffffffff);
  }
  FUN_000240bc(param_1 + 400,*(undefined8 *)(param_1 + 0x198));
  if (*(char *)(param_1 + 0x17f) < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x168),*(ulong *)(param_1 + 0x178) & 0x7fffffffffffffff);
    cVar1 = *(char *)(param_1 + 0x167);
  }
  else {
    cVar1 = *(char *)(param_1 + 0x167);
  }
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x150),*(ulong *)(param_1 + 0x160) & 0x7fffffffffffffff);
    lVar3 = *(long *)(param_1 + 0x130);
  }
  else {
    lVar3 = *(long *)(param_1 + 0x130);
  }
  if (lVar3 == 0) {
    lVar3 = *(long *)(param_1 + 0x118);
  }
  else {
    lVar4 = *(long *)(param_1 + 0x138);
    lVar2 = lVar3;
    if (lVar4 != lVar3) {
      do {
        lVar4 = lVar4 + -0x18;
      } while (lVar4 != lVar3);
      lVar2 = *(long *)(param_1 + 0x130);
    }
    *(long *)(param_1 + 0x138) = lVar3;
    __ZdlPvm(lVar2,*(long *)(param_1 + 0x140) - lVar2);
    lVar3 = *(long *)(param_1 + 0x118);
  }
  if (lVar3 == 0) {
    lVar3 = *(long *)(param_1 + 0x100);
  }
  else {
    lVar4 = *(long *)(param_1 + 0x120);
    lVar2 = lVar3;
    if (lVar4 != lVar3) {
      do {
        lVar4 = lVar4 + -0x18;
      } while (lVar4 != lVar3);
      lVar2 = *(long *)(param_1 + 0x118);
    }
    *(long *)(param_1 + 0x120) = lVar3;
    __ZdlPvm(lVar2,*(long *)(param_1 + 0x128) - lVar2);
    lVar3 = *(long *)(param_1 + 0x100);
  }
  if (lVar3 == 0) {
    lVar3 = *(long *)(param_1 + 0xe8);
  }
  else {
    lVar4 = *(long *)(param_1 + 0x108);
    lVar2 = lVar3;
    if (lVar4 != lVar3) {
      do {
        lVar4 = lVar4 + -0x18;
      } while (lVar4 != lVar3);
      lVar2 = *(long *)(param_1 + 0x100);
    }
    *(long *)(param_1 + 0x108) = lVar3;
    __ZdlPvm(lVar2,*(long *)(param_1 + 0x110) - lVar2);
    lVar3 = *(long *)(param_1 + 0xe8);
  }
  if (lVar3 == 0) {
    lVar3 = *(long *)(param_1 + 0xd0);
  }
  else {
    lVar4 = *(long *)(param_1 + 0xf0);
    lVar2 = lVar3;
    if (lVar4 != lVar3) {
      do {
        lVar4 = lVar4 + -0x18;
      } while (lVar4 != lVar3);
      lVar2 = *(long *)(param_1 + 0xe8);
    }
    *(long *)(param_1 + 0xf0) = lVar3;
    __ZdlPvm(lVar2,*(long *)(param_1 + 0xf8) - lVar2);
    lVar3 = *(long *)(param_1 + 0xd0);
  }
  if (lVar3 != 0) {
    lVar4 = *(long *)(param_1 + 0xd8);
    lVar2 = lVar3;
    if (lVar4 != lVar3) {
      do {
        lVar4 = lVar4 + -0x18;
      } while (lVar4 != lVar3);
      lVar2 = *(long *)(param_1 + 0xd0);
    }
    *(long *)(param_1 + 0xd8) = lVar3;
    __ZdlPvm(lVar2,*(long *)(param_1 + 0xe0) - lVar2);
  }
  FUN_000240bc(param_1 + 0xb8,*(undefined8 *)(param_1 + 0xc0));
  if (*(char *)(param_1 + 0xaf) < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x98),*(ulong *)(param_1 + 0xa8) & 0x7fffffffffffffff);
    cVar1 = *(char *)(param_1 + 0x97);
  }
  else {
    cVar1 = *(char *)(param_1 + 0x97);
  }
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x80),*(ulong *)(param_1 + 0x90) & 0x7fffffffffffffff);
    cVar1 = *(char *)(param_1 + 0x7f);
  }
  else {
    cVar1 = *(char *)(param_1 + 0x7f);
  }
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x68),*(ulong *)(param_1 + 0x78) & 0x7fffffffffffffff);
    cVar1 = *(char *)(param_1 + 0x2f);
  }
  else {
    cVar1 = *(char *)(param_1 + 0x2f);
  }
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x18),*(ulong *)(param_1 + 0x28) & 0x7fffffffffffffff);
  }
  return param_1;
}


