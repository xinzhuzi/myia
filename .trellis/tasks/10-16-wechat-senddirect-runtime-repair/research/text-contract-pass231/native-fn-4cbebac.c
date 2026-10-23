// Ghidra inferred pseudocode; requested=0x4cbebac
// entry=04cbebac end=04cbeeaf

void FUN_04cbebac(long param_1)

{
  undefined8 uVar1;
  long lVar2;
  int iVar3;
  undefined8 *puVar4;
  ulong uVar5;
  long *plVar6;
  undefined8 *puVar7;
  long *plVar8;
  undefined8 local_50;
  long *plStack_48;
  undefined1 uStack_31;
  
  if (*(long *)(param_1 + 0x220) == 0) {
    iVar3 = FUN_04a290c4();
    if (iVar3 == 0) {
      iVar3 = FUN_04a29d84(param_1);
      if (iVar3 == 0) {
        iVar3 = FUN_04a28ecc(param_1);
        if (iVar3 == 0) {
          uVar5 = FUN_04a28ae8(param_1);
          if (((uVar5 & 1) == 0) && (iVar3 = FUN_04a2bd4c(param_1), iVar3 == 0)) {
            iVar3 = FUN_04a28f24(param_1);
            if (iVar3 != 0) {
              FUN_04cc346c(&local_50,&uStack_31);
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            iVar3 = FUN_04a28ea8(param_1);
            if (iVar3 != 0) {
              FUN_04cbeef0(&local_50);
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            iVar3 = FUN_04a292d4(param_1);
            if (iVar3 != 0) {
              FUN_04cc22cc(&local_50,&uStack_31);
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            iVar3 = FUN_04a292c4(param_1);
            if (iVar3 != 0) {
              FUN_04cbef40(&local_50);
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            iVar3 = FUN_04a2965c(param_1);
            if (iVar3 != 0) {
              FUN_04cbf048(&local_50);
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            iVar3 = FUN_04a292e4(param_1);
            if (iVar3 != 0) {
              FUN_04cbf170(&local_50);
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            iVar3 = FUN_04a2964c(param_1);
            if (iVar3 != 0) {
              FUN_04cbf298();
              FUN_002652cc(param_1 + 0x220,&local_50);
              FUN_00129f68(&local_50);
              return;
            }
            FUN_04cbf3c0(&local_50);
            FUN_002652cc(param_1 + 0x220,&local_50);
            FUN_00129f68(&local_50);
            return;
          }
          FUN_04cc32dc(&local_50,&uStack_31);
        }
        else {
          FUN_04cc3170(&local_50,&uStack_31);
        }
        plVar8 = plStack_48;
        uVar1 = local_50;
        local_50 = 0;
        plStack_48 = (long *)0x0;
        plVar6 = *(long **)(param_1 + 0x228);
        *(long **)(param_1 + 0x228) = plVar8;
        *(undefined8 *)(param_1 + 0x220) = uVar1;
        if (plVar6 != (long *)0x0) {
          LOAcquire();
          lVar2 = plVar6[1];
          plVar6[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*plVar6 + 0x10))(plVar6);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
          }
        }
        plVar8 = plStack_48;
        if (plStack_48 == (long *)0x0) {
          return;
        }
        LOAcquire();
        lVar2 = plStack_48[1];
        plStack_48[1] = lVar2 + -1;
        LORelease();
        if (lVar2 != 0) {
          return;
        }
        (**(code **)(*plStack_48 + 0x10))(plStack_48);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        return;
      }
      puVar4 = (undefined8 *)__Znwm(0x808);
      puVar4[1] = 0;
      puVar4[2] = 0;
      *puVar4 = &PTR_FUN_09c69900;
      puVar7 = puVar4 + 3;
      _bzero(puVar7,0x7f0);
      FUN_00ad6ec4(puVar7);
    }
    else {
      puVar4 = (undefined8 *)__Znwm(0x2f0);
      puVar4[1] = 0;
      puVar4[2] = 0;
      *puVar4 = &PTR_FUN_09eb08c0;
      puVar7 = puVar4 + 3;
      _bzero(puVar7,0x2d8);
      FUN_04cc2f94(puVar7);
    }
    *(undefined8 **)(param_1 + 0x220) = puVar7;
    plVar8 = *(long **)(param_1 + 0x228);
    *(undefined8 **)(param_1 + 0x228) = puVar4;
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar8[1];
      plVar8[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        return;
      }
    }
  }
  return;
}


