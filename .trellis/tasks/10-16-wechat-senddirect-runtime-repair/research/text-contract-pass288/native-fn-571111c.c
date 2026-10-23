// Ghidra inferred pseudocode; requested=0x571111c
// entry=05710bd8 end=0571148b

/* WARNING: Removing unreachable block (ram,0x05711314) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_05710bd8(long param_1,int param_2)

{
  uint3 uVar1;
  int iVar2;
  long lVar3;
  long lVar4;
  ulong uVar5;
  long lVar6;
  undefined8 uVar7;
  long *plVar8;
  undefined8 *puVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  undefined1 *local_98;
  undefined1 *puStack_90;
  undefined2 uStack_88;
  int *local_80;
  long *plStack_78;
  long local_70;
  long local_68;
  long local_60;
  int local_54;
  undefined8 *local_50;
  long local_48;
  
  if ((*(byte *)(param_1 + 0x30) >> 5 & 1) == 0) {
    local_48 = *(long *)(param_1 + 0xb8);
    if (local_48 != 0) {
      FUN_0571a560();
    }
    puVar9 = *(undefined8 **)(param_1 + 0xd0);
    local_50 = puVar9;
    if ((puVar9 != (undefined8 *)0x0) && (*(char *)((long)puVar9 + 0xc) == '\x01')) {
      FUN_056fe3a0(*puVar9,*(undefined4 *)(puVar9 + 1));
    }
    FUN_0570a07c(param_1);
    iVar2 = FUN_05702600(param_1);
    if ((iVar2 == 0) ||
       ((((lVar3 = *(long *)(param_1 + 0xa0), (*(byte *)(lVar3 + 0x31) & 1) == 0 &&
          (*(int *)(lVar3 + 0x18) < 0)) || (*(long *)(lVar3 + 0x28) == 0)) ||
        (*(long *)(lVar3 + 0x20) == 0)))) {
      if ((DAT_0a4da54c & 1) == 0) {
        DAT_0a4da540._0_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[0];
        DAT_0a4da540._1_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[1];
        DAT_0a4da540._2_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[2];
        DAT_0a4da540._3_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[3];
        DAT_0a4da540._4_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[4];
        DAT_0a4da540._5_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[5];
        DAT_0a4da540._6_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[6];
        DAT_0a4da540._7_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[7];
        DAT_0a4da54c = 1;
        DAT_0a4da548 = (int)DAT_085722b0;
      }
      if ((DAT_0a4dab34 & 1) == 0) {
        uRam000000000a4dab28 = _UNK_08b33b08;
        _DAT_0a4dab20 = _DAT_08b33b00;
        DAT_0a4dab34 = 1;
        DAT_0a4dab30 = (int)DAT_08b33a30;
      }
      if ((DAT_0a4da824 & 1) == 0) {
        uRam000000000a4da818._0_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x18];
        uRam000000000a4da818._1_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x19];
        uRam000000000a4da818._2_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x1a];
        uRam000000000a4da818._3_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x1b];
        uRam000000000a4da818._4_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x1c];
        uRam000000000a4da818._5_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x1d];
        uRam000000000a4da818._6_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x1e];
        uRam000000000a4da818._7_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x1f];
        DAT_0a4da810 = s_file___s__not_va__s__file_not_va_08b33a60[0x10];
        DAT_0a4da810_1._0_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x11];
        DAT_0a4da810_1._1_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x12];
        DAT_0a4da810_1._2_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x13];
        DAT_0a4da810_1._3_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x14];
        DAT_0a4da810_1._4_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x15];
        DAT_0a4da810_1._5_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x16];
        DAT_0a4da810_1._6_1_ = s_file___s__not_va__s__file_not_va_08b33a60[0x17];
        DAT_0a4da820 = (undefined4)DAT_084cade8;
        DAT_0a4da824 = 1;
      }
      FUN_05707004(2,&DAT_0a4da540,&DAT_0a4dab20,0x722,&DAT_0a4da810);
      uVar7 = 0;
    }
    else {
      if (*(char *)(param_1 + 0xe0) == '\x01') {
        if ((DAT_0a4da54c & 1) == 0) {
          DAT_0a4da540._0_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[0];
          DAT_0a4da540._1_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[1];
          DAT_0a4da540._2_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[2];
          DAT_0a4da540._3_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[3];
          DAT_0a4da540._4_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[4];
          DAT_0a4da540._5_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[5];
          DAT_0a4da540._6_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[6];
          DAT_0a4da540._7_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[7];
          DAT_0a4da54c = 1;
          DAT_0a4da548 = (int)DAT_085722b0;
        }
        if ((DAT_0a4dab34 & 1) == 0) {
          uRam000000000a4dab28 = _UNK_08b33b08;
          _DAT_0a4dab20 = _DAT_08b33b00;
          DAT_0a4dab34 = 1;
          DAT_0a4dab30 = (int)DAT_08b33a30;
        }
        if ((DAT_0a4da721 & 1) == 0) {
          uVar5 = 0;
          do {
            uVar10 = *(undefined4 *)((long)&DAT_08b33d8e + uVar5);
            uVar11 = *(undefined4 *)((long)&DAT_08b33d7a + uVar5 % 0x14);
            *(uint *)((long)&DAT_0a4da6e4 + uVar5) =
                 CONCAT13((byte)((uint)uVar11 >> 0x18) ^ (byte)((uint)uVar10 >> 0x18),
                          CONCAT12((byte)((uint)uVar11 >> 0x10) ^ (byte)((uint)uVar10 >> 0x10),
                                   CONCAT11((byte)((uint)uVar11 >> 8) ^ (byte)((uint)uVar10 >> 8),
                                            (byte)uVar11 ^ (byte)uVar10)));
            uVar5 = uVar5 + 4;
          } while (uVar5 != 0x3c);
          DAT_0a4da720 = 0;
          DAT_0a4da721 = 1;
        }
        FUN_05707004(3,&DAT_0a4da540,&DAT_0a4dab20,0x727,&DAT_0a4da6e4);
        *(undefined1 *)(param_1 + 0xe0) = 0;
      }
      if (*(int *)(param_1 + 0xdc) != param_2) {
        if ((DAT_0a4da54c & 1) == 0) {
          DAT_0a4da540._0_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[0];
          DAT_0a4da540._1_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[1];
          DAT_0a4da540._2_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[2];
          DAT_0a4da540._3_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[3];
          DAT_0a4da540._4_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[4];
          DAT_0a4da540._5_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[5];
          DAT_0a4da540._6_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[6];
          DAT_0a4da540._7_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[7];
          DAT_0a4da548 = (undefined4)DAT_085722b0;
          DAT_0a4da54c = 1;
        }
        if ((DAT_0a4dab34 & 1) == 0) {
          uRam000000000a4dab28 = _UNK_08b33b08;
          _DAT_0a4dab20 = _DAT_08b33b00;
          DAT_0a4dab30 = (undefined4)DAT_08b33a30;
          DAT_0a4dab34 = 1;
        }
        if ((DAT_0a4dab4d & 1) == 0) {
          _DAT_0a4dab38 = CONCAT44((int)DAT_08b33a38,(int)DAT_08610dc8);
          uRam000000000a4dab40 = CONCAT44((int)ram0x08926660,(int)DAT_0861f478);
          DAT_0a4dab48 = (undefined4)DAT_08b33a40;
          DAT_0a4dab4c = 0;
          DAT_0a4dab4d = 1;
        }
        FUN_05707004(1,&DAT_0a4da540,&DAT_0a4dab20,0x72c,&DAT_0a4dab38);
        *(int *)(param_1 + 0xdc) = param_2;
      }
      uVar7 = 1;
      *(undefined1 *)(param_1 + 0xd8) = 1;
      if ((*(byte *)(*(long *)(param_1 + 0xa8) + 0x68) & 1) == 0) {
        if (param_2 == 0) {
          local_54 = 0;
        }
        else {
          local_54 = _time(0);
          local_54 = *(int *)(param_1 + 0xdc) + local_54;
        }
        if ((DAT_0a4da54c & 1) == 0) {
          DAT_0a4da540._0_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[0];
          DAT_0a4da540._1_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[1];
          DAT_0a4da540._2_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[2];
          DAT_0a4da540._3_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[3];
          DAT_0a4da540._4_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[4];
          DAT_0a4da540._5_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[5];
          DAT_0a4da540._6_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[6];
          DAT_0a4da540._7_1_ = s_MMKV_IO_loadFromh_cr_08b337d8[7];
          DAT_0a4da548 = (undefined4)DAT_085722b0;
          DAT_0a4da54c = 1;
        }
        if ((DAT_0a4dab34 & 1) == 0) {
          uRam000000000a4dab28 = _UNK_08b33b08;
          _DAT_0a4dab20 = _DAT_08b33b00;
          DAT_0a4dab30 = (undefined4)DAT_08b33a30;
          DAT_0a4dab34 = 1;
        }
        if ((DAT_0a4dab91 & 1) == 0) {
          uVar5 = 0;
          do {
            uVar11 = *(undefined4 *)((long)&DAT_08b345cc + uVar5);
            uVar1 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
            uVar10 = *(undefined4 *)((long)&DAT_08b345b8 + uVar5 % 0x14);
            *(uint *)((long)&DAT_0a4dab4e + uVar5) =
                 CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar10 >> 0x18),
                          CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar10 >> 0x10),
                                   CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar10 >> 8),
                                            (char)uVar1 + 0x8aU ^ (byte)uVar10)));
            uVar5 = uVar5 + 4;
          } while (uVar5 != 0x40);
          DAT_0a4dab8e = 0x7525;
          DAT_0a4dab90 = 0;
          DAT_0a4dab91 = 1;
        }
        FUN_05707004(1,&DAT_0a4da540,&DAT_0a4dab20,0x736,&DAT_0a4dab4e);
        lVar3 = *(long *)(param_1 + 0xa8);
        *(ulong *)(lVar3 + 0x68) = *(ulong *)(lVar3 + 0x68) | 1;
        *(undefined4 *)(lVar3 + 4) = 4;
        if ((*(long *)(*(long *)(param_1 + 0x80) + 0x28) == *(long *)(param_1 + 0x78)) &&
           (*(long *)(param_1 + 0x88) == 0)) {
          if ((DAT_0a4da54c & 1) == 0) {
            DAT_0a4da548 = (undefined4)DAT_085722b0;
            DAT_0a4da54c = 1;
            DAT_0a4da540 = s_MMKV_IO_loadFromh_cr_08b337d8._0_8_;
          }
          if ((DAT_0a4dab34 & 1) == 0) {
            uRam000000000a4dab28 = _UNK_08b33b08;
            _DAT_0a4dab20 = _DAT_08b33b00;
            DAT_0a4dab30 = (undefined4)DAT_08b33a30;
            DAT_0a4dab34 = 1;
          }
          if ((DAT_0a4dabd7 & 1) == 0) {
            uVar5 = 0;
            do {
              uVar11 = *(undefined4 *)((long)&DAT_08b34623 + uVar5);
              uVar1 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
              uVar10 = *(undefined4 *)((long)&DAT_08b3460f + uVar5 % 0x14);
              *(uint *)((long)&DAT_0a4dab92 + uVar5) =
                   CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar10 >> 0x18),
                            CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar10 >> 0x10),
                                     CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar10 >> 8),
                                              (char)uVar1 + 0x8aU ^ (byte)uVar10)));
              uVar5 = uVar5 + 4;
            } while (uVar5 != 0x44);
            DAT_0a4dabd6 = 0;
            DAT_0a4dabd7 = 1;
          }
          FUN_05707004(1,&DAT_0a4da540,&DAT_0a4dab20,0x73b,&DAT_0a4dab92);
          FUN_05708d04(param_1,0,0,0,1);
          uVar7 = 1;
          FUN_0571574c(*(undefined8 *)(param_1 + 0xa0),1);
          puVar9 = local_50;
        }
        else {
          local_70 = 0;
          local_68 = 0;
          local_60 = 0;
          local_80 = &local_54;
          plStack_78 = &local_70;
          lVar3 = *(long *)(*(long *)(param_1 + 0x80) + 0x20);
          if (*(long *)(param_1 + 0xb0) == 0) {
            for (plVar8 = *(long **)(*(long *)(param_1 + 0x68) + 0x10); plVar8 != (long *)0x0;
                plVar8 = (long *)*plVar8) {
              local_98 = &SUB_aaaaaaaaaaaaaaaa;
              puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
              uStack_88 = 0xaaaa;
              FUN_056fea70(&local_98,plVar8 + 5,lVar3 + 4);
              FUN_057114e8(&local_80,plVar8 + 2,&local_98);
              FUN_056ff3a0(&local_98);
            }
          }
          else {
            for (plVar8 = *(long **)(*(long *)(param_1 + 0x70) + 0x10); plVar8 != (long *)0x0;
                plVar8 = (long *)*plVar8) {
              local_98 = &SUB_aaaaaaaaaaaaaaaa;
              puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
              uStack_88 = 0xaaaa;
              FUN_056fed6c(&local_98,plVar8 + 5,lVar3 + 4,*(undefined8 *)(param_1 + 0xb0));
              FUN_057114e8(&local_80,plVar8 + 2,&local_98);
              FUN_056ff3a0(&local_98);
            }
          }
          uVar7 = FUN_0570ff3c(param_1,&local_70);
          lVar3 = local_70;
          puVar9 = local_50;
          if (local_70 != 0) {
            if (local_68 != local_70) {
              lVar6 = local_68 + -0x18;
              do {
                FUN_056ff3a0(lVar6);
                lVar4 = lVar6 + -0x18;
                lVar6 = lVar6 + -0x30;
              } while (lVar4 != lVar3);
            }
            local_68 = lVar3;
            __ZdlPvm(local_70,local_60 - local_70);
            puVar9 = local_50;
          }
        }
      }
    }
    if ((puVar9 != (undefined8 *)0x0) && (*(char *)((long)puVar9 + 0xc) == '\x01')) {
      FUN_056fe95c(*puVar9,*(undefined4 *)(puVar9 + 1));
    }
    if (local_48 != 0) {
      FUN_0571a6b0();
    }
  }
  else {
    if ((DAT_0a4da54c & 1) == 0) {
      DAT_0a4da540 = s_MMKV_IO_loadFromh_cr_08b337d8._0_8_;
      DAT_0a4da548 = (undefined4)DAT_085722b0;
      DAT_0a4da54c = 1;
    }
    if ((DAT_0a4dab34 & 1) == 0) {
      uRam000000000a4dab28 = _UNK_08b33b08;
      _DAT_0a4dab20 = _DAT_08b33b00;
      DAT_0a4dab30 = (undefined4)DAT_08b33a30;
      DAT_0a4dab34 = 1;
    }
    if ((DAT_0a4da843 & 1) == 0) {
      uRam000000000a4da838 = _UNK_08b32e28;
      _DAT_0a4da830 = _DAT_08b32e20;
      DAT_0a4da840 = 0x796c;
      DAT_0a4da842 = 0;
      DAT_0a4da843 = 1;
    }
    FUN_05707004(2,&DAT_0a4da540,&DAT_0a4dab20,0x71b,&DAT_0a4da830);
    uVar7 = 0;
  }
  return uVar7;
}


