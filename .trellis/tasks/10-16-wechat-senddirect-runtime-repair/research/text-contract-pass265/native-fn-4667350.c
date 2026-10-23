// Ghidra inferred pseudocode; requested=0x4667350
// entry=04667350 end=04667e33

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04667350(long param_1)

{
  undefined8 *******pppppppuVar1;
  undefined1 uVar2;
  uint3 uVar3;
  bool bVar4;
  long lVar5;
  int iVar6;
  undefined8 *puVar7;
  undefined8 uVar8;
  size_t sVar9;
  ulong uVar10;
  uint uVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  long lVar15;
  uint uVar16;
  undefined8 uVar17;
  long *plVar18;
  undefined4 uVar19;
  undefined4 uVar20;
  undefined8 *******local_298 [2];
  undefined7 local_288;
  char cStack_281;
  undefined8 local_280 [2];
  undefined7 local_270;
  char cStack_269;
  undefined1 auStack_1f0 [24];
  undefined8 *******local_1d8;
  ulong uStack_1d0;
  ulong local_1c8;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *puStack_1b0;
  undefined1 *puStack_1a8;
  undefined8 *******local_1a0;
  long lStack_198;
  undefined7 local_190;
  char cStack_189;
  undefined1 *local_188;
  undefined1 *local_180;
  undefined1 *puStack_178;
  undefined1 *local_170;
  undefined1 local_168 [72];
  undefined8 *******local_120;
  undefined8 local_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 *******local_d0;
  undefined1 **ppuStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
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
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  puVar7 = (undefined8 *)__Znwm(0x20);
  puVar7[1] = 0;
  puVar7[2] = 0;
  *puVar7 = &PTR_FUN_09e92b48;
  uVar8 = thunk_FUN_045317fc(puVar7 + 3);
  *(undefined8 *)(param_1 + 0x2a0) = uVar8;
  plVar18 = *(long **)(param_1 + 0x2a8);
  *(undefined8 **)(param_1 + 0x2a8) = puVar7;
  if (plVar18 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar18[1];
    plVar18[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar18 + 0x10))(plVar18);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar18);
    }
  }
  FUN_04533dc0(*(undefined8 *)(param_1 + 0x2a0));
  uVar11 = *(uint *)(param_1 + 0x128);
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  local_188 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0002b2c0(&local_188);
  FUN_00056f08(1,&local_188);
  FUN_0003e1f8(&local_120,&local_188);
  FUN_0002bd88(&local_d0,&local_120);
  FUN_0002d0bc(local_280,&local_d0);
  FUN_0002def0(&local_1a0,local_280);
  FUN_0002b440(local_280);
  FUN_0002b440(&local_d0);
  FUN_0002b440(&local_120);
  puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_000a87a0(&local_1c0);
  if ((DAT_0a45e678 & 1) == 0) {
    DAT_0a45e670[0] = s_product_08480580[0];
    DAT_0a45e670[1] = s_product_08480580[1];
    DAT_0a45e670[2] = s_product_08480580[2];
    DAT_0a45e670[3] = s_product_08480580[3];
    DAT_0a45e670[4] = s_product_08480580[4];
    DAT_0a45e670[5] = s_product_08480580[5];
    DAT_0a45e670[6] = s_product_08480580[6];
    DAT_0a45e670[7] = s_product_08480580[7];
    DAT_0a45e678 = 1;
  }
  sVar9 = _strlen(DAT_0a45e670);
  pppppppuVar1 = local_1a0;
  if (-1 < (long)cStack_189) {
    pppppppuVar1 = &local_1a0;
  }
  if (-1 < cStack_189) {
    lStack_198 = (long)cStack_189;
  }
  FUN_000a8508(&local_1c0,DAT_0a45e670,sVar9,pppppppuVar1,lStack_198);
  if ((DAT_0a45e1cd & 1) == 0) {
    DAT_0a45e1c0._0_1_ = s_input_ackernel_cpadV_08a133a0[0];
    DAT_0a45e1c0._1_1_ = s_input_ackernel_cpadV_08a133a0[1];
    DAT_0a45e1c0._2_1_ = s_input_ackernel_cpadV_08a133a0[2];
    DAT_0a45e1c0._3_1_ = s_input_ackernel_cpadV_08a133a0[3];
    DAT_0a45e1c0._4_1_ = s_input_ackernel_cpadV_08a133a0[4];
    DAT_0a45e1c0._5_1_ = s_input_ackernel_cpadV_08a133a0[5];
    DAT_0a45e1c0._6_1_ = s_input_ackernel_cpadV_08a133a0[6];
    DAT_0a45e1c0._7_1_ = s_input_ackernel_cpadV_08a133a0[7];
    DAT_0a45e1c8 = (undefined4)DAT_08482f20;
    DAT_0a45e1cc = 0;
    DAT_0a45e1cd = 1;
  }
  sVar9 = _strlen((char *)&DAT_0a45e1c0);
  if ((DAT_0a45e67b & 1) == 0) {
    DAT_0a45e679 = 0x32;
    DAT_0a45e67b = 1;
  }
  FUN_000a8524(&local_1c0,&DAT_0a45e1c0,sVar9,&DAT_0a45e679);
  if ((DAT_0a45e688 & 1) == 0) {
    DAT_0a45e680[0] = s_version_08480528[0];
    DAT_0a45e680[1] = s_version_08480528[1];
    DAT_0a45e680[2] = s_version_08480528[2];
    DAT_0a45e680[3] = s_version_08480528[3];
    DAT_0a45e680[4] = s_version_08480528[4];
    DAT_0a45e680[5] = s_version_08480528[5];
    DAT_0a45e680[6] = s_version_08480528[6];
    DAT_0a45e680[7] = s_version_08480528[7];
    DAT_0a45e688 = 1;
  }
  sVar9 = _strlen(DAT_0a45e680);
  __ZNSt3__19to_stringEj(local_280,(ulong)uVar11);
  FUN_000a8540(&local_1c0,DAT_0a45e680,sVar9,local_280);
  if (cStack_269 < '\0') {
    __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
  }
  if ((DAT_0a45e69a & 1) == 0) {
    DAT_0a45e690._0_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0];
    DAT_0a45e690._1_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[1];
    DAT_0a45e690._2_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[2];
    DAT_0a45e690._3_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[3];
    DAT_0a45e690._4_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[4];
    DAT_0a45e690._5_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[5];
    DAT_0a45e690._6_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[6];
    DAT_0a45e690._7_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[7];
    DAT_0a45e698 = 0x72;
    DAT_0a45e69a = 1;
  }
  sVar9 = _strlen((char *)&DAT_0a45e690);
  __ZNSt3__19to_stringEj(local_280,uVar11 >> 0x10 & 0xf);
  FUN_000a8540(&local_1c0,&DAT_0a45e690,sVar9,local_280);
  if (cStack_269 < '\0') {
    __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
  }
  if ((DAT_0a45e6aa & 1) == 0) {
    DAT_0a45e6a0._0_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[8];
    DAT_0a45e6a0._1_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[9];
    DAT_0a45e6a0._2_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[10];
    DAT_0a45e6a0._3_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0xb];
    DAT_0a45e6a0._4_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0xc];
    DAT_0a45e6a0._5_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0xd];
    DAT_0a45e6a0._6_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0xe];
    DAT_0a45e6a0._7_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0xf];
    DAT_0a45e6a8 = 0x72;
    DAT_0a45e6aa = 1;
  }
  sVar9 = _strlen((char *)&DAT_0a45e6a0);
  __ZNSt3__19to_stringEj(local_280,uVar11 >> 0xc & 0xf);
  FUN_000a8540(&local_1c0,&DAT_0a45e6a0,sVar9,local_280);
  if (cStack_269 < '\0') {
    __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
  }
  if ((DAT_0a45e6ba & 1) == 0) {
    DAT_0a45e6b0._0_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x10];
    DAT_0a45e6b0._1_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x11];
    DAT_0a45e6b0._2_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x12];
    DAT_0a45e6b0._3_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x13];
    DAT_0a45e6b0._4_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x14];
    DAT_0a45e6b0._5_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x15];
    DAT_0a45e6b0._6_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x16];
    DAT_0a45e6b0._7_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x17];
    DAT_0a45e6b8 = 0x72;
    DAT_0a45e6ba = 1;
  }
  sVar9 = _strlen((char *)&DAT_0a45e6b0);
  __ZNSt3__19to_stringEj(local_280,uVar11 >> 8 & 0xf);
  FUN_000a8540(&local_1c0,&DAT_0a45e6b0,sVar9,local_280);
  if (cStack_269 < '\0') {
    __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
  }
  if ((DAT_0a45e6ca & 1) == 0) {
    DAT_0a45e6c0._0_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x18];
    DAT_0a45e6c0._1_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x19];
    DAT_0a45e6c0._2_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x1a];
    DAT_0a45e6c0._3_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x1b];
    DAT_0a45e6c0._4_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x1c];
    DAT_0a45e6c0._5_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x1d];
    DAT_0a45e6c0._6_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x1e];
    DAT_0a45e6c0._7_1_ = s_major_veminor_vepatch_vebuild_ve_08480548[0x1f];
    DAT_0a45e6c8 = 0x72;
    DAT_0a45e6ca = 1;
  }
  sVar9 = _strlen((char *)&DAT_0a45e6c0);
  __ZNSt3__19to_stringEj(local_280,uVar11 & 0xff);
  FUN_000a8540(&local_1c0,&DAT_0a45e6c0,sVar9,local_280);
  if (cStack_269 < '\0') {
    __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
  }
  local_1d8 = (undefined8 *******)0x0;
  uStack_1d0 = 0;
  local_1c8 = 0;
  FUN_000a86d8(auStack_1f0,&local_1c0);
  uVar10 = FUN_00038e14(auStack_1f0,&local_1d8,200);
  if ((uVar10 & 1) == 0) {
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(&local_120);
      pppppppuVar1 = local_120;
      if (-1 < cStack_109) {
        pppppppuVar1 = &local_120;
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
      if ((DAT_0a45e6e7 & 1) == 0) {
        _DAT_0a45e6cc = CONCAT44((int)DAT_0852fb28,(int)DAT_08500cb8);
        uRam000000000a45e6d4 = CONCAT44((int)ram0x08a133b0,(int)ram0x084804f0);
        DAT_0a45e6dc = CONCAT44((int)DAT_0861ae60,(int)DAT_0847fd98);
        DAT_0a45e6e4 = 0x6f66;
        DAT_0a45e6e6 = 0;
        DAT_0a45e6e7 = 1;
      }
      FUN_05e1d050(local_280,4,pppppppuVar1,&DAT_0a45df80,&DAT_0a45e6cc,0x1f1,0,0);
      if ((DAT_0a45e722 & 1) == 0) {
        uVar10 = 0;
        do {
          uVar19 = *(undefined4 *)((long)&DAT_08a14b6d + uVar10);
          uVar3 = CONCAT12((char)((uint)uVar19 >> 8),(short)uVar19) & 0xff00ff;
          uVar20 = *(undefined4 *)((long)&DAT_08a14b59 + uVar10 % 0x14);
          *(uint *)((long)&DAT_0a45e6e8 + uVar10) =
               CONCAT13((char)((uint)uVar19 >> 0x18) + 0x8aU ^ (byte)((uint)uVar20 >> 0x18),
                        CONCAT12((char)((uint)uVar19 >> 0x10) + 0x8aU ^ (byte)((uint)uVar20 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar20 >> 8)
                                           ,(char)uVar3 + 0x8aU ^ (byte)uVar20)));
          uVar10 = uVar10 + 4;
        } while (uVar10 != 0x38);
        DAT_0a45e720 = 0x2e;
        DAT_0a45e722 = 1;
      }
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      local_60 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      ppuStack_c8 = (undefined1 **)0x0;
      local_d0 = (undefined8 *******)0x0;
      uStack_b8 = 0;
      local_c0 = 0;
      FUN_05e1d31c(local_280,&DAT_0a45e6e8,&local_d0);
      thunk_FUN_05e1d0bc(local_280);
      if (cStack_109 < '\0') {
        __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
      }
    }
  }
  else {
    iVar6 = thunk_FUN_05e1d97c(2);
    if (iVar6 != 0) {
      FUN_0488143c(local_298);
      pppppppuVar1 = local_298[0];
      if (-1 < cStack_281) {
        pppppppuVar1 = local_298;
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
      if ((DAT_0a45e6e7 & 1) == 0) {
        _DAT_0a45e6cc = CONCAT44((int)DAT_0852fb28,(int)DAT_08500cb8);
        uRam000000000a45e6d4 = CONCAT44((int)ram0x08a133b0,(int)ram0x084804f0);
        DAT_0a45e6dc = CONCAT44((int)DAT_0861ae60,(int)DAT_0847fd98);
        DAT_0a45e6e4 = 0x6f66;
        DAT_0a45e6e6 = 0;
        DAT_0a45e6e7 = 1;
      }
      FUN_05e1d050(local_280,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45e6cc,500,0,0);
      local_120 = (undefined8 *******)0x0;
      if ((DAT_0a45e65a & 1) == 0) {
        uVar10 = 0;
        do {
          uVar19 = *(undefined4 *)((long)&DAT_08a1498d + uVar10);
          uVar3 = CONCAT12((char)((uint)uVar19 >> 8),(short)uVar19) & 0xff00ff;
          uVar20 = *(undefined4 *)((long)&DAT_08a14979 + uVar10 % 0x14);
          *(uint *)((long)&DAT_0a45e612 + uVar10) =
               CONCAT13((char)((uint)uVar19 >> 0x18) + 0x8aU ^ (byte)((uint)uVar20 >> 0x18),
                        CONCAT12((char)((uint)uVar19 >> 0x10) + 0x8aU ^ (byte)((uint)uVar20 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar20 >> 8)
                                           ,(char)uVar3 + 0x8aU ^ (byte)uVar20)));
          uVar10 = uVar10 + 4;
        } while (uVar10 != 0x48);
        DAT_0a45e65a = 1;
      }
      lVar5 = 0;
      uVar10 = (ulong)uVar11;
      do {
        lVar15 = lVar5;
        uVar16 = (uint)uVar10;
        *(undefined1 *)((long)&local_118 + lVar15) =
             *(undefined1 *)
              ((long)&DAT_0a45e612 + (ulong)(uVar16 + (int)(uVar10 / 10) * -10 + 0x23));
        lVar5 = lVar15 + 1;
        uVar10 = uVar10 / 10;
      } while (9 < uVar16);
      *(undefined1 *)((long)&local_118 + lVar15 + 1) = 0;
      if (8 < lVar15 + 8U) {
        puVar14 = (undefined1 *)((long)&local_118 + lVar15);
        puVar12 = (undefined1 *)((long)&local_118 + 1);
        do {
          uVar2 = *puVar14;
          *puVar14 = puVar12[-1];
          puVar12[-1] = uVar2;
          bVar4 = puVar12 < puVar14 + -1;
          puVar14 = puVar14 + -1;
          puVar12 = puVar12 + 1;
        } while (bVar4);
      }
      local_120 = (undefined8 *******)&local_118;
      uVar10 = (ulong)(uVar11 & 0xfffff);
      lVar5 = 0;
      do {
        lVar15 = lVar5;
        uVar11 = (uint)uVar10;
        local_168[lVar15] =
             *(undefined1 *)
              ((long)&DAT_0a45e612 + (ulong)(uVar11 + (int)(uVar10 / 10) * -10 + 0x23));
        uVar10 = uVar10 / 10;
        lVar5 = lVar15 + 1;
      } while (9 < uVar11);
      local_170 = local_168;
      local_168[lVar15 + 1] = 0;
      if (8 < lVar15 + 8U) {
        puVar14 = local_168;
        puVar12 = local_168 + lVar15;
        do {
          puVar14 = puVar14 + 1;
          uVar2 = *puVar12;
          puVar13 = puVar12 + -1;
          *puVar12 = puVar14[-1];
          puVar14[-1] = uVar2;
          puVar12 = puVar13;
        } while (puVar14 < puVar13);
      }
      if ((DAT_0a45e746 & 1) == 0) {
        _DAT_0a45e724 = CONCAT44((int)DAT_085d8b00,(int)DAT_08a133b8);
        uRam000000000a45e72c = CONCAT44((int)DAT_08781048,(int)DAT_08a133c0);
        _DAT_0a45e734 = CONCAT44((int)DAT_084d89a0,(int)DAT_087d3a68);
        uRam000000000a45e73c = CONCAT44((int)DAT_084cfd10,(int)DAT_084e4840);
        DAT_0a45e744 = 0x5f;
        DAT_0a45e746 = 1;
      }
      local_d0 = &local_120;
      ppuStack_c8 = &local_170;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
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
      FUN_05e1d31c(local_280,&DAT_0a45e724,&local_d0);
      thunk_FUN_05e1d0bc(local_280);
      if (cStack_281 < '\0') {
        __ZdlPvm(local_298[0],CONCAT17(cStack_281,local_288) & 0x7fffffffffffffff);
      }
    }
    uVar10 = uStack_1d0;
    pppppppuVar1 = local_1d8;
    if (-1 < (long)local_1c8) {
      uVar10 = local_1c8 >> 0x38;
      pppppppuVar1 = &local_1d8;
    }
    FUN_00019a44(&DAT_0a05a720,pppppppuVar1,uVar10);
    FUN_000172f0(&local_1d8);
  }
  if ((long)local_1c8 < 0) {
    __ZdlPvm(local_1d8,local_1c8 & 0x7fffffffffffffff);
  }
  FUN_000a7010(&local_1c0);
  if (cStack_189 < '\0') {
    __ZdlPvm(local_1a0,CONCAT17(cStack_189,local_190) & 0x7fffffffffffffff);
  }
  FUN_0002b440(&local_188);
  uVar8 = FUN_046685b8(param_1);
  FUN_046686b8(local_280,param_1);
  FUN_04668010(uVar8,local_280);
  if (cStack_269 < '\0') {
    __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
  }
  FUN_046687e8(param_1);
  uVar17 = *(undefined8 *)(param_1 + 0x78);
  uVar8 = FUN_04a1779c();
  FUN_0456f23c(uVar17,uVar8);
  uVar17 = *(undefined8 *)(param_1 + 0x98);
  uVar8 = FUN_04a0d4a0();
  FUN_013a6570(uVar17,uVar8);
  FUN_04668950(param_1);
  FUN_04668ad0(param_1);
  FUN_04668e84();
  FUN_02216630();
  FUN_04b97eac();
  FUN_04668f94(param_1,1);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


