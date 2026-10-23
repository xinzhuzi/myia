// Ghidra inferred pseudocode; requested=0x31cae30
// entry=031cae30 end=031cb98b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_031cae30(undefined8 param_1,undefined8 param_2,long *param_3,long *******param_4)

{
  long *plVar1;
  undefined8 *******pppppppuVar2;
  long lVar3;
  int iVar4;
  long lVar5;
  ulong uVar6;
  long *plVar7;
  long *plVar8;
  long *plVar9;
  long lVar10;
  undefined8 local_210;
  long *local_208;
  long *******local_200 [2];
  undefined7 local_1f0;
  char cStack_1e9;
  undefined8 *******local_1e8 [2];
  undefined7 local_1d8;
  char cStack_1d1;
  long local_1d0;
  long *local_1c8 [17];
  long *******local_140;
  undefined1 local_138;
  undefined7 uStack_137;
  long *******local_f0;
  long *local_e8;
  undefined8 uStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar5 = FUN_03221ac0(param_2,param_4);
  if (lVar5 == 0) {
    iVar4 = thunk_FUN_05e1d97c(3);
    if (iVar4 != 0) {
      FUN_0488143c(local_1e8);
      pppppppuVar2 = local_1e8[0];
      if (-1 < cStack_1d1) {
        pppppppuVar2 = local_1e8;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e0299 & 1) == 0) {
        _DAT_0a3e0280 = CONCAT44((int)ram0x084fdd88,(int)DAT_0848c190);
        uRam000000000a3e0288 = CONCAT44((int)DAT_0856e3b0,(int)DAT_084a8110);
        DAT_0a3e0290 = CONCAT44((int)DAT_0849a618,(int)DAT_08489760);
        DAT_0a3e0298 = 0;
        DAT_0a3e0299 = 1;
      }
      FUN_05e1d050(&local_1d0,3,pppppppuVar2,&DAT_0a3dd350,&DAT_0a3e0280,0xfe1,0,0);
      FUN_030f1f08(local_200,*param_3);
      local_140 = local_200[0];
      if (-1 < cStack_1e9) {
        local_140 = (long *******)local_200;
      }
      local_138 = 0;
      if ((DAT_0a3e02e8 & 1) == 0) {
        _DAT_0a3e02c4 = CONCAT44((int)DAT_084a66b0,(int)DAT_088ba9c0);
        uRam000000000a3e02cc = CONCAT44((int)DAT_0848c098,(int)DAT_084d88c0);
        _DAT_0a3e02d4 = CONCAT44((int)DAT_08563690,(int)DAT_085636c8);
        uRam000000000a3e02dc = CONCAT44((int)ram0x0848d900,(int)DAT_088baf30);
        DAT_0a3e02e4 = (undefined4)ram0x084c9468;
        DAT_0a3e02e8 = 1;
      }
      uStack_e0 = 0;
      local_e8 = (long *)0x0;
      local_f0 = (long *******)&local_140;
      uStack_d0 = 0;
      local_d8 = 0;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_1d0,&DAT_0a3e02c4,&local_f0);
      if (cStack_1e9 < '\0') {
        __ZdlPvm(local_200[0],CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_1d0);
      if (cStack_1d1 < '\0') {
        __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
      }
    }
    goto LAB_031cb828;
  }
  plVar8 = *(long **)(lVar5 + 0x28);
  plVar7 = *(long **)(lVar5 + 0x30);
  if (plVar8 == plVar7) {
LAB_031caeb0:
    if (plVar8 == plVar7) goto LAB_031cb384;
    iVar4 = thunk_FUN_05e1d97c(2);
    if (iVar4 != 0) {
      FUN_0488143c(local_1e8);
      pppppppuVar2 = local_1e8[0];
      if (-1 < cStack_1d1) {
        pppppppuVar2 = local_1e8;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e0299 & 1) == 0) {
        _DAT_0a3e0280 = CONCAT44((int)ram0x084fdd88,(int)DAT_0848c190);
        uRam000000000a3e0288 = CONCAT44((int)DAT_0856e3b0,(int)DAT_084a8110);
        DAT_0a3e0290 = CONCAT44((int)DAT_0849a618,(int)DAT_08489760);
        DAT_0a3e0298 = 0;
        DAT_0a3e0299 = 1;
      }
      FUN_05e1d050(&local_1d0,2,pppppppuVar2,&DAT_0a3dd350,&DAT_0a3e0280,0xfd7,0,0);
      FUN_030f1f08(local_200,*param_3);
      local_140 = local_200[0];
      if (-1 < cStack_1e9) {
        local_140 = (long *******)local_200;
      }
      local_138 = 0;
      if ((DAT_0a3e02c0 & 1) == 0) {
        _DAT_0a3e029c = CONCAT44((int)DAT_084a66b0,(int)DAT_088ba9c0);
        uRam000000000a3e02a4 = CONCAT44((int)DAT_084aa990,(int)DAT_0857acd0);
        _DAT_0a3e02ac = CONCAT44((int)DAT_087fade8,(int)DAT_084f2d48);
        uRam000000000a3e02b4 = CONCAT44((int)ram0x0848d900,(int)DAT_088baf30);
        DAT_0a3e02bc = (undefined4)ram0x084c9468;
        DAT_0a3e02c0 = 1;
      }
      uStack_e0 = 0;
      local_e8 = (long *)0x0;
      local_f0 = (long *******)&local_140;
      uStack_d0 = 0;
      local_d8 = 0;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_1d0,&DAT_0a3e029c,&local_f0);
      if (cStack_1e9 < '\0') {
        __ZdlPvm(local_200[0],CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_1d0);
      if (cStack_1d1 < '\0') {
        __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
      }
    }
    plVar9 = *(long **)(lVar5 + 0x30);
    plVar7 = plVar8;
    if (plVar8 + 2 != plVar9) {
      do {
        lVar10 = plVar8[3];
        lVar3 = plVar8[2];
        plVar8[2] = 0;
        plVar8[3] = 0;
        plVar7 = (long *)plVar8[1];
        plVar8[1] = lVar10;
        *plVar8 = lVar3;
        if (plVar7 != (long *)0x0) {
          LOAcquire();
          lVar3 = plVar7[1];
          plVar7[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*plVar7 + 0x10))(plVar7);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        plVar7 = plVar8 + 2;
        plVar1 = plVar8 + 4;
        plVar8 = plVar7;
      } while (plVar1 != plVar9);
      plVar9 = *(long **)(lVar5 + 0x30);
    }
    for (; plVar9 != plVar7; plVar9 = plVar9 + -2) {
      plVar8 = (long *)plVar9[-1];
      if (plVar8 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar8[1];
        plVar8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
    }
    *(long **)(lVar5 + 0x30) = plVar7;
  }
  else {
    do {
      if (*plVar8 == *param_3) goto LAB_031caeb0;
      plVar8 = plVar8 + 2;
    } while (plVar8 != plVar7);
LAB_031cb384:
    iVar4 = thunk_FUN_05e1d97c(3);
    if (iVar4 != 0) {
      FUN_0488143c(local_1e8);
      pppppppuVar2 = local_1e8[0];
      if (-1 < cStack_1d1) {
        pppppppuVar2 = local_1e8;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e0299 & 1) == 0) {
        _DAT_0a3e0280 = CONCAT44((int)ram0x084fdd88,(int)DAT_0848c190);
        uRam000000000a3e0288 = CONCAT44((int)DAT_0856e3b0,(int)DAT_084a8110);
        DAT_0a3e0290 = CONCAT44((int)DAT_0849a618,(int)DAT_08489760);
        DAT_0a3e0298 = 0;
        DAT_0a3e0299 = 1;
      }
      FUN_05e1d050(&local_1d0,3,pppppppuVar2,&DAT_0a3dd350,&DAT_0a3e0280,0xfda,0,0);
      FUN_030f1f08(local_200,*param_3);
      local_140 = local_200[0];
      if (-1 < cStack_1e9) {
        local_140 = (long *******)local_200;
      }
      local_138 = 0;
      if ((DAT_0a3e02e8 & 1) == 0) {
        _DAT_0a3e02c4 = CONCAT44((int)DAT_084a66b0,(int)DAT_088ba9c0);
        uRam000000000a3e02cc = CONCAT44((int)DAT_0848c098,(int)DAT_084d88c0);
        _DAT_0a3e02d4 = CONCAT44((int)DAT_08563690,(int)DAT_085636c8);
        uRam000000000a3e02dc = CONCAT44((int)ram0x0848d900,(int)DAT_088baf30);
        DAT_0a3e02e4 = (undefined4)ram0x084c9468;
        DAT_0a3e02e8 = 1;
      }
      uStack_e0 = 0;
      local_e8 = (long *)0x0;
      local_f0 = (long *******)&local_140;
      uStack_d0 = 0;
      local_d8 = 0;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_1d0,&DAT_0a3e02c4,&local_f0);
      if (cStack_1e9 < '\0') {
        __ZdlPvm(local_200[0],CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_1d0);
      if (cStack_1d1 < '\0') {
        __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
      }
    }
  }
  if (*(long *)(lVar5 + 0x28) == *(long *)(lVar5 + 0x30)) {
    iVar4 = thunk_FUN_05e1d97c(3);
    if (iVar4 != 0) {
      FUN_0488143c(local_1e8);
      pppppppuVar2 = local_1e8[0];
      if (-1 < cStack_1d1) {
        pppppppuVar2 = local_1e8;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e0299 & 1) == 0) {
        _DAT_0a3e0280 = CONCAT44((int)ram0x084fdd88,(int)DAT_0848c190);
        uRam000000000a3e0288 = CONCAT44((int)DAT_0856e3b0,(int)DAT_084a8110);
        DAT_0a3e0290 = CONCAT44((int)DAT_0849a618,(int)DAT_08489760);
        DAT_0a3e0298 = 0;
        DAT_0a3e0299 = 1;
      }
      FUN_05e1d050(&local_1d0,3,pppppppuVar2,&DAT_0a3dd350,&DAT_0a3e0280,0xfdd,0,0);
      local_140 = (long *******)*param_4;
      if (-1 < *(char *)((long)param_4 + 0x17)) {
        local_140 = param_4;
      }
      local_138 = 0;
      if ((DAT_0a3e0304 & 1) == 0) {
        _DAT_0a3e02ec = CONCAT44((int)DAT_084e3ff8,(int)DAT_085b56d0);
        uRam000000000a3e02f4 = CONCAT44((int)DAT_08554250,(int)DAT_0847fe60);
        DAT_0a3e02fc = CONCAT44((int)DAT_084e3f98,(int)DAT_084ce750);
        DAT_0a3e0304 = 1;
      }
      uStack_e0 = 0;
      local_e8 = (long *)0x0;
      local_f0 = (long *******)&local_140;
      uStack_d0 = 0;
      local_d8 = 0;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_1d0,&DAT_0a3e02ec,&local_f0);
      thunk_FUN_05e1d0bc(&local_1d0);
      if (cStack_1d1 < '\0') {
        __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
      }
    }
    FUN_000424e0(&local_1d0,param_2,lVar5);
    lVar5 = local_1d0;
    local_1d0 = 0;
    if (lVar5 != 0) {
      FUN_00a9dbc8(local_1c8);
    }
  }
