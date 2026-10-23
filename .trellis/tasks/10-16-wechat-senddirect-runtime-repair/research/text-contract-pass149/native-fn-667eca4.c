// Ghidra inferred pseudocode; requested=0x667eca4
// entry=0667eca4 end=0667ef87

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0667eca4(long *param_1)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  long lVar4;
  ulong uVar5;
  undefined1 *local_140;
  long lStack_138;
  ulong local_130;
  long *local_128 [26];
  undefined1 *local_58;
  undefined8 local_50;
  undefined1 *local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar1 = FUN_0668dad0(1);
  if (iVar1 != 0) {
    if ((DAT_0a5181e5 & 1) == 0) {
      DAT_0a5181e0 = (undefined4)ram0x08782918;
      DAT_0a5181e4 = 0;
      DAT_0a5181e5 = 1;
    }
    if ((DAT_0a51832d & 1) == 0) {
      DAT_0a518328 = (undefined4)DAT_08728498;
      DAT_0a51832c = 0;
      DAT_0a51832d = 1;
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
    FUN_0668db5c(local_128,&DAT_0a5181e0,&DAT_0a518328,&DAT_0a5181f8,0x7100002800);
    if (*(char *)((long)param_1 + 0x97) < '\0') {
      FUN_00018d20(&local_140,param_1[0x10],param_1[0x11]);
    }
    else {
      lStack_138 = param_1[0x11];
      local_140 = (undefined1 *)param_1[0x10];
      local_130 = param_1[0x12];
    }
    if ((DAT_0a51833e & 1) == 0) {
      DAT_0a518330._0_1_ = s_co_job_ico_job_c________join_____09685c10[0x18];
      DAT_0a518330._1_1_ = s_co_job_ico_job_c________join_____09685c10[0x19];
      DAT_0a518330._2_1_ = s_co_job_ico_job_c________join_____09685c10[0x1a];
      DAT_0a518330._3_1_ = s_co_job_ico_job_c________join_____09685c10[0x1b];
      DAT_0a518330._4_1_ = s_co_job_ico_job_c________join_____09685c10[0x1c];
      DAT_0a518330._5_1_ = s_co_job_ico_job_c________join_____09685c10[0x1d];
      DAT_0a518330._6_1_ = s_co_job_ico_job_c________join_____09685c10[0x1e];
      DAT_0a518330._7_1_ = s_co_job_ico_job_c________join_____09685c10[0x1f];
      DAT_0a518338 = (undefined4)DAT_09684bc8;
      DAT_0a51833c = 0x20;
      DAT_0a51833e = 1;
    }
    plVar3 = local_128[0] + 0xd;
    if (*(char *)((long)local_128[0] + 0x7f) < '\0') {
      plVar3 = (long *)*plVar3;
    }
    local_58 = local_140;
    if (-1 < (long)local_130) {
      local_58 = (undefined1 *)&local_140;
    }
    local_50 = 0xaaaaaaaa00000010;
    local_40 = 0xaaaaaaaa00000006;
    local_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_128[0] + 7,&DAT_0a518330,plVar3,&local_58,1);
    lVar4 = *local_128[0];
    if ((DAT_0a518327 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a5182f1)[uVar5] = (&DAT_09685f1e)[uVar5 & 0xf] ^ (&DAT_09685f2e)[uVar5];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x36);
      DAT_0a518327 = 1;
    }
    plVar3 = (long *)(lVar4 + 0x68);
    if (*(char *)(lVar4 + 0x7f) < '\0') {
      plVar3 = (long *)*plVar3;
    }
    FUN_06680464(lVar4 + 0x38,&DAT_0a5182f1,plVar3,param_1 + 0x28,(long)param_1 + 0x141,
                 (long)param_1 + 0x143);
    FUN_0668dbac();
    if ((long)local_130 < 0) {
      __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(local_128);
  }
  if (((*(byte *)(param_1 + 0x28) & 1) == 0) && ((*(byte *)((long)param_1 + 0x143) & 1) == 0)) {
    (**(code **)(*param_1 + 0x10))(param_1);
  }
  lVar4 = FUN_06680b64(param_1);
  if (-1 < lVar4) {
    if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
      return;
    }
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  uVar2 = ___cxa_allocate_exception(0x10);
  FUN_066684a8(uVar2,lVar4);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar2,&PTR_DAT_09fb1c88,__ZNSt9exceptionD2Ev);
}


