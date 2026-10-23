// Ghidra inferred pseudocode; requested=0x31cf3a4
// entry=031cf3a4 end=031d0f63

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_031cf3a4(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  long *plVar1;
  dword *pdVar2;
  long *plVar3;
  byte bVar4;
  uint3 uVar5;
  long lVar6;
  long lVar7;
  undefined1 *puVar8;
  undefined8 *******pppppppuVar9;
  int iVar10;
  undefined8 uVar11;
  ulong uVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  long *plVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  undefined1 *local_2f0;
  long *local_2e8;
  undefined1 *local_2e0;
  long *local_2d8;
  long *local_2d0;
  long *local_2c8;
  long *local_2c0;
  long *plStack_2b8;
  undefined1 *local_2b0;
  long *local_2a8;
  dword *local_2a0;
  long *local_298;
  undefined7 local_290;
  char cStack_289;
  dword *local_288;
  long *local_280;
  undefined7 local_278;
  char cStack_271;
  long local_270;
  long *local_268;
  dword *local_260;
  long *local_258;
  undefined7 local_250;
  char cStack_249;
  undefined7 local_248;
  char cStack_241;
  undefined1 *local_240;
  long *local_238;
  undefined7 local_228;
  char cStack_221;
  byte local_220;
  undefined8 local_218;
  long *local_1d0;
  long *local_1c8;
  undefined8 local_1c0;
  dword *pdStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  long *local_198;
  undefined8 *******local_190;
  long *local_188;
  long *local_180;
  undefined8 local_178;
  dword *local_140;
  undefined1 local_138;
  undefined7 local_130;
  char cStack_129;
  dword **local_f0;
  undefined8 *******pppppppuStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar15 = (long *)*param_3;
  plVar3 = (long *)param_3[1];
  if (plVar3 != (long *)0x0) {
    plVar3[1] = plVar3[1] + 1;
  }
  local_2e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_021efaf0(&local_2e0,&local_260);
  local_2f0 = local_2e0;
  local_2e8 = local_2d8;
  lVar6 = 0;
  if (local_2d8 != (long *)0x0) {
    lVar6 = local_2d8[1];
    local_2d8[1] = lVar6 + 1;
  }
  puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  local_198 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  pdStack_1b8 = (dword *)&SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = (dword *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(lVar6,&local_1c0,0,0);
  local_1d0 = (long *)plVar15[1];
  if (local_1d0 != (long *)0x0) {
    local_1c8 = (long *)plVar15[2];
    if (local_1c8 != (long *)0x0) {
      local_1c8[1] = local_1c8[1] + 1;
    }
    lVar6 = plVar15[0x1a];
    local_268 = (long *)plVar15[0x1b];
    lVar7 = 0;
    if (local_268 != (long *)0x0) {
      lVar7 = local_268[1];
      local_268[1] = lVar7 + 1;
    }
    local_270 = lVar6;
    if (lVar6 == 0) {
      uVar11 = (**(code **)(*local_1d0 + 0x20))();
      if ((int)uVar11 != 1) {
        iVar10 = (**(code **)(*local_1d0 + 0x20))();
        if (iVar10 != 2) goto LAB_031d02f4;
        if ((local_1d0 == (long *)0x0) ||
           (local_190 = (undefined8 *******)
                        ___dynamic_cast(local_1d0,&PTR_DAT_09c37aa0,&PTR_DAT_09c3edd0,0),
           plVar1 = local_1c8, local_190 == (undefined8 *******)0x0)) {
          local_190 = (undefined8 *******)0x0;
          local_188 = (long *)0x0;
        }
        else {
          local_188 = local_1c8;
          if (local_1c8 != (long *)0x0) {
            local_1c8[1] = local_1c8[1] + 1;
          }
          if (((*(int *)(local_190 + 0x1e) != 0x31) || (*(int *)((long)local_190 + 0xf4) != 0x82))
             || (uVar12 = FUN_048a353c(local_190 + 0x12), (uVar12 & 1) != 0)) {
            if (plVar1 != (long *)0x0) {
              LOAcquire();
              lVar6 = plVar1[1];
              plVar1[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*plVar1 + 0x10))(plVar1);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
              }
            }
            goto LAB_031d02f4;
          }
        }
        iVar10 = thunk_FUN_05e1d97c(4);
        if (iVar10 != 0) {
          FUN_0488143c(&local_140);
          pdVar2 = local_140;
          if (-1 < cStack_129) {
            pdVar2 = (dword *)&local_140;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar12 = 0;
            do {
              (&DAT_0a3dd350)[uVar12] =
                   (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
              uVar12 = uVar12 + 1;
            } while (uVar12 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3e2ee3 & 1) == 0) {
            DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a3e2ee0 = 0x2928;
            DAT_0a3e2ee2 = 0;
            DAT_0a3e2ee3 = 1;
          }
          FUN_05e1d050(&local_260,4,pdVar2,&DAT_0a3dd350,0xa3e2ed8,"undation",0,0);
          if ((DAT_0a3e3577 & 1) == 0) {
            _DAT_0a3e355c = CONCAT44((int)DAT_08808ce0,(int)DAT_084d8468);
            uRam000000000a3e3564 = CONCAT44((int)DAT_088bafe8,(int)DAT_08523200);
            DAT_0a3e356c = CONCAT44((int)DAT_084caf60,(int)DAT_0856e3c0);
            DAT_0a3e3574 = 0x6465;
            DAT_0a3e3576 = 0;
            DAT_0a3e3577 = 1;
          }
          uStack_88 = 0;
          local_90 = 0;
          uStack_78 = 0;
          local_80 = 0;
          uStack_a8 = 0;
          local_b0 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_c8 = 0;
          local_d0 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          pppppppuStack_e8 = (undefined8 *******)0x0;
          local_f0 = (dword **)0x0;
          uStack_d8 = 0;
          local_e0 = 0;
          FUN_05e1d31c(&local_260,&DAT_0a3e355c,&local_f0);
          thunk_FUN_05e1d0bc(&local_260);
          if (cStack_129 < '\0') {
            __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
          }
        }
        FUN_030f6640(&local_260,1,1);
        puVar13 = local_1a0;
        FUN_030f67ac(local_1a0,&local_260);
        *(undefined8 *)(puVar13 + 0x48) = local_218;
        local_1c0 = (dword *)((ulong)local_1c0 & 0xffffffff);
        if ((local_220 & 1) == 0) {
          local_1c0 = &MACH_HEADER.cputype;
LAB_031d0d7c:
          local_1c0 = (dword *)CONCAT44(400,(int)local_1c0);
        }
        else {
          if (cStack_221 < '\0') {
            __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
          }
          if (cStack_249 < '\0') {
            __ZdlPvm(local_260,CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
          }
          local_1c0 = (dword *)CONCAT44(local_1c0._4_4_,4);
          if (local_1c0._4_4_ == 0) goto LAB_031d0d7c;
        }
        FUN_031d1444(&local_2f0,&local_1c0);
        plVar15 = local_188;
        if (local_188 == (long *)0x0) goto LAB_031d0dc0;
        goto LAB_031d0d98;
      }
      local_288 = (dword *)&SUB_aaaaaaaaaaaaaaaa;
      local_280 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_03187748(&local_288,uVar11,&local_1d0,(dword *)((ulong)&local_1c0 | 8));
      pdVar2 = local_288;
      if (local_288 == (dword *)0x0) {
        iVar10 = thunk_FUN_05e1d97c(4);
        if (iVar10 != 0) {
          FUN_0488143c(&local_190);
          pppppppuVar9 = local_190;
          if (-1 < (long)local_180) {
            pppppppuVar9 = &local_190;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar12 = 0;
            do {
              (&DAT_0a3dd350)[uVar12] =
                   (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
              uVar12 = uVar12 + 1;
            } while (uVar12 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3e2ee3 & 1) == 0) {
            DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a3e2ee0 = 0x2928;
            DAT_0a3e2ee2 = 0;
            DAT_0a3e2ee3 = 1;
          }
          FUN_05e1d050(&local_260,4,pppppppuVar9,&DAT_0a3dd350,0xa3e2ed8,"rsions/C/Foundation",0,0);
          local_140 = pdStack_1b8;
          if (-1 < (long)puStack_1a8) {
            local_140 = (dword *)((ulong)&local_1c0 | 8);
          }
          local_138 = 0;
          if ((DAT_0a3e3559 & 1) == 0) {
            _DAT_0a3e352c = CONCAT44((int)ram0x088a1110,(int)DAT_085029d8);
            uRam000000000a3e3534 = CONCAT44((int)DAT_0856e3b0,(int)DAT_084a8110);
            _DAT_0a3e353c = CONCAT44((int)DAT_0856e3c0,(int)DAT_0856e3b8);
            uRam000000000a3e3544 = CONCAT44((int)DAT_084caf68,(int)DAT_084caf60);
            DAT_0a3e354c = CONCAT44((int)DAT_08502a08,(int)DAT_084808a8);
            DAT_0a3e3554 = (undefined4)DAT_08502a10;
            DAT_0a3e3558 = 0;
            DAT_0a3e3559 = 1;
          }
          local_e0 = 0;
          pppppppuStack_e8 = (undefined8 *******)0x0;
          local_f0 = &local_140;
          local_d0 = 0;
          uStack_d8 = 0;
          local_c0 = 0;
          uStack_c8 = 0;
          local_b0 = 0;
          uStack_b8 = 0;
          local_a0 = 0;
          uStack_a8 = 0;
          local_90 = 0;
          uStack_98 = 0;
          local_80 = 0;
          uStack_88 = 0;
          uStack_78 = 0;
          FUN_05e1d31c(&local_260,&DAT_0a3e352c,&local_f0);
          thunk_FUN_05e1d0bc(&local_260);
          if ((long)local_180 < 0) {
            __ZdlPvm(local_190,(ulong)local_180 & 0x7fffffffffffffff);
          }
        }
        FUN_030f6640(&local_260,1,1);
        puVar13 = local_1a0;
        FUN_030f67ac(local_1a0,&local_260);
        *(undefined8 *)(puVar13 + 0x48) = local_218;
        local_1c0 = (dword *)((ulong)local_1c0 & 0xffffffff);
        if ((local_220 & 1) == 0) {
          local_1c0 = &MACH_HEADER.cputype;
LAB_031d02ac:
          local_1c0 = (dword *)CONCAT44(400,(int)local_1c0);
        }
        else {
          if (cStack_221 < '\0') {
            __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
          }
          if (cStack_249 < '\0') {
            __ZdlPvm(local_260,CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
          }
          local_1c0 = (dword *)CONCAT44(local_1c0._4_4_,4);
          if (local_1c0._4_4_ == 0) goto LAB_031d02ac;
        }
        FUN_031d1444(&local_2f0,&local_1c0);
      }
      else {
        local_260 = local_288;
        local_258 = local_280;
        lVar6 = 0;
        if (local_280 != (long *)0x0) {
          lVar6 = local_280[1];
          local_280[1] = lVar6 + 1;
        }
        FUN_030f27e4(lVar6,plVar15,&local_260);
        plVar1 = local_258;
        if (local_258 != (long *)0x0) {
          LOAcquire();
          lVar6 = local_258[1];
          local_258[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*local_258 + 0x10))(local_258);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
          }
        }
      }
      plVar1 = local_280;
      if (local_280 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_280[1];
        local_280[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*local_280 + 0x10))(local_280);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
        }
      }
      if (pdVar2 != (dword *)0x0) {
LAB_031d02f4:
        local_190 = (undefined8 *******)&local_1c0;
        pppppppuVar9 = local_190;
        if (plVar3 != (long *)0x0) {
          pppppppuVar9 = (undefined8 *******)plVar3[1];
          plVar3[1] = (long)pppppppuVar9 + 1;
        }
        local_188 = plVar15;
        local_180 = plVar3;
        local_178 = param_2;
        FUN_032261d4(pppppppuVar9,&local_190);
        if ((int)local_1c0 == 0 && local_1c0._4_4_ == 0) {
LAB_031d0788:
          local_2b0 = &SUB_aaaaaaaaaaaaaaaa;
          local_2a8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          if (plVar3 != (long *)0x0) {
            plVar3[1] = plVar3[1] + 1;
          }
          local_2c0 = plVar15;
          plStack_2b8 = plVar3;
          FUN_0318d680(&local_2b0,param_2,&local_2c0);
          if (plVar3 != (long *)0x0) {
            LOAcquire();
            lVar6 = plVar3[1];
            plVar3[1] = lVar6 + -1;
            LORelease();
            if (lVar6 == 0) {
              (**(code **)(*plVar3 + 0x10))(plVar3);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
            }
          }
          if (local_2b0 == (undefined1 *)0x0) {
            iVar10 = thunk_FUN_05e1d97c(4);
            if (iVar10 != 0) {
              FUN_0488143c(&local_140);
              pdVar2 = local_140;
              if (-1 < cStack_129) {
                pdVar2 = (dword *)&local_140;
              }
              if ((DAT_0a3dd363 & 1) == 0) {
                uVar12 = 0;
                do {
                  (&DAT_0a3dd350)[uVar12] =
                       (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
                  uVar12 = uVar12 + 1;
                } while (uVar12 != 0x13);
                DAT_0a3dd363 = 1;
              }
              if ((DAT_0a3e2ee3 & 1) == 0) {
                DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
                DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
                DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
                DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
                DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
                DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
                DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
                DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
                DAT_0a3e2ee0 = 0x2928;
                DAT_0a3e2ee2 = 0;
                DAT_0a3e2ee3 = 1;
              }
              FUN_05e1d050(&local_260,4,pdVar2,&DAT_0a3dd350,0xa3e2ed8,0x1184,0,0);
              if ((DAT_0a3e0730 & 1) == 0) {
                uRam000000000a3e0728._0_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x88];
                uRam000000000a3e0728._1_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x89];
                uRam000000000a3e0728._2_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x8a];
                uRam000000000a3e0728._3_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x8b];
                uRam000000000a3e0728._4_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x8c];
                uRam000000000a3e0728._5_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x8d];
                uRam000000000a3e0728._6_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x8e];
                uRam000000000a3e0728._7_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x8f];
                DAT_0a3e0720 = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x80];
                DAT_0a3e0720_1._0_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x81];
                DAT_0a3e0720_1._1_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x82];
                DAT_0a3e0720_1._2_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x83];
                DAT_0a3e0720_1._3_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x84];
                DAT_0a3e0720_1._4_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x85];
                DAT_0a3e0720_1._5_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x86];
                DAT_0a3e0720_1._6_1_ = s_DeleteAllMessageOnMessageDeleteA_088bb550[0x87];
                DAT_0a3e0730 = 1;
              }
              uStack_88 = 0;
              local_90 = 0;
              uStack_78 = 0;
              local_80 = 0;
              uStack_a8 = 0;
              local_b0 = 0;
              uStack_98 = 0;
              local_a0 = 0;
              uStack_c8 = 0;
              local_d0 = 0;
              uStack_b8 = 0;
              local_c0 = 0;
              pppppppuStack_e8 = (undefined8 *******)0x0;
              local_f0 = (dword **)0x0;
              uStack_d8 = 0;
              local_e0 = 0;
              FUN_05e1d31c(&local_260,&DAT_0a3e0720,&local_f0);
              thunk_FUN_05e1d0bc(&local_260);
              if (cStack_129 < '\0') {
                __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
              }
            }
            FUN_030f6640(&local_260,1,1);
            puVar13 = local_1a0;
            FUN_030f67ac(local_1a0,&local_260);
            *(undefined8 *)(puVar13 + 0x48) = local_218;
            local_1c0 = (dword *)((ulong)local_1c0 & 0xffffffff);
            if ((local_220 & 1) == 0) {
              local_1c0 = &MACH_HEADER.cputype;
            }
            else {
              if (cStack_221 < '\0') {
                __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
              }
              if (cStack_249 < '\0') {
                __ZdlPvm(local_260,CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
              }
              local_1c0 = (dword *)CONCAT44(local_1c0._4_4_,4);
              if (local_1c0._4_4_ != 0) goto LAB_031d0d2c;
            }
            local_1c0 = (dword *)CONCAT44(400,(int)local_1c0);
          }
          else {
            FUN_030f3214(plVar15,2);
            if (plVar3 != (long *)0x0) {
              plVar3[1] = plVar3[1] + 1;
            }
            local_2d0 = plVar15;
            local_2c8 = plVar3;
            FUN_030d28a4(&local_260,local_2b0,&local_2d0);
            local_1c0 = local_260;
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      ((ulong)&local_1c0 | 8,&local_258);
            plVar1 = local_198;
            if (local_238 != (long *)0x0) {
              local_238[1] = local_238[1] + 1;
            }
            local_1a0 = local_240;
            local_198 = local_238;
            if (plVar1 != (long *)0x0) {
              LOAcquire();
              lVar6 = plVar1[1];
              plVar1[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*plVar1 + 0x10))(plVar1);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
              }
            }
            if (local_238 != (long *)0x0) {
              LOAcquire();
              lVar6 = local_238[1];
              local_238[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*local_238 + 0x10))(local_238);
                __ZNSt3__119__shared_weak_count14__release_weakEv(local_238);
              }
            }
            if (cStack_241 < '\0') {
              __ZdlPvm(local_258,CONCAT17(cStack_241,local_248) & 0x7fffffffffffffff);
            }
            plVar1 = local_2c8;
            if (local_2c8 != (long *)0x0) {
              LOAcquire();
              lVar6 = local_2c8[1];
              local_2c8[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*local_2c8 + 0x10))(local_2c8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
              }
            }
            if (((int)local_1c0 != 0 || local_1c0._4_4_ != 0) &&
               (iVar10 = thunk_FUN_05e1d97c(4), iVar10 != 0)) {
              FUN_0488143c(&local_288);
              pdVar2 = local_288;
              if (-1 < cStack_271) {
                pdVar2 = (dword *)&local_288;
              }
              if ((DAT_0a3dd363 & 1) == 0) {
                uVar12 = 0;
                do {
                  (&DAT_0a3dd350)[uVar12] =
                       (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
                  uVar12 = uVar12 + 1;
                } while (uVar12 != 0x13);
                DAT_0a3dd363 = 1;
              }
              if ((DAT_0a3e2ee3 & 1) == 0) {
                DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
                DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
                DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
                DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
                DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
                DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
                DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
                DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
                DAT_0a3e2ee0 = 0x2928;
                DAT_0a3e2ee2 = 0;
                DAT_0a3e2ee3 = 1;
              }
              FUN_05e1d050(&local_260,4,pdVar2,&DAT_0a3dd350,0xa3e2ed8,
                           "em/Library/Frameworks/AppKit.framework/Versions/C/AppKit",0,0);
              FUN_030f1f08(&local_2a0,plVar15);
              local_140 = local_2a0;
              if (-1 < cStack_289) {
                local_140 = (dword *)&local_2a0;
              }
              local_138 = 0;
              if ((DAT_0a3e361f & 1) == 0) {
                _DAT_0a3e35f4 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
                uRam000000000a3e35fc = CONCAT44((int)ram0x087e2de8,(int)DAT_084e3ff8);
                _DAT_0a3e3604 = CONCAT44((int)ram0x084f0820,(int)DAT_087e2df0);
                uRam000000000a3e360c = CONCAT44((int)DAT_0850ad18,(int)DAT_084b0670);
                DAT_0a3e3614 = CONCAT44((int)DAT_084caf60,(int)DAT_088ae2b8);
                DAT_0a3e361c = 0x6465;
                DAT_0a3e361e = 0;
                DAT_0a3e361f = 1;
              }
              local_e0 = 0;
              pppppppuStack_e8 = (undefined8 *******)0x0;
              local_f0 = &local_140;
              local_d0 = 0;
              uStack_d8 = 0;
              local_c0 = 0;
              uStack_c8 = 0;
              local_b0 = 0;
              uStack_b8 = 0;
              local_a0 = 0;
              uStack_a8 = 0;
              local_90 = 0;
              uStack_98 = 0;
              local_80 = 0;
              uStack_88 = 0;
              uStack_78 = 0;
              FUN_05e1d31c(&local_260,&DAT_0a3e35f4,&local_f0);
              if (cStack_289 < '\0') {
                __ZdlPvm(local_2a0,CONCAT17(cStack_289,local_290) & 0x7fffffffffffffff);
              }
              thunk_FUN_05e1d0bc(&local_260);
              if (cStack_271 < '\0') {
                __ZdlPvm(local_288,CONCAT17(cStack_271,local_278) & 0x7fffffffffffffff);
              }
            }
            plVar15 = (long *)plVar15[4];
            if (plVar15 != (long *)0x0) {
              plVar1 = plVar15 + 1;
              *plVar1 = *plVar1 + 1;
              LOAcquire();
              lVar6 = *plVar1;
              *plVar1 = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*plVar15 + 0x10))(plVar15);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
              }
            }
          }
