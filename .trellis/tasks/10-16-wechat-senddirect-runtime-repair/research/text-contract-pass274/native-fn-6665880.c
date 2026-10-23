// Ghidra inferred pseudocode; requested=0x6665880
// entry=06665880 end=06665e27

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06665880(long param_1,int param_2)

{
  int iVar1;
  long lVar2;
  ulong uVar3;
  undefined8 uVar4;
  long *plVar5;
  long local_118 [7];
  undefined1 auStack_e0 [48];
  undefined8 **local_b0 [2];
  char local_99;
  long local_48;
  undefined8 local_40;
  undefined1 *local_38;
  undefined8 local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (param_2 == 1) {
    FUN_0668e56c();
  }
  else {
    lVar2 = FUN_0668d9e8(5);
    if (lVar2 == 0) {
      FUN_0668e658();
    }
    else {
      if ((DAT_0a516ff2 & 1) == 0) {
        DAT_0a516fe8._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x10];
        DAT_0a516fe8._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x11];
        DAT_0a516fe8._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x12];
        DAT_0a516fe8._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x13];
        DAT_0a516fe8._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x14];
        DAT_0a516fe8._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x15];
        DAT_0a516fe8._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x16];
        DAT_0a516fe8._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x17];
        DAT_0a516ff0 = 99;
        DAT_0a516ff2 = 1;
      }
      if ((DAT_0a5172c4 & 1) == 0) {
        DAT_0a5172c0 = (undefined4)DAT_084df390;
        DAT_0a5172c4 = 1;
      }
      if ((DAT_0a517013 & 1) == 0) {
        DAT_0a517008._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x18];
        DAT_0a517008._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x19];
        DAT_0a517008._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1a];
        DAT_0a517008._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1b];
        DAT_0a517008._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1c];
        DAT_0a517008._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1d];
        DAT_0a517008._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1e];
        DAT_0a517008._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1f];
        DAT_0a517010 = 0x7070;
        DAT_0a517012 = 0;
        DAT_0a517013 = 1;
      }
      FUN_0668db5c(local_118,&DAT_0a516fe8,&DAT_0a5172c0,&DAT_0a517008,0x1b50000a800);
      if ((DAT_0a5172df & 1) == 0) {
        _DAT_0a5172c8 = CONCAT44((int)DAT_096830c8,(int)DAT_08b2fcb0);
        uRam000000000a5172d0 = CONCAT44((int)ram0x08480938,(int)DAT_08771500);
        DAT_0a5172d8 = (undefined4)DAT_08b72b50;
        DAT_0a5172dc = 0x295f;
        DAT_0a5172de = 0;
        DAT_0a5172df = 1;
      }
      if ((DAT_0a517302 & 1) == 0) {
        _DAT_0a5172e0 = CONCAT44((int)ram0x08602690,(int)DAT_0853bef0);
        uRam000000000a5172e8 = CONCAT44((int)DAT_096830d0,(int)DAT_08738c08);
        _DAT_0a5172f0 = CONCAT44((int)DAT_0849d5c0,(int)DAT_096830d8);
        uRam000000000a5172f8 = CONCAT44((int)DAT_096830e8,(int)DAT_096830e0);
        DAT_0a517300 = 0x74;
        DAT_0a517302 = 1;
      }
      if (-1 < local_99) {
        local_b0[0] = local_b0;
      }
      FUN_06667cd0(auStack_e0,&DAT_0a5172c8,local_b0[0],&DAT_0a5172e0);
      thunk_FUN_0668e878(local_118);
    }
  }
  while( true ) {
    iVar1 = FUN_06664994(param_1);
    while (2 < iVar1 + 2U) {
      if (iVar1 == -3) {
        FUN_06663c1c(param_1);
      }
      iVar1 = FUN_06664994(param_1);
    }
    if (iVar1 == -1) break;
    if (iVar1 == -2) {
      uVar3 = FUN_0668dad0(2);
      if ((uVar3 & 1) != 0) {
        if ((DAT_0a516ff2 & 1) == 0) {
          DAT_0a516fe8._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x10];
          DAT_0a516fe8._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x11];
          DAT_0a516fe8._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x12];
          DAT_0a516fe8._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x13];
          DAT_0a516fe8._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x14];
          DAT_0a516fe8._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x15];
          DAT_0a516fe8._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x16];
          DAT_0a516fe8._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x17];
          DAT_0a516ff0 = 99;
          DAT_0a516ff2 = 1;
        }
        if ((DAT_0a5172c4 & 1) == 0) {
          DAT_0a5172c0 = (undefined4)DAT_084df390;
          DAT_0a5172c4 = 1;
        }
        if ((DAT_0a517013 & 1) == 0) {
          DAT_0a517008._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x18];
          DAT_0a517008._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x19];
          DAT_0a517008._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1a];
          DAT_0a517008._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1b];
          DAT_0a517008._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1c];
          DAT_0a517008._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1d];
          DAT_0a517008._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1e];
          DAT_0a517008._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1f];
          DAT_0a517010 = 0x7070;
          DAT_0a517012 = 0;
          DAT_0a517013 = 1;
        }
        FUN_0668db5c(local_118,&DAT_0a516fe8,&DAT_0a5172c0,&DAT_0a517008,0x1b900004800);
        if ((DAT_0a51731a & 1) == 0) {
          _DAT_0a517304 = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
          uRam000000000a51730c = CONCAT44((int)DAT_0852d448,(int)DAT_096830f0);
          DAT_0a517314 = (undefined4)DAT_08628368;
          DAT_0a517318 = 0x79;
          DAT_0a51731a = 1;
        }
        plVar5 = (long *)(local_118[0] + 0x68);
        if (*(char *)(local_118[0] + 0x7f) < '\0') {
          plVar5 = (long *)*plVar5;
        }
        local_48 = *(long *)(param_1 + 0x80);
        if (-1 < *(char *)(param_1 + 0x97)) {
          local_48 = param_1 + 0x80;
        }
        local_40 = 0xaaaaaaaa00000010;
        local_30 = 0xaaaaaaaa00000006;
        local_38 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(local_118[0] + 0x38,&DAT_0a517304,plVar5,&local_48,1);
        FUN_0668dbac();
        thunk_FUN_0668e878(local_118);
      }
      uVar4 = 0;
