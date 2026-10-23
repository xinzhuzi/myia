// Ghidra inferred pseudocode; requested=0x8a65d0
// entry=008a65d0 end=008a6897

/* WARNING: Removing unreachable block (ram,0x008a6828) */

bool FUN_008a65d0(long param_1,undefined8 param_2,long *param_3)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int iVar4;
  undefined8 *puVar5;
  char *pcVar6;
  size_t sVar7;
  long lVar8;
  undefined8 uVar9;
  undefined8 local_c8 [2];
  undefined7 local_b8;
  char cStack_b1;
  undefined8 local_b0;
  undefined8 uStack_a8;
  ulong local_a0;
  undefined8 local_90;
  undefined8 uStack_88;
  ulong local_80;
  undefined1 local_78;
  undefined7 uStack_77;
  undefined7 local_68;
  char cStack_61;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  
  iVar1 = *(int *)(*param_3 + 8);
  iVar2 = *(int *)(*param_3 + 0xc);
  if (iVar2 != iVar1) {
    __ZNSt3__19to_stringEi(&local_78,param_2);
    if ((DAT_0a2a7ab1 & 1) == 0) {
      DAT_0a2a7aa8._0_1_ = s_sendmsg_yMer_0854b730[0];
      DAT_0a2a7aa8._1_1_ = s_sendmsg_yMer_0854b730[1];
      DAT_0a2a7aa8._2_1_ = s_sendmsg_yMer_0854b730[2];
      DAT_0a2a7aa8._3_1_ = s_sendmsg_yMer_0854b730[3];
      DAT_0a2a7aa8._4_1_ = s_sendmsg_yMer_0854b730[4];
      DAT_0a2a7aa8._5_1_ = s_sendmsg_yMer_0854b730[5];
      DAT_0a2a7aa8._6_1_ = s_sendmsg_yMer_0854b730[6];
      DAT_0a2a7aa8._7_1_ = s_sendmsg_yMer_0854b730[7];
      DAT_0a2a7ab0 = 0;
      DAT_0a2a7ab1 = 1;
    }
    puVar5 = (undefined8 *)
             __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                       (&local_78,0,&DAT_0a2a7aa8);
    uStack_58 = puVar5[1];
    local_60 = *puVar5;
    local_50 = puVar5[2];
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    lVar8 = *(long *)(param_1 + 0x10);
    if (*(char *)(lVar8 + 0x26f) < '\0') {
      FUN_00018d20(&local_90,*(undefined8 *)(lVar8 + 600),*(undefined8 *)(lVar8 + 0x260));
    }
    else {
      uStack_88 = *(undefined8 *)(lVar8 + 0x260);
      local_90 = *(undefined8 *)(lVar8 + 600);
      local_80 = *(ulong *)(lVar8 + 0x268);
    }
    FUN_02214d2c(&local_60,&local_90);
    if ((long)local_80 < 0) {
      __ZdlPvm(local_90,local_80 & 0x7fffffffffffffff);
    }
    if (cStack_61 < '\0') {
      __ZdlPvm(CONCAT71(uStack_77,local_78),CONCAT17(cStack_61,local_68) & 0x7fffffffffffffff);
    }
    cStack_61 = '\0';
    local_78 = 0;
    __ZNSt3__19to_stringEi(local_c8,param_2);
    if ((DAT_0a2a7ab1 & 1) == 0) {
      DAT_0a2a7aa8._0_1_ = s_sendmsg_yMer_0854b730[0];
      DAT_0a2a7aa8._1_1_ = s_sendmsg_yMer_0854b730[1];
      DAT_0a2a7aa8._2_1_ = s_sendmsg_yMer_0854b730[2];
      DAT_0a2a7aa8._3_1_ = s_sendmsg_yMer_0854b730[3];
      DAT_0a2a7aa8._4_1_ = s_sendmsg_yMer_0854b730[4];
      DAT_0a2a7aa8._5_1_ = s_sendmsg_yMer_0854b730[5];
      DAT_0a2a7aa8._6_1_ = s_sendmsg_yMer_0854b730[6];
      DAT_0a2a7aa8._7_1_ = s_sendmsg_yMer_0854b730[7];
      DAT_0a2a7ab0 = 0;
      DAT_0a2a7ab1 = 1;
    }
    puVar5 = (undefined8 *)
             __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                       (local_c8,0,&DAT_0a2a7aa8);
    uStack_a8 = puVar5[1];
    local_b0 = *puVar5;
    local_a0 = puVar5[2];
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    FUN_02214f3c(&local_78,&local_b0);
    if ((long)local_a0 < 0) {
      __ZdlPvm(local_b0,local_a0 & 0x7fffffffffffffff);
    }
    if (cStack_b1 < '\0') {
      __ZdlPvm(local_c8[0],CONCAT17(cStack_b1,local_b8) & 0x7fffffffffffffff);
    }
    if (cStack_61 < '\0') {
      __ZdlPvm(CONCAT71(uStack_77,local_78),CONCAT17(cStack_61,local_68) & 0x7fffffffffffffff);
    }
    goto LAB_008a67f0;
  }
  uVar9 = *(undefined8 *)(param_1 + 0x10);
  pcVar6 = (char *)FUN_04e079c8();
  if (pcVar6 == (char *)0x0) {
    sVar7 = 0xffffffff;
  }
  else {
    sVar7 = _strlen(pcVar6);
  }
  FUN_06ef81e0(&local_78,pcVar6,sVar7);
  FUN_01f35d68(uVar9,&local_78);
  piVar3 = (int *)CONCAT71(uStack_77,local_78);
  if (*piVar3 != -1) {
    if (*piVar3 != 0) {
      LOAcquire();
      iVar4 = *piVar3;
      *piVar3 = iVar4 + -1;
      LORelease();
      if (iVar4 != 1) goto LAB_008a66f8;
    }
    FUN_06ea14cc(CONCAT71(uStack_77,local_78),2,8);
  }
LAB_008a66f8:
  (**(code **)(**(long **)(*(long *)(param_1 + 0x10) + 0x200) + 0x208))();
  if ((*(long *)(*(long *)(param_1 + 0x10) + 0x200) != 0) && (lVar8 = FUN_06b18cb0(), lVar8 != 0)) {
    uVar9 = FUN_06b18cb0(*(undefined8 *)(*(long *)(param_1 + 0x10) + 0x200));
    FUN_06d1e97c(uVar9,3);
  }
LAB_008a67f0:
  return iVar2 != iVar1;
}


