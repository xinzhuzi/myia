// Ghidra inferred pseudocode; requested=0x453f8ec
// entry=0453f8ec end=0453f96f

void FUN_0453f8ec(void)

{
  long lVar1;
  
  lVar1 = *(long *)PTR____stack_chk_guard_09b36c98;
  DAT_0a51e978 = FUN_0001bdfc();
  _memset(&stack0xffffffffffdfffd8,0xaa,0x200000);
  FUN_066736b0(&stack0xffffffffffdfffd8,0x200000);
  FUN_06666ec4();
  FUN_06666628();
  if (*(long *)PTR____stack_chk_guard_09b36c98 == lVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


