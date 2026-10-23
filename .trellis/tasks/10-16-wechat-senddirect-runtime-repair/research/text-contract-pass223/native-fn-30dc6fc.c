// Ghidra inferred pseudocode; requested=0x30dc6fc
// entry=030dc6fc end=030dc797

long FUN_030dc6fc(undefined8 *param_1)

{
  int iVar1;
  long *plVar2;
  undefined *puVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  
  plVar2 = (long *)FUN_0666a844(*param_1);
  if (plVar2 != (long *)0x0) {
    puVar3 = PTR___ZTIv_09b36ac0;
    if ((long *)*plVar2 != (long *)0x0) {
      puVar3 = (undefined *)(**(code **)(*(long *)*plVar2 + 0x18))();
    }
    iVar1 = _strcmp((char *)(*(ulong *)(puVar3 + 8) & 0x7fffffffffffffff),"_f6e3c5f5");
    if ((iVar1 == 0) && (*plVar2 + 8 != 0)) {
      return *plVar2 + 8;
    }
  }
  puVar4 = (undefined8 *)___cxa_allocate_exception(8);
  *puVar4 = 0;
  uVar5 = FUN_02190098();
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar5,&PTR_DAT_09fb3090,__ZNSt8bad_castD2Ev);
}


