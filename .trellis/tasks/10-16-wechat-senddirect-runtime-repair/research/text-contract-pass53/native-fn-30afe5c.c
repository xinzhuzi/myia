// Ghidra inferred pseudocode; requested=0x30afe5c
// entry=030afe5c end=030b0897

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_030afe5c(undefined8 param_1,long *param_2)

{
  undefined1 uVar1;
  bool bVar2;
  long lVar3;
  long lVar4;
  int iVar5;
  undefined8 *******pppppppuVar6;
  uint uVar7;
  undefined1 *puVar8;
  ulong uVar9;
  undefined1 *puVar10;
  undefined8 uVar11;
  long *plVar12;
  long lVar13;
  long *plVar14;
  undefined8 *******local_1d8;
  long *local_1d0;
  undefined7 local_1c8;
  char cStack_1c1;
  undefined1 auStack_1c0 [144];
  long local_130;
  long *local_128;
  long local_120;
  long *local_118;
  undefined8 *******local_110;
  undefined8 local_108;
  undefined7 local_100;
  char cStack_f9;
  undefined8 *******local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 local_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar13 = *param_2;
  lVar4 = *(long *)(lVar13 + 0x18);
  local_118 = *(long **)(lVar13 + 0x20);
  lVar3 = 0;
  if (local_118 != (long *)0x0) {
    lVar3 = local_118[1];
    local_118[1] = lVar3 + 1;
    lVar13 = *param_2;
  }
  local_120 = lVar4;
  if ((*(long *)(lVar13 + 8) == 0) ||
     (local_130 = ___dynamic_cast(lVar3,*(long *)(lVar13 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09eb2580,0)
     , local_130 == 0)) {
    local_130 = 0;
    local_128 = (long *)0x0;
    if (lVar4 == 0) goto LAB_030b00b8;
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 == 0) goto LAB_030b0224;
    FUN_0488143c(&local_110);
    pppppppuVar6 = local_110;
    if (-1 < cStack_f9) {
      pppppppuVar6 = &local_110;
    }
    if ((DAT_0a3d78e6 & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a3d78cd)[uVar9] = (&DAT_088ab71c)[uVar9] + 0x8a ^ (&DAT_088ab70c)[uVar9 & 0xf];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x19);
      DAT_0a3d78e6 = 1;
    }
    if ((DAT_0a3d83b1 & 1) == 0) {
      uRam000000000a3d83a8 = _UNK_088a7388;
      _DAT_0a3d83a0 = _DAT_088a7380;
      DAT_0a3d83b0 = 0;
      DAT_0a3d83b1 = 1;
    }
    FUN_05e1d050(auStack_1c0,4,pppppppuVar6,&DAT_0a3d78cd,&DAT_0a3d83a0,0x447,0,0);
    if ((DAT_0a3d83db & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a3d83c6)[uVar9] = (&DAT_088ac616)[uVar9] + 0x8a ^ (&DAT_088ac606)[uVar9 & 0xf];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x15);
      DAT_0a3d83db = 1;
    }
    uStack_58 = 0;
    local_60 = 0;
    local_48 = 0;
    uStack_50 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    uStack_70 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    uStack_90 = 0;
    uStack_b8 = 0;
    local_c0 = (undefined8 *******)0x0;
    uStack_a8 = 0;
    uStack_b0 = 0;
    FUN_05e1d31c(auStack_1c0,&DAT_0a3d83c6,&local_c0);
