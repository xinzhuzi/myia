// Ghidra inferred pseudocode; requested=0x6681cd8
// entry=06681cd8 end=0668228b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06681cd8(long param_1)

{
  undefined8 *******pppppppuVar1;
  long lVar2;
  ulong uVar3;
  undefined8 uVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  undefined1 local_d0;
  undefined7 uStack_cf;
  undefined7 local_c0;
  char cStack_b9;
  undefined1 *local_b8;
  undefined1 *local_b0;
  long *local_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  ulong local_90;
  undefined8 *******local_80 [2];
  undefined7 local_70;
  char cStack_69;
  undefined1 *local_68;
  
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)(param_1 + 0xef) < '\0') {
    FUN_00018d20(&local_a0,*(undefined8 *)(param_1 + 0xd8),*(undefined8 *)(param_1 + 0xe0));
  }
  else {
    uStack_98 = *(undefined8 *)(param_1 + 0xe0);
    local_a0 = *(undefined8 *)(param_1 + 0xd8);
    local_90 = *(ulong *)(param_1 + 0xe8);
  }
  if ((DAT_0a5184b4 & 1) == 0) {
    DAT_0a5184a8._0_1_ = s_co_job_gname_______c_09686138[8];
    DAT_0a5184a8._1_1_ = s_co_job_gname_______c_09686138[9];
    DAT_0a5184a8._2_1_ = s_co_job_gname_______c_09686138[10];
    DAT_0a5184a8._3_1_ = s_co_job_gname_______c_09686138[0xb];
    DAT_0a5184a8._4_1_ = s_co_job_gname_______c_09686138[0xc];
    DAT_0a5184a8._5_1_ = s_co_job_gname_______c_09686138[0xd];
    DAT_0a5184a8._6_1_ = s_co_job_gname_______c_09686138[0xe];
    DAT_0a5184a8._7_1_ = s_co_job_gname_______c_09686138[0xf];
    DAT_0a5184b0 = (undefined4)ram0x084c9468;
    DAT_0a5184b4 = 1;
  }
  FUN_066822a4(local_80,&DAT_0a5184a8,&local_a0);
  if ((DAT_0a518455 & 1) == 0) {
    DAT_0a518450 = (undefined4)ram0x08782918;
    DAT_0a518454 = 0;
    DAT_0a518455 = 1;
  }
  if ((DAT_0a5184a6 & 1) == 0) {
    DAT_0a518498._0_1_ = s_co_job_ico_job_c________join_____09685c10[0x20];
    DAT_0a518498._1_1_ = s_co_job_ico_job_c________join_____09685c10[0x21];
    DAT_0a518498._2_1_ = s_co_job_ico_job_c________join_____09685c10[0x22];
    DAT_0a518498._3_1_ = s_co_job_ico_job_c________join_____09685c10[0x23];
    DAT_0a518498._4_1_ = s_co_job_ico_job_c________join_____09685c10[0x24];
    DAT_0a518498._5_1_ = s_co_job_ico_job_c________join_____09685c10[0x25];
    DAT_0a518498._6_1_ = s_co_job_ico_job_c________join_____09685c10[0x26];
    DAT_0a518498._7_1_ = s_co_job_ico_job_c________join_____09685c10[0x27];
    DAT_0a5184a0 = (undefined4)DAT_08485ea0;
    DAT_0a5184a4 = 0x70;
    DAT_0a5184a6 = 1;
  }
  if ((DAT_0a518481 & 1) == 0) {
    uRam000000000a518478._0_1_ = s_co_job_group_cppjobs__size_______09686190[8];
    uRam000000000a518478._1_1_ = s_co_job_group_cppjobs__size_______09686190[9];
    uRam000000000a518478._2_1_ = s_co_job_group_cppjobs__size_______09686190[10];
    uRam000000000a518478._3_1_ = s_co_job_group_cppjobs__size_______09686190[0xb];
    uRam000000000a518478._4_1_ = s_co_job_group_cppjobs__size_______09686190[0xc];
    uRam000000000a518478._5_1_ = s_co_job_group_cppjobs__size_______09686190[0xd];
    uRam000000000a518478._6_1_ = s_co_job_group_cppjobs__size_______09686190[0xe];
    uRam000000000a518478._7_1_ = s_co_job_group_cppjobs__size_______09686190[0xf];
    DAT_0a518470 = s_co_job_group_cppjobs__size_______09686190[0];
    DAT_0a518470_1._0_1_ = s_co_job_group_cppjobs__size_______09686190[1];
    DAT_0a518470_1._1_1_ = s_co_job_group_cppjobs__size_______09686190[2];
    DAT_0a518470_1._2_1_ = s_co_job_group_cppjobs__size_______09686190[3];
    DAT_0a518470_1._3_1_ = s_co_job_group_cppjobs__size_______09686190[4];
    DAT_0a518470_1._4_1_ = s_co_job_group_cppjobs__size_______09686190[5];
    DAT_0a518470_1._5_1_ = s_co_job_group_cppjobs__size_______09686190[6];
    DAT_0a518470_1._6_1_ = s_co_job_group_cppjobs__size_______09686190[7];
    DAT_0a518480 = 0;
    DAT_0a518481 = 1;
  }
  thunk_FUN_0668f12c(&local_68,&DAT_0a518450,&DAT_0a518498,&DAT_0a518470,&DAT_0a518498,0x1d00000000,
                     local_80);
  if (cStack_69 < '\0') {
    __ZdlPvm(local_80[0],CONCAT17(cStack_69,local_70) & 0x7fffffffffffffff);
  }
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,local_90 & 0x7fffffffffffffff);
  }
  __ZNSt3__15mutex4lockEv(param_1 + 0x78);
  for (plVar7 = *(long **)(param_1 + 0xc0); plVar7 != (long *)(param_1 + 0xb8);
      plVar7 = (long *)plVar7[1]) {
    if (plVar7[2] != 0) {
      FUN_06686370(plVar7[2] + 8,param_1);
    }
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 0x78);
  if (*(char *)(param_1 + 0xf0) == '\x01') {
    local_b0 = &SUB_aaaaaaaaaaaaaaaa;
    local_a8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_06673848(&local_b0);
    if ((local_b0 == (undefined1 *)0x0) || (uVar3 = FUN_06674c80(&local_b0), (uVar3 & 1) != 0)) {
      FUN_066823c4(param_1);
    }
    else {
      local_b8 = &SUB_aaaaaaaaaaaaaaaa;
      if (*(char *)(param_1 + 0xef) < '\0') {
        FUN_00018d20(&local_a0,*(undefined8 *)(param_1 + 0xd8),*(undefined8 *)(param_1 + 0xe0));
      }
      else {
        uStack_98 = *(undefined8 *)(param_1 + 0xe0);
        local_a0 = *(undefined8 *)(param_1 + 0xd8);
        local_90 = *(ulong *)(param_1 + 0xe8);
      }
      if ((DAT_0a5184a6 & 1) == 0) {
        DAT_0a518498._0_1_ = s_co_job_ico_job_c________join_____09685c10[0x20];
        DAT_0a518498._1_1_ = s_co_job_ico_job_c________join_____09685c10[0x21];
        DAT_0a518498._2_1_ = s_co_job_ico_job_c________join_____09685c10[0x22];
        DAT_0a518498._3_1_ = s_co_job_ico_job_c________join_____09685c10[0x23];
        DAT_0a518498._4_1_ = s_co_job_ico_job_c________join_____09685c10[0x24];
        DAT_0a518498._5_1_ = s_co_job_ico_job_c________join_____09685c10[0x25];
        DAT_0a518498._6_1_ = s_co_job_ico_job_c________join_____09685c10[0x26];
        DAT_0a518498._7_1_ = s_co_job_ico_job_c________join_____09685c10[0x27];
        DAT_0a5184a0 = (undefined4)DAT_08485ea0;
        DAT_0a5184a4 = 0x70;
        DAT_0a5184a6 = 1;
      }
      if ((DAT_0a5184f0 & 1) == 0) {
        _DAT_0a5184b8 = CONCAT44((int)DAT_09685c58,(int)DAT_087faf40);
        uRam000000000a5184c0 = CONCAT44((int)DAT_084844a8,(int)ram0x09686148);
        _DAT_0a5184c8 = CONCAT44((int)DAT_088fbaf0,(int)DAT_08545128);
        uRam000000000a5184d0 = CONCAT44((int)DAT_084cadd8,(int)DAT_084874c0);
        _DAT_0a5184d8 = CONCAT44((int)DAT_085c6640,(int)DAT_0849e748);
        uRam000000000a5184e0 = CONCAT44((int)DAT_08782818,(int)DAT_085541f8);
        DAT_0a5184e8 = CONCAT44((int)DAT_084cf428,(int)DAT_08728498);
        DAT_0a5184f0 = 1;
      }
      FUN_06666718(local_80,&DAT_0a518498,&DAT_0a5184b8,&local_a0);
      pppppppuVar1 = local_80[0];
      if (-1 < cStack_69) {
        pppppppuVar1 = local_80;
      }
      cStack_b9 = '\0';
      local_d0 = 0;
      if ((DAT_0a518455 & 1) == 0) {
        DAT_0a518450 = (undefined4)ram0x08782918;
        DAT_0a518454 = 0;
        DAT_0a518455 = 1;
      }
      if ((DAT_0a5184a6 & 1) == 0) {
        DAT_0a5184a0 = (undefined4)DAT_08485ea0;
        DAT_0a5184a4 = 0x70;
        DAT_0a5184a6 = 1;
        DAT_0a518498 = s_co_job_ico_job_c________join_____09685c10._32_8_;
      }
      if ((DAT_0a518481 & 1) == 0) {
        uRam000000000a518478._0_1_ = s_co_job_group_cppjobs__size_______09686190[8];
        uRam000000000a518478._1_1_ = s_co_job_group_cppjobs__size_______09686190[9];
        uRam000000000a518478._2_1_ = s_co_job_group_cppjobs__size_______09686190[10];
        uRam000000000a518478._3_1_ = s_co_job_group_cppjobs__size_______09686190[0xb];
        uRam000000000a518478._4_1_ = s_co_job_group_cppjobs__size_______09686190[0xc];
        uRam000000000a518478._5_1_ = s_co_job_group_cppjobs__size_______09686190[0xd];
        uRam000000000a518478._6_1_ = s_co_job_group_cppjobs__size_______09686190[0xe];
        uRam000000000a518478._7_1_ = s_co_job_group_cppjobs__size_______09686190[0xf];
        DAT_0a518470 = s_co_job_group_cppjobs__size_______09686190[0];
        DAT_0a518470_1._0_1_ = s_co_job_group_cppjobs__size_______09686190[1];
        DAT_0a518470_1._1_1_ = s_co_job_group_cppjobs__size_______09686190[2];
        DAT_0a518470_1._2_1_ = s_co_job_group_cppjobs__size_______09686190[3];
        DAT_0a518470_1._3_1_ = s_co_job_group_cppjobs__size_______09686190[4];
        DAT_0a518470_1._4_1_ = s_co_job_group_cppjobs__size_______09686190[5];
        DAT_0a518470_1._5_1_ = s_co_job_group_cppjobs__size_______09686190[6];
        DAT_0a518470_1._6_1_ = s_co_job_group_cppjobs__size_______09686190[7];
        DAT_0a518480 = 0;
        DAT_0a518481 = 1;
      }
      thunk_FUN_0668f12c(&local_b8,&DAT_0a518450,&DAT_0a518498,&DAT_0a518470,pppppppuVar1,
                         0x2400000000,&local_d0);
      if (cStack_b9 < '\0') {
        __ZdlPvm(CONCAT71(uStack_cf,local_d0),CONCAT17(cStack_b9,local_c0) & 0x7fffffffffffffff);
      }
      if (cStack_69 < '\0') {
        __ZdlPvm(local_80[0],CONCAT17(cStack_69,local_70) & 0x7fffffffffffffff);
      }
      if ((long)local_90 < 0) {
        __ZdlPvm(local_a0,local_90 & 0x7fffffffffffffff);
      }
      if (local_b8 != (undefined1 *)0x0) {
        uVar4 = thunk_FUN_0668ef88();
        __ZdlPvm(uVar4,0xf8);
      }
    }
    plVar7 = local_a8;
    if (local_a8 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_a8[1];
      local_a8[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_a8 + 0x10))(local_a8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
  }
  if (local_68 != (undefined1 *)0x0) {
    uVar4 = thunk_FUN_0668ef88();
    __ZdlPvm(uVar4,0xf8);
  }
  if (*(char *)(param_1 + 0xef) < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0xd8),*(ulong *)(param_1 + 0xe8) & 0x7fffffffffffffff);
  }
  if (*(long *)(param_1 + 200) != 0) {
    plVar7 = *(long **)(param_1 + 0xc0);
    plVar5 = *(long **)(*(long *)(param_1 + 0xb8) + 8);
    lVar2 = *plVar7;
    *(long **)(lVar2 + 8) = plVar5;
    *plVar5 = lVar2;
    *(undefined8 *)(param_1 + 200) = 0;
    while (plVar7 != (long *)(param_1 + 0xb8)) {
      plVar6 = (long *)plVar7[1];
      plVar5 = (long *)plVar7[3];
      if (plVar5 != (long *)0x0) {
        LOAcquire();
        lVar2 = plVar5[1];
        plVar5[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
          (**(code **)(*plVar5 + 0x10))(plVar5);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      __ZdlPvm(plVar7,0x20);
      plVar7 = plVar6;
    }
  }
  __ZNSt3__15mutexD1Ev(param_1 + 0x78);
  FUN_06685cbc(param_1 + 0x10);
  FUN_0668614c(param_1);
  return;
}


