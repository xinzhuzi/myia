// Ghidra inferred pseudocode; requested=0x284f488
// entry=0284f488 end=0284f5b3

void FUN_0284f488(void)

{
  ulong uVar1;
  int iVar2;
  size_t sVar3;
  undefined8 *puVar4;
  
  if (((DAT_0a01b560 & 1) != 0) || (iVar2 = ___cxa_guard_acquire(&DAT_0a01b560), iVar2 == 0)) {
    return;
  }
  if ((DAT_0a39dce5 & 1) == 0) {
    DAT_0a39dce0 = (undefined4)DAT_084b0240;
    DAT_0a39dce4 = 0;
    DAT_0a39dce5 = 1;
  }
  sVar3 = _strlen((char *)&DAT_0a39dce0);
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&DAT_0a01b548);
  }
  if (sVar3 < 0x17) {
    puVar4 = &DAT_0a01b548;
    DAT_0a01b558 = CONCAT17((char)sVar3,(undefined7)DAT_0a01b558);
    if (sVar3 == 0) goto LAB_0284f570;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    puVar4 = (undefined8 *)__Znwm(uVar1);
    DAT_0a01b558 = uVar1 | 0x8000000000000000;
    DAT_0a01b548 = puVar4;
    DAT_0a01b550 = sVar3;
  }
  _memcpy(puVar4,&DAT_0a39dce0,sVar3);
LAB_0284f570:
  *(undefined1 *)((long)puVar4 + sVar3) = 0;
  ___cxa_atexit(PTR___ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEED1Ev_09b364f8,
                &DAT_0a01b548,0);
  ___cxa_guard_release(&DAT_0a01b560);
  return;
}