LAB_031d0d2c:
          FUN_031d1444(&local_2f0,&local_1c0);
          plVar1 = local_2a8;
          plVar15 = local_180;
          if (local_2a8 != (long *)0x0) {
            LOAcquire();
            lVar6 = local_2a8[1];
            local_2a8[1] = lVar6 + -1;
            LORelease();
            if (lVar6 == 0) {
              (**(code **)(*local_2a8 + 0x10))(local_2a8);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
              plVar15 = local_180;
            }
          }
        }
        else {
          iVar10 = thunk_FUN_05e1d97c(4);
          if (iVar10 != 0) {
            FUN_0488143c(&local_288);
            pdVar2 = local_288;
            if (-1 < cStack_271) {
              pdVar2 = (dword *)&local_288;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar12 = 0;
              do {
                (&DAT_0a3dd350)[uVar12] =
                     (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
                uVar12 = uVar12 + 1;
              } while (uVar12 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3e2ee3 & 1) == 0) {
              DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
              DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
              DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
              DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
              DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
              DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
              DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
              DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
              DAT_0a3e2ee0 = 0x2928;
              DAT_0a3e2ee2 = 0;
              DAT_0a3e2ee3 = 1;
            }
            FUN_05e1d050(&local_260,4,pdVar2,&DAT_0a3dd350,0xa3e2ed8,0x1179,0,0);
            FUN_030f1f08(&local_2a0,plVar15);
            local_140 = local_2a0;
            if (-1 < cStack_289) {
              local_140 = (dword *)&local_2a0;
            }
            local_138 = 0;
            if ((DAT_0a3e35b9 & 1) == 0) {
              uVar12 = 0;
              do {
                uVar16 = *(undefined4 *)((long)&DAT_088c6f93 + uVar12);
                uVar5 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
                uVar17 = *(undefined4 *)((long)&DAT_088c6f7f + uVar12 % 0x14);
                *(uint *)((long)&DAT_0a3e3578 + uVar12) =
                     CONCAT13((char)((uint)uVar16 >> 0x18) + 0x69U ^ (byte)((uint)uVar17 >> 0x18),
                              CONCAT12((char)((uint)uVar16 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar17 >> 0x10),
                                       CONCAT11((char)(uVar5 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar17 >> 8),
                                                (char)uVar5 + 0x69U ^ (byte)uVar17)));
                uVar12 = uVar12 + 4;
              } while (uVar12 != 0x40);
              DAT_0a3e35b8 = 0;
              DAT_0a3e35b9 = 1;
            }
            local_e0 = 0;
            pppppppuStack_e8 = (undefined8 *******)0x0;
            local_f0 = &local_140;
            local_d0 = 0;
            uStack_d8 = 0;
            local_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            local_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            local_80 = 0;
            uStack_88 = 0;
            uStack_78 = 0;
            FUN_05e1d31c(&local_260,&DAT_0a3e3578,&local_f0);
            if (cStack_289 < '\0') {
              __ZdlPvm(local_2a0,CONCAT17(cStack_289,local_290) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_260);
            if (cStack_271 < '\0') {
              __ZdlPvm(local_288,CONCAT17(cStack_271,local_278) & 0x7fffffffffffffff);
            }
          }
          FUN_032261d4(&local_190);
          if ((int)local_1c0 == 0 && local_1c0._4_4_ == 0) goto LAB_031d0788;
          iVar10 = thunk_FUN_05e1d97c(4);
          if (iVar10 != 0) {
            FUN_0488143c(&local_288);
            pdVar2 = local_288;
            if (-1 < cStack_271) {
              pdVar2 = (dword *)&local_288;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar12 = 0;
              do {
                (&DAT_0a3dd350)[uVar12] =
                     (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
                uVar12 = uVar12 + 1;
              } while (uVar12 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3e2ee3 & 1) == 0) {
              DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
              DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
              DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
              DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
              DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
              DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
              DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
              DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
              DAT_0a3e2ee0 = 0x2928;
              DAT_0a3e2ee2 = 0;
              DAT_0a3e2ee3 = 1;
            }
            FUN_05e1d050(&local_260,4,pdVar2,&DAT_0a3dd350,0xa3e2ed8,0x117c,0,0);
            FUN_030f1f08(&local_2a0,plVar15);
            local_140 = local_2a0;
            if (-1 < cStack_289) {
              local_140 = (dword *)&local_2a0;
            }
            local_138 = 0;
            if ((DAT_0a3e35f1 & 1) == 0) {
              _DAT_0a3e35bc = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
              uRam000000000a3e35c4 = CONCAT44((int)ram0x087e2de8,(int)DAT_084e3ff8);
              _DAT_0a3e35cc = CONCAT44((int)DAT_08508320,(int)DAT_087e2df0);
              uRam000000000a3e35d4 = CONCAT44((int)DAT_0889c230,(int)DAT_084a66b0);
              _DAT_0a3e35dc = CONCAT44((int)DAT_088baff0,(int)DAT_088ae220);
              uRam000000000a3e35e4 = CONCAT44((int)DAT_0857ad38,(int)DAT_0858f908);
              DAT_0a3e35ec = (undefined4)ram0x08480938;
              DAT_0a3e35f0 = 0;
              DAT_0a3e35f1 = 1;
            }
            local_e0 = 0;
            pppppppuStack_e8 = (undefined8 *******)0x0;
            local_f0 = &local_140;
            local_d0 = 0;
            uStack_d8 = 0;
            local_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            local_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            local_80 = 0;
            uStack_88 = 0;
            uStack_78 = 0;
            FUN_05e1d31c(&local_260,&DAT_0a3e35bc,&local_f0);
            if (cStack_289 < '\0') {
              __ZdlPvm(local_2a0,CONCAT17(cStack_289,local_290) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_260);
            if (cStack_271 < '\0') {
              __ZdlPvm(local_288,CONCAT17(cStack_271,local_278) & 0x7fffffffffffffff);
            }
          }
          FUN_031d1444(&local_2f0,&local_1c0);
          plVar15 = local_180;
        }
        goto joined_r0x031d0d6c;
      }
    }
    else {
      FUN_030f3214(lVar7,plVar15,2);
      iVar10 = thunk_FUN_05e1d97c(2);
      if (iVar10 == 0) {
LAB_031cf994:
        bVar4 = *(byte *)(lVar6 + 0x18);
      }
      else {
        FUN_0488143c(&local_288);
        pdVar2 = local_288;
        if (-1 < cStack_271) {
          pdVar2 = (dword *)&local_288;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar12 = 0;
          do {
            (&DAT_0a3dd350)[uVar12] = (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf]
            ;
            uVar12 = uVar12 + 1;
          } while (uVar12 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3e2ee3 & 1) == 0) {
          DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a3e2ee0 = 0x2928;
          DAT_0a3e2ee2 = 0;
          DAT_0a3e2ee3 = 1;
        }
        FUN_05e1d050(&local_260,2,pdVar2,&DAT_0a3dd350,0xa3e2ed8,
                     "ndation.framework/Versions/C/Foundation",0,0);
        FUN_030f1f08(&local_2a0,plVar15);
        lVar6 = local_270;
        local_140 = local_2a0;
        if (-1 < cStack_289) {
          local_140 = (dword *)&local_2a0;
        }
        local_138 = 0;
        if (*(char *)(local_270 + 0x18) == '\x01') {
          local_190 = (undefined8 *******)&DAT_0a3e2ec4;
          if ((DAT_0a3e2ec9 & 1) == 0) {
            DAT_0a3e2ec4 = 0x7274;
            DAT_0a3e2ec6 = 0x75;
            puVar13 = &DAT_0a3e2ec8;
            puVar8 = &DAT_0a3e2ec7;
            puVar14 = &DAT_0a3e2ec9;
LAB_031cf8a4:
            *puVar8 = 0x65;
            *puVar13 = 0;
            *puVar14 = 1;
          }
        }
        else {
          local_190 = (undefined8 *******)&DAT_0a3e2ecc;
          if ((DAT_0a3e2ed2 & 1) == 0) {
            DAT_0a3e2ecc = (undefined4)DAT_0847fe48;
            puVar8 = &DAT_0a3e2ed0;
            puVar13 = &DAT_0a3e2ed1;
            puVar14 = &DAT_0a3e2ed2;
            goto LAB_031cf8a4;
          }
        }
        local_188 = (long *)((ulong)local_188 & 0xffffffffffffff00);
        if ((DAT_0a3e34fe & 1) == 0) {
          uVar12 = 0;
          do {
            uVar16 = *(undefined4 *)((long)&DAT_088c6e92 + uVar12);
            uVar5 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
            uVar17 = *(undefined4 *)((long)&DAT_088c6e7e + uVar12 % 0x14);
            *(uint *)((long)&DAT_0a3e34be + uVar12) =
                 CONCAT13((char)((uint)uVar16 >> 0x18) + 0x69U ^ (byte)((uint)uVar17 >> 0x18),
                          CONCAT12((char)((uint)uVar16 >> 0x10) + 0x69U ^
                                   (byte)((uint)uVar17 >> 0x10),
                                   CONCAT11((char)(uVar5 >> 0x10) + 0x69U ^
                                            (byte)((uint)uVar17 >> 8),
                                            (char)uVar5 + 0x69U ^ (byte)uVar17)));
            uVar12 = uVar12 + 4;
          } while (uVar12 != 0x40);
          DAT_0a3e34fe = 1;
        }
        local_f0 = &local_140;
        pppppppuStack_e8 = &local_190;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        FUN_05e1d31c(&local_260,&DAT_0a3e34be,&local_f0);
        if (cStack_289 < '\0') {
          __ZdlPvm(local_2a0,CONCAT17(cStack_289,local_290) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_260);
        if (-1 < cStack_271) goto LAB_031cf994;
        __ZdlPvm(local_288,CONCAT17(cStack_271,local_278) & 0x7fffffffffffffff);
        bVar4 = *(byte *)(lVar6 + 0x18);
      }
      if ((bVar4 & 1) == 0) {
        FUN_03189b24(&local_260,param_2,&local_270);
        local_1c0 = local_260;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  ((ulong)&local_1c0 | 8,&local_258);
        plVar1 = local_198;
        if (local_238 != (long *)0x0) {
          local_238[1] = local_238[1] + 1;
        }
        local_1a0 = local_240;
        local_198 = local_238;
        if (plVar1 != (long *)0x0) {
          LOAcquire();
          lVar6 = plVar1[1];
          plVar1[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*plVar1 + 0x10))(plVar1);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
          }
        }
        plVar1 = local_238;
        if (local_238 != (long *)0x0) {
          LOAcquire();
          lVar6 = local_238[1];
          local_238[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*local_238 + 0x10))(local_238);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
          }
        }
        if (cStack_241 < '\0') {
          __ZdlPvm(local_258,CONCAT17(cStack_241,local_248) & 0x7fffffffffffffff);
        }
        *(undefined1 *)(local_270 + 0x18) = 1;
      }
      local_2a0 = (dword *)plVar15[3];
      local_298 = (long *)plVar15[4];
      if (local_298 != (long *)0x0) {
        local_298[1] = local_298[1] + 1;
      }
      if ((local_2a0 == (dword *)0x0) || (local_2a0[0x3d] == 0)) {
        iVar10 = thunk_FUN_05e1d97c(4);
        if (iVar10 != 0) {
          FUN_0488143c(&local_190);
          pppppppuVar9 = local_190;
          if (-1 < (long)local_180) {
            pppppppuVar9 = &local_190;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar12 = 0;
            do {
              (&DAT_0a3dd350)[uVar12] =
                   (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
              uVar12 = uVar12 + 1;
            } while (uVar12 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3e2ee3 & 1) == 0) {
            DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a3e2ee0 = 0x2928;
            DAT_0a3e2ee2 = 0;
            DAT_0a3e2ee3 = 1;
          }
          FUN_05e1d050(&local_260,4,pppppppuVar9,&DAT_0a3dd350,0xa3e2ed8,
                       ".framework/Versions/C/Foundation",0,0);
          FUN_030f1f08(&local_288,plVar15);
          local_140 = local_288;
          if (-1 < cStack_271) {
            local_140 = (dword *)&local_288;
          }
          local_138 = 0;
          if ((DAT_0a3e3529 & 1) == 0) {
            _DAT_0a3e3500 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
            uRam000000000a3e3508 = CONCAT44((int)DAT_08485ea0,(int)DAT_084e3ff8);
            _DAT_0a3e3510 = CONCAT44((int)DAT_0854aed8,(int)DAT_084d8920);
            uRam000000000a3e3518 = CONCAT44((int)DAT_088769a8,(int)DAT_0855b808);
            DAT_0a3e3520 = CONCAT44((int)ram0x08480938,(int)DAT_088bafe0);
            DAT_0a3e3528 = 0;
            DAT_0a3e3529 = 1;
          }
          local_e0 = 0;
          pppppppuStack_e8 = (undefined8 *******)0x0;
          local_f0 = &local_140;
          local_d0 = 0;
          uStack_d8 = 0;
          local_c0 = 0;
          uStack_c8 = 0;
          local_b0 = 0;
          uStack_b8 = 0;
          local_a0 = 0;
          uStack_a8 = 0;
          local_90 = 0;
          uStack_98 = 0;
          local_80 = 0;
          uStack_88 = 0;
          uStack_78 = 0;
          FUN_05e1d31c(&local_260,&DAT_0a3e3500,&local_f0);
          if (cStack_271 < '\0') {
            __ZdlPvm(local_288,CONCAT17(cStack_271,local_278) & 0x7fffffffffffffff);
          }
          thunk_FUN_05e1d0bc(&local_260);
          if ((long)local_180 < 0) {
            __ZdlPvm(local_190,(ulong)local_180 & 0x7fffffffffffffff);
          }
        }
        if ((int)local_1c0 == 0 && local_1c0._4_4_ == 0) {
          FUN_030f6640(&local_260,1,1);
          puVar13 = local_1a0;
          FUN_030f67ac(local_1a0,&local_260);
          *(undefined8 *)(puVar13 + 0x48) = local_218;
          local_1c0 = (dword *)((ulong)local_1c0 & 0xffffffff);
          if ((local_220 & 1) == 0) {
            local_1c0 = &MACH_HEADER.cputype;
          }
          else {
            if (cStack_221 < '\0') {
              __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
            }
            if (cStack_249 < '\0') {
              __ZdlPvm(local_260,CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
            }
            local_1c0 = (dword *)CONCAT44(local_1c0._4_4_,4);
            if (local_1c0._4_4_ != 0) goto LAB_031cfe18;
          }
          local_1c0 = (dword *)CONCAT44(400,(int)local_1c0);
        }
      }
LAB_031cfe18:
      FUN_031d1444(&local_2f0,&local_1c0);
      plVar15 = local_298;
joined_r0x031d0d6c:
      if (plVar15 != (long *)0x0) {
LAB_031d0d98:
        LOAcquire();
        lVar6 = plVar15[1];
        plVar15[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*plVar15 + 0x10))(plVar15);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
        }
      }
    }
