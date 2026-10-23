// Ghidra inferred pseudocode; requested=0x31cbd88
// entry=031cbd88 end=031ccaff

/* WARNING: Removing unreachable block (ram,0x031cc900) */
/* WARNING: Removing unreachable block (ram,0x031cc910) */
/* WARNING: Removing unreachable block (ram,0x031cc930) */
/* WARNING: Removing unreachable block (ram,0x031cc940) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_031cbd88(long param_1,long *param_2)

{
  undefined8 ****ppppuVar1;
  undefined8 ***pppuVar2;
  undefined8 ***pppuVar3;
  long *plVar4;
  int iVar5;
  long lVar6;
  long *plVar7;
  code *pcVar8;
  ulong uVar9;
  long *plVar10;
  long local_288;
  long lStack_280;
  ulong local_278;
  long local_270;
  long *plStack_268;
  undefined8 ***local_260 [2];
  undefined7 local_250;
  char cStack_249;
  undefined8 ***local_248;
  long *local_240;
  undefined7 local_238;
  char cStack_231;
  long local_230;
  long *local_228;
  undefined1 auStack_220 [144];
  long local_190;
  long *local_188;
  long alStack_180 [3];
  long *local_168;
  long alStack_160 [3];
  long *local_148;
  undefined8 ***local_140;
  undefined1 local_138;
  undefined7 uStack_137;
  undefined7 local_130;
  char cStack_129;
  undefined8 ***local_f0;
  long *plStack_e8;
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
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar6 = FUN_03221ac0(*(long *)(param_1 + 0xb20) + 0x88);
  if (lVar6 == 0) goto LAB_031ccac4;
  local_190 = 0;
  local_188 = (long *)0x0;
  plVar4 = *(long **)(lVar6 + 0x28);
  if (plVar4 == *(long **)(lVar6 + 0x30)) {
    iVar5 = thunk_FUN_05e1d97c(2);
    if (iVar5 != 0) {
      FUN_0488143c(&local_140);
      ppppuVar1 = (undefined8 ****)local_140;
      if (-1 < cStack_129) {
        ppppuVar1 = &local_140;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar9 = 0;
        do {
          (&DAT_0a3dd350)[uVar9] = (&DAT_088bce97)[uVar9] + 0x8a ^ (&DAT_088bce87)[uVar9 & 0xf];
          uVar9 = uVar9 + 1;
        } while (uVar9 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e0699 & 1) == 0) {
        _DAT_0a3e067c = CONCAT44((int)DAT_088baf38,(int)DAT_08482fd0);
        uRam000000000a3e0684 = CONCAT44((int)DAT_088baf48,(int)DAT_088baf40);
        DAT_0a3e068c = CONCAT44((int)DAT_088baf58,(int)DAT_088baf50);
        DAT_0a3e0694 = (undefined4)ram0x0848d900;
        DAT_0a3e0698 = 0;
        DAT_0a3e0699 = 1;
      }
      FUN_05e1d050(auStack_220,2,ppppuVar1,&DAT_0a3dd350,&DAT_0a3e067c,
                   "ext.framework/Versions/A/CoreText",0,0);
      if ((DAT_0a3e06bf & 1) == 0) {
        _DAT_0a3e069c = CONCAT44((int)ram0x08487528,(int)DAT_08610c90);
        uRam000000000a3e06a4 = CONCAT44((int)DAT_08558ee8,(int)DAT_08482350);
        _DAT_0a3e06ac = CONCAT44((int)DAT_0848d908,(int)DAT_085450c0);
        uRam000000000a3e06b4 = CONCAT44((int)DAT_084ca3d0,(int)DAT_084d1058);
        DAT_0a3e06bc = 0x7974;
        DAT_0a3e06be = 0;
        DAT_0a3e06bf = 1;
      }
      local_88 = 0;
      uStack_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_c8 = 0;
      uStack_d0 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      plStack_e8 = (long *)0x0;
      local_f0 = (undefined8 ****)0x0;
      local_d8 = 0;
      uStack_e0 = 0;
      FUN_05e1d31c(auStack_220,&DAT_0a3e069c,&local_f0);
      thunk_FUN_05e1d0bc(auStack_220);
      if (cStack_129 < '\0') {
        __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
      }
    }
  }
  else {
    lVar6 = *plVar4;
    plVar10 = (long *)plVar4[1];
    if (plVar10 != (long *)0x0) {
      plVar4 = (long *)plVar10[1];
      plVar10[1] = (long)plVar4 + 1;
    }
    local_230 = lVar6;
    local_228 = plVar10;
    iVar5 = FUN_030f320c(plVar4,lVar6);
    if (iVar5 == 6) {
      if (plVar10 != (long *)0x0) {
        plVar10[1] = plVar10[1] + 1;
      }
      local_190 = lVar6;
      local_188 = plVar10;
      iVar5 = thunk_FUN_05e1d97c(2);
      if (iVar5 != 0) {
        FUN_0488143c(&local_248);
        ppppuVar1 = (undefined8 ****)local_248;
        if (-1 < cStack_231) {
          ppppuVar1 = &local_248;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar9 = 0;
          do {
            (&DAT_0a3dd350)[uVar9] = (&DAT_088bce97)[uVar9] + 0x8a ^ (&DAT_088bce87)[uVar9 & 0xf];
            uVar9 = uVar9 + 1;
          } while (uVar9 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3e0699 & 1) == 0) {
          _DAT_0a3e067c = CONCAT44((int)DAT_088baf38,(int)DAT_08482fd0);
          uRam000000000a3e0684 = CONCAT44((int)DAT_088baf48,(int)DAT_088baf40);
          DAT_0a3e068c = CONCAT44((int)DAT_088baf58,(int)DAT_088baf50);
          DAT_0a3e0694 = (undefined4)ram0x0848d900;
          DAT_0a3e0698 = 0;
          DAT_0a3e0699 = 1;
        }
        FUN_05e1d050(auStack_220,2,ppppuVar1,&DAT_0a3dd350,&DAT_0a3e067c,
                     "mework/Versions/A/CoreText",0,0);
        lVar6 = local_190;
        FUN_030f1f08(local_260,local_190);
        local_140 = local_260[0];
        if (-1 < cStack_249) {
          local_140 = local_260;
        }
        local_138 = 0;
        if ((DAT_0a3e06f4 & 1) == 0) {
          _DAT_0a3e06c0 = CONCAT44((int)DAT_08480af8,(int)DAT_0848be60);
          uRam000000000a3e06c8 = CONCAT44((int)DAT_0882a318,(int)DAT_088ba9f0);
          _DAT_0a3e06d0 = CONCAT44((int)DAT_08485ed0,(int)DAT_088baf60);
          uRam000000000a3e06d8 = CONCAT44((int)DAT_08482350,(int)ram0x08487528);
          _DAT_0a3e06e0 = CONCAT44((int)DAT_088baf68,(int)DAT_08558ee8);
          uRam000000000a3e06e8 = CONCAT44((int)DAT_0849a618,(int)DAT_084cae10);
          DAT_0a3e06f0 = (undefined4)DAT_084d1ec0;
          DAT_0a3e06f4 = 1;
        }
        uStack_e0 = 0;
        plStack_e8 = (long *)0x0;
        local_f0 = &local_140;
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
        FUN_05e1d31c(auStack_220,&DAT_0a3e06c0,&local_f0);
        if (cStack_249 < '\0') {
          __ZdlPvm(local_260[0],CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(auStack_220);
        if (cStack_231 < '\0') {
          __ZdlPvm(local_248,CONCAT17(cStack_231,local_238) & 0x7fffffffffffffff);
        }
      }
      plVar4 = local_188;
      if (lVar6 == 0) goto LAB_031cc258;
      local_248 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
      local_240 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      plStack_268 = local_188;
      if (local_188 != (long *)0x0) {
        local_188[1] = local_188[1] + 1;
      }
      local_270 = lVar6;
      FUN_0318d680(&local_248,param_1,&local_270);
      if (plVar4 != (long *)0x0) {
        LOAcquire();
        lVar6 = plVar4[1];
        plVar4[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*plVar4 + 0x10))(plVar4);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
        }
      }
      lVar6 = local_190;
      if ((undefined8 ****)local_248 == (undefined8 ****)0x0) {
        iVar5 = thunk_FUN_05e1d97c(2);
        if (iVar5 != 0) {
          FUN_0488143c(&local_140);
          ppppuVar1 = (undefined8 ****)local_140;
          if (-1 < cStack_129) {
            ppppuVar1 = &local_140;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3dd350)[uVar9] = (&DAT_088bce97)[uVar9] + 0x8a ^ (&DAT_088bce87)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3e0699 & 1) == 0) {
            _DAT_0a3e067c = CONCAT44((int)DAT_088baf38,(int)DAT_08482fd0);
            uRam000000000a3e0684 = CONCAT44((int)DAT_088baf48,(int)DAT_088baf40);
            DAT_0a3e068c = CONCAT44((int)DAT_088baf58,(int)DAT_088baf50);
            DAT_0a3e0694 = (undefined4)ram0x0848d900;
            DAT_0a3e0698 = 0;
            DAT_0a3e0699 = 1;
          }
          FUN_05e1d050(auStack_220,2,ppppuVar1,&DAT_0a3dd350,&DAT_0a3e067c,"sions/A/CoreText",0,0);
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
          local_88 = 0;
          uStack_90 = 0;
          local_78 = 0;
          uStack_80 = 0;
          local_a8 = 0;
          uStack_b0 = 0;
          local_98 = 0;
          uStack_a0 = 0;
          local_c8 = 0;
          uStack_d0 = 0;
          local_b8 = 0;
          uStack_c0 = 0;
          plStack_e8 = (long *)0x0;
          local_f0 = (undefined8 ****)0x0;
          local_d8 = 0;
          uStack_e0 = 0;
          FUN_05e1d31c(auStack_220,&DAT_0a3e0720,&local_f0);
          thunk_FUN_05e1d0bc(auStack_220);
          if (cStack_129 < '\0') {
            __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
          }
        }
      }
      else {
        FUN_030f3214(local_190,7);
        local_f0 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
        plStack_e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_04669774();
        FUN_0466ad74(&local_140);
        pppuVar3 = local_140;
        if ((DAT_0a3e0699 & 1) == 0) {
          _DAT_0a3e067c = CONCAT44((int)DAT_088baf38,(int)DAT_08482fd0);
          uRam000000000a3e0684 = CONCAT44((int)DAT_088baf48,(int)DAT_088baf40);
          DAT_0a3e068c = CONCAT44((int)DAT_088baf58,(int)DAT_088baf50);
          DAT_0a3e0694 = (undefined4)ram0x0848d900;
          DAT_0a3e0698 = 0;
          DAT_0a3e0699 = 1;
        }
        if ((DAT_0a3dd403 & 1) == 0) {
          uVar9 = 0;
          do {
            (&DAT_0a3dd39e)[uVar9] = (&DAT_088bcf0a)[uVar9] + 0x8a ^ (&DAT_088bcefa)[uVar9 & 0xf];
            uVar9 = uVar9 + 1;
          } while (uVar9 != 0x65);
          DAT_0a3dd403 = 1;
        }
        FUN_0003bb6c(auStack_220,&DAT_0a3e067c,&DAT_0a3dd39e,"/CoreText");
        plVar10 = local_188;
        plVar4 = local_240;
        pppuVar2 = local_248;
        if (local_188 != (long *)0x0) {
          local_188[1] = local_188[1] + 1;
        }
        if (local_240 != (long *)0x0) {
          local_240[1] = local_240[1] + 1;
        }
        if (*(char *)((long)param_2 + 0x17) < '\0') {
          FUN_00018d20(&local_288,*param_2,param_2[1]);
        }
        else {
          lStack_280 = param_2[1];
          local_288 = *param_2;
          local_278 = param_2[2];
        }
        local_148 = (long *)0x0;
        plVar7 = (long *)__Znwm(0x48);
        plVar7[2] = (long)plVar10;
        plVar7[1] = lVar6;
        *plVar7 = (long)&PTR_FUN_09def470;
        plVar7[4] = (long)plVar4;
        plVar7[3] = (long)pppuVar2;
        plVar7[5] = param_1;
        if ((long)local_278 < 0) {
          FUN_00018d20(plVar7 + 6,local_288,lStack_280);
        }
        else {
          plVar7[7] = lStack_280;
          plVar7[6] = local_288;
          plVar7[8] = local_278;
        }
        if (plVar10 != (long *)0x0) {
          plVar10[1] = plVar10[1] + 1;
        }
        local_168 = (long *)0x0;
        local_148 = plVar7;
        local_168 = (long *)__Znwm(0x20);
        *local_168 = (long)&PTR_FUN_09def4f0;
        local_168[1] = lVar6;
        local_168[2] = (long)plVar10;
        local_168[3] = param_1;
        FUN_0453d344(&local_f0,pppuVar3,auStack_220,alStack_160,alStack_180,0);
        if (local_168 == alStack_180) {
          pcVar8 = *(code **)(*local_168 + 0x20);
LAB_031cc8b0:
          (*pcVar8)();
        }
        else if (local_168 != (long *)0x0) {
          pcVar8 = *(code **)(*local_168 + 0x28);
          goto LAB_031cc8b0;
        }
        if (local_148 == alStack_160) {
          pcVar8 = *(code **)(*local_148 + 0x20);
LAB_031cc8dc:
          (*pcVar8)();
        }
        else if (local_148 != (long *)0x0) {
          pcVar8 = *(code **)(*local_148 + 0x28);
          goto LAB_031cc8dc;
        }
        if ((long)local_278 < 0) {
          __ZdlPvm(local_288,local_278 & 0x7fffffffffffffff);
        }
        plVar4 = (long *)CONCAT71(uStack_137,local_138);
        if (plVar4 != (long *)0x0) {
          LOAcquire();
          lVar6 = plVar4[1];
          plVar4[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*plVar4 + 0x10))(plVar4);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
          }
        }
        plVar4 = plStack_e8;
        if (plStack_e8 != (long *)0x0) {
          plVar10 = plStack_e8 + 1;
          *plVar10 = *plVar10 + 1;
          *plVar10 = *plVar10 + 1;
        }
        plVar10 = *(long **)(local_190 + 0x68);
        *(undefined8 ****)(local_190 + 0x60) = local_f0;
        *(long **)(local_190 + 0x68) = plStack_e8;
        if (plVar10 != (long *)0x0) {
          LOAcquire();
          lVar6 = plVar10[1];
          plVar10[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*plVar10 + 0x10))(plVar10);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
          }
        }
        if (plVar4 != (long *)0x0) {
          LOAcquire();
          lVar6 = plVar4[1];
          plVar4[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*plVar4 + 0x10))(plVar4);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
          }
        }
        plVar4 = plStack_e8;
        if (plStack_e8 != (long *)0x0) {
          LOAcquire();
          lVar6 = plStack_e8[1];
          plStack_e8[1] = lVar6 + -1;
          LORelease();
          if (lVar6 == 0) {
            (**(code **)(*plStack_e8 + 0x10))(plStack_e8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
          }
        }
      }
      plVar4 = local_240;
      if (local_240 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_240[1];
        local_240[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*local_240 + 0x10))(local_240);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
        }
      }
    }
    else {
LAB_031cc258:
      iVar5 = thunk_FUN_05e1d97c(2);
      if (iVar5 != 0) {
        FUN_0488143c(&local_140);
        ppppuVar1 = (undefined8 ****)local_140;
        if (-1 < cStack_129) {
          ppppuVar1 = &local_140;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar9 = 0;
          do {
            (&DAT_0a3dd350)[uVar9] = (&DAT_088bce97)[uVar9] + 0x8a ^ (&DAT_088bce87)[uVar9 & 0xf];
            uVar9 = uVar9 + 1;
          } while (uVar9 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3e0699 & 1) == 0) {
          _DAT_0a3e067c = CONCAT44((int)DAT_088baf38,(int)DAT_08482fd0);
          uRam000000000a3e0684 = CONCAT44((int)DAT_088baf48,(int)DAT_088baf40);
          DAT_0a3e068c = CONCAT44((int)DAT_088baf58,(int)DAT_088baf50);
          DAT_0a3e0694 = (undefined4)ram0x0848d900;
          DAT_0a3e0698 = 0;
          DAT_0a3e0699 = 1;
        }
        FUN_05e1d050(auStack_220,2,ppppuVar1,&DAT_0a3dd350,&DAT_0a3e067c,"rk/Versions/A/CoreText",0,
                     0);
        if ((DAT_0a3e071e & 1) == 0) {
          _DAT_0a3e06f8 = CONCAT44((int)DAT_084a04e8,(int)DAT_084c7770);
          uRam000000000a3e0700 = CONCAT44((int)DAT_0848c098,(int)DAT_088baf70);
          _DAT_0a3e0708 = CONCAT44((int)DAT_08610c90,(int)DAT_084d89b0);
          uRam000000000a3e0710 = CONCAT44((int)DAT_0861c300,(int)ram0x08487528);
          DAT_0a3e0718 = (undefined4)DAT_08492618;
          DAT_0a3e071c = 0x74;
          DAT_0a3e071e = 1;
        }
        local_88 = 0;
        uStack_90 = 0;
        local_78 = 0;
        uStack_80 = 0;
        local_a8 = 0;
        uStack_b0 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        local_c8 = 0;
        uStack_d0 = 0;
        local_b8 = 0;
        uStack_c0 = 0;
        plStack_e8 = (long *)0x0;
        local_f0 = (undefined8 ****)0x0;
        local_d8 = 0;
        uStack_e0 = 0;
        FUN_05e1d31c(auStack_220,&DAT_0a3e06f8,&local_f0);
        thunk_FUN_05e1d0bc(auStack_220);
        if (cStack_129 < '\0') {
          __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
        }
      }
    }
    plVar4 = local_228;
    if (local_228 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_228[1];
      local_228[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_228 + 0x10))(local_228);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
    }
  }
  plVar4 = local_188;
  if (local_188 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_188[1];
    local_188[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_188 + 0x10))(local_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
LAB_031ccac4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


