// Ghidra inferred pseudocode; requested=0x667e8cc
// entry=0667e8cc end=0667ec0f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0667e8cc(long param_1)

{
  byte *pbVar1;
  byte bVar2;
  undefined8 uVar3;
  int iVar4;
  undefined ***pppuVar5;
  long *plVar6;
  long lVar7;
  code *pcVar8;
  ulong uVar9;
  undefined8 ***local_180;
  undefined8 uStack_178;
  ulong local_170;
  long *local_168 [26];
  undefined **local_98;
  undefined8 uStack_90;
  long local_88;
  undefined ***local_80;
  undefined **local_78;
  undefined8 uStack_70;
  long local_68;
  undefined ***local_60;
  undefined8 ***local_58;
  undefined8 local_50;
  undefined1 *local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pbVar1 = (byte *)(param_1 + 0x143);
  LOAcquire();
  bVar2 = *pbVar1;
  *pbVar1 = 1;
  LORelease();
  if ((bVar2 & 1) != 0) goto LAB_0667ebdc;
  iVar4 = FUN_0668dad0(1);
  if (iVar4 != 0) {
    if ((DAT_0a5181e5 & 1) == 0) {
      DAT_0a5181e0 = (undefined4)ram0x08782918;
      DAT_0a5181e4 = 0;
      DAT_0a5181e5 = 1;
    }
    if ((DAT_0a5182d7 & 1) == 0) {
      DAT_0a5182d0 = (undefined4)DAT_0849e748;
      DAT_0a5182d4 = 0x6c65;
      DAT_0a5182d6 = 0;
      DAT_0a5182d7 = 1;
    }
    if ((DAT_0a518203 & 1) == 0) {
      DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
      DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
      DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
      DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
      DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
      DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
      DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
      DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
      DAT_0a518200 = 0x7070;
      DAT_0a518202 = 0;
      DAT_0a518203 = 1;
    }
    FUN_0668db5c(local_168,&DAT_0a5181e0,&DAT_0a5182d0,&DAT_0a5181f8,0x5800002800);
    if (*(char *)(param_1 + 0x97) < '\0') {
      FUN_00018d20(&local_180,*(undefined8 *)(param_1 + 0x80),*(undefined8 *)(param_1 + 0x88));
    }
    else {
      uStack_178 = *(undefined8 *)(param_1 + 0x88);
      local_180 = *(undefined8 ****)(param_1 + 0x80);
      local_170 = *(ulong *)(param_1 + 0x90);
    }
    if ((DAT_0a5182f0 & 1) == 0) {
      uRam000000000a5182e8._0_1_ = s_cancel_________09685c70[8];
      uRam000000000a5182e8._1_1_ = s_cancel_________09685c70[9];
      uRam000000000a5182e8._2_1_ = s_cancel_________09685c70[10];
      uRam000000000a5182e8._3_1_ = s_cancel_________09685c70[0xb];
      uRam000000000a5182e8._4_1_ = s_cancel_________09685c70[0xc];
      uRam000000000a5182e8._5_1_ = s_cancel_________09685c70[0xd];
      uRam000000000a5182e8._6_1_ = s_cancel_________09685c70[0xe];
      uRam000000000a5182e8._7_1_ = s_cancel_________09685c70[0xf];
      DAT_0a5182e0 = s_cancel_________09685c70[0];
      DAT_0a5182e0_1._0_1_ = s_cancel_________09685c70[1];
      DAT_0a5182e0_1._1_1_ = s_cancel_________09685c70[2];
      DAT_0a5182e0_1._2_1_ = s_cancel_________09685c70[3];
      DAT_0a5182e0_1._3_1_ = s_cancel_________09685c70[4];
      DAT_0a5182e0_1._4_1_ = s_cancel_________09685c70[5];
      DAT_0a5182e0_1._5_1_ = s_cancel_________09685c70[6];
      DAT_0a5182e0_1._6_1_ = s_cancel_________09685c70[7];
      DAT_0a5182f0 = 1;
    }
    plVar6 = local_168[0] + 0xd;
    if (*(char *)((long)local_168[0] + 0x7f) < '\0') {
      plVar6 = (long *)*plVar6;
    }
    local_58 = local_180;
    if (-1 < (long)local_170) {
      local_58 = &local_180;
    }
    local_50 = 0xaaaaaaaa00000010;
    local_40 = 0xaaaaaaaa00000006;
    local_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_168[0] + 7,&DAT_0a5182e0,plVar6,&local_58,1);
    lVar7 = *local_168[0];
    if ((DAT_0a518327 & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a5182f1)[uVar9] = (&DAT_09685f1e)[uVar9 & 0xf] ^ (&DAT_09685f2e)[uVar9];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x36);
      DAT_0a518327 = 1;
    }
    plVar6 = (long *)(lVar7 + 0x68);
    if (*(char *)(lVar7 + 0x7f) < '\0') {
      plVar6 = (long *)*plVar6;
    }
    FUN_06680464(lVar7 + 0x38,&DAT_0a5182f1,plVar6,param_1 + 0x140,param_1 + 0x141,pbVar1);
    FUN_0668dbac();
    if ((long)local_170 < 0) {
      __ZdlPvm(local_180,local_170 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(local_168);
  }
  *(undefined1 *)(param_1 + 0x141) = 0;
  plVar6 = *(long **)(param_1 + 0xf8);
  uVar3 = *(undefined8 *)(param_1 + 0x98);
  if ((*(byte *)(param_1 + 0x140) & 1) == 0) {
    if ((*(long *)(param_1 + 0xa0) == 0) ||
       (local_88 = __ZNSt3__119__shared_weak_count4lockEv(), local_88 == 0)) goto LAB_0667ec08;
    local_98 = &PTR_FUN_09fb2ef8;
    uStack_90 = uVar3;
    local_80 = &local_98;
    (**(code **)(*plVar6 + 0x10))(plVar6,&local_98);
    pppuVar5 = local_80;
    if (local_80 != &local_98) goto LAB_0667ebcc;
LAB_0667eb7c:
    pcVar8 = (code *)(*pppuVar5)[4];
  }
  else {
    if ((*(long *)(param_1 + 0xa0) == 0) ||
       (local_68 = __ZNSt3__119__shared_weak_count4lockEv(), local_68 == 0)) {
LAB_0667ec08:
                    /* WARNING: Subroutine does not return */
      FUN_00283500();
    }
    local_78 = &PTR_FUN_09fb2e78;
    uStack_70 = uVar3;
    local_60 = &local_78;
    (**(code **)(*plVar6 + 0x10))(plVar6,&local_78);
    pppuVar5 = local_60;
    if (local_60 == &local_78) goto LAB_0667eb7c;
LAB_0667ebcc:
    if (pppuVar5 == (undefined ***)0x0) goto LAB_0667ebdc;
    pcVar8 = (code *)(*pppuVar5)[5];
  }
  (*pcVar8)();
LAB_0667ebdc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


