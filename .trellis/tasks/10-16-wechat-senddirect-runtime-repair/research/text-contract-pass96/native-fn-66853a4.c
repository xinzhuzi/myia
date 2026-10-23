// Ghidra inferred pseudocode; requested=0x66853a4
// entry=066853a4 end=06685563

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 *
FUN_066853a4(undefined8 *param_1,char *param_2,char *param_3,undefined4 param_4,long param_5,
            undefined4 param_6,undefined8 *param_7)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  long *plVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  char *local_68;
  undefined4 local_5c;
  undefined *local_58;
  
  param_1[6] = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  param_1[5] = 0;
  param_1[4] = 0;
  param_1[1] = 0;
  *param_1 = 0;
  param_1[7] = 0x80000000ffffffff;
  param_1[9] = 0;
  uVar2 = FUN_066845a4();
  *param_1 = uVar2;
  lVar3 = FUN_02e0a888();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,lVar3);
  uVar2 = *(undefined8 *)(lVar3 + 0x18);
  uVar6 = *(undefined8 *)(lVar3 + 0x30);
  uVar5 = *(undefined8 *)(lVar3 + 0x28);
  param_1[5] = *(undefined8 *)(lVar3 + 0x20);
  param_1[4] = uVar2;
  param_1[7] = uVar6;
  param_1[6] = uVar5;
  if ((DAT_0a518930 & 1) == 0) {
    uRam000000000a518928._0_1_ = s_co_with_timeout_096865c0[8];
    uRam000000000a518928._1_1_ = s_co_with_timeout_096865c0[9];
    uRam000000000a518928._2_1_ = s_co_with_timeout_096865c0[10];
    uRam000000000a518928._3_1_ = s_co_with_timeout_096865c0[0xb];
    uRam000000000a518928._4_1_ = s_co_with_timeout_096865c0[0xc];
    uRam000000000a518928._5_1_ = s_co_with_timeout_096865c0[0xd];
    uRam000000000a518928._6_1_ = s_co_with_timeout_096865c0[0xe];
    uRam000000000a518928._7_1_ = s_co_with_timeout_096865c0[0xf];
    DAT_0a518920 = s_co_with_timeout_096865c0[0];
    DAT_0a518920_1._0_1_ = s_co_with_timeout_096865c0[1];
    DAT_0a518920_1._1_1_ = s_co_with_timeout_096865c0[2];
    DAT_0a518920_1._2_1_ = s_co_with_timeout_096865c0[3];
    DAT_0a518920_1._3_1_ = s_co_with_timeout_096865c0[4];
    DAT_0a518920_1._4_1_ = s_co_with_timeout_096865c0[5];
    DAT_0a518920_1._5_1_ = s_co_with_timeout_096865c0[6];
    DAT_0a518920_1._6_1_ = s_co_with_timeout_096865c0[7];
    DAT_0a518930 = 1;
  }
  local_58 = &DAT_0a518920;
  if ((DAT_0a51894b & 1) == 0) {
    DAT_0a518940._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
    DAT_0a518940._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
    DAT_0a518940._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
    DAT_0a518940._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
    DAT_0a518940._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
    DAT_0a518940._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
    DAT_0a518940._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
    DAT_0a518940._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
    DAT_0a518948 = 0x2928;
    DAT_0a51894a = 0;
    DAT_0a51894b = 1;
  }
  local_5c = param_4;
  iVar1 = _strcmp(param_2,(char *)&DAT_0a518940);
  local_68 = param_3;
  if (iVar1 != 0) {
    local_68 = param_2;
  }
  if ((DAT_0a518959 & 1) == 0) {
    DAT_0a518950 = DAT_096865d0;
    DAT_0a518958 = 0;
    DAT_0a518959 = 1;
  }
  FUN_066855b4(&local_80,&DAT_0a518950,&local_58,&local_68,&local_5c);
  if (*(char *)((long)param_1 + 0x1f) < '\0') {
    __ZdlPvm(param_1[1],param_1[3] & 0x7fffffffffffffff);
  }
  param_1[2] = uStack_78;
  param_1[1] = local_80;
  param_1[3] = local_70;
  if (param_5 != 0) {
    param_1[4] = param_5;
  }
  *(undefined4 *)(param_1 + 8) = param_6;
  uVar2 = *param_7;
  *param_7 = 0;
  plVar4 = (long *)param_1[9];
  param_1[9] = uVar2;
  if (plVar4 != (long *)0x0) {
    (**(code **)(*plVar4 + 8))();
  }
  return param_1;
}


