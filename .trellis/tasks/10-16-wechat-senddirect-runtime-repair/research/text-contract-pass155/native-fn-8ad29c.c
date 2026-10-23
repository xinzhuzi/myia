// Ghidra inferred pseudocode; requested=0x8ad29c
// entry=008ad29c end=008ad453

void FUN_008ad29c(undefined8 *param_1,undefined8 *param_2)

{
  ulong uVar1;
  undefined8 *******pppppppuVar2;
  undefined8 uVar3;
  undefined8 ******local_58;
  ulong uStack_50;
  undefined7 local_48;
  byte bStack_41;
  
  if (*(int *)((long)param_2 + 0x1c) == 0) {
    if (*(char *)((long)param_2 + 0x3f) < '\0') {
      if (param_2[6] != 0) {
        FUN_00018d20(param_1,param_2[5]);
        return;
      }
    }
    else if (*(char *)((long)param_2 + 0x3f) != '\0') {
      uVar3 = param_2[5];
      param_1[1] = param_2[6];
      *param_1 = uVar3;
      param_1[2] = param_2[7];
      return;
    }
  }
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    FUN_00018d20(param_1,*param_2,param_2[1]);
  }
  else {
    uVar3 = *param_2;
    param_1[1] = param_2[1];
    *param_1 = uVar3;
    param_1[2] = param_2[2];
  }
  if ((DAT_0a2a7daa & 1) == 0) {
    DAT_0a2a7da8 = 0x5f;
    DAT_0a2a7daa = 1;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc(param_1,&DAT_0a2a7da8)
  ;
  __ZNSt3__19to_stringEj(&local_58,*(undefined4 *)(param_2 + 3));
  uVar1 = uStack_50;
  pppppppuVar2 = (undefined8 *******)local_58;
  if (-1 < (char)bStack_41) {
    uVar1 = (ulong)bStack_41;
    pppppppuVar2 = &local_58;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
            (param_1,pppppppuVar2,uVar1);
  if ((char)bStack_41 < '\0') {
    __ZdlPvm(local_58,CONCAT17(bStack_41,local_48) & 0x7fffffffffffffff);
  }
  if ((DAT_0a2a7daa & 1) == 0) {
    DAT_0a2a7da8 = 0x5f;
    DAT_0a2a7daa = 1;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc(param_1,&DAT_0a2a7da8)
  ;
  __ZNSt3__19to_stringEj(&local_58,*(undefined4 *)((long)param_2 + 0x1c));
  pppppppuVar2 = (undefined8 *******)local_58;
  if (-1 < (char)bStack_41) {
    uStack_50 = (ulong)bStack_41;
    pppppppuVar2 = &local_58;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
            (param_1,pppppppuVar2,uStack_50);
  if ((char)bStack_41 < '\0') {
    __ZdlPvm(local_58,CONCAT17(bStack_41,local_48) & 0x7fffffffffffffff);
  }
  return;
}