LAB_06665dfc:
      if (*(long *)PTR____stack_chk_guard_09b36c98 != local_28) {
                    /* WARNING: Subroutine does not return */
        ___stack_chk_fail(uVar4);
      }
      return;
    }
  }
  iVar1 = FUN_0668dad0(2);
  if (iVar1 != 0) {
    if ((DAT_0a516ff2 & 1) == 0) {
      DAT_0a516fe8._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x10];
      DAT_0a516fe8._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x11];
      DAT_0a516fe8._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x12];
      DAT_0a516fe8._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x13];
      DAT_0a516fe8._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x14];
      DAT_0a516fe8._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x15];
      DAT_0a516fe8._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x16];
      DAT_0a516fe8._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x17];
      DAT_0a516ff0 = 99;
      DAT_0a516ff2 = 1;
    }
    if ((DAT_0a5172c4 & 1) == 0) {
      DAT_0a5172c0 = (undefined4)DAT_084df390;
      DAT_0a5172c4 = 1;
    }
    if ((DAT_0a517013 & 1) == 0) {
      DAT_0a517008._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x18];
      DAT_0a517008._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x19];
      DAT_0a517008._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1a];
      DAT_0a517008._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1b];
      DAT_0a517008._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1c];
      DAT_0a517008._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1d];
      DAT_0a517008._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1e];
      DAT_0a517008._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1f];
      DAT_0a517010 = 0x7070;
      DAT_0a517012 = 0;
      DAT_0a517013 = 1;
    }
    FUN_0668db5c(local_118,&DAT_0a516fe8,&DAT_0a5172c0,&DAT_0a517008,0x1bd00004800);
    if ((DAT_0a517331 & 1) == 0) {
      _DAT_0a51731c = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
      uRam000000000a517324 = CONCAT44((int)DAT_0852d448,(int)DAT_096830f0);
      DAT_0a51732c = (undefined4)DAT_0848c320;
      DAT_0a517330 = 0;
      DAT_0a517331 = 1;
    }
    plVar5 = (long *)(local_118[0] + 0x68);
    if (*(char *)(local_118[0] + 0x7f) < '\0') {
      plVar5 = (long *)*plVar5;
    }
    local_48 = *(long *)(param_1 + 0x80);
    if (-1 < *(char *)(param_1 + 0x97)) {
      local_48 = param_1 + 0x80;
    }
    local_40 = 0xaaaaaaaa00000010;
    local_30 = 0xaaaaaaaa00000006;
    local_38 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_118[0] + 0x38,&DAT_0a51731c,plVar5,&local_48,1);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_118);
  }
  uVar4 = 1;
  goto LAB_06665dfc;
}


