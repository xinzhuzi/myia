// Ghidra inferred pseudocode; requested=0x2857158
// entry=02857158 end=02857b8b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02857158(long param_1,undefined8 param_2,long param_3)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  char cVar3;
  uint3 uVar4;
  undefined1 *puVar5;
  long lVar6;
  int iVar7;
  long *plVar8;
  undefined1 *puVar9;
  ulong uVar10;
  undefined1 *puVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  undefined1 *local_280;
  long *local_278;
  undefined8 **local_270 [2];
  undefined7 local_260;
  char cStack_259;
  undefined1 local_258;
  undefined7 uStack_257;
  long *local_250;
  undefined7 local_248;
  char cStack_241;
  undefined8 **local_1c8;
  ulong local_1c0;
  ulong local_1b8;
  long local_178;
  undefined1 local_170;
  long local_128;
  undefined1 local_120;
  long *local_d8;
  long *local_d0;
  undefined8 **local_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(local_270);
    pppuVar1 = (undefined8 ***)local_270[0];
    if (-1 < cStack_259) {
      pppuVar1 = local_270;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39e179 & 1) == 0) {
      DAT_0a39e170._0_1_ = s_SendRudpRudp_088051a0[0];
      DAT_0a39e170._1_1_ = s_SendRudpRudp_088051a0[1];
      DAT_0a39e170._2_1_ = s_SendRudpRudp_088051a0[2];
      DAT_0a39e170._3_1_ = s_SendRudpRudp_088051a0[3];
      DAT_0a39e170._4_1_ = s_SendRudpRudp_088051a0[4];
      DAT_0a39e170._5_1_ = s_SendRudpRudp_088051a0[5];
      DAT_0a39e170._6_1_ = s_SendRudpRudp_088051a0[6];
      DAT_0a39e170._7_1_ = s_SendRudpRudp_088051a0[7];
      DAT_0a39e178 = 0;
      DAT_0a39e179 = 1;
    }
    FUN_05e1d050(&local_258,2,pppuVar1,&DAT_0a39dff8,&DAT_0a39e170,0x10e,0,0);
    plVar8 = *(long **)(param_3 + 0x10);
    plVar2 = *(long **)(param_3 + 0x18);
    local_128 = *plVar8;
    if (-1 < *(char *)((long)plVar8 + 0x17)) {
      local_128 = (long)plVar8;
    }
    local_120 = 0;
    local_178 = *plVar2;
    if (-1 < *(char *)((long)plVar2 + 0x17)) {
      local_178 = (long)plVar2;
    }
    local_170 = 0;
    cVar3 = *(char *)(*(long *)(param_3 + 0x30) + 0x17);
    if (cVar3 < '\0') {
      if (*(long *)(*(long *)(param_3 + 0x30) + 8) == 0) goto LAB_02857304;
LAB_028572c4:
      local_1c8 = (undefined8 **)&DAT_0a39e368;
      if ((DAT_0a39e36d & 1) == 0) {
        DAT_0a39e368 = 0x7274;
        DAT_0a39e36a = 0x75;
        puVar9 = &DAT_0a39e36c;
        puVar5 = &DAT_0a39e36b;
        puVar11 = &DAT_0a39e36d;
LAB_02857334:
        *puVar5 = 0x65;
        *puVar9 = 0;
        *puVar11 = 1;
      }
    }
    else {
      if (cVar3 != '\0') goto LAB_028572c4;
LAB_02857304:
      local_1c8 = (undefined8 **)&DAT_0a39e370;
      if ((DAT_0a39e376 & 1) == 0) {
        DAT_0a39e370 = (undefined4)DAT_0847fe48;
        puVar5 = &DAT_0a39e374;
        puVar9 = &DAT_0a39e375;
        puVar11 = &DAT_0a39e376;
        goto LAB_02857334;
      }
    }
    local_1c0 = local_1c0 & 0xffffffffffffff00;
    if ((DAT_0a39e1a4 & 1) == 0) {
      _DAT_0a39e17c = CONCAT44((int)ram0x088051a8,(int)DAT_08546648);
      uRam000000000a39e184 = CONCAT44((int)DAT_085e35b0,(int)ram0x084cd9a0);
      _DAT_0a39e18c = CONCAT44((int)ram0x08489fc8,(int)DAT_08502a58);
      uRam000000000a39e194 = CONCAT44((int)DAT_084925f8,(int)DAT_08502a58);
      DAT_0a39e19c = CONCAT44((int)DAT_084ec370,(int)DAT_087e32a8);
      DAT_0a39e1a4 = 1;
    }
    local_d8 = &local_128;
    local_d0 = &local_178;
    local_c8 = &local_1c8;
    uStack_b8 = 0;
    uStack_c0 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    local_60 = 0;
    FUN_05e1d31c(&local_258,&DAT_0a39e17c,&local_d8);
    thunk_FUN_05e1d0bc(&local_258);
    if (cStack_259 < '\0') {
      __ZdlPvm(local_270[0],CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff);
    }
  }
  if (*(char *)(param_1 + 0x60) == '\x01') {
    plVar8 = (long *)FUN_04669774();
    iVar7 = (**(code **)(*plVar8 + 0x70))();
    if (iVar7 == 0) goto LAB_02857470;
    FUN_04669774();
    iVar7 = FUN_04670f7c();
    if (iVar7 != 0) goto LAB_02857470;
    local_1c8 = (undefined8 ***)0x0;
    local_1c0 = 0;
    local_1b8 = 0;
    uVar10 = FUN_05ab3f60(param_3,&local_1c8);
    if ((uVar10 & 1) == 0) {
      iVar7 = thunk_FUN_05e1d97c(3);
      if (iVar7 != 0) {
        FUN_0488143c(local_270);
        pppuVar1 = (undefined8 ***)local_270[0];
        if (-1 < cStack_259) {
          pppuVar1 = local_270;
        }
        if ((DAT_0a39e011 & 1) == 0) {
          _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
          uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
          DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
          DAT_0a39e010 = 0;
          DAT_0a39e011 = 1;
        }
        if ((DAT_0a39e179 & 1) == 0) {
          DAT_0a39e170._0_1_ = s_SendRudpRudp_088051a0[0];
          DAT_0a39e170._1_1_ = s_SendRudpRudp_088051a0[1];
          DAT_0a39e170._2_1_ = s_SendRudpRudp_088051a0[2];
          DAT_0a39e170._3_1_ = s_SendRudpRudp_088051a0[3];
          DAT_0a39e170._4_1_ = s_SendRudpRudp_088051a0[4];
          DAT_0a39e170._5_1_ = s_SendRudpRudp_088051a0[5];
          DAT_0a39e170._6_1_ = s_SendRudpRudp_088051a0[6];
          DAT_0a39e170._7_1_ = s_SendRudpRudp_088051a0[7];
          DAT_0a39e178 = 0;
          DAT_0a39e179 = 1;
        }
        FUN_05e1d050(&local_258,3,pppuVar1,&DAT_0a39dff8,&DAT_0a39e170,0x119,0,0);
        plVar8 = *(long **)(param_3 + 0x10);
        plVar2 = *(long **)(param_3 + 0x18);
        local_128 = *plVar8;
        if (-1 < *(char *)((long)plVar8 + 0x17)) {
          local_128 = (long)plVar8;
        }
        local_120 = 0;
        local_178 = *plVar2;
        if (-1 < *(char *)((long)plVar2 + 0x17)) {
          local_178 = (long)plVar2;
        }
        local_170 = 0;
        if ((DAT_0a39e222 & 1) == 0) {
          _DAT_0a39e1f4 = CONCAT44((int)ram0x088051a8,(int)DAT_08546648);
          uRam000000000a39e1fc = CONCAT44((int)DAT_0855f188,(int)DAT_08558ee8);
          _DAT_0a39e204 = CONCAT44((int)DAT_084caf50,(int)DAT_0852e7d0);
          uRam000000000a39e20c = CONCAT44((int)DAT_0849d680,(int)DAT_0852a910);
          DAT_0a39e214 = CONCAT44((int)DAT_087e3208,(int)DAT_08593ff0);
          DAT_0a39e21c = (undefined4)DAT_085029a0;
          DAT_0a39e220 = 0x5f;
          DAT_0a39e222 = 1;
        }
        local_d8 = &local_128;
        local_d0 = &local_178;
        uStack_c0 = 0;
        local_c8 = (undefined8 ***)0x0;
        local_b0 = 0;
        uStack_b8 = 0;
        local_a0 = 0;
        uStack_a8 = 0;
        local_90 = 0;
        uStack_98 = 0;
        local_80 = 0;
        uStack_88 = 0;
        local_70 = 0;
        uStack_78 = 0;
        local_60 = 0;
        uStack_68 = 0;
        FUN_05e1d31c(&local_258,&DAT_0a39e1f4,&local_d8);
        thunk_FUN_05e1d0bc(&local_258);
        if (cStack_259 < '\0') {
          __ZdlPvm(local_270[0],CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff);
        }
      }
    }
    else {
      local_280 = &SUB_aaaaaaaaaaaaaaaa;
      local_278 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_0466aca8(&local_d8);
      FUN_01205740(&local_258,local_d8);
      FUN_02662244(&local_280,CONCAT71(uStack_257,local_258));
      if (local_250 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_250[1];
        local_250[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*local_250 + 0x10))(local_250);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_250);
        }
      }
      plVar8 = local_d0;
      if (local_d0 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_d0[1];
        local_d0[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      if (local_280 == (undefined1 *)0x0) {
        iVar7 = thunk_FUN_05e1d97c(3);
        if (iVar7 != 0) {
          FUN_0488143c(local_270);
          pppuVar1 = (undefined8 ***)local_270[0];
          if (-1 < cStack_259) {
            pppuVar1 = local_270;
          }
          if ((DAT_0a39e011 & 1) == 0) {
            _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
            uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
            DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
            DAT_0a39e010 = 0;
            DAT_0a39e011 = 1;
          }
          if ((DAT_0a39e179 & 1) == 0) {
            DAT_0a39e170._0_1_ = s_SendRudpRudp_088051a0[0];
            DAT_0a39e170._1_1_ = s_SendRudpRudp_088051a0[1];
            DAT_0a39e170._2_1_ = s_SendRudpRudp_088051a0[2];
            DAT_0a39e170._3_1_ = s_SendRudpRudp_088051a0[3];
            DAT_0a39e170._4_1_ = s_SendRudpRudp_088051a0[4];
            DAT_0a39e170._5_1_ = s_SendRudpRudp_088051a0[5];
            DAT_0a39e170._6_1_ = s_SendRudpRudp_088051a0[6];
            DAT_0a39e170._7_1_ = s_SendRudpRudp_088051a0[7];
            DAT_0a39e178 = 0;
            DAT_0a39e179 = 1;
          }
          FUN_05e1d050(&local_258,3,pppuVar1,&DAT_0a39dff8,&DAT_0a39e170,0x11f,0,0);
          plVar8 = *(long **)(param_3 + 0x10);
          plVar2 = *(long **)(param_3 + 0x18);
          local_128 = *plVar8;
          if (-1 < *(char *)((long)plVar8 + 0x17)) {
            local_128 = (long)plVar8;
          }
          local_120 = 0;
          local_178 = *plVar2;
          if (-1 < *(char *)((long)plVar2 + 0x17)) {
            local_178 = (long)plVar2;
          }
          local_170 = 0;
          if ((DAT_0a39e26c & 1) == 0) {
            uVar10 = 0;
            do {
              uVar12 = *(undefined4 *)((long)&DAT_08805c12 + uVar10);
              uVar4 = CONCAT12((char)((uint)uVar12 >> 8),(short)uVar12) & 0xff00ff;
              uVar13 = *(undefined4 *)((long)&DAT_08805bfe + uVar10 % 0x14);
              *(uint *)((long)&DAT_0a39e223 + uVar10) =
                   CONCAT13((char)((uint)uVar12 >> 0x18) + 0x8aU ^ (byte)((uint)uVar13 >> 0x18),
                            CONCAT12((char)((uint)uVar12 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar13 >> 0x10),
                                     CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar13 >> 8),
                                              (char)uVar4 + 0x8aU ^ (byte)uVar13)));
              uVar10 = uVar10 + 4;
            } while (uVar10 != 0x48);
            DAT_0a39e26b = 0;
            DAT_0a39e26c = 1;
          }
          local_d8 = &local_128;
          local_d0 = &local_178;
          uStack_c0 = 0;
          local_c8 = (undefined8 ***)0x0;
          local_b0 = 0;
          uStack_b8 = 0;
          local_a0 = 0;
          uStack_a8 = 0;
          local_90 = 0;
          uStack_98 = 0;
          local_80 = 0;
          uStack_88 = 0;
          local_70 = 0;
          uStack_78 = 0;
          local_60 = 0;
          uStack_68 = 0;
          FUN_05e1d31c(&local_258,&DAT_0a39e223,&local_d8);
          thunk_FUN_05e1d0bc(&local_258);
          if (cStack_259 < '\0') {
            uVar10 = CONCAT17(cStack_259,local_260);
            goto LAB_02857b4c;
          }
        }
      }
      else {
        cStack_241 = '\0';
        local_258 = 0;
        FUN_0265e9b8(local_280,param_2,0x3ed,&local_1c8,&local_258,0);
        if (cStack_241 < '\0') {
          local_270[0] = (undefined8 **)CONCAT71(uStack_257,local_258);
          uVar10 = CONCAT17(cStack_241,local_248);
LAB_02857b4c:
          __ZdlPvm(local_270[0],uVar10 & 0x7fffffffffffffff);
        }
      }
      plVar8 = local_278;
      if (local_278 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_278[1];
        local_278[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*local_278 + 0x10))(local_278);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
    }
  }
  else {
LAB_02857470:
    iVar7 = thunk_FUN_05e1d97c(3);
    if (iVar7 == 0) goto LAB_02857654;
    FUN_0488143c(&local_1c8);
    pppuVar1 = (undefined8 ***)local_1c8;
    if (-1 < (long)local_1b8) {
      pppuVar1 = &local_1c8;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39e179 & 1) == 0) {
      DAT_0a39e170._0_1_ = s_SendRudpRudp_088051a0[0];
      DAT_0a39e170._1_1_ = s_SendRudpRudp_088051a0[1];
      DAT_0a39e170._2_1_ = s_SendRudpRudp_088051a0[2];
      DAT_0a39e170._3_1_ = s_SendRudpRudp_088051a0[3];
      DAT_0a39e170._4_1_ = s_SendRudpRudp_088051a0[4];
      DAT_0a39e170._5_1_ = s_SendRudpRudp_088051a0[5];
      DAT_0a39e170._6_1_ = s_SendRudpRudp_088051a0[6];
      DAT_0a39e170._7_1_ = s_SendRudpRudp_088051a0[7];
      DAT_0a39e178 = 0;
      DAT_0a39e179 = 1;
    }
    FUN_05e1d050(&local_258,3,pppuVar1,&DAT_0a39dff8,&DAT_0a39e170,0x113,0,0);
    plVar8 = *(long **)(param_3 + 0x10);
    plVar2 = *(long **)(param_3 + 0x18);
    local_128 = *plVar8;
    if (-1 < *(char *)((long)plVar8 + 0x17)) {
      local_128 = (long)plVar8;
    }
    local_120 = 0;
    local_178 = *plVar2;
    if (-1 < *(char *)((long)plVar2 + 0x17)) {
      local_178 = (long)plVar2;
    }
    local_170 = 0;
    if ((DAT_0a39e1f2 & 1) == 0) {
      uVar10 = 0;
      do {
        uVar12 = *(undefined4 *)((long)&DAT_08805b6f + uVar10);
        uVar4 = CONCAT12((char)((uint)uVar12 >> 8),(short)uVar12) & 0xff00ff;
        uVar13 = *(undefined4 *)((long)&DAT_08805b5b + uVar10 % 0x14);
        *(uint *)((long)&DAT_0a39e1a5 + uVar10) =
             CONCAT13((char)((uint)uVar12 >> 0x18) + 0x8aU ^ (byte)((uint)uVar13 >> 0x18),
                      CONCAT12((char)((uint)uVar12 >> 0x10) + 0x8aU ^ (byte)((uint)uVar13 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar13 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar13)));
        uVar10 = uVar10 + 4;
      } while (uVar10 != 0x4c);
      DAT_0a39e1f1 = 0;
      DAT_0a39e1f2 = 1;
    }
    local_d8 = &local_128;
    local_d0 = &local_178;
    uStack_c0 = 0;
    local_c8 = (undefined8 ***)0x0;
    local_b0 = 0;
    uStack_b8 = 0;
    local_a0 = 0;
    uStack_a8 = 0;
    local_90 = 0;
    uStack_98 = 0;
    local_80 = 0;
    uStack_88 = 0;
    local_70 = 0;
    uStack_78 = 0;
    local_60 = 0;
    uStack_68 = 0;
    FUN_05e1d31c(&local_258,&DAT_0a39e1a5,&local_d8);
    thunk_FUN_05e1d0bc(&local_258);
  }
  if ((long)local_1b8 < 0) {
    __ZdlPvm(local_1c8,local_1b8 & 0x7fffffffffffffff);
  }
LAB_02857654:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


