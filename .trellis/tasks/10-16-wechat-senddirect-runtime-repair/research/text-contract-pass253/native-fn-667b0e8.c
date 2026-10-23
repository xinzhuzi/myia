// Ghidra inferred pseudocode; requested=0x667b0e8
// entry=0667b0e8 end=0667b39b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long FUN_0667b0e8(long param_1)

{
  int iVar1;
  long *plVar2;
  long local_138 [26];
  undefined8 local_68;
  undefined1 *local_60;
  long lStack_58;
  undefined8 local_50;
  undefined1 *puStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (((DAT_0a517ac0 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_0a517ac0), iVar1 != 0)) {
    FUN_06676a4c(&DAT_0a5179d0);
    ___cxa_guard_release(&DAT_0a517ac0);
  }
  FUN_0667a760(&DAT_0a517a48,*(undefined8 *)(param_1 + 0x3a0),param_1 + 0x3a8,1);
  iVar1 = FUN_0668dad0(1);
  if (iVar1 != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a518133 & 1) == 0) {
      DAT_0a518128._0_1_ = s__coroutiy__i_09684ca8[0];
      DAT_0a518128._1_1_ = s__coroutiy__i_09684ca8[1];
      DAT_0a518128._2_1_ = s__coroutiy__i_09684ca8[2];
      DAT_0a518128._3_1_ = s__coroutiy__i_09684ca8[3];
      DAT_0a518128._4_1_ = s__coroutiy__i_09684ca8[4];
      DAT_0a518128._5_1_ = s__coroutiy__i_09684ca8[5];
      DAT_0a518128._6_1_ = s__coroutiy__i_09684ca8[6];
      DAT_0a518128._7_1_ = s__coroutiy__i_09684ca8[7];
      DAT_0a518130 = 0x656e;
      DAT_0a518132 = 0;
      DAT_0a518133 = 1;
    }
    if ((DAT_0a517aec & 1) == 0) {
      DAT_0a517ae0._0_1_ = s_co_core_resume_ie__i_09684bb0[0];
      DAT_0a517ae0._1_1_ = s_co_core_resume_ie__i_09684bb0[1];
      DAT_0a517ae0._2_1_ = s_co_core_resume_ie__i_09684bb0[2];
      DAT_0a517ae0._3_1_ = s_co_core_resume_ie__i_09684bb0[3];
      DAT_0a517ae0._4_1_ = s_co_core_resume_ie__i_09684bb0[4];
      DAT_0a517ae0._5_1_ = s_co_core_resume_ie__i_09684bb0[5];
      DAT_0a517ae0._6_1_ = s_co_core_resume_ie__i_09684bb0[6];
      DAT_0a517ae0._7_1_ = s_co_core_resume_ie__i_09684bb0[7];
      DAT_0a517ae8 = (undefined4)DAT_085722b0;
      DAT_0a517aec = 1;
    }
    FUN_0668db5c(local_138,&DAT_0a517ad8,&DAT_0a518128,&DAT_0a517ae0,0x12f00002800);
    if ((DAT_0a518158 & 1) == 0) {
      _DAT_0a518134 = CONCAT44((int)DAT_087ec760,(int)DAT_089069d8);
      uRam000000000a51813c = CONCAT44((int)DAT_084c8ef8,(int)DAT_0852e8a0);
      _DAT_0a518144 = CONCAT44((int)DAT_084de688,(int)ram0x09684cb0);
      uRam000000000a51814c = CONCAT44((int)DAT_08b69bc8,(int)DAT_0877c0b0);
      DAT_0a518154 = (undefined4)DAT_09684c88;
      DAT_0a518158 = 1;
    }
    plVar2 = (long *)(local_138[0] + 0x68);
    if (*(char *)(local_138[0] + 0x7f) < '\0') {
      plVar2 = (long *)*plVar2;
    }
    local_68 = *(undefined8 *)(param_1 + 0x3a0);
    local_60 = &DAT_aaaaaaaa0000000b;
    lStack_58 = *(long *)(param_1 + 0x3a8);
    if (-1 < *(char *)(param_1 + 0x3bf)) {
      lStack_58 = param_1 + 0x3a8;
    }
    local_40 = 0xaaaaaaaa00000006;
    local_50 = 0xaaaaaaaa00000010;
    puStack_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_138[0] + 0x38,&DAT_0a518134,plVar2,&local_68,2);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_138);
  }
  _free(*(void **)(param_1 + 0x3d0));
  if (*(char *)(param_1 + 0x3bf) < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x3a8),*(ulong *)(param_1 + 0x3b8) & 0x7fffffffffffffff);
  }
  if (*(long *)(param_1 + 8) != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


