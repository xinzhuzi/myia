// Ghidra inferred pseudocode; requested=0x286fbac
// entry=0286fbac end=0286fe9b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0286fbac(undefined8 param_1,long param_2,undefined8 param_3,long *param_4)

{
  ulong uVar1;
  undefined1 uVar2;
  undefined1 *puVar3;
  size_t sVar4;
  undefined8 uVar5;
  long lVar6;
  undefined8 *******pppppppuVar7;
  code *pcVar8;
  long local_c8;
  undefined8 *******local_c0;
  size_t local_b8;
  undefined8 local_b0;
  ulong local_a8 [2];
  undefined7 local_98;
  char cStack_91;
  undefined1 local_90 [8];
  undefined1 *local_88;
  undefined1 *local_80;
  undefined1 *local_78;
  long local_70;
  long alStack_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_003b276c(&local_80,0,0,0,1);
  uVar1 = *(ulong *)(param_2 + 8);
  if (-1 < (char)*(byte *)(param_2 + 0x17)) {
    uVar1 = (ulong)*(byte *)(param_2 + 0x17);
  }
  if (uVar1 != 0) {
    local_50 = (long *)0x0;
    FUN_0074916c(local_90,param_2,alStack_68,0,0);
    puVar3 = local_78;
    uVar2 = (char)local_80;
    local_80 = (undefined1 *)CONCAT71(local_80._1_7_,local_90[0]);
    local_90[0] = uVar2;
    local_78 = local_88;
    local_88 = puVar3;
    FUN_001fa1c8(&local_88);
    if (local_50 == alStack_68) {
      pcVar8 = *(code **)(*local_50 + 0x20);
LAB_0286fc90:
      (*pcVar8)();
    }
    else if (local_50 != (long *)0x0) {
      pcVar8 = *(code **)(*local_50 + 0x28);
      goto LAB_0286fc90;
    }
    if ((char)local_80 == '\t') {
      cStack_91 = '\0';
      local_a8[0] = local_a8[0] & 0xffffffffffffff00;
      if ((DAT_0a39e30b & 1) == 0) {
        _DAT_0a39e2f4 = CONCAT44((int)DAT_084cae70,(int)ram0x086dc648);
        uRam000000000a39e2fc = CONCAT44((int)DAT_08483220,(int)DAT_084df3f0);
        DAT_0a39e304 = (undefined4)DAT_088051c8;
        DAT_0a39e308 = 0x4e4f;
        DAT_0a39e30a = 0;
        DAT_0a39e30b = 1;
      }
      sVar4 = _strlen(&DAT_0a39e2f4);
      if (0x7ffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_c0);
      }
      if (sVar4 < 0x17) {
        local_b0 = CONCAT17((char)sVar4,(undefined7)local_b0);
        pppppppuVar7 = &local_c0;
        if (sVar4 != 0) goto LAB_0286fddc;
      }
      else {
        uVar1 = 0x19;
        if ((sVar4 | 7) != 0x17) {
          uVar1 = (sVar4 | 7) + 1;
        }
        pppppppuVar7 = (undefined8 *******)__Znwm(uVar1);
        local_b0 = uVar1 | 0x8000000000000000;
        local_c0 = pppppppuVar7;
        local_b8 = sVar4;
LAB_0286fddc:
        _memcpy(pppppppuVar7,&DAT_0a39e2f4,sVar4);
      }
      *(undefined1 *)((long)pppppppuVar7 + sVar4) = 0;
      local_70 = *param_4;
      *param_4 = 0;
      (**(code **)(local_70 + 8))(local_70,local_a8,&local_c0);
      FUN_00033d2c(&local_70);
      if ((long)local_b0 < 0) {
        __ZdlPvm(local_c0,local_b0 & 0x7fffffffffffffff);
      }
      if (cStack_91 < '\0') {
        __ZdlPvm(local_a8[0],CONCAT17(cStack_91,local_98) & 0x7fffffffffffffff);
      }
      goto LAB_0286fe54;
    }
  }
  uVar5 = __Znwm(1);
  lVar6 = __Znwm(0x38);
  FUN_00033c40(lVar6,FUN_028701cc,FUN_02870250);
  *(code **)(lVar6 + 0x20) = FUN_028700a0;
  *(undefined8 *)(lVar6 + 0x28) = uVar5;
  *(long *)(lVar6 + 0x30) = *param_4;
  *param_4 = 0;
  local_a8[0] = 0;
  local_c8 = lVar6;
  FUN_0291d53c(uVar5,&local_80,param_3,&local_c8);
  FUN_00033d2c(&local_c8);
  FUN_00033d2c(local_a8);
LAB_0286fe54:
  FUN_001fa1c8(&local_78,(ulong)local_80 & 0xff);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


