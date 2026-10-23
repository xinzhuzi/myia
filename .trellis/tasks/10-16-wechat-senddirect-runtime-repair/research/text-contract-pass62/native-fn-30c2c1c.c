// Ghidra inferred pseudocode; requested=0x30c2c1c
// entry=030c2c1c end=030c2d9f

undefined4
FUN_030c2c1c(long *param_1,undefined8 param_2,undefined8 param_3,long param_4,long *param_5)

{
  ulong uVar1;
  long lVar2;
  long *plVar3;
  undefined8 uVar4;
  long *plVar5;
  code *pcVar6;
  long *plVar7;
  long *plVar8;
  undefined1 *local_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *local_68;
  undefined1 *local_60;
  
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  local_90 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_030c14a4(&local_90);
  uVar1 = *(ulong *)(param_4 + 0x10);
  if (-1 < (char)*(byte *)(param_4 + 0x1f)) {
    uVar1 = (ulong)*(byte *)(param_4 + 0x1f);
  }
  if (uVar1 != 0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&puStack_78,param_4 + 8);
  }
  plVar3 = (long *)__Znwm(0xe0);
  FUN_030c2de4(plVar3,&local_90);
  uVar4 = (**(code **)(*plVar3 + 0x20))(plVar3);
  FUN_0465db80(uVar4,param_2);
  plVar8 = plVar3 + 0xd;
  plVar5 = (long *)*plVar8;
  plVar7 = plVar3 + 10;
  *plVar8 = 0;
  if (plVar5 == plVar7) {
    pcVar6 = *(code **)(*plVar5 + 0x20);
LAB_030c2cec:
    (*pcVar6)();
  }
  else if (plVar5 != (long *)0x0) {
    pcVar6 = *(code **)(*plVar5 + 0x28);
    goto LAB_030c2cec;
  }
  plVar5 = (long *)param_5[3];
  if (plVar5 != (long *)0x0) {
    if (plVar5 == param_5) {
      *plVar8 = (long)plVar7;
      (**(code **)(*plVar5 + 0x18))(plVar5,plVar7);
      goto LAB_030c2d28;
    }
    *plVar8 = (long)plVar5;
    plVar8 = param_5 + 3;
  }
  *plVar8 = 0;
LAB_030c2d28:
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar3 + 7,param_3);
  *(undefined1 *)(plVar3 + 0xe) = *(undefined1 *)(param_4 + 0x20);
  *(undefined4 *)((long)plVar3 + 0x74) = *(undefined4 *)(param_4 + 0x24);
  (**(code **)(*param_1 + 0x28))(param_1,plVar3);
  uVar4 = FUN_046a80c0();
  FUN_046a829c(uVar4,plVar3 + 3);
  lVar2 = plVar3[1];
  if ((long)local_68 < 0) {
    __ZdlPvm(puStack_78,(ulong)local_68 & 0x7fffffffffffffff);
  }
  return (int)lVar2;
}


