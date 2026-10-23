// Ghidra inferred pseudocode; requested=0x3b1afc
// entry=003b1afc end=003b1c13

long * FUN_003b1afc(long *param_1,long param_2,long param_3)

{
  long lVar1;
  uint uVar2;
  int iVar3;
  long *plVar4;
  long lVar5;
  undefined8 uVar6;
  undefined1 *local_68;
  undefined1 *puStack_60;
  undefined1 auStack_58 [8];
  
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_60 = &SUB_aaaaaaaaaaaaaaaa;
  __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryC1ERS3_(&local_68,param_1);
  if ((char)local_68 == '\x01') {
    lVar5 = (long)param_1 + *(long *)(*param_1 + -0x18);
    uVar6 = *(undefined8 *)(lVar5 + 0x28);
    uVar2 = *(uint *)(lVar5 + 8);
    iVar3 = *(int *)(lVar5 + 0x90);
    if (iVar3 == -1) {
      __ZNKSt3__18ios_base6getlocEv(auStack_58,lVar5);
      plVar4 = (long *)__ZNKSt3__16locale9use_facetERNS0_2idE
                                 (auStack_58,PTR___ZNSt3__15ctypeIcE2idE_09b367c8);
      iVar3 = (**(code **)(*plVar4 + 0x38))(plVar4,0x20);
      __ZNSt3__16localeD1Ev(auStack_58);
      *(int *)(lVar5 + 0x90) = iVar3;
    }
    lVar1 = param_2 + param_3;
    if ((uVar2 & 0xb0) != 0x20) {
      lVar1 = param_2;
    }
    lVar5 = FUN_003b1c70(uVar6,param_2,lVar1,param_2 + param_3,lVar5,(int)(char)iVar3);
    if (lVar5 == 0) {
      lVar5 = (long)param_1 + *(long *)(*param_1 + -0x18);
      __ZNSt3__18ios_base5clearEj(lVar5,*(uint *)(lVar5 + 0x20) | 5);
    }
  }
  __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEE6sentryD1Ev(&local_68);
  return param_1;
}


