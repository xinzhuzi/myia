// Ghidra inferred pseudocode; requested=0x6669058
// entry=06669058 end=066692c7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06669058(long param_1,undefined8 *param_2,undefined8 param_3)

{
  int iVar1;
  ulong uVar2;
  long *plVar3;
  undefined8 uVar4;
  long local_138 [26];
  undefined *local_68;
  undefined8 local_60;
  undefined *puStack_58;
  undefined8 local_50;
  undefined1 *puStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  __ZNSt3__115recursive_mutex4lockEv(param_1 + 0x10);
  if (*(int *)(param_1 + 0x9c) == 0) {
    *(int *)(param_1 + 0x9c) = (int)param_3;
    uVar4 = *param_2;
    *param_2 = 0;
    plVar3 = *(long **)(param_1 + 0x90);
    *(undefined8 *)(param_1 + 0x90) = uVar4;
    if (plVar3 != (long *)0x0) {
      (**(code **)(*plVar3 + 8))();
    }
    uVar4 = *(undefined8 *)(param_1 + 0x80);
    __ZNSt3__15mutex4lockEv(uVar4);
    __ZNSt3__15mutex6unlockEv(uVar4);
    __ZNSt3__118condition_variable10notify_oneEv(param_1 + 0x50);
    if (*(long *)(param_1 + 0xd8) != 0) {
      FUN_066692f0(param_1,param_3);
    }
  }
  else {
    uVar2 = FUN_0668dad0(3);
    if ((uVar2 & 1) != 0) {
      if ((DAT_0a51749d & 1) == 0) {
        DAT_0a517498 = (undefined4)ram0x08782918;
        DAT_0a51749c = 0;
        DAT_0a51749d = 1;
      }
      if ((DAT_0a517525 & 1) == 0) {
        uRam000000000a517518._0_1_ = s_operation_cancelstart_resolve_re_096839e0[0x18];
        uRam000000000a517518._1_1_ = s_operation_cancelstart_resolve_re_096839e0[0x19];
        uRam000000000a517518._2_1_ = s_operation_cancelstart_resolve_re_096839e0[0x1a];
        uRam000000000a517518._3_1_ = s_operation_cancelstart_resolve_re_096839e0[0x1b];
        uRam000000000a517518._4_1_ = s_operation_cancelstart_resolve_re_096839e0[0x1c];
        uRam000000000a517518._5_1_ = s_operation_cancelstart_resolve_re_096839e0[0x1d];
        uRam000000000a517518._6_1_ = s_operation_cancelstart_resolve_re_096839e0[0x1e];
        uRam000000000a517518._7_1_ = s_operation_cancelstart_resolve_re_096839e0[0x1f];
        DAT_0a517510 = s_operation_cancelstart_resolve_re_096839e0[0x10];
        DAT_0a517510_1._0_1_ = s_operation_cancelstart_resolve_re_096839e0[0x11];
        DAT_0a517510_1._1_1_ = s_operation_cancelstart_resolve_re_096839e0[0x12];
        DAT_0a517510_1._2_1_ = s_operation_cancelstart_resolve_re_096839e0[0x13];
        DAT_0a517510_1._3_1_ = s_operation_cancelstart_resolve_re_096839e0[0x14];
        DAT_0a517510_1._4_1_ = s_operation_cancelstart_resolve_re_096839e0[0x15];
        DAT_0a517510_1._5_1_ = s_operation_cancelstart_resolve_re_096839e0[0x16];
        DAT_0a517510_1._6_1_ = s_operation_cancelstart_resolve_re_096839e0[0x17];
        DAT_0a517520 = (undefined4)DAT_084f2d40;
        DAT_0a517524 = 0;
        DAT_0a517525 = 1;
      }
      if ((DAT_0a5174bc & 1) == 0) {
        DAT_0a5174b0._0_1_ = s_LoginOldpromise_rgs__08a9dfa8[8];
        DAT_0a5174b0._1_1_ = s_LoginOldpromise_rgs__08a9dfa8[9];
        DAT_0a5174b0._2_1_ = s_LoginOldpromise_rgs__08a9dfa8[10];
        DAT_0a5174b0._3_1_ = s_LoginOldpromise_rgs__08a9dfa8[0xb];
        DAT_0a5174b0._4_1_ = s_LoginOldpromise_rgs__08a9dfa8[0xc];
        DAT_0a5174b0._5_1_ = s_LoginOldpromise_rgs__08a9dfa8[0xd];
        DAT_0a5174b0._6_1_ = s_LoginOldpromise_rgs__08a9dfa8[0xe];
        DAT_0a5174b0._7_1_ = s_LoginOldpromise_rgs__08a9dfa8[0xf];
        DAT_0a5174b8 = (undefined4)DAT_085722b0;
        DAT_0a5174bc = 1;
      }
      FUN_0668db5c(local_138,&DAT_0a517498,&DAT_0a517510,&DAT_0a5174b0,0xa700006800);
      iVar1 = *(int *)(param_1 + 0x9c);
      if ((DAT_0a51755d & 1) == 0) {
        uVar2 = 0;
        do {
          (&DAT_0a517526)[uVar2] = (&DAT_09683d21)[uVar2 & 0xf] ^ (&DAT_09683d31)[uVar2];
          uVar2 = uVar2 + 1;
        } while (uVar2 != 0x37);
        DAT_0a51755d = 1;
      }
      local_68 = (&PTR_s_pending_09fb1c60)[iVar1];
      puStack_58 = (&PTR_s_pending_09fb1c60)[(int)param_3];
      plVar3 = (long *)(local_138[0] + 0x68);
      if (*(char *)(local_138[0] + 0x7f) < '\0') {
        plVar3 = (long *)*plVar3;
      }
      local_60 = 0xaaaaaaaa00000010;
      local_40 = 0xaaaaaaaa00000006;
      local_50 = 0xaaaaaaaa00000010;
      puStack_48 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_138[0] + 0x38,&DAT_0a517526,plVar3,&local_68,2);
      FUN_0668dbac();
      thunk_FUN_0668e878(local_138);
    }
  }
  __ZNSt3__115recursive_mutex6unlockEv(param_1 + 0x10);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


