// Ghidra inferred pseudocode; requested=0x4cbc3ac
// entry=04cbc3ac end=04cbc4bf

void FUN_04cbc3ac(long param_1,int param_2)

{
  long *plVar1;
  undefined8 *puVar2;
  long lVar3;
  
  if (*(char *)(param_1 + 600) != '\x01' || param_2 != 0) {
    FUN_04cbebac();
    plVar1 = *(long **)(param_1 + 0x220);
    if (plVar1 != (long *)0x0) {
      (**(code **)(*plVar1 + 0x18))(plVar1,param_1);
    }
    *(undefined8 *)(param_1 + 0x108) = *(undefined8 *)(param_1 + 0xc);
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
      plVar1 = *(long **)(param_1 + 0x238);
      *(undefined8 **)(param_1 + 0x238) = puVar2;
      puVar2[4] = 0;
      puVar2[3] = 0;
      puVar2[0x22] = 0;
      puVar2[0x21] = 0;
      puVar2[0x24] = 0;
      puVar2[0x23] = 0;
      *(undefined8 **)(param_1 + 0x230) = puVar2 + 3;
      if (plVar1 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar1[1];
        plVar1[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar1 + 0x10))(plVar1);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
        }
      }
    }
    lVar3 = (long)*(char *)(param_1 + 0x177);
    if (lVar3 < 0) {
      lVar3 = *(long *)(param_1 + 0x168);
    }
    if (lVar3 != 0) {
      FUN_04d1c60c(*(undefined8 *)(param_1 + 0x230),param_1 + 0x160);
    }
    *(undefined1 *)(param_1 + 600) = 1;
  }
  return;
}


