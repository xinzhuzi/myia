// Ghidra inferred pseudocode; requested=0x30e3fb0
// entry=030e3fb0 end=030e6e4f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030e3fb0(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  ulong uVar1;
  long lVar2;
  size_t sVar3;
  long *plVar4;
  undefined8 *******pppppppuVar5;
  undefined8 ******local_98;
  long *local_90;
  undefined8 local_88;
  undefined8 ******local_80;
  size_t local_78;
  undefined8 local_70;
  undefined1 uStack_61;
  
  FUN_030e74f4(&local_80);
  FUN_030e7aa0(&local_98,&uStack_61,param_3);
  FUN_030e7be8(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,1);
  FUN_030e74f4(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e75c4(&local_80);
  FUN_030e8468(&local_98,&uStack_61,param_3);
  FUN_030e85b0(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,3);
  FUN_030e75c4(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,2);
  FUN_030e75c4(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e7694(&local_80);
  FUN_030e899c(&local_98,&uStack_61,param_3);
  FUN_030e8ae4(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,6);
  FUN_030e7694(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x4a);
  FUN_030e7694(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x82);
  FUN_030e7694(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x83);
  FUN_030e7694(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e7764(&local_80);
  FUN_030e8ed0(&local_98,&uStack_61,param_3);
  FUN_030e90c0(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x2b);
  FUN_030e7764(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e7834(&local_80);
  FUN_030e94ac(&local_98,&uStack_61,param_3);
  FUN_030e95f4(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d96cc & 1) == 0) {
    _DAT_0a3d96b4 = CONCAT44((int)DAT_084a6be8,(int)DAT_085098f0);
    uRam000000000a3d96bc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d96c4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d96cc = 1;
  }
  sVar3 = _strlen(&DAT_0a3d96b4);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e4444;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e4444:
    _memcpy(pppppppuVar5,&DAT_0a3d96b4,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030e99e0(&local_98,&uStack_61,param_3);
  FUN_030e9b18(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d96e8 & 1) == 0) {
    _DAT_0a3d96d0 = CONCAT44((int)DAT_088b0058,(int)DAT_08537e50);
    uRam000000000a3d96d8 = CONCAT44((int)DAT_084a66b0,(int)DAT_085cb7f0);
    DAT_0a3d96e0 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d96e8 = 1;
  }
  sVar3 = _strlen(&DAT_0a3d96d0);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e456c;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e456c:
    _memcpy(pppppppuVar5,&DAT_0a3d96d0,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030e9f04(&local_98,&uStack_61,param_3);
  FUN_030ea04c(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d970a & 1) == 0) {
    _DAT_0a3d96ec = CONCAT44((int)DAT_08518868,(int)DAT_087e0408);
    uRam000000000a3d96f4 = CONCAT44((int)DAT_088b0060,(int)DAT_086e6970);
    DAT_0a3d96fc = CONCAT44((int)DAT_088b0068,(int)DAT_0848f630);
    DAT_0a3d9704 = (undefined4)DAT_08480590;
    DAT_0a3d9708 = 0x72;
    DAT_0a3d970a = 1;
  }
  sVar3 = _strlen(&DAT_0a3d96ec);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e46b0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e46b0:
    _memcpy(pppppppuVar5,&DAT_0a3d96ec,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030ea438(&local_98,&uStack_61,param_3);
  FUN_030ea570(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,1);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x8b);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,4);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,5);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x21);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x2c);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x24);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x33);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x3f);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x65);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x58);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x13);
  if ((DAT_0a3d96cc & 1) == 0) {
    _DAT_0a3d96b4 = CONCAT44((int)DAT_084a6be8,(int)DAT_085098f0);
    uRam000000000a3d96bc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d96c4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d96cc = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d96b4);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e4a74:
    _memcpy(pppppppuVar5,&DAT_0a3d96b4,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e4a74;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x28);
  if ((DAT_0a3d96e8 & 1) == 0) {
    _DAT_0a3d96d0 = CONCAT44((int)DAT_088b0058,(int)DAT_08537e50);
    uRam000000000a3d96d8 = CONCAT44((int)DAT_084a66b0,(int)DAT_085cb7f0);
    DAT_0a3d96e0 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d96e8 = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d96d0);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e4b78:
    _memcpy(pppppppuVar5,&DAT_0a3d96d0,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e4b78;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x44);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x32);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x69);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x5c);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x5d);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x6b);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,3);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,2000);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x18);
  if ((DAT_0a3d96cc & 1) == 0) {
    _DAT_0a3d96b4 = CONCAT44((int)DAT_084a6be8,(int)DAT_085098f0);
    uRam000000000a3d96bc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d96c4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d96cc = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d96b4);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e4e54:
    _memcpy(pppppppuVar5,&DAT_0a3d96b4,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e4e54;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x52);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x6f);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x60);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x35);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x84);
  FUN_030e7834(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d9724 & 1) == 0) {
    _DAT_0a3d970c = CONCAT44((int)DAT_08508328,(int)DAT_084b0220);
    uRam000000000a3d9714 = CONCAT44((int)DAT_084a66b0,(int)DAT_088b0070);
    DAT_0a3d971c = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d9724 = 1;
  }
  sVar3 = _strlen(&DAT_0a3d970c);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e507c;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e507c:
    _memcpy(pppppppuVar5,&DAT_0a3d970c,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030ea95c(&local_98,&uStack_61,param_3);
  FUN_030eaa94(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x39);
  if ((DAT_0a3d9724 & 1) == 0) {
    _DAT_0a3d970c = CONCAT44((int)DAT_08508328,(int)DAT_084b0220);
    uRam000000000a3d9714 = CONCAT44((int)DAT_084a66b0,(int)DAT_088b0070);
    DAT_0a3d971c = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d9724 = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d970c);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e51a8:
    _memcpy(pppppppuVar5,&DAT_0a3d970c,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e51a8;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030eae48(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d974a & 1) == 0) {
    _DAT_0a3d9728 = CONCAT44((int)DAT_0849a650,(int)DAT_08531fb8);
    uRam000000000a3d9730 = CONCAT44((int)DAT_088b0078,(int)DAT_084d65d8);
    _DAT_0a3d9738 = CONCAT44((int)DAT_0848f630,(int)DAT_084f8878);
    uRam000000000a3d9740 = CONCAT44((int)DAT_08480590,(int)DAT_088b0068);
    DAT_0a3d9748 = 0x72;
    DAT_0a3d974a = 1;
  }
  sVar3 = _strlen(&DAT_0a3d9728);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e52c0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e52c0:
    _memcpy(pppppppuVar5,&DAT_0a3d9728,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030eb240(&local_98,&uStack_61,param_3);
  FUN_030eb378(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x54);
  if ((DAT_0a3d974a & 1) == 0) {
    _DAT_0a3d9728 = CONCAT44((int)DAT_0849a650,(int)DAT_08531fb8);
    uRam000000000a3d9730 = CONCAT44((int)DAT_088b0078,(int)DAT_084d65d8);
    _DAT_0a3d9738 = CONCAT44((int)DAT_0848f630,(int)DAT_084f8878);
    uRam000000000a3d9740 = CONCAT44((int)DAT_08480590,(int)DAT_088b0068);
    DAT_0a3d9748 = 0x72;
    DAT_0a3d974a = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d9728);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e5404:
    _memcpy(pppppppuVar5,&DAT_0a3d9728,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e5404;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030eae48(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x67);
  if ((DAT_0a3d974a & 1) == 0) {
    _DAT_0a3d9728 = CONCAT44((int)DAT_0849a650,(int)DAT_08531fb8);
    uRam000000000a3d9730 = CONCAT44((int)DAT_088b0078,(int)DAT_084d65d8);
    _DAT_0a3d9738 = CONCAT44((int)DAT_0848f630,(int)DAT_084f8878);
    uRam000000000a3d9740 = CONCAT44((int)DAT_08480590,(int)DAT_088b0068);
    DAT_0a3d9748 = 0x72;
    DAT_0a3d974a = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d9728);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e551c:
    _memcpy(pppppppuVar5,&DAT_0a3d9728,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e551c;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030eae48(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e7900(&local_80);
  FUN_030eb72c(&local_98,&uStack_61,param_3);
  FUN_030eb910(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x22);
  FUN_030e7900(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d977f & 1) == 0) {
    _DAT_0a3d9768 = CONCAT44((int)DAT_0849d688,(int)DAT_084b0520);
    uRam000000000a3d9770 = CONCAT44((int)DAT_087ef148,(int)DAT_084b0670);
    DAT_0a3d9778 = (undefined4)DAT_08492398;
    DAT_0a3d977c = 0x7265;
    DAT_0a3d977e = 0;
    DAT_0a3d977f = 1;
  }
  sVar3 = _strlen(&DAT_0a3d9768);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e56ac;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e56ac:
    _memcpy(pppppppuVar5,&DAT_0a3d9768,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030ebcfc(&local_98,&uStack_61,param_3);
  FUN_030ebe44(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x2f);
  if ((DAT_0a3d977f & 1) == 0) {
    _DAT_0a3d9768 = CONCAT44((int)DAT_0849d688,(int)DAT_084b0520);
    uRam000000000a3d9770 = CONCAT44((int)DAT_087ef148,(int)DAT_084b0670);
    DAT_0a3d9778 = (undefined4)DAT_08492398;
    DAT_0a3d977c = 0x7265;
    DAT_0a3d977e = 0;
    DAT_0a3d977f = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d9768);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e57d0:
    _memcpy(pppppppuVar5,&DAT_0a3d9768,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e57d0;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,8);
  if ((DAT_0a3d977f & 1) == 0) {
    _DAT_0a3d9768 = CONCAT44((int)DAT_0849d688,(int)DAT_084b0520);
    uRam000000000a3d9770 = CONCAT44((int)DAT_087ef148,(int)DAT_084b0670);
    DAT_0a3d9778 = (undefined4)DAT_08492398;
    DAT_0a3d977c = 0x7265;
    DAT_0a3d977e = 0;
    DAT_0a3d977f = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d9768);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e58cc:
    _memcpy(pppppppuVar5,&DAT_0a3d9768,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e58cc;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e79d0(&local_80);
  FUN_030ec230(&local_98,&uStack_61,param_3);
  FUN_030ec3a4(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x32);
  FUN_030e79d0(&local_98);
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d97a9 & 1) == 0) {
    _DAT_0a3d9794 = CONCAT44((int)DAT_088b0080,(int)DAT_084d1d30);
    uRam000000000a3d979c = CONCAT44((int)DAT_088aaf20,(int)DAT_084a8110);
    DAT_0a3d97a4 = (undefined4)DAT_084d88d0;
    DAT_0a3d97a8 = 0;
    DAT_0a3d97a9 = 1;
  }
  sVar3 = _strlen(&DAT_0a3d9794);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e5a54;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e5a54:
    _memcpy(pppppppuVar5,&DAT_0a3d9794,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030ec790(&local_98,&uStack_61,param_3);
  FUN_030ec8d8(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,"elease_02/out/build_arm64/RelWithDebInfo");
  if ((DAT_0a3d97a9 & 1) == 0) {
    _DAT_0a3d9794 = CONCAT44((int)DAT_088b0080,(int)DAT_084d1d30);
    uRam000000000a3d979c = CONCAT44((int)DAT_088aaf20,(int)DAT_084a8110);
    DAT_0a3d97a4 = (undefined4)DAT_084d88d0;
    DAT_0a3d97a8 = 0;
    DAT_0a3d97a9 = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d9794);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e5b74:
    _memcpy(pppppppuVar5,&DAT_0a3d9794,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e5b74;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d97c3 & 1) == 0) {
    _DAT_0a3d97ac = CONCAT44((int)DAT_08482f20,(int)DAT_0848a170);
    uRam000000000a3d97b4 = CONCAT44((int)DAT_087ef148,(int)DAT_084b0670);
    DAT_0a3d97bc = (undefined4)DAT_08492398;
    DAT_0a3d97c0 = 0x7265;
    DAT_0a3d97c2 = 0;
    DAT_0a3d97c3 = 1;
  }
  sVar3 = _strlen(&DAT_0a3d97ac);
  if (0x7ffffffffffffff7 < sVar3) goto LAB_030e6da4;
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e5c70;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e5c70:
    _memcpy(pppppppuVar5,&DAT_0a3d97ac,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030eccc4(&local_98,&uStack_61,param_3);
  FUN_030ece0c(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x30);
  if ((DAT_0a3d97c3 & 1) == 0) {
    _DAT_0a3d97ac = CONCAT44((int)DAT_08482f20,(int)DAT_0848a170);
    uRam000000000a3d97b4 = CONCAT44((int)DAT_087ef148,(int)DAT_084b0670);
    DAT_0a3d97bc = (undefined4)DAT_08492398;
    DAT_0a3d97c0 = 0x7265;
    DAT_0a3d97c2 = 0;
    DAT_0a3d97c3 = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d97ac);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e5d98:
    _memcpy(pppppppuVar5,&DAT_0a3d97ac,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e5d98;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3d97dc & 1) == 0) {
    _DAT_0a3d97c4 = CONCAT44((int)DAT_085095b8,(int)ram0x08490a68);
    uRam000000000a3d97cc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d97d4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d97dc = 1;
  }
  sVar3 = _strlen(&DAT_0a3d97c4);
  if (0x7ffffffffffffff7 < sVar3) {
LAB_030e6da4:
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_80);
  }
  if (sVar3 < 0x17) {
    local_70 = CONCAT17((char)sVar3,(undefined7)local_70);
    pppppppuVar5 = &local_80;
    if (sVar3 != 0) goto LAB_030e5e94;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = pppppppuVar5;
    local_78 = sVar3;
LAB_030e5e94:
    _memcpy(pppppppuVar5,&DAT_0a3d97c4,sVar3);
  }
  *(undefined1 *)((long)pppppppuVar5 + sVar3) = 0;
  FUN_030ed1f8(&local_98,&uStack_61,param_3);
  FUN_030ed340(param_1,&local_80,&local_80,&local_98);
  plVar4 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_90[1];
    local_90[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x2a);
  if ((DAT_0a3d97dc & 1) == 0) {
    _DAT_0a3d97c4 = CONCAT44((int)DAT_085095b8,(int)ram0x08490a68);
    uRam000000000a3d97cc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d97d4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d97dc = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d97c4);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e5fc0:
    _memcpy(pppppppuVar5,&DAT_0a3d97c4,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e5fc0;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x42);
  if ((DAT_0a3d97dc & 1) == 0) {
    _DAT_0a3d97c4 = CONCAT44((int)DAT_085095b8,(int)ram0x08490a68);
    uRam000000000a3d97cc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d97d4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d97dc = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d97c4);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e60b4:
    _memcpy(pppppppuVar5,&DAT_0a3d97c4,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e60b4;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  __ZNSt3__19to_stringEi(&local_80,0x43);
  if ((DAT_0a3d97dc & 1) == 0) {
    _DAT_0a3d97c4 = CONCAT44((int)DAT_085095b8,(int)ram0x08490a68);
    uRam000000000a3d97cc = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
    DAT_0a3d97d4 = CONCAT44((int)DAT_08483f50,(int)ram0x084cf8c0);
    DAT_0a3d97dc = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d97c4);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
LAB_030e61ac:
    _memcpy(pppppppuVar5,&DAT_0a3d97c4,(size_t)plVar4);
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 != (long *)0x0) goto LAB_030e61ac;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  FUN_030e3df8(&local_80,0x31,0x87);
  if ((DAT_0a3d970a & 1) == 0) {
    _DAT_0a3d96ec = CONCAT44((int)DAT_08518868,(int)DAT_087e0408);
    uRam000000000a3d96f4 = CONCAT44((int)DAT_088b0060,(int)DAT_086e6970);
    DAT_0a3d96fc = CONCAT44((int)DAT_088b0068,(int)DAT_0848f630);
    DAT_0a3d9704 = (undefined4)DAT_08480590;
    DAT_0a3d9708 = 0x72;
    DAT_0a3d970a = 1;
  }
  plVar4 = (long *)_strlen(&DAT_0a3d96ec);
  if ((long *)0x7ffffffffffffff7 < plVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_98);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar4) {
    uVar1 = 0x19;
    if (((ulong)plVar4 | 7) != 0x17) {
      uVar1 = ((ulong)plVar4 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_88 = uVar1 | 0x8000000000000000;
    local_98 = pppppppuVar5;
    local_90 = plVar4;
  }
  else {
    local_88 = CONCAT17((char)plVar4,(undefined7)local_88);
    pppppppuVar5 = &local_98;
    if (plVar4 == (long *)0x0) goto LAB_030e62dc;
  }
  _memcpy(pppppppuVar5,&DAT_0a3d96ec,(size_t)plVar4);
LAB_030e62dc:
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar4) = 0;
  FUN_030e7fd4(param_2,&local_80,&local_80,&local_98);
  if ((long)local_88 < 0) {
    __ZdlPvm(local_98,local_88 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  return;
}


