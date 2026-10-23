// Ghidra inferred pseudocode; requested=0x4668f94
// entry=04668f94 end=04669327

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04668f94(long param_1,ulong param_2)

{
  undefined1 **ppuVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long lVar4;
  int iVar5;
  undefined1 *puVar6;
  uint uVar7;
  undefined1 *puVar8;
  long lVar9;
  undefined1 *puVar10;
  ulong uVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  undefined1 *local_200 [2];
  undefined7 local_1f0;
  char cStack_1e9;
  undefined1 auStack_1e8 [144];
  undefined1 *local_158;
  undefined1 local_150 [72];
  undefined1 *local_108;
  undefined1 local_100 [72];
  undefined1 **local_b8;
  undefined1 **ppuStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 != 0) {
    FUN_0488143c(local_200);
    ppuVar1 = (undefined1 **)local_200[0];
    if (-1 < cStack_1e9) {
      ppuVar1 = local_200;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e5ef & 1) == 0) {
      DAT_0a45e5e0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[8];
      DAT_0a45e5e0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[9];
      DAT_0a45e5e0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[10];
      DAT_0a45e5e0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0xb];
      DAT_0a45e5e0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0xc];
      DAT_0a45e5e0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0xd];
      DAT_0a45e5e0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0xe];
      DAT_0a45e5e0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0xf];
      DAT_0a45e5e8 = (undefined4)DAT_0876b0c0;
      DAT_0a45e5ec = 0x6567;
      DAT_0a45e5ee = 0;
      DAT_0a45e5ef = 1;
    }
    FUN_05e1d050(auStack_1e8,2,ppuVar1,&DAT_0a45df80,&DAT_0a45e5e0,0x52f,0,0);
    uVar7 = *(uint *)(param_1 + 0x2b0);
    local_108 = (undefined1 *)0x0;
    if ((DAT_0a45e65a & 1) == 0) {
      uVar11 = 0;
      do {
        uVar12 = *(undefined4 *)((long)&DAT_08a1498d + uVar11);
        uVar3 = CONCAT12((char)((uint)uVar12 >> 8),(short)uVar12) & 0xff00ff;
        uVar13 = *(undefined4 *)((long)&DAT_08a14979 + uVar11 % 0x14);
        *(uint *)((long)&DAT_0a45e612 + uVar11) =
             CONCAT13((char)((uint)uVar12 >> 0x18) + 0x8aU ^ (byte)((uint)uVar13 >> 0x18),
                      CONCAT12((char)((uint)uVar12 >> 0x10) + 0x8aU ^ (byte)((uint)uVar13 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar13 >> 8),
                                        (char)uVar3 + 0x8aU ^ (byte)uVar13)));
        uVar11 = uVar11 + 4;
      } while (uVar11 != 0x48);
      DAT_0a45e65a = 1;
    }
    uVar11 = (ulong)uVar7;
    lVar4 = 0;
    do {
      lVar9 = lVar4;
      uVar7 = (uint)uVar11;
      local_100[lVar9] =
           *(undefined1 *)((long)&DAT_0a45e612 + (ulong)(uVar7 + (int)(uVar11 / 10) * -10 + 0x23));
      uVar11 = uVar11 / 10;
      lVar4 = lVar9 + 1;
    } while (9 < uVar7);
    local_100[lVar9 + 1] = 0;
    if (8 < lVar9 + 8U) {
      puVar10 = local_100;
      puVar6 = local_100 + lVar9;
      do {
        puVar10 = puVar10 + 1;
        uVar2 = *puVar6;
        puVar8 = puVar6 + -1;
        *puVar6 = puVar10[-1];
        puVar10[-1] = uVar2;
        puVar6 = puVar8;
      } while (puVar10 < puVar8);
    }
    local_108 = local_100;
    local_158 = local_150;
    lVar4 = 0;
    uVar11 = param_2;
    do {
      lVar9 = lVar4;
      uVar7 = (uint)uVar11;
      local_150[lVar9] =
           *(undefined1 *)
            ((long)&DAT_0a45e612 + (ulong)(uVar7 + (int)((uVar11 & 0xffffffff) / 10) * -10 + 0x23));
      lVar4 = lVar9 + 1;
      uVar11 = (uVar11 & 0xffffffff) / 10;
    } while (9 < uVar7);
    local_150[lVar9 + 1] = 0;
    if (8 < lVar9 + 8U) {
      puVar10 = local_150;
      puVar6 = local_150 + lVar9;
      do {
        puVar10 = puVar10 + 1;
        uVar2 = *puVar6;
        puVar8 = puVar6 + -1;
        *puVar6 = puVar10[-1];
        puVar10[-1] = uVar2;
        puVar6 = puVar8;
      } while (puVar10 < puVar8);
    }
    if ((DAT_0a45e611 & 1) == 0) {
      _DAT_0a45e5f0 = CONCAT44((int)DAT_084b0358,(int)DAT_08625560);
      uRam000000000a45e5f8 = CONCAT44((int)DAT_0852d518,(int)DAT_088bb3d0);
      _DAT_0a45e600 = CONCAT44((int)DAT_0848a050,(int)DAT_084f2d48);
      uRam000000000a45e608 = CONCAT44((int)DAT_084d57c0,(int)DAT_086f3dc0);
      DAT_0a45e610 = 0;
      DAT_0a45e611 = 1;
    }
    local_b8 = &local_108;
    ppuStack_b0 = &local_158;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    uStack_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    uStack_70 = 0;
    uStack_78 = 0;
    uStack_60 = 0;
    local_68 = 0;
    uStack_50 = 0;
    uStack_58 = 0;
    uStack_40 = 0;
    local_48 = 0;
    FUN_05e1d31c(auStack_1e8,&DAT_0a45e5f0,&local_b8);
    thunk_FUN_05e1d0bc(auStack_1e8);
    if (cStack_1e9 < '\0') {
      __ZdlPvm(local_200[0],CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
    }
  }
  *(int *)(param_1 + 0x2b0) = (int)param_2;
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


