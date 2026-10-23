// Ghidra inferred pseudocode; requested=0x28565f4
// entry=028565f4 end=02856953

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_028565f4(undefined8 param_1,long param_2)

{
  undefined8 ****ppppuVar1;
  undefined4 uVar2;
  uint3 uVar3;
  int iVar4;
  long *plVar5;
  long lVar6;
  long lVar7;
  ulong uVar8;
  long *plVar9;
  long *plVar10;
  undefined4 uVar11;
  undefined8 ***local_178 [2];
  undefined7 local_168;
  char cStack_161;
  long *local_160;
  long *local_158;
  long lStack_150;
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
  undefined8 uStack_60;
  undefined8 uStack_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_178);
    ppppuVar1 = (undefined8 ****)local_178[0];
    if (-1 < cStack_161) {
      ppppuVar1 = local_178;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39e0a9 & 1) == 0) {
      _DAT_0a39e094 = CONCAT44((int)DAT_085465d8,(int)DAT_087ec730);
      uRam000000000a39e09c = CONCAT44((int)DAT_085465e8,(int)DAT_085465e0);
      DAT_0a39e0a4 = (undefined4)DAT_08698728;
      DAT_0a39e0a8 = 0;
      DAT_0a39e0a9 = 1;
    }
    FUN_05e1d050(&local_160,2,ppppuVar1,&DAT_0a39dff8,&DAT_0a39e094,0xf1,0,0);
    if ((DAT_0a39e0e7 & 1) == 0) {
      uVar8 = 0;
      do {
        uVar11 = *(undefined4 *)((long)&DAT_08805a04 + uVar8);
        uVar3 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
        uVar2 = *(undefined4 *)((long)&DAT_088059f0 + uVar8 % 0x14);
        *(uint *)((long)&DAT_0a39e0aa + uVar8) =
             CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar2 >> 0x18),
                      CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^ (byte)((uint)uVar2 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar2 >> 8),
                                        (char)uVar3 + 0x8aU ^ (byte)uVar2)));
        uVar8 = uVar8 + 4;
      } while (uVar8 != 0x3c);
      DAT_0a39e0e6 = 0;
      DAT_0a39e0e7 = 1;
    }
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    uStack_a0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    uStack_c0 = 0;
    FUN_05e1d31c(&local_160,&DAT_0a39e0aa,&local_d0);
    thunk_FUN_05e1d0bc(&local_160);
    if (cStack_161 < '\0') {
      __ZdlPvm(local_178[0],CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
    }
  }
  *(undefined1 *)(param_2 + 0x60) = 0;
  plVar9 = *(long **)(param_2 + 0x48);
  lStack_150 = *(long *)(param_2 + 0x58);
  plVar10 = *(long **)(param_2 + 0x50);
  *(undefined8 *)(param_2 + 0x50) = 0;
  *(undefined8 *)(param_2 + 0x58) = 0;
  *(undefined8 *)(param_2 + 0x48) = 0;
  local_160 = plVar9;
  local_158 = plVar10;
  for (; plVar9 != plVar10; plVar9 = plVar9 + 4) {
    if ((long *)plVar9[3] == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_0021eccc();
    }
    (**(code **)(*(long *)plVar9[3] + 0x30))();
  }
  if (*(long *)(param_2 + 0x38) != 0) {
    plVar9 = (long *)*(long *)(param_2 + 0x30);
    while (plVar9 != (long *)0x0) {
      lVar6 = *plVar9;
      FUN_02877908(plVar9 + 5);
      if (*(char *)((long)plVar9 + 0x27) < '\0') {
        __ZdlPvm(plVar9[2],plVar9[4] & 0x7fffffffffffffff);
      }
      __ZdlPvm(plVar9,0x98);
      plVar9 = (long *)lVar6;
    }
    *(undefined8 *)(param_2 + 0x30) = 0;
    lVar6 = *(long *)(param_2 + 0x28);
    if (lVar6 != 0) {
      lVar7 = 0;
      do {
        *(undefined8 *)(*(long *)(param_2 + 0x20) + lVar7 * 8) = 0;
        lVar7 = lVar7 + 1;
      } while (lVar6 != lVar7);
    }
    *(undefined8 *)(param_2 + 0x38) = 0;
  }
  FUN_02322b5c(param_1);
  plVar9 = local_160;
  plVar10 = local_158;
  if (local_160 != (long *)0x0) {
    while (plVar10 != plVar9) {
      plVar5 = (long *)plVar10[-1];
      plVar10 = plVar10 + -4;
      if (plVar10 == plVar5) {
        (**(code **)(*plVar5 + 0x20))();
      }
      else if (plVar5 != (long *)0x0) {
        (**(code **)(*plVar5 + 0x28))();
      }
    }
    __ZdlPvm(plVar9,lStack_150 - (long)plVar9);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


