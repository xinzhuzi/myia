// Ghidra inferred pseudocode; requested=0x3280514
// entry=03280514 end=03280b4b

/* WARNING: Type propagation algorithm not settling */

ulong FUN_03280514(undefined8 param_1,long param_2)

{
  undefined8 *******pppppppuVar1;
  long *plVar2;
  int iVar3;
  undefined8 *puVar4;
  ulong uVar5;
  ulong uVar6;
  long lVar7;
  long lVar8;
  undefined8 local_280;
  undefined8 uStack_278;
  ulong local_270;
  undefined8 *******local_260 [2];
  undefined7 local_250;
  char cStack_249;
  undefined8 *******local_248 [2];
  undefined7 local_238;
  char cStack_231;
  undefined8 *******local_230;
  long lStack_228;
  ulong local_220;
  undefined8 uStack_218;
  undefined8 local_210;
  long local_1a0;
  long lStack_198;
  long *local_190;
  undefined8 uStack_188;
  undefined8 local_180;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined8 ******ppppppuStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *puStack_140;
  undefined1 *local_138;
  undefined8 *******local_128;
  undefined1 local_120;
  undefined8 *******local_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((DAT_0a3e5fbd & 1) == 0) {
    uVar5 = 0;
    do {
      (&DAT_0a3e5fa5)[uVar5] = (&DAT_088cd316)[uVar5] + 0x69 ^ (&DAT_088cd306)[uVar5 & 0xf];
      uVar5 = uVar5 + 1;
    } while (uVar5 != 0x18);
    DAT_0a3e5fbd = 1;
  }
  if ((DAT_0a3e500e & 1) == 0) {
    uVar5 = 0;
    do {
      (&DAT_0a3e4fa9)[uVar5] = (&DAT_088cb9eb)[uVar5] + 0x8a ^ (&DAT_088cb9db)[uVar5 & 0xf];
      uVar5 = uVar5 + 1;
    } while (uVar5 != 0x65);
    DAT_0a3e500e = 1;
  }
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  local_138 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  ppppppuStack_158 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0003bb6c(&local_230,&DAT_0a3e5fa5,&DAT_0a3e4fa9,0xeff);
  local_170 = (undefined1 *)CONCAT44(local_170._4_4_,2);
  local_150 = (undefined1 *)lStack_228;
  ppppppuStack_158 = local_230;
  local_160 = (undefined1 *)0x0;
  puStack_148 = (undefined1 *)0x0;
  puStack_140 = (undefined1 *)0x0;
  local_138 = (undefined1 *)0x0;
  puStack_168 = (undefined1 *)FUN_0474715c();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&puStack_148,&DAT_0a3e5fa5);
  FUN_04cbfafc(param_2);
  lStack_198 = 0;
  local_1a0 = 0;
  uStack_188 = 0;
  local_190 = (long *)0x0;
  local_180 = 0xaaaaaaaa3f800000;
  lStack_228 = 0;
  local_230 = (undefined8 *******)0x0;
  uStack_218 = 0;
  local_220 = 0;
  local_210 = 0xaaaaaaaa3f800000;
  local_d8._0_4_ = *(undefined4 *)(param_2 + 0x198);
  FUN_01733804(&local_230,&local_d8,&local_d8);
  local_d8._0_4_ = *(undefined4 *)(param_2 + 0x19c);
  FUN_01733804(&local_230,&local_d8,&local_d8);
  local_d8 = (undefined8 *******)CONCAT44(local_d8._4_4_,*(undefined4 *)(param_2 + 0x110));
  FUN_01733804(&local_230,&local_d8,&local_d8);
  uVar5 = FUN_03aef3f8(param_1,&local_230,&local_1a0);
  pppppppuVar1 = local_230;
  plVar2 = (long *)local_220;
  while (plVar2 != (long *)0x0) {
    lVar8 = *plVar2;
    local_230 = pppppppuVar1;
    __ZdlPvm(plVar2,0x18);
    pppppppuVar1 = local_230;
    plVar2 = (long *)lVar8;
  }
  local_230 = (undefined8 *******)0x0;
  if (pppppppuVar1 != (undefined8 *******)0x0) {
    __ZdlPvm(pppppppuVar1,lStack_228 << 3);
  }
  if ((uVar5 & 1) == 0) {
    iVar3 = thunk_FUN_05e1d97c(4);
    lVar8 = local_1a0;
    plVar2 = local_190;
    if (iVar3 == 0) goto joined_r0x03280aa0;
    FUN_0488143c(local_248);
    pppppppuVar1 = local_248[0];
    if (-1 < cStack_231) {
      pppppppuVar1 = local_248;
    }
    if ((DAT_0a3e46b7 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3e46a4)[uVar6] = (&DAT_088ca7e4)[uVar6] + 0x8a ^ (&DAT_088ca7d4)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x13);
      DAT_0a3e46b7 = 1;
    }
    if ((DAT_0a3e5fbd & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3e5fa5)[uVar6] = (&DAT_088cd316)[uVar6] + 0x69 ^ (&DAT_088cd306)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x18);
      DAT_0a3e5fbd = 1;
    }
    FUN_05e1d050(&local_230,4,pppppppuVar1,&DAT_0a3e46a4,&DAT_0a3e5fa5,0xf05,0,0);
    FUN_04cbe4cc(local_260,param_2);
    local_128 = local_260[0];
    if (-1 < cStack_249) {
      local_128 = local_260;
    }
    local_120 = 0;
    if ((DAT_0a3e5fd7 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3e5fbe)[uVar6] = (&DAT_088cd33e)[uVar6] + 0x69 ^ (&DAT_088cd32e)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x19);
      DAT_0a3e5fd7 = 1;
    }
    local_d8 = &local_128;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    uStack_c0 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    uStack_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    local_60 = 0;
    FUN_05e1d31c(&local_230,&DAT_0a3e5fbe,&local_d8);
    if (cStack_249 < '\0') {
      __ZdlPvm(local_260[0],CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_230);
    lVar8 = local_1a0;
    plVar2 = local_190;
    if (-1 < cStack_231) goto joined_r0x03280aa0;
    uVar6 = CONCAT17(cStack_231,local_238);
  }
  else {
    local_230 = &local_d8;
    local_d8._0_4_ = *(undefined4 *)(param_2 + 0x198);
    lVar8 = FUN_03026804(&local_1a0,&local_d8,&DAT_08b7a8b8,&local_230,&local_128);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_2 + 0x18,lVar8 + 0x18);
    local_d8._0_4_ = *(undefined4 *)(param_2 + 0x19c);
    local_230 = &local_d8;
    lVar8 = FUN_03026804(&local_1a0,&local_d8,&DAT_08b7a8b8,&local_230,&local_128);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_2 + 0x30,lVar8 + 0x18);
    local_d8 = (undefined8 *******)CONCAT44(local_d8._4_4_,*(undefined4 *)(param_2 + 0x110));
    local_230 = &local_d8;
    lVar8 = FUN_03026804(&local_1a0,&local_d8,&DAT_08b7a8b8,&local_230,&local_128);
    FUN_04cbb728(param_2,lVar8 + 0x18);
    FUN_04cbf804(param_2);
    FUN_04cbe440(&local_230,param_2);
    if ((DAT_0a3e5ff5 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3e5fd8)[uVar6] = (&DAT_088cd367)[uVar6] + 0x69 ^ (&DAT_088cd357)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x1d);
      DAT_0a3e5ff5 = 1;
    }
    puVar4 = (undefined8 *)
             __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                       (&local_230,0,&DAT_0a3e5fd8);
    uStack_278 = puVar4[1];
    local_280 = *puVar4;
    local_270 = puVar4[2];
    puVar4[1] = 0;
    puVar4[2] = 0;
    *puVar4 = 0;
    FUN_02ac5bf8(&local_170,&local_280,0x32);
    local_248[0] = local_230;
    uVar6 = local_220;
    if ((long)local_270 < 0) {
      __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
      local_248[0] = local_230;
      uVar6 = local_220;
    }
    local_230 = local_248[0];
    local_220 = uVar6;
    lVar8 = local_1a0;
    plVar2 = local_190;
    if (-1 < (long)uVar6) goto joined_r0x03280aa0;
  }
  __ZdlPvm(local_248[0],uVar6 & 0x7fffffffffffffff);
  lVar8 = local_1a0;
  plVar2 = local_190;
joined_r0x03280aa0:
  while (plVar2 != (long *)0x0) {
    lVar7 = *plVar2;
    local_1a0 = lVar8;
    if (*(char *)((long)plVar2 + 0x2f) < '\0') {
      __ZdlPvm(plVar2[3],plVar2[5] & 0x7fffffffffffffff);
    }
    __ZdlPvm(plVar2,0x30);
    lVar8 = local_1a0;
    plVar2 = (long *)lVar7;
  }
  local_1a0 = 0;
  if (lVar8 != 0) {
    __ZdlPvm(lVar8,lStack_198 << 3);
  }
  if ((long)local_138 < 0) {
    __ZdlPvm(puStack_148,(ulong)local_138 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return uVar5;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


