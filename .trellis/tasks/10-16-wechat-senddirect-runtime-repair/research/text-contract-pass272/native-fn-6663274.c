// Ghidra inferred pseudocode; requested=0x6663274
// entry=06663274 end=0666379b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06663274(long param_1,undefined8 param_2,undefined2 param_3,undefined8 param_4,uint param_5
                 ,undefined4 param_6)

{
  int *piVar1;
  int iVar2;
  undefined4 *puVar3;
  long *plVar4;
  ulong uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  ulong local_168;
  long local_160 [26];
  uint local_8c;
  undefined8 local_88;
  long local_80;
  undefined1 *local_78;
  undefined8 local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_8c = param_5;
  if ((*(int *)(param_1 + 0x100) == 1) && (iVar2 = FUN_0668dad0(3), iVar2 != 0)) {
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
    if ((DAT_0a517061 & 1) == 0) {
      DAT_0a517058._0_1_ = s_name____add_task_loo_09683030[8];
      DAT_0a517058._1_1_ = s_name____add_task_loo_09683030[9];
      DAT_0a517058._2_1_ = s_name____add_task_loo_09683030[10];
      DAT_0a517058._3_1_ = s_name____add_task_loo_09683030[0xb];
      DAT_0a517058._4_1_ = s_name____add_task_loo_09683030[0xc];
      DAT_0a517058._5_1_ = s_name____add_task_loo_09683030[0xd];
      DAT_0a517058._6_1_ = s_name____add_task_loo_09683030[0xe];
      DAT_0a517058._7_1_ = s_name____add_task_loo_09683030[0xf];
      DAT_0a517060 = 0;
      DAT_0a517061 = 1;
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
    FUN_0668db5c(local_160,&DAT_0a516fe8,&DAT_0a517058,&DAT_0a517008,0xa100006800);
    if ((DAT_0a51709f & 1) == 0) {
      _DAT_0a517064 = CONCAT44((int)DAT_087faf40,(int)DAT_084d57f8);
      uRam000000000a51706c = CONCAT44((int)DAT_084d6610,(int)ram0x09683040);
      _DAT_0a517074 = CONCAT44((int)DAT_084d8858,(int)DAT_08487490);
      uRam000000000a51707c = CONCAT44((int)DAT_09683048,(int)DAT_08771938);
      _DAT_0a517084 = CONCAT44((int)DAT_084c7768,(int)DAT_08868c50);
      uRam000000000a51708c = CONCAT44((int)DAT_0896cb08,(int)DAT_0856c328);
      DAT_0a517094 = CONCAT44((int)DAT_086cad10,(int)DAT_08787078);
      DAT_0a51709c = 0x6465;
      DAT_0a51709e = 0;
      DAT_0a51709f = 1;
    }
    plVar4 = (long *)(local_160[0] + 0x68);
    if (*(char *)(local_160[0] + 0x7f) < '\0') {
      plVar4 = (long *)*plVar4;
    }
    local_88 = *(long *)(param_1 + 0x80);
    if (-1 < *(char *)(param_1 + 0x97)) {
      local_88 = param_1 + 0x80;
    }
    local_80 = -0x55555555fffffff0;
    local_70 = 0xaaaaaaaa00000006;
    local_78 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_160[0] + 0x38,&DAT_0a517064,plVar4,&local_88,1);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_160);
  }
  local_168 = FUN_066874a4();
  puVar3 = (undefined4 *)__Znwm(0x18);
  *(undefined8 *)(puVar3 + 4) = param_4;
  uVar6 = (undefined4)((ulong)param_2 >> 0x20);
  puVar3[2] = uVar6;
  puVar3[3] = (int)param_2;
  *(undefined2 *)(puVar3 + 1) = param_3;
  *puVar3 = param_6;
  *(undefined2 *)((long)puVar3 + 6) = 0;
  local_88 = CONCAT44(0xaaaaaaaa,uVar6);
  LOAcquire();
  local_80 = *(long *)(param_1 + 0x108);
  *(long *)(param_1 + 0x108) = local_80 + 1;
  LORelease();
  local_78 = (undefined1 *)(local_168 + local_8c);
  if (local_8c == 0xffffffff) {
    local_78 = (undefined1 *)0xffffffffffffffff;
  }
  iVar2 = FUN_0668dad0(0);
  if (iVar2 != 0) {
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
    if ((DAT_0a517061 & 1) == 0) {
      DAT_0a517058._0_1_ = s_name____add_task_loo_09683030[8];
      DAT_0a517058._1_1_ = s_name____add_task_loo_09683030[9];
      DAT_0a517058._2_1_ = s_name____add_task_loo_09683030[10];
      DAT_0a517058._3_1_ = s_name____add_task_loo_09683030[0xb];
      DAT_0a517058._4_1_ = s_name____add_task_loo_09683030[0xc];
      DAT_0a517058._5_1_ = s_name____add_task_loo_09683030[0xd];
      DAT_0a517058._6_1_ = s_name____add_task_loo_09683030[0xe];
      DAT_0a517058._7_1_ = s_name____add_task_loo_09683030[0xf];
      DAT_0a517060 = 0;
      DAT_0a517061 = 1;
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
    FUN_0668db5c(local_160,&DAT_0a516fe8,&DAT_0a517058,&DAT_0a517008,0xb200000800);
    if ((DAT_0a51711b & 1) == 0) {
      uVar5 = 0;
      do {
        uVar6 = *(undefined4 *)((long)&DAT_0968334d + uVar5);
        uVar7 = *(undefined4 *)((long)&DAT_09683339 + uVar5 % 0x14);
        *(uint *)((long)&DAT_0a5170a0 + uVar5) =
             CONCAT13((byte)((uint)uVar7 >> 0x18) ^ (byte)((uint)uVar6 >> 0x18),
                      CONCAT12((byte)((uint)uVar7 >> 0x10) ^ (byte)((uint)uVar6 >> 0x10),
                               CONCAT11((byte)((uint)uVar7 >> 8) ^ (byte)((uint)uVar6 >> 8),
                                        (byte)uVar7 ^ (byte)uVar6)));
        uVar5 = uVar5 + 4;
      } while (uVar5 != 0x78);
      DAT_0a517118 = 0x7d20;
      DAT_0a51711a = 0;
      DAT_0a51711b = 1;
    }
    plVar4 = (long *)(local_160[0] + 0x68);
    if (*(char *)(local_160[0] + 0x7f) < '\0') {
      plVar4 = (long *)*plVar4;
    }
    FUN_06667018(local_160[0] + 0x38,&DAT_0a5170a0,plVar4,param_1 + 0x80,puVar3 + 2,puVar3 + 3,
                 puVar3 + 1,&local_168,&local_8c,puVar3,(undefined2 *)((long)puVar3 + 6),&local_80,
                 &local_78);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_160);
  }
  __ZNSt3__15mutex4lockEv(param_1 + 8);
  *(undefined4 **)(*(long *)(param_1 + 0x98) + (ulong)(uint)puVar3[2] * 8) = puVar3;
  FUN_066637cc(param_1 + 0xe0,&local_88);
  if ((*(long *)(*(long *)(param_1 + 0xe0) + 8) == local_80) ||
     (*(ulong *)(*(long *)(param_1 + 0xe0) + 0x10) <= local_168)) {
    piVar1 = (int *)(param_1 + 0x110);
    LOAcquire();
    iVar2 = *piVar1;
    *piVar1 = iVar2 + 1;
    LORelease();
    if (*(long **)(param_1 + 0x78) == (long *)0x0) {
      __ZNSt3__118condition_variable10notify_oneEv
                (CONCAT44((int)((ulong)piVar1 >> 0x20),iVar2),param_1 + 0x48);
    }
    else {
      (**(code **)(**(long **)(param_1 + 0x78) + 0x18))();
    }
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 8);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


