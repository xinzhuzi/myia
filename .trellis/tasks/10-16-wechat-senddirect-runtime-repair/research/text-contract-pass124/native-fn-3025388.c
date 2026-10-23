// Ghidra inferred pseudocode; requested=0x3025388
// entry=03025388 end=030255bf

void FUN_03025388(void *param_1,undefined8 param_2,long param_3)

{
  byte bVar1;
  int iVar2;
  long *plVar3;
  int iVar4;
  long lVar5;
  undefined8 local_b8 [12];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  _memcpy(param_1,&DAT_088a1320,0x278);
  FUN_00ac6038(param_1);
  lVar5 = *(long *)(param_3 + 0x10);
  if (lVar5 != param_3 + 8) {
    iVar4 = 0;
    do {
      plVar3 = (long *)FUN_056fad30(lVar5 + 0x10);
      iVar2 = FUN_056f4fec(param_2,iVar4);
      bVar1 = (**(code **)(*plVar3 + 0x10))(plVar3);
      if (bVar1 < 3) {
        if (bVar1 == 1) {
          if (iVar2 == 0) {
            (**(code **)(*plVar3 + 0x20))(plVar3,param_1);
          }
          else {
            local_b8[0] = FUN_056f5028(param_2,iVar4);
            (**(code **)(*plVar3 + 0x28))(plVar3,param_1,local_b8);
          }
        }
        else if (bVar1 == 2) {
          if (iVar2 == 0) {
            (**(code **)(*plVar3 + 0x20))(plVar3,param_1);
          }
          else {
            local_b8[0] = FUN_056f5064(param_2,iVar4);
            (**(code **)(*plVar3 + 0x28))(plVar3,param_1,local_b8);
          }
        }
      }
      else if (bVar1 == 3) {
        if (iVar2 == 0) {
          (**(code **)(*plVar3 + 0x20))(plVar3,param_1);
        }
        else {
          FUN_056f50a4(local_b8,param_2,iVar4);
          (**(code **)(*plVar3 + 0x28))(plVar3,param_1,local_b8);
          FUN_0562fd84(local_b8);
        }
      }
      else if (bVar1 == 4) {
        if (iVar2 == 0) {
          (**(code **)(*plVar3 + 0x20))(plVar3,param_1);
        }
        else {
          FUN_056f50ec(local_b8,param_2,iVar4);
          (**(code **)(*plVar3 + 0x28))(plVar3,param_1,local_b8);
          FUN_0563255c(local_b8);
        }
      }
      iVar4 = iVar4 + 1;
      lVar5 = *(long *)(lVar5 + 8);
    } while (lVar5 != param_3 + 8);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


