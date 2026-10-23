// Ghidra inferred pseudocode; requested=0x462e4d4
// entry=0462e4d4 end=0462e96f

undefined8 * FUN_0462e4d4(undefined8 *param_1)

{
  ulong uVar1;
  undefined8 uVar2;
  size_t sVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined *****pppppuVar6;
  undefined ***pppuVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  undefined ****local_88;
  undefined8 *local_80;
  undefined8 local_78;
  undefined ****local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  param_1[1] = &PTR_FUN_09e8fd78;
  *param_1 = &PTR_FUN_09e8fc30;
  param_1[2] = &PTR_FUN_09e8fda0;
  *(undefined1 *)(param_1 + 3) = 1;
  puVar9 = param_1 + 0xe;
  *puVar9 = 0;
  puVar8 = param_1 + 0xd;
  *puVar8 = puVar9;
  param_1[0xf] = 0;
  param_1[5] = 0;
  param_1[4] = 0;
  param_1[7] = 0;
  param_1[6] = 0;
  param_1[9] = 0;
  param_1[8] = 0;
  param_1[0xb] = 0;
  param_1[10] = 0;
  param_1[0xc] = 0;
  param_1[0x10] = 0x32aaaba7;
  param_1[0x12] = 0;
  param_1[0x11] = 0;
  param_1[0x14] = 0;
  param_1[0x13] = 0;
  param_1[0x16] = 0;
  param_1[0x15] = 0;
  param_1[0x18] = 0;
  param_1[0x17] = 0;
  param_1[0x1a] = 0;
  param_1[0x19] = 0;
  *(undefined8 *)((long)param_1 + 0xdc) = 0;
  *(undefined8 *)((long)param_1 + 0xd4) = 0;
  param_1[0x1d] = 0;
  param_1[0x1e] = 0;
  FUN_0004fa1c(puVar8,0);
  *puVar8 = puVar9;
  param_1[0xf] = 0;
  *puVar9 = 0;
  uVar2 = __Znwm(0x10);
  FUN_04656d94(uVar2,param_1);
  param_1[6] = uVar2;
  uVar2 = __Znwm(0x10);
  FUN_04656fc4(uVar2,param_1 + 1);
  param_1[7] = uVar2;
  uVar2 = __Znwm(8);
  FUN_0462db28();
  param_1[9] = uVar2;
  uVar2 = __Znwm(8);
  FUN_0462e354();
  param_1[10] = uVar2;
  uVar2 = __Znwm(0x10);
  FUN_0463c49c();
  param_1[8] = uVar2;
  if ((DAT_0a45ce90 & 1) == 0) {
    DAT_0a45ce88[0] = s_default_084c7818[0];
    DAT_0a45ce88[1] = s_default_084c7818[1];
    DAT_0a45ce88[2] = s_default_084c7818[2];
    DAT_0a45ce88[3] = s_default_084c7818[3];
    DAT_0a45ce88[4] = s_default_084c7818[4];
    DAT_0a45ce88[5] = s_default_084c7818[5];
    DAT_0a45ce88[6] = s_default_084c7818[6];
    DAT_0a45ce88[7] = s_default_084c7818[7];
    DAT_0a45ce90 = 1;
  }
  sVar3 = _strlen(DAT_0a45ce88);
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_88);
  }
  if (sVar3 < 0x17) {
    local_78 = CONCAT17((char)sVar3,(undefined7)local_78);
    pppppuVar6 = &local_88;
    if (sVar3 != 0) goto LAB_0462e688;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppuVar6 = (undefined *****)__Znwm(uVar1);
    local_78 = uVar1 | 0x8000000000000000;
    local_88 = (undefined ****)pppppuVar6;
    local_80 = (undefined8 *)sVar3;
LAB_0462e688:
    _memcpy(pppppuVar6,DAT_0a45ce88,sVar3);
  }
  *(undefined1 *)((long)pppppuVar6 + sVar3) = 0;
  uVar2 = FUN_0594199c(&local_88);
  if ((long)local_78 < 0) {
    __ZdlPvm(local_88,local_78 & 0x7fffffffffffffff);
  }
  uVar4 = __Znwm(0x1b0);
  thunk_FUN_05ab105c(uVar4,uVar2);
  FUN_0462eaf0(uVar2,uVar4);
  FUN_05ab0c5c(param_1[9]);
  uVar4 = __Znwm(0x138);
  thunk_FUN_05dafb00(uVar4,uVar2);
  FUN_0462ebec(uVar2,uVar4);
  FUN_05daddd0(param_1[6]);
  uVar4 = __Znwm(0x80);
  thunk_FUN_0597a624(uVar4,uVar2);
  FUN_0462ece8(uVar2,uVar4);
  FUN_05975054(param_1[7]);
  uVar4 = __Znwm(0xf8);
  thunk_FUN_05cabda0(uVar4,uVar2);
  FUN_0462ede4(uVar2,uVar4);
  FUN_05cab538(param_1[10]);
  uVar4 = __Znwm(0x38);
  thunk_FUN_05cf25cc(uVar4,uVar2);
  FUN_0462eee0(uVar2,uVar4);
  FUN_05cf0c08(param_1[8]);
  uVar4 = __Znwm(0x50);
  thunk_FUN_05ac4688(uVar4,uVar2);
  FUN_0462efdc(uVar2,uVar4);
  uVar4 = __Znwm(0x28);
  thunk_FUN_05dd8994(uVar4,uVar2);
  FUN_0462f0d8(uVar2,uVar4);
  uVar4 = __Znwm(0x30);
  thunk_FUN_05cc1854(uVar4,uVar2);
  FUN_0462f1d4(uVar2,uVar4);
  uVar5 = __Znwm(0x10);
  FUN_0462d86c(uVar5,param_1);
  param_1[0xb] = uVar5;
  FUN_05cc1c54(uVar4,uVar5);
  param_1[0xc] = uVar4;
  param_1[4] = uVar2;
  FUN_05cef588();
  if ((DAT_0a45ce90 & 1) == 0) {
    DAT_0a45ce88[0] = s_default_084c7818[0];
    DAT_0a45ce88[1] = s_default_084c7818[1];
    DAT_0a45ce88[2] = s_default_084c7818[2];
    DAT_0a45ce88[3] = s_default_084c7818[3];
    DAT_0a45ce88[4] = s_default_084c7818[4];
    DAT_0a45ce88[5] = s_default_084c7818[5];
    DAT_0a45ce88[6] = s_default_084c7818[6];
    DAT_0a45ce88[7] = s_default_084c7818[7];
    DAT_0a45ce90 = 1;
  }
  sVar3 = _strlen(DAT_0a45ce88);
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_88);
  }
  if (sVar3 < 0x17) {
    local_78 = CONCAT17((char)sVar3,(undefined7)local_78);
    pppppuVar6 = &local_88;
    if (sVar3 != 0) goto LAB_0462e894;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppuVar6 = (undefined *****)__Znwm(uVar1);
    local_78 = uVar1 | 0x8000000000000000;
    local_88 = (undefined ****)pppppuVar6;
    local_80 = (undefined8 *)sVar3;
LAB_0462e894:
    _memcpy(pppppuVar6,DAT_0a45ce88,sVar3);
  }
  *(undefined1 *)((long)pppppuVar6 + sVar3) = 0;
  FUN_05cef5b8(1,&local_88);
  if ((long)local_78 < 0) {
    __ZdlPvm(local_88,local_78 & 0x7fffffffffffffff);
  }
  _registerNetworkChangeNotifier();
  local_88 = (undefined ****)&PTR_FUN_09e8ff28;
  local_80 = param_1;
  local_70 = (undefined ****)&local_88;
  _addCallbackToNetworkChangeNotifier(&local_88);
  if ((undefined *****)local_70 == &local_88) {
    pppuVar7 = (undefined ***)(*local_70)[4];
  }
  else {
    if ((undefined *****)local_70 == (undefined *****)0x0) goto LAB_0462e918;
    pppuVar7 = (undefined ***)(*local_70)[5];
  }
  (*(code *)pppuVar7)();
LAB_0462e918:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


