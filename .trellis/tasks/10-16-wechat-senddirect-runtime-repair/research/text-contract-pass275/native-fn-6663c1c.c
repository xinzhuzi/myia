// Ghidra inferred pseudocode; requested=0x6663c1c
// entry=06663c1c end=0666493f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06663c1c(long param_1)

{
  int *piVar1;
  int *piVar2;
  long lVar3;
  int iVar4;
  int iVar5;
  ulong uVar6;
  long *plVar7;
  long *plVar8;
  ulong uVar9;
  long lVar10;
  long lVar11;
  ulong uVar12;
  long *local_158 [26];
  long local_88;
  undefined1 *local_80;
  long local_78 [2];
  undefined8 uStack_68;
  undefined8 local_60;
  undefined1 *puStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_88 = param_1 + 8;
  local_80 = &DAT_aaaaaaaaaaaaaa01;
  __ZNSt3__15mutex4lockEv();
  if (*(int *)(param_1 + 0x100) == 1) goto LAB_06663fec;
  if (*(long *)(param_1 + 0xe0) != *(long *)(param_1 + 0xe8)) {
    uVar6 = FUN_066874a4();
    uVar9 = *(ulong *)(*(long *)(param_1 + 0xe0) + 0x10);
    if (uVar9 != 0xffffffffffffffff) {
      uVar12 = uVar9 - uVar6;
      if ((uVar9 < uVar6 || uVar12 == 0) || (iVar5 = (int)uVar12, iVar5 == 0)) {
        iVar5 = FUN_0668dad0(0);
        if (iVar5 != 0) {
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
          if ((DAT_0a517131 & 1) == 0) {
            uRam000000000a517128._0_1_ = s_wait_task_ready___________wait_0_09683130[8];
            uRam000000000a517128._1_1_ = s_wait_task_ready___________wait_0_09683130[9];
            uRam000000000a517128._2_1_ = s_wait_task_ready___________wait_0_09683130[10];
            uRam000000000a517128._3_1_ = s_wait_task_ready___________wait_0_09683130[0xb];
            uRam000000000a517128._4_1_ = s_wait_task_ready___________wait_0_09683130[0xc];
            uRam000000000a517128._5_1_ = s_wait_task_ready___________wait_0_09683130[0xd];
            uRam000000000a517128._6_1_ = s_wait_task_ready___________wait_0_09683130[0xe];
            uRam000000000a517128._7_1_ = s_wait_task_ready___________wait_0_09683130[0xf];
            DAT_0a517120 = s_wait_task_ready___________wait_0_09683130[0];
            DAT_0a517120_1._0_1_ = s_wait_task_ready___________wait_0_09683130[1];
            DAT_0a517120_1._1_1_ = s_wait_task_ready___________wait_0_09683130[2];
            DAT_0a517120_1._2_1_ = s_wait_task_ready___________wait_0_09683130[3];
            DAT_0a517120_1._3_1_ = s_wait_task_ready___________wait_0_09683130[4];
            DAT_0a517120_1._4_1_ = s_wait_task_ready___________wait_0_09683130[5];
            DAT_0a517120_1._5_1_ = s_wait_task_ready___________wait_0_09683130[6];
            DAT_0a517120_1._6_1_ = s_wait_task_ready___________wait_0_09683130[7];
            DAT_0a517130 = 0;
            DAT_0a517131 = 1;
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
          FUN_0668db5c(local_158,&DAT_0a516fe8,&DAT_0a517120,&DAT_0a517008,0x12700000800);
          if ((DAT_0a517162 & 1) == 0) {
            uRam000000000a517158._0_1_ = s_wait_task_ready___________wait_0_09683130[0x18];
            uRam000000000a517158._1_1_ = s_wait_task_ready___________wait_0_09683130[0x19];
            uRam000000000a517158._2_1_ = s_wait_task_ready___________wait_0_09683130[0x1a];
            uRam000000000a517158._3_1_ = s_wait_task_ready___________wait_0_09683130[0x1b];
            uRam000000000a517158._4_1_ = s_wait_task_ready___________wait_0_09683130[0x1c];
            uRam000000000a517158._5_1_ = s_wait_task_ready___________wait_0_09683130[0x1d];
            uRam000000000a517158._6_1_ = s_wait_task_ready___________wait_0_09683130[0x1e];
            uRam000000000a517158._7_1_ = s_wait_task_ready___________wait_0_09683130[0x1f];
            DAT_0a517150 = s_wait_task_ready___________wait_0_09683130[0x10];
            DAT_0a517150_1._0_1_ = s_wait_task_ready___________wait_0_09683130[0x11];
            DAT_0a517150_1._1_1_ = s_wait_task_ready___________wait_0_09683130[0x12];
            DAT_0a517150_1._2_1_ = s_wait_task_ready___________wait_0_09683130[0x13];
            DAT_0a517150_1._3_1_ = s_wait_task_ready___________wait_0_09683130[0x14];
            DAT_0a517150_1._4_1_ = s_wait_task_ready___________wait_0_09683130[0x15];
            DAT_0a517150_1._5_1_ = s_wait_task_ready___________wait_0_09683130[0x16];
            DAT_0a517150_1._6_1_ = s_wait_task_ready___________wait_0_09683130[0x17];
            DAT_0a517160 = 0x29;
            DAT_0a517162 = 1;
          }
          plVar7 = local_158[0] + 0xd;
          if (*(char *)((long)local_158[0] + 0x7f) < '\0') {
            plVar7 = (long *)*plVar7;
          }
          local_78[0] = *(long *)(param_1 + 0x80);
          if (-1 < *(char *)(param_1 + 0x97)) {
            local_78[0] = param_1 + 0x80;
          }
          local_78[1] = 0xaaaaaaaa00000010;
          local_60 = 0xaaaaaaaa00000006;
          uStack_68 = &DAT_aaaaaaaa00000000;
          FUN_0668e1e4(local_158[0] + 7,&DAT_0a517150,plVar7,local_78,1);
          FUN_0668dbac();
          thunk_FUN_0668e878(local_158);
        }
        goto LAB_06663fec;
      }
      if (iVar5 == -1) goto LAB_06663ca4;
      iVar4 = FUN_0668dad0(0);
      if (iVar4 != 0) {
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
        if ((DAT_0a517131 & 1) == 0) {
          uRam000000000a517128._0_1_ = s_wait_task_ready___________wait_0_09683130[8];
          uRam000000000a517128._1_1_ = s_wait_task_ready___________wait_0_09683130[9];
          uRam000000000a517128._2_1_ = s_wait_task_ready___________wait_0_09683130[10];
          uRam000000000a517128._3_1_ = s_wait_task_ready___________wait_0_09683130[0xb];
          uRam000000000a517128._4_1_ = s_wait_task_ready___________wait_0_09683130[0xc];
          uRam000000000a517128._5_1_ = s_wait_task_ready___________wait_0_09683130[0xd];
          uRam000000000a517128._6_1_ = s_wait_task_ready___________wait_0_09683130[0xe];
          uRam000000000a517128._7_1_ = s_wait_task_ready___________wait_0_09683130[0xf];
          DAT_0a517120 = s_wait_task_ready___________wait_0_09683130[0];
          DAT_0a517120_1._0_1_ = s_wait_task_ready___________wait_0_09683130[1];
          DAT_0a517120_1._1_1_ = s_wait_task_ready___________wait_0_09683130[2];
          DAT_0a517120_1._2_1_ = s_wait_task_ready___________wait_0_09683130[3];
          DAT_0a517120_1._3_1_ = s_wait_task_ready___________wait_0_09683130[4];
          DAT_0a517120_1._4_1_ = s_wait_task_ready___________wait_0_09683130[5];
          DAT_0a517120_1._5_1_ = s_wait_task_ready___________wait_0_09683130[6];
          DAT_0a517120_1._6_1_ = s_wait_task_ready___________wait_0_09683130[7];
          DAT_0a517130 = 0;
          DAT_0a517131 = 1;
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
        FUN_0668db5c(local_158,&DAT_0a516fe8,&DAT_0a517120,&DAT_0a517008,0x12a00000800);
        if ((DAT_0a517183 & 1) == 0) {
          uRam000000000a517178._0_1_ = s_wait_task_ready___________wait_0_09683130[0x28];
          uRam000000000a517178._1_1_ = s_wait_task_ready___________wait_0_09683130[0x29];
          uRam000000000a517178._2_1_ = s_wait_task_ready___________wait_0_09683130[0x2a];
          uRam000000000a517178._3_1_ = s_wait_task_ready___________wait_0_09683130[0x2b];
          uRam000000000a517178._4_1_ = s_wait_task_ready___________wait_0_09683130[0x2c];
          uRam000000000a517178._5_1_ = s_wait_task_ready___________wait_0_09683130[0x2d];
          uRam000000000a517178._6_1_ = s_wait_task_ready___________wait_0_09683130[0x2e];
          uRam000000000a517178._7_1_ = s_wait_task_ready___________wait_0_09683130[0x2f];
          DAT_0a517170 = s_wait_task_ready___________wait_0_09683130[0x20];
          DAT_0a517170_1._0_1_ = s_wait_task_ready___________wait_0_09683130[0x21];
          DAT_0a517170_1._1_1_ = s_wait_task_ready___________wait_0_09683130[0x22];
          DAT_0a517170_1._2_1_ = s_wait_task_ready___________wait_0_09683130[0x23];
          DAT_0a517170_1._3_1_ = s_wait_task_ready___________wait_0_09683130[0x24];
          DAT_0a517170_1._4_1_ = s_wait_task_ready___________wait_0_09683130[0x25];
          DAT_0a517170_1._5_1_ = s_wait_task_ready___________wait_0_09683130[0x26];
          DAT_0a517170_1._6_1_ = s_wait_task_ready___________wait_0_09683130[0x27];
          DAT_0a517180 = 0x295f;
          DAT_0a517182 = 0;
          DAT_0a517183 = 1;
        }
        plVar7 = local_158[0] + 0xd;
        if (*(char *)((long)local_158[0] + 0x7f) < '\0') {
          plVar7 = (long *)*plVar7;
        }
        local_78[0] = *(long *)(param_1 + 0x80);
        if (-1 < *(char *)(param_1 + 0x97)) {
          local_78[0] = param_1 + 0x80;
        }
        local_78[1] = 0xaaaaaaaa00000010;
        uStack_68 = (undefined1 *)CONCAT44(0xaaaaaaaa,iVar5);
        local_50 = 0xaaaaaaaa00000006;
        local_60 = 0xaaaaaaaa00000007;
        puStack_58 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(local_158[0] + 7,&DAT_0a517170,plVar7,local_78,2);
        FUN_0668dbac();
        thunk_FUN_0668e878(local_158);
      }
      if (*(long *)(param_1 + 0x78) == 0) {
        uVar12 = uVar12 & 0xffffffff;
        if (uVar12 != 0) {
          lVar11 = __ZNSt3__16chrono12steady_clock3nowEv();
          uVar6 = __ZNSt3__16chrono12system_clock3nowEv();
          if (uVar6 == 0) {
            lVar10 = 0;
          }
          else if ((long)uVar6 < 1) {
            if (0xffdf3b645a1cac08 < uVar6) goto LAB_06664250;
            lVar10 = -0x8000000000000000;
          }
          else if (uVar6 < 0x20c49ba5e353f8) {
LAB_06664250:
            lVar10 = uVar6 * 1000;
          }
          else {
            lVar10 = 0x7fffffffffffffff;
          }
          lVar3 = 0x7fffffffffffffff;
          if (lVar10 <= (long)(uVar12 * 1000000 ^ 0x7fffffffffffffff)) {
            lVar3 = lVar10 + uVar12 * 1000000;
          }
          __ZNSt3__118condition_variable15__do_timed_waitERNS_11unique_lockINS_5mutexEEENS_6chrono10time_pointINS5_12system_clockENS5_8durationIxNS_5ratioILl1ELl1000000000EEEEEEE
                    (param_1 + 0x48,&local_88,lVar3);
          lVar10 = __ZNSt3__16chrono12steady_clock3nowEv();
          if (lVar10 - lVar11 < (long)(uVar12 * 1000000)) goto LAB_06664294;
        }
LAB_06664488:
        iVar5 = FUN_0668dad0(0);
        if (iVar5 != 0) {
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
          if ((DAT_0a517131 & 1) == 0) {
            uRam000000000a517128._0_1_ = s_wait_task_ready___________wait_0_09683130[8];
            uRam000000000a517128._1_1_ = s_wait_task_ready___________wait_0_09683130[9];
            uRam000000000a517128._2_1_ = s_wait_task_ready___________wait_0_09683130[10];
            uRam000000000a517128._3_1_ = s_wait_task_ready___________wait_0_09683130[0xb];
            uRam000000000a517128._4_1_ = s_wait_task_ready___________wait_0_09683130[0xc];
            uRam000000000a517128._5_1_ = s_wait_task_ready___________wait_0_09683130[0xd];
            uRam000000000a517128._6_1_ = s_wait_task_ready___________wait_0_09683130[0xe];
            uRam000000000a517128._7_1_ = s_wait_task_ready___________wait_0_09683130[0xf];
            DAT_0a517120 = s_wait_task_ready___________wait_0_09683130[0];
            DAT_0a517120_1._0_1_ = s_wait_task_ready___________wait_0_09683130[1];
            DAT_0a517120_1._1_1_ = s_wait_task_ready___________wait_0_09683130[2];
            DAT_0a517120_1._2_1_ = s_wait_task_ready___________wait_0_09683130[3];
            DAT_0a517120_1._3_1_ = s_wait_task_ready___________wait_0_09683130[4];
            DAT_0a517120_1._4_1_ = s_wait_task_ready___________wait_0_09683130[5];
            DAT_0a517120_1._5_1_ = s_wait_task_ready___________wait_0_09683130[6];
            DAT_0a517120_1._6_1_ = s_wait_task_ready___________wait_0_09683130[7];
            DAT_0a517130 = 0;
            DAT_0a517131 = 1;
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
          FUN_0668db5c(local_158,&DAT_0a516fe8,&DAT_0a517120,&DAT_0a517008,0x13500000800);
          if ((DAT_0a5171a2 & 1) == 0) {
            uRam000000000a517198._0_1_ = s_wait_task_ready___________wait_0_09683130[0x48];
            uRam000000000a517198._1_1_ = s_wait_task_ready___________wait_0_09683130[0x49];
            uRam000000000a517198._2_1_ = s_wait_task_ready___________wait_0_09683130[0x4a];
            uRam000000000a517198._3_1_ = s_wait_task_ready___________wait_0_09683130[0x4b];
            uRam000000000a517198._4_1_ = s_wait_task_ready___________wait_0_09683130[0x4c];
            uRam000000000a517198._5_1_ = s_wait_task_ready___________wait_0_09683130[0x4d];
            uRam000000000a517198._6_1_ = s_wait_task_ready___________wait_0_09683130[0x4e];
            uRam000000000a517198._7_1_ = s_wait_task_ready___________wait_0_09683130[0x4f];
            DAT_0a517190 = s_wait_task_ready___________wait_0_09683130[0x40];
            DAT_0a517190_1._0_1_ = s_wait_task_ready___________wait_0_09683130[0x41];
            DAT_0a517190_1._1_1_ = s_wait_task_ready___________wait_0_09683130[0x42];
            DAT_0a517190_1._2_1_ = s_wait_task_ready___________wait_0_09683130[0x43];
            DAT_0a517190_1._3_1_ = s_wait_task_ready___________wait_0_09683130[0x44];
            DAT_0a517190_1._4_1_ = s_wait_task_ready___________wait_0_09683130[0x45];
            DAT_0a517190_1._5_1_ = s_wait_task_ready___________wait_0_09683130[0x46];
            DAT_0a517190_1._6_1_ = s_wait_task_ready___________wait_0_09683130[0x47];
            DAT_0a5171a0 = 0x74;
            DAT_0a5171a2 = 1;
          }
          plVar7 = local_158[0] + 0xd;
          if (*(char *)((long)local_158[0] + 0x7f) < '\0') {
            plVar7 = (long *)*plVar7;
          }
          local_78[0] = *(long *)(param_1 + 0x80);
          if (-1 < *(char *)(param_1 + 0x97)) {
            local_78[0] = param_1 + 0x80;
          }
          local_78[1] = 0xaaaaaaaa00000010;
          local_60 = 0xaaaaaaaa00000006;
          uStack_68 = &DAT_aaaaaaaa00000000;
          FUN_0668e1e4(local_158[0] + 7,&DAT_0a517190,plVar7,local_78,1);
LAB_066645dc:
          FUN_0668dbac();
          thunk_FUN_0668e878(local_158);
        }
      }
      else {
        if (((ulong)local_80 & 1) == 0) {
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
        iVar5 = (**(code **)(**(long **)(param_1 + 0x78) + 0x10))(*(long **)(param_1 + 0x78),uVar12)
        ;
        if (iVar5 != 0) goto LAB_06664488;
LAB_06664294:
        piVar1 = (int *)(param_1 + 0x114);
        LOAcquire();
        iVar5 = *piVar1;
        *piVar1 = iVar5 + 1;
        LORelease();
        iVar5 = FUN_0668dad0(iVar5,0);
        if (iVar5 != 0) {
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
          if ((DAT_0a517131 & 1) == 0) {
            uRam000000000a517128._0_1_ = s_wait_task_ready___________wait_0_09683130[8];
            uRam000000000a517128._1_1_ = s_wait_task_ready___________wait_0_09683130[9];
            uRam000000000a517128._2_1_ = s_wait_task_ready___________wait_0_09683130[10];
            uRam000000000a517128._3_1_ = s_wait_task_ready___________wait_0_09683130[0xb];
            uRam000000000a517128._4_1_ = s_wait_task_ready___________wait_0_09683130[0xc];
            uRam000000000a517128._5_1_ = s_wait_task_ready___________wait_0_09683130[0xd];
            uRam000000000a517128._6_1_ = s_wait_task_ready___________wait_0_09683130[0xe];
            uRam000000000a517128._7_1_ = s_wait_task_ready___________wait_0_09683130[0xf];
            DAT_0a517120 = s_wait_task_ready___________wait_0_09683130[0];
            DAT_0a517120_1._0_1_ = s_wait_task_ready___________wait_0_09683130[1];
            DAT_0a517120_1._1_1_ = s_wait_task_ready___________wait_0_09683130[2];
            DAT_0a517120_1._2_1_ = s_wait_task_ready___________wait_0_09683130[3];
            DAT_0a517120_1._3_1_ = s_wait_task_ready___________wait_0_09683130[4];
            DAT_0a517120_1._4_1_ = s_wait_task_ready___________wait_0_09683130[5];
            DAT_0a517120_1._5_1_ = s_wait_task_ready___________wait_0_09683130[6];
            DAT_0a517120_1._6_1_ = s_wait_task_ready___________wait_0_09683130[7];
            DAT_0a517130 = 0;
            DAT_0a517131 = 1;
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
          FUN_0668db5c(local_158,&DAT_0a516fe8,&DAT_0a517120,&DAT_0a517008,0x13800000800);
          plVar7 = local_158[0];
          if ((DAT_0a5171bb & 1) == 0) {
            _DAT_0a5171a4 = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
            uRam000000000a5171ac = CONCAT44((int)DAT_084aeb08,(int)DAT_086e1250);
            DAT_0a5171b4 = (undefined4)ram0x085618c0;
            DAT_0a5171b8 = 0x203a;
            DAT_0a5171ba = 0;
            DAT_0a5171bb = 1;
          }
          plVar8 = local_158[0] + 0xd;
          if (*(char *)((long)local_158[0] + 0x7f) < '\0') {
            plVar8 = (long *)*plVar8;
          }
          local_78[0] = *(long *)(param_1 + 0x80);
          if (-1 < *(char *)(param_1 + 0x97)) {
            local_78[0] = param_1 + 0x80;
          }
          local_78[1] = 0xaaaaaaaa00000010;
          local_60 = 0xaaaaaaaa00000006;
          uStack_68 = &DAT_aaaaaaaa00000000;
          FUN_0668e1e4(local_158[0] + 7,&DAT_0a5171a4,plVar8,local_78,1);
          lVar11 = *plVar7;
          if ((DAT_0a5171d3 & 1) == 0) {
            uRam000000000a5171c8._0_1_ = s_wait_task_ready___________wait_0_09683130[0x38];
            uRam000000000a5171c8._1_1_ = s_wait_task_ready___________wait_0_09683130[0x39];
            uRam000000000a5171c8._2_1_ = s_wait_task_ready___________wait_0_09683130[0x3a];
            uRam000000000a5171c8._3_1_ = s_wait_task_ready___________wait_0_09683130[0x3b];
            uRam000000000a5171c8._4_1_ = s_wait_task_ready___________wait_0_09683130[0x3c];
            uRam000000000a5171c8._5_1_ = s_wait_task_ready___________wait_0_09683130[0x3d];
            uRam000000000a5171c8._6_1_ = s_wait_task_ready___________wait_0_09683130[0x3e];
            uRam000000000a5171c8._7_1_ = s_wait_task_ready___________wait_0_09683130[0x3f];
            DAT_0a5171c0 = s_wait_task_ready___________wait_0_09683130[0x30];
            DAT_0a5171c0_1._0_1_ = s_wait_task_ready___________wait_0_09683130[0x31];
            DAT_0a5171c0_1._1_1_ = s_wait_task_ready___________wait_0_09683130[0x32];
            DAT_0a5171c0_1._2_1_ = s_wait_task_ready___________wait_0_09683130[0x33];
            DAT_0a5171c0_1._3_1_ = s_wait_task_ready___________wait_0_09683130[0x34];
            DAT_0a5171c0_1._4_1_ = s_wait_task_ready___________wait_0_09683130[0x35];
            DAT_0a5171c0_1._5_1_ = s_wait_task_ready___________wait_0_09683130[0x36];
            DAT_0a5171c0_1._6_1_ = s_wait_task_ready___________wait_0_09683130[0x37];
            DAT_0a5171d0 = 0x5f25;
            DAT_0a5171d2 = 0;
            DAT_0a5171d3 = 1;
          }
          plVar7 = (long *)(lVar11 + 0x68);
          if (*(char *)(lVar11 + 0x7f) < '\0') {
            plVar7 = (long *)*plVar7;
          }
          FUN_06667328(lVar11 + 0x38,&DAT_0a5171c0,plVar7,piVar1);
          goto LAB_066645dc;
        }
      }
      if (*(long *)(param_1 + 0x78) == 0) {
        piVar1 = (int *)(param_1 + 0x114);
        piVar2 = (int *)(param_1 + 0x110);
        if (0x14 < *piVar1 - *piVar2) {
          iVar5 = FUN_0668dad0(4);
          if (iVar5 != 0) {
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
            if ((DAT_0a517131 & 1) == 0) {
              uRam000000000a517128._0_1_ = s_wait_task_ready___________wait_0_09683130[8];
              uRam000000000a517128._1_1_ = s_wait_task_ready___________wait_0_09683130[9];
              uRam000000000a517128._2_1_ = s_wait_task_ready___________wait_0_09683130[10];
              uRam000000000a517128._3_1_ = s_wait_task_ready___________wait_0_09683130[0xb];
              uRam000000000a517128._4_1_ = s_wait_task_ready___________wait_0_09683130[0xc];
              uRam000000000a517128._5_1_ = s_wait_task_ready___________wait_0_09683130[0xd];
              uRam000000000a517128._6_1_ = s_wait_task_ready___________wait_0_09683130[0xe];
              uRam000000000a517128._7_1_ = s_wait_task_ready___________wait_0_09683130[0xf];
              DAT_0a517120 = s_wait_task_ready___________wait_0_09683130[0];
              DAT_0a517120_1._0_1_ = s_wait_task_ready___________wait_0_09683130[1];
              DAT_0a517120_1._1_1_ = s_wait_task_ready___________wait_0_09683130[2];
              DAT_0a517120_1._2_1_ = s_wait_task_ready___________wait_0_09683130[3];
              DAT_0a517120_1._3_1_ = s_wait_task_ready___________wait_0_09683130[4];
              DAT_0a517120_1._4_1_ = s_wait_task_ready___________wait_0_09683130[5];
              DAT_0a517120_1._5_1_ = s_wait_task_ready___________wait_0_09683130[6];
              DAT_0a517120_1._6_1_ = s_wait_task_ready___________wait_0_09683130[7];
              DAT_0a517130 = 0;
              DAT_0a517131 = 1;
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
            FUN_0668db5c(local_158,&DAT_0a516fe8,&DAT_0a517120,&DAT_0a517008,0x13d00008800);
            if ((DAT_0a5171f3 & 1) == 0) {
              _DAT_0a5171d4 = CONCAT44((int)DAT_0877c108,(int)DAT_084d57f8);
              uRam000000000a5171dc = CONCAT44((int)DAT_09683060,(int)DAT_08b5e8b8);
              DAT_0a5171e4 = CONCAT44((int)DAT_085a5e90,(int)DAT_09683068);
              DAT_0a5171ec = (undefined4)DAT_09683070;
              DAT_0a5171f0 = 0x203a;
              DAT_0a5171f2 = 0;
              DAT_0a5171f3 = 1;
            }
            plVar7 = (long *)FUN_04540044(local_158[0],&DAT_0a5171d4,param_1 + 0x80);
            lVar11 = *plVar7;
            if ((DAT_0a51721b & 1) == 0) {
              _DAT_0a5171f4 = CONCAT44((int)DAT_0849a5e8,(int)DAT_09683078);
              _DAT_0a517204 = CONCAT44((int)DAT_084a0c00,(int)DAT_084e3ff8);
              DAT_0a517214 = (undefined4)DAT_0877bfd8;
              uRam000000000a5171fc = CONCAT44(DAT_0a517214,(int)DAT_08480b48);
              uRam000000000a51720c = CONCAT44((int)DAT_08480b48,(int)DAT_09683080);
              DAT_0a517218 = 0x5f25;
              DAT_0a51721a = 0;
              DAT_0a51721b = 1;
            }
            plVar7 = (long *)(lVar11 + 0x68);
            if (*(char *)(lVar11 + 0x7f) < '\0') {
              plVar7 = (long *)*plVar7;
            }
            FUN_06667550(lVar11 + 0x38,&DAT_0a5171f4,plVar7,piVar1,piVar2);
            FUN_0668dbac();
            thunk_FUN_0668e878(local_158);
          }
          *piVar1 = 0;
          *piVar2 = 0;
          local_158[0] = (long *)0x989680;
          __ZNSt3__111this_thread9sleep_forERKNS_6chrono8durationIxNS_5ratioILl1ELl1000000000EEEEE
                    (local_158);
        }
      }
      goto LAB_06663fec;
    }
  }
LAB_06663ca4:
  uVar6 = FUN_0668dad0(0);
  if ((uVar6 & 1) != 0) {
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
    if ((DAT_0a517131 & 1) == 0) {
      uRam000000000a517128._0_1_ = s_wait_task_ready___________wait_0_09683130[8];
      uRam000000000a517128._1_1_ = s_wait_task_ready___________wait_0_09683130[9];
      uRam000000000a517128._2_1_ = s_wait_task_ready___________wait_0_09683130[10];
      uRam000000000a517128._3_1_ = s_wait_task_ready___________wait_0_09683130[0xb];
      uRam000000000a517128._4_1_ = s_wait_task_ready___________wait_0_09683130[0xc];
      uRam000000000a517128._5_1_ = s_wait_task_ready___________wait_0_09683130[0xd];
      uRam000000000a517128._6_1_ = s_wait_task_ready___________wait_0_09683130[0xe];
      uRam000000000a517128._7_1_ = s_wait_task_ready___________wait_0_09683130[0xf];
      DAT_0a517120 = s_wait_task_ready___________wait_0_09683130[0];
      DAT_0a517120_1._0_1_ = s_wait_task_ready___________wait_0_09683130[1];
      DAT_0a517120_1._1_1_ = s_wait_task_ready___________wait_0_09683130[2];
      DAT_0a517120_1._2_1_ = s_wait_task_ready___________wait_0_09683130[3];
      DAT_0a517120_1._3_1_ = s_wait_task_ready___________wait_0_09683130[4];
      DAT_0a517120_1._4_1_ = s_wait_task_ready___________wait_0_09683130[5];
      DAT_0a517120_1._5_1_ = s_wait_task_ready___________wait_0_09683130[6];
      DAT_0a517120_1._6_1_ = s_wait_task_ready___________wait_0_09683130[7];
      DAT_0a517130 = 0;
      DAT_0a517131 = 1;
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
    FUN_0668db5c(local_158,&DAT_0a516fe8,&DAT_0a517120,&DAT_0a517008,0x11d00000800);
    if ((DAT_0a51714d & 1) == 0) {
      _DAT_0a517134 = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
      uRam000000000a51713c = CONCAT44((int)DAT_09683088,(int)DAT_0877c2e0);
      DAT_0a517144 = CONCAT44((int)DAT_09683098,(int)DAT_09683090);
      DAT_0a51714c = 0;
      DAT_0a51714d = 1;
    }
    plVar7 = local_158[0] + 0xd;
    if (*(char *)((long)local_158[0] + 0x7f) < '\0') {
      plVar7 = (long *)*plVar7;
    }
    local_78[0] = *(long *)(param_1 + 0x80);
    if (-1 < *(char *)(param_1 + 0x97)) {
      local_78[0] = param_1 + 0x80;
    }
    local_78[1] = 0xaaaaaaaa00000010;
    local_60 = 0xaaaaaaaa00000006;
    uStack_68 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_158[0] + 7,&DAT_0a517134,plVar7,local_78,1);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_158);
  }
  if (*(long *)(param_1 + 0x78) == 0) {
    __ZNSt3__118condition_variable4waitERNS_11unique_lockINS_5mutexEEE(param_1 + 0x48,&local_88);
  }
  else {
    if (((ulong)local_80 & 1) == 0) {
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
    (**(code **)(**(long **)(param_1 + 0x78) + 0x10))(*(long **)(param_1 + 0x78),0xffffffff);
  }
  LOAcquire();
  *(int *)(param_1 + 0x114) = *(int *)(param_1 + 0x114) + 1;
  LORelease();
LAB_06663fec:
  if ((char)local_80 == '\x01') {
    __ZNSt3__15mutex6unlockEv(local_88);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


