// Ghidra inferred pseudocode; requested=0x2d23bc0
// entry=02d23bc0 end=02d249f3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02d23bc0(undefined8 param_1,undefined1 *param_2)

{
  char *pcVar1;
  undefined8 *******pppppppuVar2;
  undefined1 uVar3;
  char *pcVar4;
  undefined4 uVar5;
  uint3 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  code *pcVar11;
  undefined8 **ppuVar12;
  long *plVar13;
  bool bVar14;
  undefined8 *puVar15;
  long lVar16;
  int iVar17;
  ulong uVar18;
  undefined1 *puVar19;
  long *plVar20;
  uint uVar21;
  long lVar22;
  ulong uVar23;
  undefined1 *puVar24;
  long *plVar25;
  undefined4 uVar26;
  undefined4 uVar27;
  undefined4 uVar28;
  undefined4 uVar29;
  undefined4 uVar30;
  undefined1 *local_248;
  long *local_240;
  undefined8 *******local_238 [2];
  undefined7 local_228;
  char cStack_221;
  undefined1 *local_220;
  code *local_218;
  code *local_210;
  undefined8 uStack_208;
  code *local_200;
  undefined8 *local_190;
  undefined8 local_188;
  undefined8 *local_140;
  undefined8 local_138;
  undefined8 **local_f0;
  undefined8 **local_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_0466aca8(&local_190);
  FUN_01205740(&local_140,local_190);
  FUN_02603584(&local_f0,local_140);
  local_218 = FUN_02d5ebc0;
  local_210 = FUN_02d23364;
  uStack_208 = 0;
  local_200 = FUN_02d5ebdc;
  local_220 = param_2;
  FUN_06686570(local_f0 + 0x18,&local_220);
  ppuVar12 = local_e8;
  if (local_e8 != (undefined8 **)0x0) {
    LOAcquire();
    puVar15 = local_e8[1];
    local_e8[1] = (undefined8 *)((long)puVar15 + -1);
    LORelease();
    if (puVar15 == (undefined8 *)0x0) {
      (*(code *)(*local_e8)[2])(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar12);
    }
  }
  plVar25 = local_138;
  if (local_138 != (long *)0x0) {
    LOAcquire();
    lVar16 = local_138[1];
    local_138[1] = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*local_138 + 0x10))(local_138);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
    }
  }
  plVar25 = local_188;
  if (local_188 != (long *)0x0) {
    LOAcquire();
    lVar16 = local_188[1];
    local_188[1] = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*local_188 + 0x10))(local_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
    }
  }
  if (*(long *)("/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit" +
               (long)(param_2 + 0x18)) != 0) {
    FUN_02d81830();
    plVar25 = *(long **)("/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit" +
                        (long)(param_2 + 0x20));
    pcVar1 = "/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit" +
             (long)(param_2 + 0x18);
    pcVar4 = "/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit" +
             (long)(param_2 + 0x20);
    pcVar4[0] = '\0';
    pcVar4[1] = '\0';
    pcVar4[2] = '\0';
    pcVar4[3] = '\0';
    pcVar4[4] = '\0';
    pcVar4[5] = '\0';
    pcVar4[6] = '\0';
    pcVar4[7] = '\0';
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    pcVar1[4] = '\0';
    pcVar1[5] = '\0';
    pcVar1[6] = '\0';
    pcVar1[7] = '\0';
    if (plVar25 != (long *)0x0) {
      LOAcquire();
      lVar16 = plVar25[1];
      plVar25[1] = lVar16 + -1;
      LORelease();
      if (lVar16 == 0) {
        (**(code **)(*plVar25 + 0x10))(plVar25);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
      }
    }
  }
  (**(code **)(*(long *)(param_2 + 0xa08) + 0x10))(param_2 + 0xa08,*(undefined8 *)(param_2 + 0xc10))
  ;
  (**(code **)(*(long *)(param_2 + 0xc98) + 0x10))(param_2 + 0xc98,*(undefined8 *)(param_2 + 0xe80))
  ;
  (**(code **)(*(long *)(param_2 + 0xe88) + 0x10))(param_2 + 0xe88,*(undefined8 *)(param_2 + 0xff0))
  ;
  (**(code **)(*(long *)(param_2 + 0xf00) + 0x10))(param_2 + 0xf00,*(undefined8 *)(param_2 + 0xff8))
  ;
  FUN_04669774();
  lVar16 = FUN_01f4e748();
  (**(code **)(*(long *)(lVar16 + 0x1e8) + 0x10))(lVar16 + 0x1e8,*(undefined8 *)(param_2 + 0x1000));
  *(undefined8 *)(param_2 + 0x1000) = 0;
  FUN_04b1cb28("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" +
               (long)(param_2 + 0x30));
  *(undefined8 *)
   ("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" + (long)(param_2 + 0x20)) =
       *(undefined8 *)
        ("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" +
        (long)(param_2 + 0x18));
  ("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" + (long)(param_2 + 4))[0] =
       '\0';
  ("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" + (long)(param_2 + 4))[1] =
       '\0';
  pcVar1 = "/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" + (long)(param_2 + 8)
  ;
  pcVar4 = "/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" +
           (long)(param_2 + 0x10);
  pcVar4[0] = '\0';
  pcVar4[1] = '\0';
  pcVar4[2] = '\0';
  pcVar4[3] = '\0';
  pcVar4[4] = '\0';
  pcVar4[5] = '\0';
  pcVar4[6] = '\0';
  pcVar4[7] = '\0';
  pcVar1[0] = '\0';
  pcVar1[1] = '\0';
  pcVar1[2] = '\0';
  pcVar1[3] = '\0';
  pcVar1[4] = '\0';
  pcVar1[5] = '\0';
  pcVar1[6] = '\0';
  pcVar1[7] = '\0';
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  local_218 = (code *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_f0);
  FUN_045518a8(&local_220,local_f0);
  ppuVar12 = local_e8;
  if (local_e8 != (undefined8 **)0x0) {
    LOAcquire();
    puVar15 = local_e8[1];
    local_e8[1] = (undefined8 *)((long)puVar15 + -1);
    LORelease();
    if (puVar15 == (undefined8 *)0x0) {
      (*(code *)(*local_e8)[2])(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar12);
    }
  }
  if (local_220 != (undefined1 *)0x0) {
    plVar25 = (long *)FUN_045734b4(local_220,0x13);
    (**(code **)(*plVar25 + 0x10))
              (plVar25,*(undefined8 *)
                        (
                        "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
                        + (long)(param_2 + 0x10)));
    pcVar1 = "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation" +
             (long)(param_2 + 0x10);
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    pcVar1[4] = '\0';
    pcVar1[5] = '\0';
    pcVar1[6] = '\0';
    pcVar1[7] = '\0';
    plVar25 = (long *)FUN_045734b4(local_220,0xf);
    (**(code **)(*plVar25 + 0x10))(plVar25,param_2);
    plVar25 = (long *)FUN_045734b4(local_220,0x1a);
    (**(code **)(*plVar25 + 0x10))
              (plVar25,*(undefined8 *)
                        (
                        "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
                        + (long)(param_2 + 0x18)));
    pcVar1 = "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation" +
             (long)(param_2 + 0x18);
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    pcVar1[4] = '\0';
    pcVar1[5] = '\0';
    pcVar1[6] = '\0';
    pcVar1[7] = '\0';
  }
  pcVar11 = local_218;
  if (local_218 != (code *)0x0) {
    LOAcquire();
    lVar16 = *(long *)((long)local_218 + 8);
    *(long *)((long)local_218 + 8) = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*(long *)local_218 + 0x10))(local_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pcVar11);
    }
  }
  FUN_0466aca8(&local_190);
  FUN_01205740(&local_140,local_190);
  FUN_025bf050(&local_f0,local_140);
  local_218 = (code *)&DAT_02d66e2c;
  local_210 = FUN_02d238dc;
  uStack_208 = 0;
  local_200 = FUN_02d66e44;
  local_220 = param_2;
  FUN_06686570(local_f0 + 4,&local_220);
  ppuVar12 = local_e8;
  if (local_e8 != (undefined8 **)0x0) {
    LOAcquire();
    puVar15 = local_e8[1];
    local_e8[1] = (undefined8 *)((long)puVar15 + -1);
    LORelease();
    if (puVar15 == (undefined8 *)0x0) {
      (*(code *)(*local_e8)[2])(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar12);
    }
  }
  plVar25 = local_138;
  if (local_138 != (long *)0x0) {
    LOAcquire();
    lVar16 = local_138[1];
    local_138[1] = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*local_138 + 0x10))(local_138);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
    }
  }
  if (local_188 != (long *)0x0) {
    LOAcquire();
    lVar16 = local_188[1];
    local_188[1] = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*local_188 + 0x10))(local_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_188);
    }
  }
  FUN_0466aca8(&local_140);
  FUN_01205740(&local_f0,local_140);
  FUN_025c07c8(&local_220,local_f0);
  (**(code **)(*(long *)(local_220 + 0x98) + 0x10))
            (local_220 + 0x98,*(undefined8 *)(param_2 + (long)&dylib_command_00001048.dylib.name));
  pcVar11 = local_218;
  if (local_218 != (code *)0x0) {
    LOAcquire();
    lVar16 = *(long *)((long)local_218 + 8);
    *(long *)((long)local_218 + 8) = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*(long *)local_218 + 0x10))(local_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pcVar11);
    }
  }
  ppuVar12 = local_e8;
  if (local_e8 != (undefined8 **)0x0) {
    LOAcquire();
    puVar15 = local_e8[1];
    local_e8[1] = (undefined8 *)((long)puVar15 + -1);
    LORelease();
    if (puVar15 == (undefined8 *)0x0) {
      (*(code *)(*local_e8)[2])(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar12);
    }
  }
  plVar25 = local_138;
  if (local_138 != (long *)0x0) {
    LOAcquire();
    lVar16 = local_138[1];
    local_138[1] = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*local_138 + 0x10))(local_138);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
    }
  }
  FUN_0466aca8(&local_140);
  FUN_01205740(&local_f0,local_140);
  FUN_025c07c8(&local_220,local_f0);
  (**(code **)(*(long *)(local_220 + 0x20) + 0x10))
            (local_220 + 0x20,
             *(undefined8 *)(param_2 + 8 + (long)&dylib_command_00001048.dylib.name));
  pcVar11 = local_218;
  if (local_218 != (code *)0x0) {
    LOAcquire();
    lVar16 = *(long *)((long)local_218 + 8);
    *(long *)((long)local_218 + 8) = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*(long *)local_218 + 0x10))(local_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pcVar11);
    }
  }
  ppuVar12 = local_e8;
  if (local_e8 != (undefined8 **)0x0) {
    LOAcquire();
    puVar15 = local_e8[1];
    local_e8[1] = (undefined8 *)((long)puVar15 + -1);
    LORelease();
    if (puVar15 == (undefined8 *)0x0) {
      (*(code *)(*local_e8)[2])(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar12);
    }
  }
  if (local_138 != (long *)0x0) {
    LOAcquire();
    lVar16 = local_138[1];
    local_138[1] = lVar16 + -1;
    LORelease();
    if (lVar16 == 0) {
      (**(code **)(*local_138 + 0x10))(local_138);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_138);
    }
  }
  *(undefined8 *)(param_2 + (long)&dylib_command_00001048.dylib.name) = 0;
  *(undefined8 *)(param_2 + 8 + (long)&dylib_command_00001048.dylib.name) = 0;
  if (*(long *)("/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation" +
               (long)(param_2 + 0x48)) != 0) {
    plVar25 = (long *)*(long *)(
                               "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
                               + (long)(param_2 + 0x40));
    while (plVar25 != (long *)0x0) {
      lVar16 = *plVar25;
      if (*(char *)((long)plVar25 + 0x27) < '\0') {
        __ZdlPvm(plVar25[2],plVar25[4] & 0x7fffffffffffffff);
      }
      __ZdlPvm(plVar25,0x28);
      plVar25 = (long *)lVar16;
    }
    pcVar1 = "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation" +
             (long)(param_2 + 0x40);
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    pcVar1[4] = '\0';
    pcVar1[5] = '\0';
    pcVar1[6] = '\0';
    pcVar1[7] = '\0';
    lVar16 = *(long *)(
                      "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
                      + (long)(param_2 + 0x38));
    if (lVar16 != 0) {
      lVar22 = 0;
      do {
        *(undefined8 *)
         (*(long *)("/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
                   + (long)(param_2 + 0x30)) + lVar22 * 8) = 0;
        lVar22 = lVar22 + 1;
      } while (lVar16 != lVar22);
    }
    pcVar1 = "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation" +
             (long)(param_2 + 0x48);
    pcVar1[0] = '\0';
    pcVar1[1] = '\0';
    pcVar1[2] = '\0';
    pcVar1[3] = '\0';
    pcVar1[4] = '\0';
    pcVar1[5] = '\0';
    pcVar1[6] = '\0';
    pcVar1[7] = '\0';
  }
  if ("/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
      [(long)(param_2 + 0x29)] == '\x01') {
    "/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation"
    [(long)(param_2 + 0x29)] = '\0';
  }
  puVar15 = (undefined8 *)FUN_02e0a888(param_2 + 0xe88);
  uVar10 = _UNK_08860af8;
  uVar9 = _DAT_08860af0;
  uVar8 = DAT_08698728;
  uVar7 = DAT_084c8608;
  if ((long *)*puVar15 != puVar15 + 1) {
    uVar26 = (undefined4)DAT_085465d8;
    uVar30 = (undefined4)DAT_087ec730;
    uVar5 = (undefined4)DAT_085465e0;
    uVar29 = (undefined4)DAT_085465e8;
    plVar25 = (long *)*puVar15;
    do {
      if (*(int *)((long)plVar25 + 0x7fc) == 1) {
        iVar17 = thunk_FUN_05e1d97c(2);
        if (iVar17 != 0) {
          FUN_0488143c(local_238);
          pppppppuVar2 = local_238[0];
          if (-1 < cStack_221) {
            pppppppuVar2 = local_238;
          }
          if ((DAT_0a3bd664 & 1) == 0) {
            uRam000000000a3bd658 = uVar10;
            _DAT_0a3bd650 = uVar9;
            DAT_0a3bd664 = 1;
            DAT_0a3bd660 = (int)uVar7;
          }
          if ((DAT_0a3bd6f1 & 1) == 0) {
            DAT_0a3bd6f0 = 0;
            DAT_0a3bd6f1 = 1;
            _DAT_0a3bd6dc = CONCAT44(uVar26,uVar30);
            uRam000000000a3bd6e4 = CONCAT44(uVar29,uVar5);
            DAT_0a3bd6ec = (int)uVar8;
          }
          FUN_05e1d050(&local_220,2,pppppppuVar2,&DAT_0a3bd650,&DAT_0a3bd6dc,0x1b3,0,0);
          uVar18 = plVar25[4];
          local_140 = (undefined8 *)0x0;
          if ((DAT_0a3bf600 & 1) == 0) {
            uVar23 = 0;
            do {
              uVar27 = *(undefined4 *)((long)&DAT_08866d9f + uVar23);
              uVar6 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
              uVar28 = *(undefined4 *)((long)&DAT_08866d8b + uVar23 % 0x14);
              *(uint *)((long)&DAT_0a3bf5b8 + uVar23) =
                   CONCAT13((char)((uint)uVar27 >> 0x18) + 0x69U ^ (byte)((uint)uVar28 >> 0x18),
                            CONCAT12((char)((uint)uVar27 >> 0x10) + 0x69U ^
                                     (byte)((uint)uVar28 >> 0x10),
                                     CONCAT11((char)(uVar6 >> 0x10) + 0x69U ^
                                              (byte)((uint)uVar28 >> 8),
                                              (char)uVar6 + 0x69U ^ (byte)uVar28)));
              uVar23 = uVar23 + 4;
            } while (uVar23 != 0x48);
            DAT_0a3bf600 = 1;
          }
          lVar16 = 0;
          do {
            lVar22 = lVar16;
            *(undefined1 *)((long)&local_138 + lVar22) = (&DAT_0a3bf5db)[uVar18 % 10];
            bVar14 = 9 < uVar18;
            uVar18 = uVar18 / 10;
            lVar16 = lVar22 + 1;
          } while (bVar14);
          *(undefined1 *)((long)&local_138 + lVar22 + 1) = 0;
          if (8 < lVar22 + 8U) {
            puVar19 = (undefined1 *)((long)&local_138 + lVar22);
            puVar24 = (undefined1 *)((long)&local_138 + 1);
            do {
              uVar3 = *puVar19;
              *puVar19 = puVar24[-1];
              puVar24[-1] = uVar3;
              bVar14 = puVar24 < puVar19 + -1;
              puVar19 = puVar19 + -1;
              puVar24 = puVar24 + 1;
            } while (bVar14);
          }
          local_140 = &local_138;
          lVar16 = 0;
          uVar18 = (ulong)*(uint *)(plVar25 + 0xfd);
          do {
            lVar22 = lVar16;
            uVar21 = (uint)uVar18;
            *(undefined1 *)((long)&local_188 + lVar22) =
                 *(undefined1 *)
                  ((long)&DAT_0a3bf5b8 + (ulong)(uVar21 + (int)(uVar18 / 10) * -10 + 0x23));
            lVar16 = lVar22 + 1;
            uVar18 = uVar18 / 10;
          } while (9 < uVar21);
          *(undefined1 *)((long)&local_188 + lVar22 + 1) = 0;
          if (8 < lVar22 + 8U) {
            puVar19 = (undefined1 *)((long)&local_188 + lVar22);
            puVar24 = (undefined1 *)((long)&local_188 + 1);
            do {
              uVar3 = *puVar19;
              *puVar19 = puVar24[-1];
              puVar24[-1] = uVar3;
              bVar14 = puVar24 < puVar19 + -1;
              puVar19 = puVar19 + -1;
              puVar24 = puVar24 + 1;
            } while (bVar14);
          }
          if ((DAT_0a3bd754 & 1) == 0) {
            uVar18 = 0;
            do {
              uVar27 = *(undefined4 *)((long)&DAT_08863d43 + uVar18);
              uVar6 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
              uVar28 = *(undefined4 *)((long)&DAT_08863d2f + uVar18 % 0x14);
              *(uint *)((long)&DAT_0a3bd6f2 + uVar18) =
                   CONCAT13((char)((uint)uVar27 >> 0x18) + 0x8aU ^ (byte)((uint)uVar28 >> 0x18),
                            CONCAT12((char)((uint)uVar27 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar28 >> 0x10),
                                     CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar28 >> 8),
                                              (char)uVar6 + 0x8aU ^ (byte)uVar28)));
              uVar18 = uVar18 + 4;
            } while (uVar18 != 0x60);
            DAT_0a3bd752 = 0x29;
            DAT_0a3bd754 = 1;
          }
          uStack_d8 = 0;
          local_e0 = 0;
          uStack_c8 = 0;
          uStack_d0 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_78 = 0;
          local_80 = 0;
          local_190 = &local_188;
          local_f0 = &local_140;
          local_e8 = &local_190;
          FUN_05e1d31c(&local_220,&DAT_0a3bd6f2,&local_f0);
          thunk_FUN_05e1d0bc(&local_220);
          if (cStack_221 < '\0') {
            __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
          }
        }
        FUN_02d24b2c(param_2,plVar25[4],3,3,(int)plVar25[0xfe]);
        plVar13 = (long *)plVar25[1];
        if ((long *)plVar25[1] == (long *)0x0) goto LAB_02d248e8;
LAB_02d248d8:
        do {
          plVar20 = plVar13;
          plVar13 = (long *)*plVar20;
        } while ((long *)*plVar20 != (long *)0x0);
      }
      else {
        local_248 = &SUB_aaaaaaaaaaaaaaaa;
        local_240 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_04765e5c(&local_248,plVar25[4]);
        FUN_047669ac(local_248,(int)plVar25[0xfd]);
        FUN_047669b4(local_248,*(undefined4 *)((long)plVar25 + 0x7f4));
        FUN_047669bc(local_248,(int)plVar25[0xfe]);
        FUN_01d4c79c(local_248,(int)plVar25[0xff]);
        FUN_047669c4(local_248,4);
        FUN_02d24db0(param_2,&local_248);
        FUN_047689b4(local_248);
        FUN_02d24b2c(param_2,plVar25[4],3,3,(int)plVar25[0xfe]);
        FUN_0478afb4(0xb,0,plVar25 + 5,4);
        iVar17 = thunk_FUN_05e1d97c(2);
        if (iVar17 != 0) {
          FUN_0488143c(local_238);
          pppppppuVar2 = local_238[0];
          if (-1 < cStack_221) {
            pppppppuVar2 = local_238;
          }
          if ((DAT_0a3bd664 & 1) == 0) {
            uRam000000000a3bd658 = uVar10;
            _DAT_0a3bd650 = uVar9;
            DAT_0a3bd664 = 1;
            DAT_0a3bd660 = (int)uVar7;
          }
          if ((DAT_0a3bd6f1 & 1) == 0) {
            DAT_0a3bd6f0 = 0;
            DAT_0a3bd6f1 = 1;
            _DAT_0a3bd6dc = CONCAT44(uVar26,uVar30);
            uRam000000000a3bd6e4 = CONCAT44(uVar29,uVar5);
            DAT_0a3bd6ec = (int)uVar8;
          }
          FUN_05e1d050(&local_220,2,pppppppuVar2,&DAT_0a3bd650,&DAT_0a3bd6dc,0x1c5,0,0);
          uVar18 = plVar25[4];
          local_140 = (undefined8 *)0x0;
          if ((DAT_0a3bf600 & 1) == 0) {
            uVar23 = 0;
            do {
              uVar27 = *(undefined4 *)((long)&DAT_08866d9f + uVar23);
              uVar6 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
              uVar28 = *(undefined4 *)((long)&DAT_08866d8b + uVar23 % 0x14);
              *(uint *)((long)&DAT_0a3bf5b8 + uVar23) =
                   CONCAT13((char)((uint)uVar27 >> 0x18) + 0x69U ^ (byte)((uint)uVar28 >> 0x18),
                            CONCAT12((char)((uint)uVar27 >> 0x10) + 0x69U ^
                                     (byte)((uint)uVar28 >> 0x10),
                                     CONCAT11((char)(uVar6 >> 0x10) + 0x69U ^
                                              (byte)((uint)uVar28 >> 8),
                                              (char)uVar6 + 0x69U ^ (byte)uVar28)));
              uVar23 = uVar23 + 4;
            } while (uVar23 != 0x48);
            DAT_0a3bf600 = 1;
          }
          lVar16 = 0;
          do {
            lVar22 = lVar16;
            *(undefined1 *)((long)&local_138 + lVar22) = (&DAT_0a3bf5db)[uVar18 % 10];
            bVar14 = 9 < uVar18;
            uVar18 = uVar18 / 10;
            lVar16 = lVar22 + 1;
          } while (bVar14);
          *(undefined1 *)((long)&local_138 + lVar22 + 1) = 0;
          if (8 < lVar22 + 8U) {
            puVar19 = (undefined1 *)((long)&local_138 + lVar22);
            puVar24 = (undefined1 *)((long)&local_138 + 1);
            do {
              uVar3 = *puVar19;
              *puVar19 = puVar24[-1];
              puVar24[-1] = uVar3;
              bVar14 = puVar24 < puVar19 + -1;
              puVar19 = puVar19 + -1;
              puVar24 = puVar24 + 1;
            } while (bVar14);
          }
          local_140 = &local_138;
          lVar16 = 0;
          uVar18 = (ulong)*(uint *)(plVar25 + 0xfd);
          do {
            lVar22 = lVar16;
            uVar21 = (uint)uVar18;
            *(undefined1 *)((long)&local_188 + lVar22) =
                 *(undefined1 *)
                  ((long)&DAT_0a3bf5b8 + (ulong)(uVar21 + (int)(uVar18 / 10) * -10 + 0x23));
            lVar16 = lVar22 + 1;
            uVar18 = uVar18 / 10;
          } while (9 < uVar21);
          *(undefined1 *)((long)&local_188 + lVar22 + 1) = 0;
          if (8 < lVar22 + 8U) {
            puVar19 = (undefined1 *)((long)&local_188 + lVar22);
            puVar24 = (undefined1 *)((long)&local_188 + 1);
            do {
              uVar3 = *puVar19;
              *puVar19 = puVar24[-1];
              puVar24[-1] = uVar3;
              bVar14 = puVar24 < puVar19 + -1;
              puVar19 = puVar19 + -1;
              puVar24 = puVar24 + 1;
            } while (bVar14);
          }
          if ((DAT_0a3bd790 & 1) == 0) {
            uVar18 = 0;
            do {
              uVar27 = *(undefined4 *)((long)&DAT_08863db9 + uVar18);
              uVar6 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
              uVar28 = *(undefined4 *)((long)&DAT_08863da5 + uVar18 % 0x14);
              *(uint *)((long)&DAT_0a3bd755 + uVar18) =
                   CONCAT13((char)((uint)uVar27 >> 0x18) + 0x8aU ^ (byte)((uint)uVar28 >> 0x18),
                            CONCAT12((char)((uint)uVar27 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar28 >> 0x10),
                                     CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar28 >> 8),
                                              (char)uVar6 + 0x8aU ^ (byte)uVar28)));
              uVar18 = uVar18 + 4;
            } while (uVar18 != 0x38);
            DAT_0a3bd78d = 0x5f25;
            DAT_0a3bd78f = 0;
            DAT_0a3bd790 = 1;
          }
          uStack_d8 = 0;
          local_e0 = 0;
          uStack_c8 = 0;
          uStack_d0 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_78 = 0;
          local_80 = 0;
          local_190 = &local_188;
          local_f0 = &local_140;
          local_e8 = &local_190;
          FUN_05e1d31c(&local_220,&DAT_0a3bd755,&local_f0);
          thunk_FUN_05e1d0bc(&local_220);
          if (cStack_221 < '\0') {
            __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
          }
        }
        plVar13 = local_240;
        if (local_240 != (long *)0x0) {
          LOAcquire();
          lVar16 = local_240[1];
          local_240[1] = lVar16 + -1;
          LORelease();
          if (lVar16 == 0) {
            (**(code **)(*local_240 + 0x10))(local_240);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
        }
        plVar13 = (long *)plVar25[1];
        if ((long *)plVar25[1] != (long *)0x0) goto LAB_02d248d8;
LAB_02d248e8:
        do {
          plVar20 = (long *)plVar25[2];
          bVar14 = (long *)*plVar20 != plVar25;
          plVar25 = plVar20;
        } while (bVar14);
      }
      plVar25 = plVar20;
    } while (plVar20 != puVar15 + 1);
  }
  FUN_02e05948(param_2 + 0xe88);
  FUN_0476911c();
  local_218 = (code *)&SUB_aaaaaaaaaaaaaaaa;
  local_210 = (code *)&SUB_aaaaaaaaaaaaaaaa;
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_02d25030(&local_220,param_2);
  FUN_047b8e28(&local_220);
  FUN_02e39c24(param_2 + 0x988);
  ("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" + (long)(param_2 + 1))[0] =
       '\0';
  ("/System/Library/Frameworks/CoreText.framework/Versions/A/CoreText" + (long)(param_2 + 1))[1] =
       '\0';
  FUN_02deac20();
  FUN_02dec5f0();
  FUN_02322b5c(param_1);
  FUN_002d995c(&local_220,local_218);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


