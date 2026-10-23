// Ghidra inferred pseudocode; requested=0x666a844
// entry=0666a844 end=0666a9f7

long FUN_0666a844(long param_1)

{
  code *pcVar1;
  int iVar2;
  undefined *puVar3;
  undefined8 uVar4;
  undefined8 *puVar5;
  long lVar6;
  ulong uVar7;
  undefined1 *puVar8;
  long *plVar9;
  undefined1 auStack_48 [8];
  undefined1 *local_40;
  undefined1 *local_38;
  
  puVar8 = (undefined1 *)(param_1 + 0x10);
  local_38 = &DAT_aaaaaaaaaaaaaa01;
  local_40 = puVar8;
  __ZNSt3__115recursive_mutex4lockEv(puVar8);
  if (*(int *)(param_1 + 0x9c) == 0) {
    do {
      FUN_0666bd74(param_1 + 0x50,&local_40);
      iVar2 = *(int *)(param_1 + 0x9c);
    } while (iVar2 == 0);
    puVar8 = local_40;
    if (((ulong)local_38 & 1) == 0) goto LAB_0666a8a8;
  }
  __ZNSt3__115recursive_mutex6unlockEv(puVar8);
  iVar2 = *(int *)(param_1 + 0x9c);
LAB_0666a8a8:
  if (iVar2 == 2) {
    plVar9 = (long *)(param_1 + 0x90);
    puVar3 = PTR___ZTIv_09b36ac0;
    if ((long *)*plVar9 != (long *)0x0) {
      puVar3 = (undefined *)(**(code **)(*(long *)*plVar9 + 0x18))();
    }
    uVar7 = *(ulong *)(puVar3 + 8);
    if ((uVar7 == 0x8000000009683a60) ||
       (((long)uVar7 < 0 &&
        (iVar2 = _strcmp((char *)(uVar7 & 0x7fffffffffffffff),"_8608202b"), iVar2 == 0)))) {
      local_40 = &SUB_aaaaaaaaaaaaaaaa;
      uVar4 = FUN_04a56044(plVar9);
      __ZNSt13exception_ptrC1ERKS_(&local_40,uVar4);
      __ZNSt13exception_ptrC1ERKS_(auStack_48,&local_40);
      __ZSt17rethrow_exceptionSt13exception_ptr(auStack_48);
                    /* WARNING: Does not return */
      pcVar1 = (code *)SoftwareBreakpoint(1,0x666a9b8);
      (*pcVar1)();
    }
    puVar3 = PTR___ZTIv_09b36ac0;
    if ((long *)*plVar9 != (long *)0x0) {
      puVar3 = (undefined *)(**(code **)(*(long *)*plVar9 + 0x18))();
    }
    uVar7 = *(ulong *)(puVar3 + 8);
    if ((uVar7 == 0x8000000009683a6a) ||
       (((long)uVar7 < 0 &&
        (iVar2 = _strcmp((char *)(uVar7 & 0x7fffffffffffffff),"_e2635e7e"), iVar2 == 0)))) {
      puVar5 = (undefined8 *)___cxa_allocate_exception(0x10);
      lVar6 = FUN_0666aa48(plVar9);
      *puVar5 = &PTR___ZNSt9exceptionD2Ev_09fb1c48;
      puVar5[1] = *(undefined8 *)(lVar6 + 8);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(puVar5,&PTR_DAT_09fb1c88,__ZNSt9exceptionD2Ev);
    }
  }
  return param_1 + 0x90;
}