LAB_030b0204:
    thunk_FUN_05e1d0bc(auStack_1c0);
    if (cStack_f9 < '\0') {
      uVar9 = CONCAT17(cStack_f9,local_100);
      pppppppuVar6 = local_110;
LAB_030b021c:
      __ZdlPvm(pppppppuVar6,uVar9 & 0x7fffffffffffffff);
    }
  }
  else {
    plVar14 = *(long **)(lVar13 + 0x10);
    if (plVar14 != (long *)0x0) {
      plVar14[1] = plVar14[1] + 1;
    }
    local_128 = plVar14;
    if (lVar4 == 0) {
LAB_030b00b8:
      iVar5 = thunk_FUN_05e1d97c(4);
      if (iVar5 == 0) goto LAB_030b0224;
      FUN_0488143c(&local_110);
      pppppppuVar6 = local_110;
      if (-1 < cStack_f9) {
        pppppppuVar6 = &local_110;
      }
      if ((DAT_0a3d78e6 & 1) == 0) {
        uVar9 = 0;
        do {
          (&DAT_0a3d78cd)[uVar9] = (&DAT_088ab71c)[uVar9] + 0x8a ^ (&DAT_088ab70c)[uVar9 & 0xf];
          uVar9 = uVar9 + 1;
        } while (uVar9 != 0x19);
        DAT_0a3d78e6 = 1;
      }
      if ((DAT_0a3d83b1 & 1) == 0) {
        uRam000000000a3d83a8 = _UNK_088a7388;
        _DAT_0a3d83a0 = _DAT_088a7380;
        DAT_0a3d83b0 = 0;
        DAT_0a3d83b1 = 1;
      }
      FUN_05e1d050(auStack_1c0,4,pppppppuVar6,&DAT_0a3d78cd,&DAT_0a3d83a0,0x442,0,0);
      if ((DAT_0a3d83c5 & 1) == 0) {
        uVar9 = 0;
        do {
          (&DAT_0a3d83b2)[uVar9] = (&DAT_088ac5f3)[uVar9] + 0x8a ^ (&DAT_088ac5e3)[uVar9 & 0xf];
          uVar9 = uVar9 + 1;
        } while (uVar9 != 0x13);
        DAT_0a3d83c5 = 1;
      }
      uStack_58 = 0;
      local_60 = 0;
      local_48 = 0;
      uStack_50 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      local_c0 = (undefined8 *******)0x0;
      uStack_a8 = 0;
      uStack_b0 = 0;
      FUN_05e1d31c(auStack_1c0,&DAT_0a3d83b2,&local_c0);
      goto LAB_030b0204;
    }
    if (*(int *)(lVar4 + 0xc) == 3) {
      local_1d8 = (undefined8 *******)
                  ___dynamic_cast(local_130,&PTR_DAT_09eb2580,&PTR_DAT_09eb25b0,0);
      if (local_1d8 == (undefined8 *******)0x0) {
        local_1d8 = (undefined8 *******)0x0;
        local_1d0 = (long *)0x0;
        iVar5 = thunk_FUN_05e1d97c(4);
        if (iVar5 != 0) {
          FUN_0488143c(&local_110);
          pppppppuVar6 = local_110;
          if (-1 < cStack_f9) {
            pppppppuVar6 = &local_110;
          }
          if ((DAT_0a3d78e6 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3d78cd)[uVar9] = (&DAT_088ab71c)[uVar9] + 0x8a ^ (&DAT_088ab70c)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x19);
            DAT_0a3d78e6 = 1;
          }
          if ((DAT_0a3d83b1 & 1) == 0) {
            uRam000000000a3d83a8 = _UNK_088a7388;
            _DAT_0a3d83a0 = _DAT_088a7380;
            DAT_0a3d83b0 = 0;
            DAT_0a3d83b1 = 1;
          }
          FUN_05e1d050(auStack_1c0,4,pppppppuVar6,&DAT_0a3d78cd,&DAT_0a3d83a0,0x452,0,0);
          if ((DAT_0a3d8427 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3d840d)[uVar9] = (&DAT_088ac67b)[uVar9] + 0x8a ^ (&DAT_088ac66b)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x1a);
            DAT_0a3d8427 = 1;
          }
          uStack_58 = 0;
          local_60 = 0;
          local_48 = 0;
          uStack_50 = 0;
          uStack_78 = 0;
          local_80 = 0;
          uStack_68 = 0;
          uStack_70 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_b8 = 0;
          local_c0 = (undefined8 *******)0x0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          FUN_05e1d31c(auStack_1c0,&DAT_0a3d840d,&local_c0);
          thunk_FUN_05e1d0bc(auStack_1c0);
          if (cStack_f9 < '\0') {
            __ZdlPvm(local_110,CONCAT17(cStack_f9,local_100) & 0x7fffffffffffffff);
          }
        }
LAB_030b084c:
        uVar11 = 0;
        plVar14 = local_1d0;
      }
      else {
        if (plVar14 != (long *)0x0) {
          plVar14[1] = plVar14[1] + 1;
        }
        local_1d0 = plVar14;
        if ((*(long *)(lVar4 + 0x220) == 0) ||
           (lVar3 = ___dynamic_cast(*(long *)(lVar4 + 0x220),&PTR_DAT_09eb1040,&PTR_DAT_09eb2418,0),
           lVar3 == 0)) {
          iVar5 = thunk_FUN_05e1d97c(4);
          if (iVar5 == 0) goto LAB_030b084c;
          FUN_0488143c(&local_110);
          pppppppuVar6 = local_110;
          if (-1 < cStack_f9) {
            pppppppuVar6 = &local_110;
          }
          if ((DAT_0a3d78e6 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3d78cd)[uVar9] = (&DAT_088ab71c)[uVar9] + 0x8a ^ (&DAT_088ab70c)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x19);
            DAT_0a3d78e6 = 1;
          }
          if ((DAT_0a3d83b1 & 1) == 0) {
            uRam000000000a3d83a8 = _UNK_088a7388;
            _DAT_0a3d83a0 = _DAT_088a7380;
            DAT_0a3d83b0 = 0;
            DAT_0a3d83b1 = 1;
          }
          FUN_05e1d050(auStack_1c0,4,pppppppuVar6,&DAT_0a3d78cd,&DAT_0a3d83a0,0x45d,0,0);
          if ((DAT_0a3d8445 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3d8428)[uVar9] = (&DAT_088ac6a5)[uVar9] + 0x8a ^ (&DAT_088ac695)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x1d);
            DAT_0a3d8445 = 1;
          }
          uStack_58 = 0;
          local_60 = 0;
          local_48 = 0;
          uStack_50 = 0;
          uStack_78 = 0;
          local_80 = 0;
          uStack_68 = 0;
          uStack_70 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_b8 = 0;
          local_c0 = (undefined8 *******)0x0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          FUN_05e1d31c(auStack_1c0,&DAT_0a3d8428,&local_c0);
          thunk_FUN_05e1d0bc(auStack_1c0);
          if (cStack_f9 < '\0') {
            __ZdlPvm(local_110,CONCAT17(cStack_f9,local_100) & 0x7fffffffffffffff);
          }
          uVar11 = 0;
          plVar14 = local_1d0;
        }
        else {
          plVar12 = *(long **)(lVar4 + 0x228);
          if (plVar12 != (long *)0x0) {
            plVar12[1] = plVar12[1] + 1;
            uVar11 = 1;
            LOAcquire();
            lVar4 = plVar12[1];
            plVar12[1] = lVar4 + -1;
            LORelease();
            plVar14 = local_1d0;
            if (lVar4 != 0) goto joined_r0x030b0854;
            (**(code **)(*plVar12 + 0x10))(plVar12);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
          }
          uVar11 = 1;
          plVar14 = local_1d0;
        }
      }
