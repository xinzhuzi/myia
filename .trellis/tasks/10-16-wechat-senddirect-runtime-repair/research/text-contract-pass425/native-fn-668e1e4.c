// Ghidra inferred pseudocode; requested=0x668e1e4
// entry=0668e1e4 end=0668e56b

undefined8 FUN_0668e1e4(undefined8 param_1,byte *param_2,char *param_3,long param_4,ulong param_5)

{
  byte *pbVar1;
  long lVar2;
  char *pcVar3;
  byte bVar4;
  undefined1 *puVar5;
  long lVar6;
  ulong uVar7;
  
  uVar7 = 0;
  pcVar3 = "nullptr";
  if (param_3 != (char *)0x0) {
    pcVar3 = param_3;
  }
  do {
    while( true ) {
      lVar6 = 0;
      bVar4 = *param_2;
      while( true ) {
        if (bVar4 == 0) {
          if (param_2 < param_2 + lVar6) {
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                      (param_1,param_2,lVar6);
          }
          return 1;
        }
        if (bVar4 == 0x25) break;
        lVar6 = lVar6 + 1;
        bVar4 = param_2[lVar6];
      }
      pbVar1 = param_2 + lVar6;
      bVar4 = pbVar1[1];
      if (bVar4 - 0x42 < 0x37 && (1L << ((ulong)(bVar4 - 0x42) & 0x3f) & 0x40400120400001U) != 0)
      break;
      if ((byte)(bVar4 - 0x30) < 10) {
        if (param_2 < pbVar1) {
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                    (param_1,param_2,lVar6);
        }
        if (param_5 <= (ulong)bVar4 - 0x30) {
          if ((DAT_0a518e82 & 1) == 0) {
            uVar7 = 0;
            do {
              (&DAT_0a518e44)[uVar7] = (&DAT_096875e9)[uVar7] + 0x8a ^ (&DAT_096875d9)[uVar7 & 0xf];
              uVar7 = uVar7 + 1;
            } while (uVar7 != 0x3e);
            goto LAB_0668e548;
          }
          goto LAB_0668e550;
        }
        FUN_06689490(param_1,param_4 + ((ulong)bVar4 - 0x30) * 0x10);
      }
      else if (bVar4 == 0x40) {
        if (param_2 < pbVar1) {
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                    (param_1,param_2,lVar6);
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc(param_1,pcVar3);
      }
      else {
        if (bVar4 != 0x25) {
          if ((DAT_0a518ec9 & 1) == 0) {
            uVar7 = 0;
            do {
              (&DAT_0a518e83)[uVar7] = (&DAT_09687637)[uVar7] + 0x8a ^ (&DAT_09687627)[uVar7 & 0xf];
              uVar7 = uVar7 + 1;
            } while (uVar7 != 0x46);
            DAT_0a518ec9 = 1;
          }
          puVar5 = &DAT_0a518e83;
LAB_0668e55c:
          FUN_066893d8(param_1,puVar5);
          return 0;
        }
        if (param_2 < pbVar1 + 1) {
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                    (param_1,param_2,lVar6 + 1);
        }
      }
      param_2 = param_2 + lVar6 + 2;
    }
    if (param_2 < pbVar1) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                (param_1,param_2,lVar6);
    }
    if (param_5 <= uVar7) {
      if ((DAT_0a518e82 & 1) == 0) {
        uVar7 = 0;
        do {
          (&DAT_0a518e44)[uVar7] = (&DAT_096875e9)[uVar7] + 0x8a ^ (&DAT_096875d9)[uVar7 & 0xf];
          uVar7 = uVar7 + 1;
        } while (uVar7 != 0x3e);
LAB_0668e548:
        DAT_0a518e82 = 1;
      }
LAB_0668e550:
      puVar5 = &DAT_0a518e44;
      goto LAB_0668e55c;
    }
    lVar2 = param_4 + uVar7 * 0x10;
    if (bVar4 < 0x62) {
      if (bVar4 == 0x42) {
        FUN_06689828(param_1);
      }
      else if (bVar4 == 0x58) {
LAB_0668e3b4:
        FUN_06689b94(param_1,lVar2,bVar4 == 0x58);
      }
      else if (bVar4 == 0x5f) {
        FUN_06689490(param_1);
      }
    }
    else if (bVar4 == 0x62) {
      FUN_06689618(param_1,lVar2);
    }
    else if ((bVar4 == 0x70) || (bVar4 == 0x78)) goto LAB_0668e3b4;
    uVar7 = uVar7 + 1;
    param_2 = param_2 + lVar6 + 2;
  } while( true );
}


