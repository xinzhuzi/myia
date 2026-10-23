// Ghidra inferred pseudocode; requested=0x6664994
// entry=06664994 end=06664fcb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_06664994(long param_1)

{
  long lVar1;
  ushort uVar2;
  undefined4 uVar3;
  ulong *puVar4;
  ulong uVar5;
  ulong *puVar6;
  long lVar7;
  long lVar8;
  undefined4 *puVar9;
  long lVar10;
  undefined8 uVar11;
  uint *puVar12;
  long *plVar13;
  ulong uVar14;
  undefined8 local_178;
  long local_170;
  long local_168;
  undefined4 local_a4;
  ulong local_a0;
  ulong uStack_98;
  ulong local_90;
  long local_88;
  undefined1 *local_80;
  long local_78 [2];
  undefined4 uStack_68;
  undefined4 uStack_64;
  undefined8 local_60;
  undefined1 *local_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_88 = param_1 + 8;
  local_80 = &DAT_aaaaaaaaaaaaaa01;
  __ZNSt3__15mutex4lockEv();
  if (*(int *)(param_1 + 0x100) == 1) {
    uVar11 = 0xffffffff;
  }
  else {
    plVar13 = (long *)(param_1 + 0xe0);
    puVar4 = (ulong *)*plVar13;
    puVar6 = *(ulong **)(param_1 + 0xe8);
    if (puVar4 != puVar6) {
      do {
        if (puVar4[2] != 0) {
          uStack_98 = puVar4[1];
          uVar14 = *puVar4;
          local_90 = puVar4[2];
          local_a0._0_4_ = (undefined4)uVar14;
          uVar3 = (undefined4)local_a0;
          local_a4 = (undefined4)local_a0;
          puVar12 = *(uint **)(*(long *)(param_1 + 0x98) + (uVar14 & 0xffffffff) * 8);
          local_a0 = uVar14;
          if (*(long *)(puVar12 + 4) == 0) {
            uVar5 = FUN_0668dad0(0);
            if ((uVar5 & 1) != 0) {
              if ((DAT_0a516ff2 & 1) == 0) {
                DAT_0a516fe8._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x10];
                DAT_0a516fe8._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x11];
                DAT_0a516fe8._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x12];
                DAT_0a516fe8._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x13];
                DAT_0a516fe8._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x14];
                DAT_0a516fe8._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x15];
                DAT_0a516fe8._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x16];
                DAT_0a516fe8._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x17];
                DAT_0a516ff0 = 99;
                DAT_0a516ff2 = 1;
              }
              if ((DAT_0a51722e & 1) == 0) {
                DAT_0a517220._0_1_ = s_try_run_run_taskk__a_096830a0[0];
                DAT_0a517220._1_1_ = s_try_run_run_taskk__a_096830a0[1];
                DAT_0a517220._2_1_ = s_try_run_run_taskk__a_096830a0[2];
                DAT_0a517220._3_1_ = s_try_run_run_taskk__a_096830a0[3];
                DAT_0a517220._4_1_ = s_try_run_run_taskk__a_096830a0[4];
                DAT_0a517220._5_1_ = s_try_run_run_taskk__a_096830a0[5];
                DAT_0a517220._6_1_ = s_try_run_run_taskk__a_096830a0[6];
                DAT_0a517220._7_1_ = s_try_run_run_taskk__a_096830a0[7];
                DAT_0a517228 = (undefined4)DAT_08518828;
                DAT_0a51722c = 0x5f;
                DAT_0a51722e = 1;
              }
              if ((DAT_0a517013 & 1) == 0) {
                DAT_0a517008._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0x18];
                DAT_0a517008._1_1_ = s_reason__name____owl_asynlooper_c_09683008[0x19];
                DAT_0a517008._2_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1a];
                DAT_0a517008._3_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1b];
                DAT_0a517008._4_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1c];
                DAT_0a517008._5_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1d];
                DAT_0a517008._6_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1e];
                DAT_0a517008._7_1_ = s_reason__name____owl_asynlooper_c_09683008[0x1f];
                DAT_0a517010 = 0x7070;
                DAT_0a517012 = 0;
                DAT_0a517013 = 1;
              }
              FUN_0668db5c(&local_178,&DAT_0a516fe8,&DAT_0a517220,&DAT_0a517008,0x16f00000800);
              if ((DAT_0a517251 & 1) == 0) {
                _DAT_0a517230 = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
                uRam000000000a517238 = CONCAT44((int)DAT_087716a0,(int)DAT_0854de60);
                _DAT_0a517240 = CONCAT44((int)DAT_08485360,(int)DAT_084b03c8);
                uRam000000000a517248 = CONCAT44((int)DAT_0862c950,(int)DAT_08607240);
                DAT_0a517250 = 0;
                DAT_0a517251 = 1;
              }
              plVar13 = (long *)(local_178 + 0x68);
              if (*(char *)(local_178 + 0x7f) < '\0') {
                plVar13 = (long *)*plVar13;
              }
              local_78[0] = *(long *)(param_1 + 0x80);
              if (-1 < *(char *)(param_1 + 0x97)) {
                local_78[0] = param_1 + 0x80;
              }
              local_78[1] = 0xaaaaaaaa00000010;
              _uStack_68 = CONCAT44(0xaaaaaaaa,uVar3);
              local_50 = 0xaaaaaaaa00000006;
              local_60 = 0xaaaaaaaa00000007;
              local_58 = &DAT_aaaaaaaa00000000;
              FUN_0668e1e4(local_178 + 0x38,&DAT_0a517230,plVar13,local_78,2);
              FUN_0668dbac();
              thunk_FUN_0668e878(&local_178);
            }
            *(undefined8 *)(*(long *)(param_1 + 0x98) + (uVar14 & 0xffffffff) * 8) = 0;
            lVar8 = *(long *)(param_1 + 0xb8);
            lVar10 = *(long *)(param_1 + 0xc0);
            lVar1 = 0;
            if (lVar10 != lVar8) {
              lVar1 = (lVar10 - lVar8) * 0x80 + -1;
            }
            lVar7 = *(long *)(param_1 + 0xd8);
            if (lVar1 == lVar7 + *(long *)(param_1 + 0xd0)) {
              FUN_06667878(param_1 + 0xb0);
              lVar7 = *(long *)(param_1 + 0xd8);
              lVar8 = *(long *)(param_1 + 0xb8);
              lVar10 = *(long *)(param_1 + 0xc0);
            }
            if (lVar10 == lVar8) {
              puVar9 = (undefined4 *)0x0;
            }
            else {
              uVar14 = *(long *)(param_1 + 0xd0) + lVar7;
              puVar9 = (undefined4 *)
                       (*(long *)(lVar8 + (uVar14 >> 7 & 0x1fffffffffffff8)) + (uVar14 & 0x3ff) * 4)
              ;
            }
            *puVar9 = uVar3;
            *(long *)(param_1 + 0xd8) = lVar7 + 1;
            FUN_066676c0(*(long *)(param_1 + 0xe0),*(long *)(param_1 + 0xe8),&local_178,
                         (*(long *)(param_1 + 0xe8) - *(long *)(param_1 + 0xe0) >> 3) *
                         -0x5555555555555555);
            *(long *)(param_1 + 0xe8) = *(long *)(param_1 + 0xe8) + -0x18;
            if (puVar12 != (uint *)0x0) {
              if (*(long **)(puVar12 + 4) != (long *)0x0) {
                (**(code **)(**(long **)(puVar12 + 4) + 8))();
                puVar12[4] = 0;
                puVar12[5] = 0;
              }
              __ZdlPvm(puVar12,0x18);
            }
            uVar11 = 0xfffffffc;
          }
          else {
            uVar5 = FUN_066874a4();
            if (uVar5 < local_90) {
              uVar11 = 0xfffffffd;
              goto LAB_06664a40;
            }
            if ((short)puVar12[1] == 2) {
              local_90 = 0;
              FUN_066676c0(*(long *)(param_1 + 0xe0),*(long *)(param_1 + 0xe8),&local_178,
                           (*(long *)(param_1 + 0xe8) - *(long *)(param_1 + 0xe0) >> 3) *
                           -0x5555555555555555);
              *(long *)(param_1 + 0xe8) = *(long *)(param_1 + 0xe8) + -0x18;
              FUN_066637cc(plVar13,&local_a0);
              *(ushort *)((long)puVar12 + 6) = *(ushort *)((long)puVar12 + 6) | 1;
              if (((ulong)local_80 & 1) == 0) {
LAB_06664f48:
                if ((DAT_0a517410 & 1) == 0) {
                  _DAT_0a5173f0 = CONCAT44((int)DAT_09683050,(int)ram0x085a1170);
                  uRam000000000a5173f8 = CONCAT44((int)DAT_09683058,(int)DAT_08b4d180);
                  _DAT_0a517400 = CONCAT44((int)DAT_08487d20,(int)DAT_08b4d180);
                  uRam000000000a517408 = CONCAT44((int)DAT_084d00d8,(int)DAT_08522670);
                  DAT_0a517410 = 1;
                }
                    /* WARNING: Subroutine does not return */
                __ZNSt3__120__throw_system_errorEiPKc(1,&DAT_0a5173f0);
              }
              __ZNSt3__15mutex6unlockEv(local_88);
              local_80 = (undefined1 *)((ulong)local_80 & 0xffffffffffffff00);
              FUN_066650a0(param_1,puVar12);
              FUN_066655b0(&local_88);
              uVar2 = *(ushort *)((long)puVar12 + 6);
              *(ushort *)((long)puVar12 + 6) = uVar2 & 0xfffe;
              if ((uVar2 >> 1 & 1) != 0) {
                *(undefined8 *)(*(long *)(param_1 + 0x98) + (uVar14 & 0xffffffff) * 8) = 0;
                FUN_0666500c(param_1 + 0xb0,&local_a4);
                goto LAB_06664f14;
              }
              local_168 = 0;
              local_178 = CONCAT44(0xaaaaaaaa,uVar3);
              LOAcquire();
              local_170 = *(long *)(param_1 + 0x108);
              *(long *)(param_1 + 0x108) = local_170 + 1;
              LORelease();
              local_168 = FUN_066874a4();
              local_168 = local_168 + (ulong)*puVar12;
              FUN_066637cc(plVar13,&local_178);
            }
            else {
              *(undefined8 *)(*(long *)(param_1 + 0x98) + (uVar14 & 0xffffffff) * 8) = 0;
              lVar8 = *(long *)(param_1 + 0xb8);
              lVar10 = *(long *)(param_1 + 0xc0);
              lVar1 = 0;
              if (lVar10 != lVar8) {
                lVar1 = (lVar10 - lVar8) * 0x80 + -1;
              }
              lVar7 = *(long *)(param_1 + 0xd8);
              if (lVar1 == lVar7 + *(long *)(param_1 + 0xd0)) {
                FUN_06667878(param_1 + 0xb0);
                lVar7 = *(long *)(param_1 + 0xd8);
                lVar8 = *(long *)(param_1 + 0xb8);
                lVar10 = *(long *)(param_1 + 0xc0);
              }
              if (lVar10 == lVar8) {
                puVar9 = (undefined4 *)0x0;
              }
              else {
                uVar14 = *(long *)(param_1 + 0xd0) + lVar7;
                puVar9 = (undefined4 *)
                         (*(long *)(lVar8 + (uVar14 >> 7 & 0x1fffffffffffff8)) +
                         (uVar14 & 0x3ff) * 4);
              }
              *puVar9 = uVar3;
              *(long *)(param_1 + 0xd8) = lVar7 + 1;
              FUN_066676c0(*(long *)(param_1 + 0xe0),*(long *)(param_1 + 0xe8),&local_178,
                           (*(long *)(param_1 + 0xe8) - *(long *)(param_1 + 0xe0) >> 3) *
                           -0x5555555555555555);
              *(long *)(param_1 + 0xe8) = *(long *)(param_1 + 0xe8) + -0x18;
              if (((ulong)local_80 & 1) == 0) goto LAB_06664f48;
              __ZNSt3__15mutex6unlockEv(local_88);
              local_80 = (undefined1 *)((ulong)local_80 & 0xffffffffffffff00);
              FUN_066650a0(param_1,puVar12);
LAB_06664f14:
              uVar11 = 0;
              if (puVar12 == (uint *)0x0) goto LAB_06664a40;
              if (*(long **)(puVar12 + 4) != (long *)0x0) {
                (**(code **)(**(long **)(puVar12 + 4) + 8))();
                puVar12[4] = 0;
                puVar12[5] = 0;
              }
              __ZdlPvm(puVar12,0x18);
            }
            uVar11 = 0;
          }
          goto LAB_06664a40;
        }
        FUN_066676c0(puVar4,puVar6,&local_178,
                     ((long)puVar6 - (long)puVar4 >> 3) * -0x5555555555555555);
        puVar4 = *(ulong **)(param_1 + 0xe0);
        puVar6 = (ulong *)(*(long *)(param_1 + 0xe8) + -0x18);
        *(ulong **)(param_1 + 0xe8) = puVar6;
      } while (puVar4 != puVar6);
    }
    uVar11 = 0xfffffffe;
  }
LAB_06664a40:
  if ((char)local_80 == '\x01') {
    __ZNSt3__15mutex6unlockEv(local_88);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar11;
}


