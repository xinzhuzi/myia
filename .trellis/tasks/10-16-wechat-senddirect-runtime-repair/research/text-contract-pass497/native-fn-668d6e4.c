// Ghidra inferred pseudocode; requested=0x668d6e4
// entry=0668d6e4 end=0668d9bf

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0668d6e4(undefined4 *param_1)

{
  long lVar1;
  long lVar2;
  uint *puVar3;
  long *plVar4;
  int extraout_w8;
  long lVar5;
  long lVar6;
  undefined1 in_wzr;
  undefined1 *local_140 [26];
  undefined1 uStack_69;
  undefined1 **local_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (DAT_0a518cb8 != -1) {
    local_140[0] = &uStack_69;
    local_68 = local_140;
    __ZNSt3__111__call_onceERVmPvPFvS2_E(&DAT_0a518cb8,&local_68,FUN_0669440c);
  }
  puVar3 = (uint *)(*(code *)PTR___tlv_bootstrap_0a24df10)(*DAT_0a518cb0);
  if (extraout_w8 < 4 && (*puVar3 & 1) == 0) {
    if ((DAT_0a518dd9 & 1) == 0) {
      DAT_0a518dd4 = (undefined4)ram0x08782918;
      DAT_0a518dd8 = 0;
      DAT_0a518dd9 = 1;
    }
    if ((DAT_0a518de2 & 1) == 0) {
      DAT_0a518ddc = (undefined4)DAT_084d8970;
      DAT_0a518de0 = 0x74;
      DAT_0a518de2 = 1;
    }
    if ((DAT_0a518df1 & 1) == 0) {
      DAT_0a518de8._0_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[0];
      DAT_0a518de8._1_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[1];
      DAT_0a518de8._2_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[2];
      DAT_0a518de8._3_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[3];
      DAT_0a518de8._4_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[4];
      DAT_0a518de8._5_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[5];
      DAT_0a518de8._6_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[6];
      DAT_0a518de8._7_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[7];
      DAT_0a518df0 = 0;
      DAT_0a518df1 = 1;
    }
    FUN_0668e6bc(local_140,0,0,0,3,&DAT_0a518dd4,0,&DAT_0a518ddc,&DAT_0a518de8,0x100000397);
    if ((DAT_0a518e06 & 1) == 0) {
      DAT_0a518df8._0_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[8];
      DAT_0a518df8._1_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[9];
      DAT_0a518df8._2_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[10];
      DAT_0a518df8._3_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[0xb];
      DAT_0a518df8._4_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[0xc];
      DAT_0a518df8._5_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[0xd];
      DAT_0a518df8._6_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[0xe];
      DAT_0a518df8._7_1_ = s_zlog_cppzlog_resset_leve__>__s___096883b8[0xf];
      DAT_0a518e00 = (undefined4)ram0x08483f40;
      DAT_0a518e04 = 0x21;
      DAT_0a518e06 = 1;
    }
    plVar4 = (long *)(local_140[0] + 0x68);
    if ((char)local_140[0][0x7f] < '\0') {
      plVar4 = (long *)*plVar4;
    }
    local_60 = 0xaaaaaaaa00000006;
    local_68 = (undefined1 **)&DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_140[0] + 0x38,&DAT_0a518df8,plVar4,&local_68,0);
    FUN_0668e878(local_140);
  }
  __ZNSt3__115recursive_mutex4lockEv(param_1 + 0x28);
  FUN_0668d5c8(param_1 + 6);
  lVar2 = *(long *)(param_1 + 0x1c);
  lVar6 = *(long *)(param_1 + 0x1e);
  *(undefined8 *)(param_1 + 0x1c) = 0;
  *(undefined8 *)(param_1 + 0x1e) = 0;
  lVar5 = *(long *)(param_1 + 0x20);
  *(undefined8 *)(param_1 + 0x20) = 0;
  for (; lVar6 != lVar2; lVar6 = lVar6 + -0x10) {
    plVar4 = *(long **)(lVar6 + -8);
    if (plVar4 != (long *)0x0) {
      LOAcquire();
      lVar1 = plVar4[1];
      plVar4[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*plVar4 + 0x10))(plVar4);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
    }
  }
  if (lVar2 != 0) {
    __ZdlPvm(lVar2,lVar5 - lVar2);
  }
  *param_1 = 0;
  *(undefined1 *)(param_1 + 1) = in_wzr;
  *(undefined1 *)((long)param_1 + 5) = in_wzr;
  plVar4 = *(long **)(param_1 + 4);
  *(undefined8 *)(param_1 + 2) = 0;
  *(undefined8 *)(param_1 + 4) = 0;
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar4[1];
    plVar4[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  __ZNSt3__115recursive_mutex6unlockEv(param_1 + 0x28);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


