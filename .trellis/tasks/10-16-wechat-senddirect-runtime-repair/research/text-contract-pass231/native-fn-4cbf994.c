// Ghidra inferred pseudocode; requested=0x4cbf994
// entry=04cbf994 end=04cbfa87

void FUN_04cbf994(long param_1)

{
  long lVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  long *plVar4;
  undefined8 local_38 [2];
  undefined7 local_28;
  char cStack_21;
  
  if (*(long *)(param_1 + 0x230) == 0) {
    puVar2 = (undefined8 *)__Znwm(0x128);
    puVar2[1] = 0;
    puVar2[2] = 0;
    *puVar2 = &PTR_FUN_09dd9070;
    puVar2[6] = 0;
    puVar2[5] = 0;
    puVar2[8] = 0;
    puVar2[7] = 0;
    puVar2[10] = 0;
    puVar2[9] = 0;
    puVar2[0xc] = 0;
    puVar2[0xb] = 0;
    puVar2[0xe] = 0;
    puVar2[0xd] = 0;
    puVar2[0x10] = 0;
    puVar2[0xf] = 0;
    puVar2[0x12] = 0;
    puVar2[0x11] = 0;
    puVar2[0x14] = 0;
    puVar2[0x13] = 0;
    puVar2[0x16] = 0;
    puVar2[0x15] = 0;
    puVar2[0x18] = 0;
    puVar2[0x17] = 0;
    puVar2[0x1a] = 0;
    puVar2[0x19] = 0;
    puVar2[0x1c] = 0;
    puVar2[0x1b] = 0;
    puVar2[0x1e] = 0;
    puVar2[0x1d] = 0;
    puVar2[0x20] = 0;
    puVar2[0x1f] = 0;
    plVar4 = *(long **)(param_1 + 0x238);
    *(undefined8 **)(param_1 + 0x238) = puVar2;
    puVar3 = puVar2 + 3;
    puVar2[4] = 0;
    *puVar3 = 0;
    puVar2[0x22] = 0;
    puVar2[0x21] = 0;
    puVar2[0x24] = 0;
    puVar2[0x23] = 0;
    *(undefined8 **)(param_1 + 0x230) = puVar3;
    if (plVar4 != (long *)0x0) {
      LOAcquire();
      lVar1 = plVar4[1];
      plVar4[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*plVar4 + 0x10))(plVar4);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
      puVar3 = *(undefined8 **)(param_1 + 0x230);
    }
    if (puVar3 == (undefined8 *)0x0) {
      return;
    }
  }
  FUN_04d1dd74(local_38);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x160,local_38)
  ;
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38[0],CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  return;
}


