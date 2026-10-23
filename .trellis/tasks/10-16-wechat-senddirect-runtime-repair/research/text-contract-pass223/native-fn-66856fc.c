// Ghidra inferred pseudocode; requested=0x66856fc
// entry=066856fc end=066859c3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_066856fc(undefined8 *param_1)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  long *plVar4;
  long local_118 [7];
  undefined1 auStack_e0 [48];
  undefined8 **local_b0 [2];
  char local_99;
  undefined1 *local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar2 = FUN_06674d5c();
  if (lVar2 < 0) {
    uVar3 = ___cxa_allocate_exception(0x10);
    FUN_066684a8(uVar3,lVar2);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar3,&PTR_DAT_09fb1c88,__ZNSt9exceptionD2Ev);
  }
  iVar1 = FUN_06668c3c(*param_1);
  if (iVar1 == 2) {
    if ((DAT_0a518965 & 1) == 0) {
      DAT_0a518960 = (undefined4)ram0x08782918;
      DAT_0a518964 = 0;
      DAT_0a518965 = 1;
    }
    if ((DAT_0a51896e & 1) == 0) {
      DAT_0a518968 = (undefined4)DAT_08728748;
      DAT_0a51896c = 0x74;
      DAT_0a51896e = 1;
    }
    if ((DAT_0a51897e & 1) == 0) {
      DAT_0a518970._0_1_ = s_coroutinCoAsync_087e2ce0[0];
      DAT_0a518970._1_1_ = s_coroutinCoAsync_087e2ce0[1];
      DAT_0a518970._2_1_ = s_coroutinCoAsync_087e2ce0[2];
      DAT_0a518970._3_1_ = s_coroutinCoAsync_087e2ce0[3];
      DAT_0a518970._4_1_ = s_coroutinCoAsync_087e2ce0[4];
      DAT_0a518970._5_1_ = s_coroutinCoAsync_087e2ce0[5];
      DAT_0a518970._6_1_ = s_coroutinCoAsync_087e2ce0[6];
      DAT_0a518970._7_1_ = s_coroutinCoAsync_087e2ce0[7];
      DAT_0a518978 = (undefined4)DAT_096865d8;
      DAT_0a51897c = 0x70;
      DAT_0a51897e = 1;
    }
    FUN_0668db5c(local_118,&DAT_0a518960,&DAT_0a518968,&DAT_0a518970,0x1f0000b000);
    if ((DAT_0a51898e & 1) == 0) {
      DAT_0a518980._0_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[0];
      DAT_0a518980._1_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[1];
      DAT_0a518980._2_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[2];
      DAT_0a518980._3_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[3];
      DAT_0a518980._4_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[4];
      DAT_0a518980._5_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[5];
      DAT_0a518980._6_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[6];
      DAT_0a518980._7_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[7];
      DAT_0a518988 = (undefined4)DAT_084d8788;
      DAT_0a51898c = 0x20;
      DAT_0a51898e = 1;
    }
    if (-1 < local_99) {
      local_b0[0] = local_b0;
    }
    local_40 = 0xaaaaaaaa00000006;
    local_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(auStack_e0,&DAT_0a518980,local_b0[0],&local_48,0);
    if ((DAT_0a5189bb & 1) == 0) {
      _DAT_0a518990 = CONCAT44((int)DAT_08744798,(int)DAT_08728748);
      uRam000000000a518998 = CONCAT44((int)DAT_08487478,(int)DAT_088bab90);
      _DAT_0a5189a0 = CONCAT44((int)DAT_08558f90,(int)DAT_084d4af0);
      uRam000000000a5189a8 = CONCAT44((int)DAT_084c7770,(int)DAT_084cadd8);
      DAT_0a5189b0 = CONCAT44((int)DAT_084d8768,(int)DAT_084c7778);
      DAT_0a5189b8 = 0x2164;
      DAT_0a5189ba = 0;
      DAT_0a5189bb = 1;
    }
    plVar4 = (long *)(local_118[0] + 0x68);
    if (*(char *)(local_118[0] + 0x7f) < '\0') {
      plVar4 = (long *)*plVar4;
    }
    local_40 = 0xaaaaaaaa00000006;
    local_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_118[0] + 0x38,&DAT_0a518990,plVar4,&local_48,0);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_118);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