LAB_031d0dc0:
    plVar15 = local_268;
    if (local_268 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_268[1];
      local_268[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_268 + 0x10))(local_268);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
      }
    }
    goto LAB_031d0df0;
  }
  local_1d0 = (long *)0x0;
  local_1c8 = (long *)0x0;
  iVar10 = thunk_FUN_05e1d97c(4);
  if (iVar10 != 0) {
    FUN_0488143c(&local_140);
    pdVar2 = local_140;
    if (-1 < cStack_129) {
      pdVar2 = (dword *)&local_140;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar12 = 0;
      do {
        (&DAT_0a3dd350)[uVar12] = (&DAT_088bce97)[uVar12] + 0x8a ^ (&DAT_088bce87)[uVar12 & 0xf];
        uVar12 = uVar12 + 1;
      } while (uVar12 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3e2ee3 & 1) == 0) {
      DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a3e2ee0 = 0x2928;
      DAT_0a3e2ee2 = 0;
      DAT_0a3e2ee3 = 1;
    }
    FUN_05e1d050(&local_260,4,pdVar2,&DAT_0a3dd350,0xa3e2ed8,
                 "/Frameworks/Foundation.framework/Versions/C/Foundation",0,0);
    if ((DAT_0a3e34bd & 1) == 0) {
      _DAT_0a3e34a4 = CONCAT44((int)DAT_08557bc8,(int)DAT_08480908);
      uRam000000000a3e34ac = CONCAT44((int)ram0x08491928,(int)DAT_085e8930);
      DAT_0a3e34b4 = CONCAT44((int)DAT_08483058,(int)DAT_08483050);
      DAT_0a3e34bc = 0;
      DAT_0a3e34bd = 1;
    }
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    pppppppuStack_e8 = (undefined8 *******)0x0;
    local_f0 = (dword **)0x0;
    uStack_d8 = 0;
    local_e0 = 0;
    FUN_05e1d31c(&local_260,&DAT_0a3e34a4,&local_f0);
    thunk_FUN_05e1d0bc(&local_260);
    if (cStack_129 < '\0') {
      __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
    }
  }
  FUN_030f6640(&local_260,1,1);
  puVar13 = local_1a0;
  FUN_030f67ac(local_1a0,&local_260);
  *(undefined8 *)(puVar13 + 0x48) = local_218;
  local_1c0 = (dword *)((ulong)local_1c0 & 0xffffffff);
  if ((local_220 & 1) == 0) {
    local_1c0 = &MACH_HEADER.cputype;
LAB_031cf85c:
    local_1c0 = (dword *)CONCAT44(400,(int)local_1c0);
  }
  else {
    if (cStack_221 < '\0') {
      __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
    }
    if (cStack_249 < '\0') {
      __ZdlPvm(local_260,CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
    }
    local_1c0 = (dword *)CONCAT44(local_1c0._4_4_,4);
    if (local_1c0._4_4_ == 0) goto LAB_031cf85c;
  }
  FUN_031d1444(&local_2f0,&local_1c0);
LAB_031d0df0:
  plVar1 = local_1c8;
  plVar15 = local_198;
  if (local_1c8 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_1c8[1];
    local_1c8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_1c8 + 0x10))(local_1c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      plVar15 = local_198;
    }
  }
  local_198 = plVar15;
  if (plVar15 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar15[1];
    plVar15[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar15 + 0x10))(plVar15);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
    }
  }
  if ((long)puStack_1a8 < 0) {
    __ZdlPvm(pdStack_1b8,(ulong)puStack_1a8 & 0x7fffffffffffffff);
  }
  plVar15 = local_2e8;
  if (local_2e8 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_2e8[1];
    local_2e8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_2e8 + 0x10))(local_2e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
    }
  }
  plVar15 = local_2d8;
  *param_1 = local_2e0;
  param_1[1] = local_2d8;
  if ((local_2d8 != (long *)0x0) && (local_2d8[1] = local_2d8[1] + 1, local_2d8 != (long *)0x0)) {
    LOAcquire();
    lVar6 = local_2d8[1];
    local_2d8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_2d8 + 0x10))(local_2d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
    }
  }
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar3[1];
    plVar3[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


