// Ghidra inferred pseudocode; requested=0x667db24
// entry=0667db24 end=0667dbd7

void FUN_0667db24(long param_1)

{
  long *plVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  long lVar5;
  
  lVar4 = *(long *)(param_1 + 8);
  if (*(int *)(lVar4 + 0x288) != 3) {
    lVar5 = *(long *)(param_1 + 0x18);
    plVar1 = (long *)__Znwm(0x20);
    plVar1[1] = lVar5;
    *plVar1 = (long)&PTR_FUN_09df9538;
    plVar1[2] = (long)PTR___ZTIx_09b36ac8;
    plVar1[3] = (long)(plVar1 + 1);
    plVar3 = *(long **)(lVar4 + 0x398);
    if (plVar3 != (long *)0x0) {
      plVar2 = (long *)*plVar3;
      *plVar3 = (long)plVar1;
      if (plVar2 != (long *)0x0) {
        (**(code **)(*plVar2 + 8))();
      }
      plVar1 = (long *)0x0;
      *(undefined8 *)(lVar4 + 0x398) = 0;
    }
    *(undefined8 *)(lVar4 + 0x390) = 0;
    FUN_06677e1c(lVar4);
    if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x0667dbc4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*plVar1 + 8))(plVar1);
      return;
    }
  }
  return;
}


