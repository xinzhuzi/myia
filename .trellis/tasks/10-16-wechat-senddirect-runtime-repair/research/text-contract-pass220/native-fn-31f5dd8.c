// Ghidra inferred pseudocode; requested=0x31f5dd8
// entry=031f5dd8 end=031f645f

/* WARNING: Removing unreachable block (ram,0x031f638c) */
/* WARNING: Type propagation algorithm not settling */

void FUN_031f5dd8(undefined8 param_1,undefined8 param_2,long *param_3)

{
  undefined8 ******ppppppuVar1;
  undefined8 ******ppppppuVar2;
  undefined8 *puVar3;
  undefined8 *******pppppppuVar4;
  long *plVar5;
  undefined8 *******pppppppuVar6;
  undefined8 *puVar7;
  long lVar8;
  undefined8 *****pppppuVar9;
  int iVar10;
  long lVar11;
  undefined8 uVar12;
  long lVar13;
  undefined8 *puVar14;
  long lVar15;
  undefined8 uVar16;
  undefined8 local_168;
  long *local_160;
  undefined8 local_158;
  long *local_150;
  undefined8 local_148;
  long *local_140;
  undefined1 auStack_138 [8];
  undefined8 local_130;
  undefined7 local_120;
  char cStack_119;
  long *local_110;
  undefined8 *******local_108;
  undefined8 ******local_100;
  undefined7 local_f8;
  byte bStack_f1;
  undefined8 *******local_f0;
  undefined8 ******ppppppuStack_e8;
  undefined8 ******local_e0;
  undefined8 local_d8;
  long *local_d0;
  ulong local_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  undefined4 local_a0;
  undefined4 uStack_9c;
  long local_90;
  long lStack_88;
  long *local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 *local_68;
  undefined8 *local_60;
  undefined8 *local_58;
  
  iVar10 = FUN_04bb3974(param_2);
  if (iVar10 != 0) {
    local_68 = (undefined8 *)0x0;
    local_60 = (undefined8 *)0x0;
    local_58 = (undefined8 *)0x0;
    FUN_0039488c(&local_68,param_3[1] - *param_3 >> 5);
    lStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = (long *)0x0;
    local_70 = 0xaaaaaaaa3f800000;
    puVar3 = (undefined8 *)param_3[1];
    for (puVar14 = (undefined8 *)*param_3; puVar7 = local_60, puVar14 != puVar3;
        puVar14 = puVar14 + 4) {
      if (*(int *)(puVar14 + 3) == 4) {
        if (local_60 < local_58) {
          if (*(char *)((long)puVar14 + 0x17) < '\0') {
            FUN_00018d20(local_60,*puVar14,puVar14[1]);
            local_60 = puVar7 + 3;
          }
          else {
            uVar16 = puVar14[1];
            uVar12 = *puVar14;
            local_60[2] = puVar14[2];
            local_60[1] = uVar16;
            *local_60 = uVar12;
            local_60 = local_60 + 3;
          }
        }
        else {
          local_60 = (undefined8 *)FUN_00c8c564(&local_68,puVar14);
        }
        FUN_003e8854(&local_90,puVar14,puVar14);
      }
    }
    lVar8 = local_90;
    plVar5 = local_80;
    if (local_68 != local_60) {
      puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
      local_c0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
      local_a0 = 0xffffffff;
      uStack_9c = 0xaaaaaaaa;
      FUN_0466aca8(&local_108);
      FUN_01205740(&local_f0,local_108);
      FUN_0230000c(&local_d8,local_f0);
      FUN_02ac8808(&local_c0,local_d8,&local_90,1);
      if (local_d0 != (long *)0x0) {
        LOAcquire();
        lVar8 = local_d0[1];
        local_d0[1] = lVar8 + -1;
        LORelease();
        if (lVar8 == 0) {
          (**(code **)(*local_d0 + 0x10))(local_d0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_d0);
        }
      }
      ppppppuVar2 = ppppppuStack_e8;
      if (ppppppuStack_e8 != (undefined8 ******)0x0) {
        LOAcquire();
        pppppuVar9 = ppppppuStack_e8[1];
        ppppppuStack_e8[1] = (undefined8 *****)((long)pppppuVar9 + -1);
        LORelease();
        if (pppppuVar9 == (undefined8 *****)0x0) {
          (*(code *)(*ppppppuStack_e8)[2])(ppppppuStack_e8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar2);
        }
      }
      ppppppuVar2 = local_100;
      if (local_100 != (undefined8 ******)0x0) {
        LOAcquire();
        pppppuVar9 = local_100[1];
        local_100[1] = (undefined8 *****)((long)pppppuVar9 + -1);
        LORelease();
        if (pppppuVar9 == (undefined8 *****)0x0) {
          (*(code *)(*local_100)[2])(local_100);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar2);
        }
      }
      local_d8 = 0;
      local_d0 = (long *)0x0;
      local_c8 = 0;
      if ((long)local_60 - (long)local_68 != 0) {
        lVar8 = 0;
        lVar13 = ((long)local_60 - (long)local_68 >> 3) * -0x5555555555555555;
        lVar15 = lVar13 + -1;
        if (lVar13 == 0 || lVar15 == 0) {
          lVar13 = 1;
        }
        do {
          puVar14 = local_68;
          lVar11 = FUN_00da468c(&local_c0,(long)local_68 + lVar8);
          local_f0 = (undefined8 *******)0x0;
          ppppppuStack_e8 = (undefined8 ******)0x0;
          local_e0 = (undefined8 ******)0x0;
          if (lVar11 == 0) {
LAB_031f604c:
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_f0,(long)puVar14 + lVar8);
          }
          else {
            if (*(char *)(lVar11 + 0x3f) < '\0') {
              if (*(long *)(lVar11 + 0x30) != 0) goto LAB_031f6024;
              goto LAB_031f604c;
            }
            if (*(char *)(lVar11 + 0x3f) == '\0') goto LAB_031f604c;
LAB_031f6024:
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_f0,lVar11 + 0x28);
            ppppppuVar2 = ppppppuStack_e8;
            if (-1 < (long)local_e0) {
              ppppppuVar2 = (undefined8 ******)((ulong)local_e0 >> 0x38);
            }
            if (ppppppuVar2 == (undefined8 ******)0x0) goto LAB_031f604c;
          }
          FUN_04bb0de8(&local_108,(long)puVar14 + lVar8,&local_f0);
          ppppppuVar2 = local_100;
          pppppppuVar4 = local_108;
          if (-1 < (char)bStack_f1) {
            ppppppuVar2 = (undefined8 ******)(ulong)bStack_f1;
            pppppppuVar4 = &local_108;
          }
          uVar12 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                             (&local_d8,pppppppuVar4,ppppppuVar2);
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_d8,uVar12)
          ;
          if ((char)bStack_f1 < '\0') {
            __ZdlPvm(local_108,CONCAT17(bStack_f1,local_f8) & 0x7fffffffffffffff);
          }
          if (lVar15 != 0) {
            uVar12 = FUN_04df6268();
            uVar12 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                               (&local_d8,uVar12);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_d8,uVar12);
          }
          if ((long)local_e0 < 0) {
            __ZdlPvm(local_f0,(ulong)local_e0 & 0x7fffffffffffffff);
          }
          lVar8 = lVar8 + 0x18;
          lVar15 = lVar15 + -1;
          lVar13 = lVar13 + -1;
        } while (lVar13 != 0);
      }
      local_108 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
      local_100 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
      FUN_0077bdd0(&local_108,&local_f0);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (local_108 + 0x12,param_2);
      *(undefined4 *)((long)local_108 + 0xe4) = 10000;
      FUN_04df1ac8();
      FUN_00067f80(&local_f0);
      pppppppuVar6 = local_108;
      pppppppuVar4 = local_108 + 0xb9;
      if (*(char *)((long)local_108 + 0x5df) < '\0') {
        __ZdlPvm(local_108[0xb9],(ulong)local_108[0xbb] & 0x7fffffffffffffff);
      }
      pppppppuVar6[0xba] = ppppppuStack_e8;
      *pppppppuVar4 = local_f0;
      pppppppuVar6[0xbb] = local_e0;
      *(undefined4 *)((long)local_108 + 0x7c) = 1;
      FUN_0466aca8(&local_168);
      FUN_01205740(&local_158,local_168);
      FUN_0268f370(&local_148,local_158);
      ppppppuVar2 = local_100;
      if (local_100 == (undefined8 ******)0x0) {
        ppppppuStack_e8 = (undefined8 ******)0x0;
      }
      else {
        ppppppuVar1 = local_100 + 1;
        *ppppppuVar1 = (undefined8 *****)((long)*ppppppuVar1 + 1);
        ppppppuStack_e8 = local_100;
        *ppppppuVar1 = (undefined8 *****)((long)*ppppppuVar1 + 1);
      }
      local_f0 = local_108;
      FUN_0317df64(auStack_138,local_148,&local_f0,0);
      plVar5 = local_110;
      if (ppppppuVar2 != (undefined8 ******)0x0) {
        LOAcquire();
        pppppuVar9 = ppppppuVar2[1];
        ppppppuVar2[1] = (undefined8 *****)((long)pppppuVar9 + -1);
        LORelease();
        if (pppppuVar9 == (undefined8 *****)0x0) {
          (*(code *)(*ppppppuVar2)[2])(ppppppuVar2);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar2);
          plVar5 = local_110;
        }
      }
      if (plVar5 != (long *)0x0) {
        LOAcquire();
        lVar8 = plVar5[1];
        plVar5[1] = lVar8 + -1;
        LORelease();
        if (lVar8 == 0) {
          (**(code **)(*plVar5 + 0x10))(plVar5);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      if (cStack_119 < '\0') {
        __ZdlPvm(local_130,CONCAT17(cStack_119,local_120) & 0x7fffffffffffffff);
      }
      if (ppppppuVar2 != (undefined8 ******)0x0) {
        LOAcquire();
        pppppuVar9 = ppppppuVar2[1];
        ppppppuVar2[1] = (undefined8 *****)((long)pppppuVar9 + -1);
        LORelease();
        if (pppppuVar9 == (undefined8 *****)0x0) {
          (*(code *)(*ppppppuVar2)[2])(ppppppuVar2);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar2);
        }
      }
      if (local_140 != (long *)0x0) {
        LOAcquire();
        lVar8 = local_140[1];
        local_140[1] = lVar8 + -1;
        LORelease();
        if (lVar8 == 0) {
          (**(code **)(*local_140 + 0x10))(local_140);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_140);
        }
      }
      if (local_150 != (long *)0x0) {
        LOAcquire();
        lVar8 = local_150[1];
        local_150[1] = lVar8 + -1;
        LORelease();
        if (lVar8 == 0) {
          (**(code **)(*local_150 + 0x10))(local_150);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_150);
        }
      }
      ppppppuVar2 = local_100;
      if (local_160 != (long *)0x0) {
        LOAcquire();
        lVar8 = local_160[1];
        local_160[1] = lVar8 + -1;
        LORelease();
        if (lVar8 == 0) {
          (**(code **)(*local_160 + 0x10))(local_160);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_160);
          ppppppuVar2 = local_100;
        }
      }
      local_100 = ppppppuVar2;
      if (ppppppuVar2 != (undefined8 ******)0x0) {
        LOAcquire();
        pppppuVar9 = ppppppuVar2[1];
        ppppppuVar2[1] = (undefined8 *****)((long)pppppuVar9 + -1);
        LORelease();
        if (pppppuVar9 == (undefined8 *****)0x0) {
          (*(code *)(*ppppppuVar2)[2])(ppppppuVar2);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar2);
        }
      }
      if ((long)local_c8 < 0) {
        __ZdlPvm(local_d8,local_c8 & 0x7fffffffffffffff);
      }
      FUN_001f36ac(&local_c0);
      lVar8 = local_90;
      plVar5 = local_80;
    }
    while (plVar5 != (long *)0x0) {
      lVar13 = *plVar5;
      local_90 = lVar8;
      if (*(char *)((long)plVar5 + 0x27) < '\0') {
        __ZdlPvm(plVar5[2],plVar5[4] & 0x7fffffffffffffff);
      }
      __ZdlPvm(plVar5,0x28);
      lVar8 = local_90;
      plVar5 = (long *)lVar13;
    }
    local_90 = 0;
    if (lVar8 != 0) {
      __ZdlPvm(lVar8,lStack_88 << 3);
    }
    if (local_68 != (undefined8 *)0x0) {
      for (; local_60 != local_68; local_60 = local_60 + -3) {
      }
      local_60 = local_68;
      __ZdlPvm(local_68,(long)local_58 - (long)local_68);
    }
  }
  return;
}