joined_r0x030b0854:
      local_1d0 = plVar14;
      if (plVar14 != (long *)0x0) {
        LOAcquire();
        lVar4 = plVar14[1];
        plVar14[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*plVar14 + 0x10))(plVar14);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
        }
      }
      goto LAB_030b0228;
    }
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(&local_1d8);
      pppppppuVar6 = local_1d8;
      if (-1 < cStack_1c1) {
        pppppppuVar6 = &local_1d8;
      }
      if ((DAT_0a3d78e6 & 1) == 0) {
        uVar9 = 0;
        do {
          (&DAT_0a3d78cd)[uVar9] = (&DAT_088ab71c)[uVar9] + 0x8a ^ (&DAT_088ab70c)[uVar9 & 0xf];
          uVar9 = uVar9 + 1;
        } while (uVar9 != 0x19);
        DAT_0a3d78e6 = 1;
      }
      if ((DAT_0a3d83b1 & 1) == 0) {
        uRam000000000a3d83a8 = _UNK_088a7388;
        _DAT_0a3d83a0 = _DAT_088a7380;
        DAT_0a3d83b0 = 0;
        DAT_0a3d83b1 = 1;
      }
      FUN_05e1d050(auStack_1c0,4,pppppppuVar6,&DAT_0a3d78cd,&DAT_0a3d83a0,0x44c,0,0);
      uVar7 = *(uint *)(local_120 + 0xc);
      local_110 = (undefined8 *******)&local_108;
      if ((DAT_0a3d849a & 1) == 0) {
        uVar9 = 0;
        do {
          (&DAT_0a3d8452)[uVar9] = (&DAT_088ac779)[uVar9] + 0x8a ^ (&DAT_088ac769)[uVar9 & 0xf];
          uVar9 = uVar9 + 1;
        } while (uVar9 != 0x48);
        DAT_0a3d849a = 1;
      }
      uVar9 = (ulong)uVar7;
      lVar4 = 0;
      do {
        lVar3 = lVar4;
        uVar7 = (uint)uVar9;
        *(undefined1 *)((long)&local_108 + lVar3) =
             (&DAT_0a3d8452)[uVar7 + (int)(uVar9 / 10) * -10 + 0x23];
        uVar9 = uVar9 / 10;
        lVar4 = lVar3 + 1;
      } while (9 < uVar7);
      *(undefined1 *)((long)&local_108 + lVar3 + 1) = 0;
      if (8 < lVar3 + 8U) {
        puVar8 = (undefined1 *)((long)&local_108 + lVar3);
        puVar10 = (undefined1 *)((long)&local_108 + 1);
        do {
          uVar1 = *puVar8;
          *puVar8 = puVar10[-1];
          puVar10[-1] = uVar1;
          bVar2 = puVar10 < puVar8 + -1;
          puVar8 = puVar8 + -1;
          puVar10 = puVar10 + 1;
        } while (bVar2);
      }
      if ((DAT_0a3d840c & 1) == 0) {
        uVar9 = 0;
        do {
          (&DAT_0a3d83dc)[uVar9] = (&DAT_088ac63b)[uVar9] + 0x8a ^ (&DAT_088ac62b)[uVar9 & 0xf];
          uVar9 = uVar9 + 1;
        } while (uVar9 != 0x30);
        DAT_0a3d840c = 1;
      }
      uStack_b0 = 0;
      uStack_b8 = 0;
      local_c0 = &local_110;
      local_a0 = 0;
      uStack_a8 = 0;
      uStack_90 = 0;
      uStack_98 = 0;
      local_80 = 0;
      uStack_88 = 0;
      uStack_70 = 0;
      uStack_78 = 0;
      local_60 = 0;
      uStack_68 = 0;
      uStack_50 = 0;
      uStack_58 = 0;
      local_48 = 0;
      FUN_05e1d31c(auStack_1c0,&DAT_0a3d83dc,&local_c0);
      thunk_FUN_05e1d0bc(auStack_1c0);
      if (-1 < cStack_1c1) goto LAB_030b0224;
      uVar9 = CONCAT17(cStack_1c1,local_1c8);
      pppppppuVar6 = local_1d8;
      goto LAB_030b021c;
    }
  }
LAB_030b0224:
  uVar11 = 0;
LAB_030b0228:
  plVar14 = local_128;
  if (local_128 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_128[1];
    local_128[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_128 + 0x10))(local_128);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
    }
  }
  plVar14 = local_118;
  if (local_118 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_118[1];
    local_118[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_118 + 0x10))(local_118);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar11;
}


