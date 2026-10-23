// Ghidra inferred pseudocode; requested=0x30c3c34
// entry=030c3a3c end=030c3ceb

void FUN_030c3a3c(undefined8 *param_1)

{
  undefined1 **ppuVar1;
  undefined1 uVar2;
  long lVar3;
  int iVar4;
  uint uVar5;
  undefined1 *puVar6;
  undefined1 *puVar7;
  undefined1 *puVar8;
  ulong uVar9;
  long lVar10;
  undefined1 *local_1b0 [2];
  undefined7 local_1a0;
  char cStack_199;
  undefined1 auStack_198 [144];
  undefined1 *local_108;
  undefined1 local_100 [72];
  undefined1 **local_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_1b0);
    ppuVar1 = (undefined1 **)local_1b0[0];
    if (-1 < cStack_199) {
      ppuVar1 = local_1b0;
    }
    if ((DAT_0a3d8991 & 1) == 0) {
      DAT_0a3d8988._0_1_ = s_mm_cgi_hest__0875d530[0];
      DAT_0a3d8988._1_1_ = s_mm_cgi_hest__0875d530[1];
      DAT_0a3d8988._2_1_ = s_mm_cgi_hest__0875d530[2];
      DAT_0a3d8988._3_1_ = s_mm_cgi_hest__0875d530[3];
      DAT_0a3d8988._4_1_ = s_mm_cgi_hest__0875d530[4];
      DAT_0a3d8988._5_1_ = s_mm_cgi_hest__0875d530[5];
      DAT_0a3d8988._6_1_ = s_mm_cgi_hest__0875d530[6];
      DAT_0a3d8988._7_1_ = s_mm_cgi_hest__0875d530[7];
      DAT_0a3d8990 = 0;
      DAT_0a3d8991 = 1;
    }
    if ((DAT_0a3d89bb & 1) == 0) {
      DAT_0a3d89b0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a3d89b0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a3d89b0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a3d89b0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a3d89b0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a3d89b0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a3d89b0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a3d89b0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a3d89b8 = 0x2928;
      DAT_0a3d89ba = 0;
      DAT_0a3d89bb = 1;
    }
    FUN_05e1d050(auStack_198,2,ppuVar1,&DAT_0a3d8988,&DAT_0a3d89b0,0xf1,0,0);
    uVar5 = *(uint *)(param_1 + 1);
    local_108 = local_100;
    if ((DAT_0a3d8966 & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a3d891e)[uVar9] = (&DAT_088ad8be)[uVar9] + 0x8a ^ (&DAT_088ad8ae)[uVar9 & 0xf];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x48);
      DAT_0a3d8966 = 1;
    }
    uVar9 = (ulong)uVar5;
    lVar3 = 0;
    do {
      lVar10 = lVar3;
      uVar5 = (uint)uVar9;
      local_100[lVar10] = (&DAT_0a3d891e)[uVar5 + (int)(uVar9 / 10) * -10 + 0x23];
      uVar9 = uVar9 / 10;
      lVar3 = lVar10 + 1;
    } while (9 < uVar5);
    local_100[lVar10 + 1] = 0;
    if (8 < lVar10 + 8U) {
      puVar8 = local_100;
      puVar6 = local_100 + lVar10;
      do {
        puVar8 = puVar8 + 1;
        uVar2 = *puVar6;
        puVar7 = puVar6 + -1;
        *puVar6 = puVar8[-1];
        puVar8[-1] = uVar2;
        puVar6 = puVar7;
      } while (puVar8 < puVar7);
    }
    if ((DAT_0a3d89db & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a3d89bc)[uVar9] = (&DAT_088ad9ff)[uVar9] + 0x8a ^ (&DAT_088ad9ef)[uVar9 & 0xf];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x1f);
      DAT_0a3d89db = 1;
    }
    uStack_a8 = 0;
    local_b0 = 0;
    local_b8 = &local_108;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    local_60 = 0;
    uStack_48 = 0;
    local_50 = 0;
    local_40 = 0;
    FUN_05e1d31c(auStack_198,&DAT_0a3d89bc,&local_b8);
    thunk_FUN_05e1d0bc(auStack_198);
    if (cStack_199 < '\0') {
      __ZdlPvm(local_1b0[0],CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff);
    }
  }
  (**(code **)(*(long *)*param_1 + 0x30))((long *)*param_1,*(undefined4 *)(param_1 + 1));
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