LAB_031cb828:
  iVar4 = FUN_030f320c(*param_3);
  if ((iVar4 == 8) || (iVar4 = FUN_030f320c(*param_3), iVar4 == 10)) {
    FUN_0466aca8(&local_140);
    FUN_01205740(&local_f0,local_140);
    FUN_0317f064(&local_1d0,local_f0);
    local_210 = *(undefined8 *)(*param_3 + 0x18);
    local_208 = *(long **)(*param_3 + 0x20);
    lVar5 = 0;
    if (local_208 != (long *)0x0) {
      lVar5 = local_208[1];
      local_208[1] = lVar5 + 1;
    }
    FUN_03534e3c(lVar5,local_1d0,&local_210);
    plVar8 = local_208;
    if (local_208 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_208[1];
      local_208[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_208 + 0x10))(local_208);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    if (local_1c8[0] != (long *)0x0) {
      LOAcquire();
      lVar5 = local_1c8[0][1];
      local_1c8[0][1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_1c8[0] + 0x10))(local_1c8[0]);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_1c8[0]);
      }
    }
    plVar8 = local_e8;
    if (local_e8 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_e8[1];
      local_e8[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_e8 + 0x10))(local_e8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = (long *)CONCAT71(uStack_137,local_138);
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar8[1];
      plVar8[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_70) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


