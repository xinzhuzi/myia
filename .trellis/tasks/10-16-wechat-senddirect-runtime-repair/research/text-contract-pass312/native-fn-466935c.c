// Ghidra inferred pseudocode; requested=0x466935c
// entry=0466935c end=0466973f

void FUN_0466935c(long param_1,undefined4 *param_2)

{
  undefined8 ******ppppppuVar1;
  undefined1 uVar2;
  ushort uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  long lVar6;
  int iVar7;
  uint uVar8;
  undefined1 *puVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  ulong uVar12;
  long lVar13;
  undefined8 *****local_2f0 [2];
  undefined7 local_2e0;
  char cStack_2d9;
  undefined1 auStack_2d8 [144];
  undefined8 *local_248;
  undefined1 local_240;
  undefined1 *local_1f8;
  undefined1 local_1f0 [72];
  undefined8 *local_1a8;
  undefined1 local_1a0;
  undefined8 *local_158;
  undefined1 local_150;
  char *local_108;
  char acStack_100 [72];
  char **local_b8;
  undefined8 **ppuStack_b0;
  undefined8 **local_a8;
  undefined1 **ppuStack_a0;
  undefined8 **local_98;
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
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(local_2f0);
    ppppppuVar1 = (undefined8 ******)local_2f0[0];
    if (-1 < cStack_2d9) {
      ppppppuVar1 = local_2f0;
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
    if ((DAT_0a45df9d & 1) == 0) {
      DAT_0a45df90._0_1_ = s_SetProxyProcessProxy_08618548[0];
      DAT_0a45df90._1_1_ = s_SetProxyProcessProxy_08618548[1];
      DAT_0a45df90._2_1_ = s_SetProxyProcessProxy_08618548[2];
      DAT_0a45df90._3_1_ = s_SetProxyProcessProxy_08618548[3];
      DAT_0a45df90._4_1_ = s_SetProxyProcessProxy_08618548[4];
      DAT_0a45df90._5_1_ = s_SetProxyProcessProxy_08618548[5];
      DAT_0a45df90._6_1_ = s_SetProxyProcessProxy_08618548[6];
      DAT_0a45df90._7_1_ = s_SetProxyProcessProxy_08618548[7];
      DAT_0a45df98 = (undefined4)DAT_084d8880;
      DAT_0a45df9c = 0;
      DAT_0a45df9d = 1;
    }
    FUN_05e1d050(auStack_2d8,2,ppppppuVar1,&DAT_0a45df80,&DAT_0a45df90,0xbd,0,0);
    if ((DAT_0a45e7e9 & 1) == 0) {
      DAT_0a45e7e6 = 0x6425;
      DAT_0a45e7e8 = 0;
      DAT_0a45e7e9 = 1;
    }
    _snprintf(acStack_100,0x41,(char *)&DAT_0a45e7e6);
    local_108 = acStack_100;
    local_158 = *(undefined8 **)(param_2 + 2);
    if (-1 < *(char *)((long)param_2 + 0x1f)) {
      local_158 = (undefined8 *)(param_2 + 2);
    }
    local_150 = 0;
    local_1a8 = *(undefined8 **)(param_2 + 8);
    if (-1 < *(char *)((long)param_2 + 0x37)) {
      local_1a8 = (undefined8 *)(param_2 + 8);
    }
    local_1a0 = 0;
    uVar3 = *(ushort *)(param_2 + 0xe);
    local_1f8 = local_1f0;
    if ((DAT_0a45e65a & 1) == 0) {
      uVar12 = 0;
      do {
        uVar4 = *(undefined4 *)((long)&DAT_08a1498d + uVar12);
        uVar5 = *(undefined4 *)((long)&DAT_08a14979 + uVar12 % 0x14);
        *(uint *)((long)&DAT_0a45e612 + uVar12) =
             CONCAT13((char)((uint)uVar4 >> 0x18) + 0x8aU ^ (byte)((uint)uVar5 >> 0x18),
                      CONCAT12((char)((uint)uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar5 >> 0x10),
                               CONCAT11((char)((uint)uVar4 >> 8) + 0x8aU ^ (byte)((uint)uVar5 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar5)));
        uVar12 = uVar12 + 4;
      } while (uVar12 != 0x48);
      DAT_0a45e65a = 1;
    }
    uVar12 = (ulong)uVar3;
    lVar6 = 0;
    do {
      lVar13 = lVar6;
      uVar8 = (uint)uVar12;
      local_1f0[lVar13] =
           *(undefined1 *)
            ((long)&DAT_0a45e612 + (long)(int)(uVar8 + (int)(uVar12 / 10) * -10 + 0x23));
      uVar12 = uVar12 / 10;
      lVar6 = lVar13 + 1;
    } while (9 < uVar8);
    local_1f0[lVar13 + 1] = 0;
    if (8 < lVar13 + 8U) {
      puVar11 = local_1f0;
      puVar9 = local_1f0 + lVar13;
      do {
        puVar11 = puVar11 + 1;
        uVar2 = *puVar9;
        puVar10 = puVar9 + -1;
        *puVar9 = puVar11[-1];
        puVar11[-1] = uVar2;
        puVar9 = puVar10;
      } while (puVar11 < puVar10);
    }
    local_248 = *(undefined8 **)(param_2 + 0x10);
    if (-1 < *(char *)((long)param_2 + 0x57)) {
      local_248 = (undefined8 *)(param_2 + 0x10);
    }
    local_240 = 0;
    if ((DAT_0a45dfda & 1) == 0) {
      uVar12 = 0;
      do {
        uVar4 = *(undefined4 *)((long)&DAT_08a13eca + uVar12);
        uVar5 = *(undefined4 *)((long)&DAT_08a13eb6 + uVar12 % 0x14);
        *(uint *)((long)&DAT_0a45df9e + uVar12) =
             CONCAT13((char)((uint)uVar4 >> 0x18) + 0x8aU ^ (byte)((uint)uVar5 >> 0x18),
                      CONCAT12((char)((uint)uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar5 >> 0x10),
                               CONCAT11((char)((uint)uVar4 >> 8) + 0x8aU ^ (byte)((uint)uVar5 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar5)));
        uVar12 = uVar12 + 4;
      } while (uVar12 != 0x3c);
      DAT_0a45dfda = 1;
    }
    local_b8 = &local_108;
    ppuStack_b0 = &local_158;
    local_a8 = &local_1a8;
    ppuStack_a0 = &local_1f8;
    local_98 = &local_248;
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
    FUN_05e1d31c(auStack_2d8,&DAT_0a45df9e,&local_b8);
    thunk_FUN_05e1d0bc(auStack_2d8);
    if (cStack_2d9 < '\0') {
      __ZdlPvm(local_2f0[0],CONCAT17(cStack_2d9,local_2e0) & 0x7fffffffffffffff);
    }
  }
  *(undefined4 *)(param_1 + 0x1e0) = *param_2;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x1e8,param_2 + 2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x200,param_2 + 8);
  *(undefined2 *)(param_1 + 0x218) = *(undefined2 *)(param_2 + 0xe);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x220,param_2 + 0x10);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x238,param_2 + 0x16);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


