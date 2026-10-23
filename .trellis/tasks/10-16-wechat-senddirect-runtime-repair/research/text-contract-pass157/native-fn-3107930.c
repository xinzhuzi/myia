// Ghidra inferred pseudocode; requested=0x3107930
// entry=03107930 end=03107a3f

void FUN_03107930(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  undefined8 *puVar1;
  uint uVar2;
  undefined8 *puVar3;
  long lVar4;
  undefined8 local_48 [2];
  undefined7 local_38;
  char cStack_31;
  
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  puVar3 = (undefined8 *)__Znwm(0x290);
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = &PTR_FUN_09c92390;
  puVar1 = puVar3 + 3;
  _bzero(puVar1,0x278);
  FUN_00ac6038(puVar1);
  *param_1 = puVar1;
  param_1[1] = puVar3;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (puVar3 + 6,*param_3 + 0x18);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (puVar3 + 9,*param_3 + 0x30);
  *(undefined4 *)(puVar3 + 0x26) = *(undefined4 *)(*param_3 + 0x118);
  FUN_04cbbc88(local_48);
  FUN_04cbb728(puVar1,local_48);
  if (cStack_31 < '\0') {
    __ZdlPvm(local_48[0],CONCAT17(cStack_31,local_38) & 0x7fffffffffffffff);
  }
  lVar4 = *param_3;
  uVar2 = *(uint *)(lVar4 + 0x114);
  *(uint *)((long)puVar3 + 300) = uVar2;
  puVar3[0x23] = (ulong)uVar2 * 1000;
  puVar3[0x23] = *(undefined8 *)(lVar4 + 0x100);
  *(undefined4 *)(puVar3 + 0x28) = *(undefined4 *)(lVar4 + 0x128);
  FUN_04cbf994();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (puVar3 + 0x2f,*param_3 + 0x160);
  FUN_04cbbd20(puVar1,1);
  return;
}


