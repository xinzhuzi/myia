// Ghidra inferred pseudocode; requested=0x66650a0
// entry=066650a0 end=06665553

/* WARNING: Removing unreachable block (ram,0x06665524) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_066650a0(long *param_1,long param_2)

{
  undefined4 uVar1;
  uint3 uVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  long lVar6;
  ulong uVar7;
  undefined8 ***pppuVar8;
  undefined4 uVar9;
  undefined8 **local_188 [2];
  undefined7 local_178;
  char cStack_171;
  undefined1 *local_b8;
  long *local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  long lStack_90;
  undefined8 local_88;
  undefined1 *puStack_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((DAT_0a517262 & 1) == 0) {
    DAT_0a517258 = s_try_run_run_taskk__a_096830a0._8_8_;
    DAT_0a517260 = 0x5f;
    DAT_0a517262 = 1;
  }
  if ((DAT_0a517280 & 1) == 0) {
    _DAT_0a517264 = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
    uRam000000000a51726c = CONCAT44((int)ram0x088df230,(int)DAT_084d8778);
    DAT_0a517274 = CONCAT44((int)DAT_084de5d8,(int)DAT_084cf930);
    DAT_0a51727c = (undefined4)ram0x084c9468;
    DAT_0a517280 = 1;
  }
  local_b8 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_06665720(local_188,&DAT_0a517258,&DAT_0a517264,param_1 + 0x10,param_2 + 8,param_2 + 0xc);
  pppuVar8 = (undefined8 ***)local_188[0];
  if (-1 < cStack_171) {
    pppuVar8 = local_188;
  }
  uStack_a0 = uStack_a0 & 0xffffffffffffff;
  local_b0 = (long *)((ulong)local_b0 & 0xffffffffffffff00);
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
  if ((DAT_0a517262 & 1) == 0) {
    DAT_0a517258._0_1_ = s_try_run_run_taskk__a_096830a0[8];
    DAT_0a517258._1_1_ = s_try_run_run_taskk__a_096830a0[9];
    DAT_0a517258._2_1_ = s_try_run_run_taskk__a_096830a0[10];
    DAT_0a517258._3_1_ = s_try_run_run_taskk__a_096830a0[0xb];
    DAT_0a517258._4_1_ = s_try_run_run_taskk__a_096830a0[0xc];
    DAT_0a517258._5_1_ = s_try_run_run_taskk__a_096830a0[0xd];
    DAT_0a517258._6_1_ = s_try_run_run_taskk__a_096830a0[0xe];
    DAT_0a517258._7_1_ = s_try_run_run_taskk__a_096830a0[0xf];
    DAT_0a517260 = 0x5f;
    DAT_0a517262 = 1;
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
  thunk_FUN_0668f12c(&local_b8,&DAT_0a516fe8,&DAT_0a517258,&DAT_0a517008,pppuVar8,0x1a100000000,
                     &local_b0);
  if (cStack_171 < '\0') {
    __ZdlPvm(local_188[0],CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
  }
  lVar4 = __ZNSt3__16chrono12steady_clock3nowEv();
  if (((*(long **)(param_2 + 0x10) != (long *)0x0) &&
      (iVar3 = (**(code **)(**(long **)(param_2 + 0x10) + 0x10))(), *(short *)(param_2 + 4) == 2))
     && (1 < iVar3 - 1U)) {
    uVar5 = (**(code **)(**(long **)(param_2 + 0x10) + 0x18))();
    (**(code **)(*param_1 + 0x48))(param_1,2,uVar5);
  }
  lVar6 = __ZNSt3__16chrono12steady_clock3nowEv();
  if ((499999999 < lVar6 - lVar4) && (uVar7 = FUN_0668dad0(4), (uVar7 & 1) != 0)) {
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
    if ((DAT_0a517262 & 1) == 0) {
      DAT_0a517258._0_1_ = s_try_run_run_taskk__a_096830a0[8];
      DAT_0a517258._1_1_ = s_try_run_run_taskk__a_096830a0[9];
      DAT_0a517258._2_1_ = s_try_run_run_taskk__a_096830a0[10];
      DAT_0a517258._3_1_ = s_try_run_run_taskk__a_096830a0[0xb];
      DAT_0a517258._4_1_ = s_try_run_run_taskk__a_096830a0[0xc];
      DAT_0a517258._5_1_ = s_try_run_run_taskk__a_096830a0[0xd];
      DAT_0a517258._6_1_ = s_try_run_run_taskk__a_096830a0[0xe];
      DAT_0a517258._7_1_ = s_try_run_run_taskk__a_096830a0[0xf];
      DAT_0a517260 = 0x5f;
      DAT_0a517262 = 1;
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
    FUN_0668db5c(local_188,&DAT_0a516fe8,&DAT_0a517258,&DAT_0a517008,0x1b000008800);
    if ((DAT_0a5172bd & 1) == 0) {
      uVar7 = 0;
      do {
        uVar9 = *(undefined4 *)((long)&DAT_09683606 + uVar7);
        uVar2 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
        uVar1 = *(undefined4 *)((long)&DAT_096835f2 + uVar7 % 0x14);
        *(uint *)((long)&DAT_0a517281 + uVar7) =
             CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar1 >> 0x18),
                      CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^ (byte)((uint)uVar1 >> 0x10),
                               CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar1 >> 8),
                                        (char)uVar2 + 0x8aU ^ (byte)uVar1)));
        uVar7 = uVar7 + 4;
      } while (uVar7 != 0x3c);
      DAT_0a5172bd = 1;
    }
    pppuVar8 = (undefined8 ***)(local_188[0] + 0xd);
    if (*(char *)((long)local_188[0] + 0x7f) < '\0') {
      pppuVar8 = (undefined8 ***)*pppuVar8;
    }
    local_b0 = (long *)param_1[0x10];
    if (-1 < *(char *)((long)param_1 + 0x97)) {
      local_b0 = param_1 + 0x10;
    }
    local_98 = 0xaaaaaaaa00000007;
    local_a8 = 0xaaaaaaaa00000010;
    uStack_a0 = CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_2 + 8));
    local_78 = 0xaaaaaaaa00000006;
    local_88 = 0xaaaaaaaa0000000a;
    puStack_80 = &DAT_aaaaaaaa00000000;
    lStack_90 = (lVar6 - lVar4) / 1000000;
    FUN_0668e1e4(local_188[0] + 7,&DAT_0a517281,pppuVar8,&local_b0,3);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_188);
  }
  if (local_b8 != (undefined1 *)0x0) {
    uVar5 = thunk_FUN_0668ef88();
    __ZdlPvm(uVar5,0xf8);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_70) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


