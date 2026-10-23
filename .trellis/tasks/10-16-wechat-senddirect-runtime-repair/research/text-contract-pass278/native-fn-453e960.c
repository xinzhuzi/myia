// Ghidra inferred pseudocode; requested=0x453e960
// entry=0453e904 end=0453ec43

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0453e904(long param_1)

{
  int iVar1;
  long *plVar2;
  long local_108 [26];
  undefined1 *local_38;
  undefined8 local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  *(undefined1 *)(param_1 + 0x40) = 1;
  if (*(long *)(param_1 + 0x10) != 0) {
    FUN_0668272c(*(long *)(param_1 + 0x10) + 8);
    FUN_066823c4(*(long *)(param_1 + 0x10) + 8);
    if (*(long **)(param_1 + 0x10) != (long *)0x0) {
      (**(code **)(**(long **)(param_1 + 0x10) + 8))();
    }
    *(undefined8 *)(param_1 + 0x10) = 0;
  }
  if (*(long *)(param_1 + 8) != 0) {
    FUN_0668272c(*(long *)(param_1 + 8) + 8);
    iVar1 = FUN_0668dad0(2);
    if (iVar1 != 0) {
      if ((DAT_0a45582d & 1) == 0) {
        DAT_0a455828 = (undefined4)ram0x08782918;
        DAT_0a45582c = 0;
        DAT_0a45582d = 1;
      }
      if ((DAT_0a455841 & 1) == 0) {
        uRam000000000a455838._0_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x18];
        uRam000000000a455838._1_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x19];
        uRam000000000a455838._2_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1a];
        uRam000000000a455838._3_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1b];
        uRam000000000a455838._4_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1c];
        uRam000000000a455838._5_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1d];
        uRam000000000a455838._6_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1e];
        uRam000000000a455838._7_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1f];
        DAT_0a455830 = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x10];
        DAT_0a455830_1._0_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x11];
        DAT_0a455830_1._1_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x12];
        DAT_0a455830_1._2_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x13];
        DAT_0a455830_1._3_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x14];
        DAT_0a455830_1._4_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x15];
        DAT_0a455830_1._5_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x16];
        DAT_0a455830_1._6_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x17];
        DAT_0a455840 = 0;
        DAT_0a455841 = 1;
      }
      if ((DAT_0a455765 & 1) == 0) {
        DAT_0a455758._0_1_ = s_coroutinCoAsync_087e2ce0[0];
        DAT_0a455758._1_1_ = s_coroutinCoAsync_087e2ce0[1];
        DAT_0a455758._2_1_ = s_coroutinCoAsync_087e2ce0[2];
        DAT_0a455758._3_1_ = s_coroutinCoAsync_087e2ce0[3];
        DAT_0a455758._4_1_ = s_coroutinCoAsync_087e2ce0[4];
        DAT_0a455758._5_1_ = s_coroutinCoAsync_087e2ce0[5];
        DAT_0a455758._6_1_ = s_coroutinCoAsync_087e2ce0[6];
        DAT_0a455758._7_1_ = s_coroutinCoAsync_087e2ce0[7];
        DAT_0a455760 = (undefined4)DAT_084c8598;
        DAT_0a455764 = 0;
        DAT_0a455765 = 1;
      }
      FUN_0668db5c(local_108,&DAT_0a455828,&DAT_0a455830,&DAT_0a455758,0x15300004800);
      if ((DAT_0a455853 & 1) == 0) {
        DAT_0a455848._0_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x20];
        DAT_0a455848._1_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x21];
        DAT_0a455848._2_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x22];
        DAT_0a455848._3_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x23];
        DAT_0a455848._4_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x24];
        DAT_0a455848._5_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x25];
        DAT_0a455848._6_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x26];
        DAT_0a455848._7_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x27];
        DAT_0a455850 = 0x6e69;
        DAT_0a455852 = 0;
        DAT_0a455853 = 1;
      }
      plVar2 = (long *)(local_108[0] + 0x68);
      if (*(char *)(local_108[0] + 0x7f) < '\0') {
        plVar2 = (long *)*plVar2;
      }
      local_30 = 0xaaaaaaaa00000006;
      local_38 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_108[0] + 0x38,&DAT_0a455848,plVar2,&local_38,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(local_108);
    }
    FUN_066823c4(*(long *)(param_1 + 8) + 8);
    iVar1 = FUN_0668dad0(2);
    if (iVar1 != 0) {
      if ((DAT_0a45582d & 1) == 0) {
        DAT_0a455828 = (undefined4)ram0x08782918;
        DAT_0a45582c = 0;
        DAT_0a45582d = 1;
      }
      if ((DAT_0a455841 & 1) == 0) {
        uRam000000000a455838._0_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x18];
        uRam000000000a455838._1_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x19];
        uRam000000000a455838._2_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1a];
        uRam000000000a455838._3_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1b];
        uRam000000000a455838._4_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1c];
        uRam000000000a455838._5_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1d];
        uRam000000000a455838._6_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1e];
        uRam000000000a455838._7_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x1f];
        DAT_0a455830 = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x10];
        DAT_0a455830_1._0_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x11];
        DAT_0a455830_1._1_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x12];
        DAT_0a455830_1._2_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x13];
        DAT_0a455830_1._3_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x14];
        DAT_0a455830_1._4_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x15];
        DAT_0a455830_1._5_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x16];
        DAT_0a455830_1._6_1_ = s_coLaunchInterfaccancelAndJoinAll_089febc0[0x17];
        DAT_0a455840 = 0;
        DAT_0a455841 = 1;
      }
      if ((DAT_0a455765 & 1) == 0) {
        DAT_0a455758._0_1_ = s_coroutinCoAsync_087e2ce0[0];
        DAT_0a455758._1_1_ = s_coroutinCoAsync_087e2ce0[1];
        DAT_0a455758._2_1_ = s_coroutinCoAsync_087e2ce0[2];
        DAT_0a455758._3_1_ = s_coroutinCoAsync_087e2ce0[3];
        DAT_0a455758._4_1_ = s_coroutinCoAsync_087e2ce0[4];
        DAT_0a455758._5_1_ = s_coroutinCoAsync_087e2ce0[5];
        DAT_0a455758._6_1_ = s_coroutinCoAsync_087e2ce0[6];
        DAT_0a455758._7_1_ = s_coroutinCoAsync_087e2ce0[7];
        DAT_0a455760 = (undefined4)DAT_084c8598;
        DAT_0a455764 = 0;
        DAT_0a455765 = 1;
      }
      FUN_0668db5c(local_108,&DAT_0a455828,&DAT_0a455830,&DAT_0a455758,0x15500004800);
      if ((DAT_0a455861 & 1) == 0) {
        DAT_0a455858._0_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x28];
        DAT_0a455858._1_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x29];
        DAT_0a455858._2_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x2a];
        DAT_0a455858._3_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x2b];
        DAT_0a455858._4_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x2c];
        DAT_0a455858._5_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x2d];
        DAT_0a455858._6_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x2e];
        DAT_0a455858._7_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x2f];
        DAT_0a455860 = 0;
        DAT_0a455861 = 1;
      }
      plVar2 = (long *)(local_108[0] + 0x68);
      if (*(char *)(local_108[0] + 0x7f) < '\0') {
        plVar2 = (long *)*plVar2;
      }
      local_30 = 0xaaaaaaaa00000006;
      local_38 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_108[0] + 0x38,&DAT_0a455858,plVar2,&local_38,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(local_108);
    }
  }
  FUN_0668da74();
  FUN_0668dd34();
  FUN_0668da74();
  FUN_0668e174();
  FUN_0668da74();
  FUN_0668d6e4();
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


