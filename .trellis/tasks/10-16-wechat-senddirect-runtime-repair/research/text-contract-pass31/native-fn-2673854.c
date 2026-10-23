// Ghidra inferred pseudocode; requested=0x2673854
// entry=02673854 end=02673a43

void FUN_02673854(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 long param_5)

{
  int iVar1;
  long lVar2;
  undefined8 *puVar3;
  undefined4 uVar4;
  undefined8 uVar5;
  undefined8 local_78 [2];
  undefined7 local_68;
  char cStack_61;
  undefined8 local_60;
  undefined8 uStack_58;
  ulong local_50;
  
  *(uint *)(param_5 + 0x148) = *(uint *)(param_5 + 0x148) | 1;
  *(undefined4 *)(param_5 + 0x68) = 4;
  iVar1 = FUN_02673688();
  uVar4 = 7;
  if (iVar1 == 0) {
    uVar4 = 3;
  }
  *(uint *)(param_5 + 0x148) = *(uint *)(param_5 + 0x148) | 0x100000;
  *(undefined4 *)(param_5 + 0xcc) = uVar4;
  lVar2 = __ZNSt3__16chrono12system_clock3nowEv();
  __ZNSt3__19to_stringEx(local_78,lVar2 / 1000);
  if ((DAT_0a391f8c & 1) == 0) {
    DAT_0a391f88 = (undefined4)DAT_087e2e20;
    DAT_0a391f8c = 1;
  }
  puVar3 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                     (local_78,0,&DAT_0a391f88);
  uStack_58 = puVar3[1];
  local_60 = *puVar3;
  local_50 = puVar3[2];
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = 0;
  *(uint *)(param_5 + 0x148) = *(uint *)(param_5 + 0x148) | 0x40000;
  puVar3 = *(undefined8 **)(param_5 + 0xc0);
  if (puVar3 == &DAT_0a524ad0) {
    puVar3 = (undefined8 *)__Znwm(0x18);
    *puVar3 = 0;
    puVar3[1] = 0;
    puVar3[2] = 0;
    *(undefined8 **)(param_5 + 0xc0) = puVar3;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar3,&local_60);
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  if (cStack_61 < '\0') {
    __ZdlPvm(local_78[0],CONCAT17(cStack_61,local_68) & 0x7fffffffffffffff);
  }
  *(uint *)(param_5 + 0x148) = *(uint *)(param_5 + 0x148) | 0x20000000;
  puVar3 = *(undefined8 **)(param_5 + 0x110);
  if (puVar3 == &DAT_0a524ad0) {
    puVar3 = (undefined8 *)__Znwm(0x18);
    puVar3[1] = 0;
    puVar3[2] = 0;
    *puVar3 = 0;
    *(undefined8 **)(param_5 + 0x110) = puVar3;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar3,param_3);
  *(undefined4 *)(param_5 + 0x6c) = 0;
  uVar5 = *(undefined8 *)(param_5 + 0x148);
  *(ulong *)(param_5 + 0x148) =
       CONCAT17((byte)((ulong)uVar5 >> 0x38) | (byte)((ulong)DAT_087e2e28 >> 0x38),
                CONCAT16((byte)((ulong)uVar5 >> 0x30) | (byte)((ulong)DAT_087e2e28 >> 0x30),
                         CONCAT15((byte)((ulong)uVar5 >> 0x28) | (byte)((ulong)DAT_087e2e28 >> 0x28)
                                  ,CONCAT14((byte)((ulong)uVar5 >> 0x20) |
                                            (byte)((ulong)DAT_087e2e28 >> 0x20),
                                            CONCAT13((byte)((ulong)uVar5 >> 0x18) |
                                                     (byte)((ulong)DAT_087e2e28 >> 0x18),
                                                     CONCAT12((byte)((ulong)uVar5 >> 0x10) |
                                                              (byte)((ulong)DAT_087e2e28 >> 0x10),
                                                              CONCAT11((byte)((ulong)uVar5 >> 8) |
                                                                       (byte)((ulong)DAT_087e2e28 >>
                                                                             8),(byte)uVar5 |
                                                                                (byte)DAT_087e2e28))
                                                    )))));
  puVar3 = *(undefined8 **)(param_5 + 0x138);
  if (puVar3 == &DAT_0a524ad0) {
    puVar3 = (undefined8 *)__Znwm(0x18);
    puVar3[1] = 0;
    puVar3[2] = 0;
    *puVar3 = 0;
    *(undefined8 **)(param_5 + 0x138) = puVar3;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar3,param_4);
  FUN_02673568(param_1,param_2,param_5);
  return;
}


