// Ghidra inferred pseudocode; requested=0x6666214
// entry=06666214 end=066662c7

undefined8 * FUN_06666214(undefined8 *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 uVar1;
  undefined8 in_xzr;
  undefined8 local_50;
  undefined8 uStack_48;
  
  *param_1 = &PTR_thunk_FUN_06666304_09fb1a48;
  param_1[1] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  __ZNSt3__17promiseIvEC1Ev(param_1 + 7);
  param_1[3] = param_2;
  uVar1 = __Znwm(0x118);
  FUN_0666258c(uVar1,param_2,param_3);
  param_1[1] = uVar1;
  param_1[2] = uVar1;
  param_1[4] = in_xzr;
  __ZNSt3__17promiseIvE10get_futureEv(&local_50,param_1 + 7);
  uVar1 = local_50;
  uStack_48 = param_1[6];
  local_50 = 0;
  param_1[6] = uVar1;
  __ZNSt3__16futureIvED1Ev(&uStack_48);
  __ZNSt3__16futureIvED1Ev(&local_50);
  param_1[8] = 0;
  return param_1;
}


