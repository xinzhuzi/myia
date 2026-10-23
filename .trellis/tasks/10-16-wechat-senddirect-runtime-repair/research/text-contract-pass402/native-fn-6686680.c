// Ghidra inferred pseudocode; requested=0x6686680
// entry=06686680 end=0668688b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06686680(undefined8 *param_1,long param_2)

{
  long lVar1;
  undefined8 uVar2;
  long *plVar3;
  long *plVar4;
  long *plVar5;
  
  if (*(char *)(param_2 + 0x98) == '\x01') {
    if ((*(byte *)(param_1 + 1) & 1) == 0) {
      if ((DAT_0a5189f8 & 1) == 0) {
        _DAT_0a5189d8 = CONCAT44((int)DAT_09683050,(int)ram0x085a1170);
        uRam000000000a5189e0 = CONCAT44((int)DAT_09683058,(int)DAT_08b4d180);
        _DAT_0a5189e8 = CONCAT44((int)DAT_08487d20,(int)DAT_08b4d180);
        uRam000000000a5189f0 = CONCAT44((int)DAT_084d00d8,(int)DAT_08522670);
        DAT_0a5189f8 = 1;
      }
                    /* WARNING: Subroutine does not return */
      __ZNSt3__120__throw_system_errorEiPKc(1,&DAT_0a5189d8);
    }
    __ZNSt3__115recursive_mutex6unlockEv(*param_1);
    *(undefined1 *)(param_1 + 1) = 0;
    if (param_2 != 0) {
      plVar4 = *(long **)(param_2 + 0x80);
      if (plVar4 != (long *)0x0) {
        do {
          plVar5 = (long *)*plVar4;
          plVar3 = (long *)plVar4[10];
          if (plVar3 != (long *)0x0) {
            LOAcquire();
            lVar1 = plVar3[1];
            plVar3[1] = lVar1 + -1;
            LORelease();
            if (lVar1 == 0) {
              (**(code **)(*plVar3 + 0x10))(plVar3);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
            }
          }
          __ZdlPvm(plVar4,0x60);
          plVar4 = plVar5;
        } while (plVar5 != (long *)0x0);
        *(undefined8 *)(param_2 + 0x80) = 0;
        *(long **)(param_2 + 0x88) = (long *)(param_2 + 0x80);
      }
      __ZNSt3__115recursive_mutexD1Ev(param_2 + 0x40);
      uVar2 = __ZNSt3__15mutexD1Ev(param_2);
      __ZdlPvm(uVar2,0xa0);
      return;
    }
  }
  else {
    __ZNSt3__15mutex4lockEv(param_2);
    if (*(char *)(param_2 + 0x99) == '\x01') {
      plVar4 = (long *)(param_2 + 0x80);
      plVar3 = (long *)*plVar4;
      while (plVar3 != (long *)0x0) {
        while (plVar5 = plVar3, (*(byte *)(plVar5 + 7) >> 1 & 1) == 0) {
          plVar3 = (long *)*plVar5;
          plVar4 = plVar5;
          if ((long *)*plVar5 == (long *)0x0) goto LAB_066867bc;
        }
        if (plVar5 == *(long **)(param_2 + 0x88)) {
          *(long **)(param_2 + 0x88) = plVar4;
        }
        *plVar4 = *plVar5;
        plVar3 = (long *)plVar5[10];
        if (plVar3 != (long *)0x0) {
          LOAcquire();
          lVar1 = plVar3[1];
          plVar3[1] = lVar1 + -1;
          LORelease();
          if (lVar1 == 0) {
            (**(code **)(*plVar3 + 0x10))(plVar3);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
          }
        }
        __ZdlPvm(plVar5,0x60);
        plVar3 = (long *)*plVar4;
      }
LAB_066867bc:
      *(undefined1 *)(param_2 + 0x99) = 0;
    }
    __ZNSt3__15mutex6unlockEv(param_2);
    *(undefined8 *)(param_2 + 0x90) = 0;
  }
  return;
}


