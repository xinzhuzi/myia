// Ghidra inferred pseudocode; requested=0x3262d74
// entry=03262d74 end=032632e7

void FUN_03262d74(long param_1,long *param_2,long *param_3)

{
  undefined4 *puVar1;
  long lVar2;
  undefined1 uVar3;
  bool bVar4;
  ulong uVar5;
  undefined8 uVar6;
  undefined8 ****ppppuVar7;
  code *pcVar8;
  undefined1 *puVar9;
  undefined1 *puVar10;
  long lVar11;
  undefined4 local_210;
  undefined4 uStack_20c;
  undefined7 local_200;
  char cStack_1f9;
  undefined8 ***local_1f8;
  undefined8 local_1f0;
  undefined7 local_1e8;
  char cStack_1e1;
  long *local_1a8;
  undefined1 local_1a0;
  long alStack_158 [3];
  long *local_140;
  long **local_c8;
  undefined8 ***local_c0;
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
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar5 = param_2[1];
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar5 = (ulong)*(byte *)((long)param_2 + 0x17);
  }
  if ((uVar5 == 0) || (*param_3 == param_3[1])) {
    uVar6 = thunk_FUN_05e1d97c(4);
    if ((int)uVar6 == 0) goto LAB_032632b4;
    FUN_0488143c(&local_210);
    puVar1 = (undefined4 *)CONCAT44(uStack_20c,local_210);
    if (-1 < cStack_1f9) {
      puVar1 = &local_210;
    }
    if ((DAT_0a3e46b7 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e46a4)[uVar5] = (&DAT_088ca7e4)[uVar5] + 0x8a ^ (&DAT_088ca7d4)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x13);
      DAT_0a3e46b7 = 1;
    }
    if ((DAT_0a3e4a50 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e4a2c)[uVar5] = (&DAT_088cb029)[uVar5] + 0x69 ^ (&DAT_088cb019)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x24);
      DAT_0a3e4a50 = 1;
    }
    FUN_05e1d050(alStack_158,4,puVar1,&DAT_0a3e46a4,&DAT_0a3e4a2c,0x148,0,0);
    local_1a8 = (long *)*param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      local_1a8 = param_2;
    }
    local_1a0 = 0;
    lVar2 = *param_3;
    lVar11 = param_3[1];
    local_1f8 = (undefined8 ***)&local_1f0;
    if ((DAT_0a3e6342 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e62fa)[uVar5] = (&DAT_088cd869)[uVar5] + 0x69 ^ (&DAT_088cd859)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x48);
      DAT_0a3e6342 = 1;
    }
    uVar5 = (lVar11 - lVar2 >> 3) * -0x3333333333333333;
    lVar2 = 0;
    do {
      lVar11 = lVar2;
      *(undefined1 *)((long)&local_1f0 + lVar11) = (&DAT_0a3e631d)[uVar5 % 10];
      bVar4 = 9 < uVar5;
      uVar5 = uVar5 / 10;
      lVar2 = lVar11 + 1;
    } while (bVar4);
    *(undefined1 *)((long)&local_1f0 + lVar11 + 1) = 0;
    if (8 < lVar11 + 8U) {
      puVar9 = (undefined1 *)((long)&local_1f0 + lVar11);
      puVar10 = (undefined1 *)((long)&local_1f0 + 1);
      do {
        uVar3 = *puVar9;
        *puVar9 = puVar10[-1];
        puVar10[-1] = uVar3;
        bVar4 = puVar10 < puVar9 + -1;
        puVar9 = puVar9 + -1;
        puVar10 = puVar10 + 1;
      } while (bVar4);
    }
    if ((DAT_0a3e4aa8 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e4a51)[uVar5] = (&DAT_088cb05d)[uVar5] + 0x8a ^ (&DAT_088cb04d)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x57);
      DAT_0a3e4aa8 = 1;
    }
    local_c8 = &local_1a8;
    local_c0 = &local_1f8;
    local_b0 = 0;
    uStack_b8 = 0;
    local_a0 = 0;
    uStack_a8 = 0;
    local_90 = 0;
    uStack_98 = 0;
    local_80 = 0;
    uStack_88 = 0;
    local_70 = 0;
    uStack_78 = 0;
    local_60 = 0;
    uStack_68 = 0;
    local_50 = 0;
    uStack_58 = 0;
    FUN_05e1d31c(alStack_158,&DAT_0a3e4a51,&local_c8);
    thunk_FUN_05e1d0bc(alStack_158);
    if (cStack_1f9 < '\0') {
      ppppuVar7 = (undefined8 ****)CONCAT44(uStack_20c,local_210);
      uVar5 = CONCAT17(cStack_1f9,local_200);
LAB_0326328c:
      __ZdlPvm(ppppuVar7,uVar5 & 0x7fffffffffffffff);
    }
  }
  else {
    local_210 = 0;
    uVar5 = FUN_03aee340(param_1,param_2,&local_210);
    if ((uVar5 & 1) != 0) {
      local_140 = (long *)__Znwm(0x28);
      *local_140 = (long)&PTR_FUN_09df1820;
      local_140[1] = param_1;
      local_140[2] = (long)param_3;
      local_140[3] = (long)&local_210;
      local_140[4] = (long)param_2;
      uVar6 = FUN_03aeddb4(param_1,alStack_158);
      if (local_140 == alStack_158) {
        pcVar8 = *(code **)(*local_140 + 0x20);
      }
      else {
        if (local_140 == (long *)0x0) goto LAB_032632b4;
        pcVar8 = *(code **)(*local_140 + 0x28);
      }
      (*pcVar8)(local_140);
      goto LAB_032632b4;
    }
    uVar6 = thunk_FUN_05e1d97c(4);
    if ((int)uVar6 == 0) goto LAB_032632b4;
    FUN_0488143c(&local_1f8);
    ppppuVar7 = (undefined8 ****)local_1f8;
    if (-1 < cStack_1e1) {
      ppppuVar7 = &local_1f8;
    }
    if ((DAT_0a3e46b7 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e46a4)[uVar5] = (&DAT_088ca7e4)[uVar5] + 0x8a ^ (&DAT_088ca7d4)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x13);
      DAT_0a3e46b7 = 1;
    }
    if ((DAT_0a3e4a50 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e4a2c)[uVar5] = (&DAT_088cb029)[uVar5] + 0x69 ^ (&DAT_088cb019)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x24);
      DAT_0a3e4a50 = 1;
    }
    FUN_05e1d050(alStack_158,4,ppppuVar7,&DAT_0a3e46a4,&DAT_0a3e4a2c,0x14e,0,0);
    local_1a8 = (long *)*param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      local_1a8 = param_2;
    }
    local_1a0 = 0;
    if ((DAT_0a3e4af7 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3e4aa9)[uVar5] = (&DAT_088cb0c4)[uVar5] + 0x8a ^ (&DAT_088cb0b4)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x4e);
      DAT_0a3e4af7 = 1;
    }
    uStack_b8 = 0;
    local_c0 = (undefined8 ****)0x0;
    local_c8 = &local_1a8;
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
    local_50 = 0;
    FUN_05e1d31c(alStack_158,&DAT_0a3e4aa9,&local_c8);
    thunk_FUN_05e1d0bc(alStack_158);
    if (cStack_1e1 < '\0') {
      uVar5 = CONCAT17(cStack_1e1,local_1e8);
      ppppuVar7 = (undefined8 ****)local_1f8;
      goto LAB_0326328c;
    }
  }
  uVar6 = 0;
LAB_032632b4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar6);
}


