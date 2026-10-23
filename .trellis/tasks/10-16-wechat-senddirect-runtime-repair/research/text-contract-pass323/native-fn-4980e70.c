// Ghidra inferred pseudocode; requested=0x4980e70
// entry=04980e70 end=0498127f

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04980e70(long *param_1,long *param_2)

{
  void *pvVar1;
  ulong uVar2;
  long *plVar3;
  short *psVar4;
  undefined1 *puVar5;
  byte bVar6;
  undefined1 *puVar7;
  short *******pppppppsVar8;
  undefined1 *puVar9;
  char cVar10;
  code *pcVar11;
  int iVar12;
  size_t sVar13;
  long *plVar14;
  void *pvVar15;
  int iVar16;
  long lVar17;
  ulong uVar18;
  undefined1 *puVar19;
  ulong uVar20;
  short *******local_78;
  undefined1 *local_70;
  undefined8 local_68;
  
  bVar6 = *(byte *)((long)param_2 + 0x17);
  uVar20 = param_2[1];
  uVar2 = uVar20;
  if (-1 < (char)bVar6) {
    uVar2 = (ulong)bVar6;
  }
  if (uVar2 == 0) {
    *(undefined1 *)((long)param_1 + 0x17) = 0;
    *(undefined1 *)param_1 = 0;
    return;
  }
  if ((DAT_0a48e012 & 1) == 0) {
    DAT_0a48e008 = s__chatroo_085051b0._0_8_;
    DAT_0a48e010 = 0x6d;
    DAT_0a48e012 = 1;
  }
  lVar17 = *param_2;
  plVar3 = (long *)lVar17;
  if (-1 < (char)bVar6) {
    plVar3 = param_2;
  }
  sVar13 = _strlen((char *)&DAT_0a48e008);
  if (sVar13 == 0) {
LAB_04981214:
    if (-1 < (char)bVar6) {
      lVar17 = *param_2;
      param_1[1] = param_2[1];
      *param_1 = lVar17;
      param_1[2] = param_2[2];
      return;
    }
    FUN_00018d20(param_1,lVar17,uVar20);
    return;
  }
  pvVar1 = (void *)((long)plVar3 + uVar2);
  if ((long)sVar13 <= (long)uVar2) {
    cVar10 = (char)DAT_0a48e008;
    plVar14 = plVar3;
    uVar18 = uVar2;
    do {
      if ((0xfffffffffffffffe < uVar18 - sVar13) ||
         (pvVar15 = _memchr(plVar14,(int)cVar10,(uVar18 - sVar13) + 1), pvVar15 == (void *)0x0))
      break;
      iVar12 = _memcmp(pvVar15,&DAT_0a48e008,sVar13);
      if (iVar12 == 0) {
        if ((pvVar15 != pvVar1) && ((long)pvVar15 - (long)plVar3 != -1)) goto LAB_04981214;
        break;
      }
      plVar14 = (long *)((long)pvVar15 + 1);
      uVar18 = (long)pvVar1 - (long)plVar14;
    } while ((long)sVar13 <= (long)uVar18);
  }
  if ((DAT_0a48e020 & 1) == 0) {
    DAT_0a48e018[0] = s__openim_08a76140[0];
    DAT_0a48e018[1] = s__openim_08a76140[1];
    DAT_0a48e018[2] = s__openim_08a76140[2];
    DAT_0a48e018[3] = s__openim_08a76140[3];
    DAT_0a48e018[4] = s__openim_08a76140[4];
    DAT_0a48e018[5] = s__openim_08a76140[5];
    DAT_0a48e018[6] = s__openim_08a76140[6];
    DAT_0a48e018[7] = s__openim_08a76140[7];
    DAT_0a48e020 = 1;
  }
  sVar13 = _strlen(DAT_0a48e018);
  if (sVar13 == 0) goto LAB_04981214;
  if ((long)sVar13 <= (long)uVar2) {
    cVar10 = DAT_0a48e018[0];
    plVar14 = plVar3;
    uVar18 = uVar2;
    do {
      if ((0xfffffffffffffffe < uVar18 - sVar13) ||
         (pvVar15 = _memchr(plVar14,(int)cVar10,(uVar18 - sVar13) + 1), pvVar15 == (void *)0x0))
      break;
      iVar12 = _memcmp(pvVar15,DAT_0a48e018,sVar13);
      if (iVar12 == 0) {
        if ((pvVar15 != pvVar1) && ((long)pvVar15 - (long)plVar3 != -1)) goto LAB_04981214;
        break;
      }
      plVar14 = (long *)((long)pvVar15 + 1);
      uVar18 = (long)pvVar1 - (long)plVar14;
    } while ((long)sVar13 <= (long)uVar18);
  }
  if ((DAT_0a48e030 & 1) == 0) {
    DAT_0a48e028[0] = s__weclaw_08a76148[0];
    DAT_0a48e028[1] = s__weclaw_08a76148[1];
    DAT_0a48e028[2] = s__weclaw_08a76148[2];
    DAT_0a48e028[3] = s__weclaw_08a76148[3];
    DAT_0a48e028[4] = s__weclaw_08a76148[4];
    DAT_0a48e028[5] = s__weclaw_08a76148[5];
    DAT_0a48e028[6] = s__weclaw_08a76148[6];
    DAT_0a48e028[7] = s__weclaw_08a76148[7];
    DAT_0a48e030 = 1;
  }
  sVar13 = _strlen(DAT_0a48e028);
  if (sVar13 == 0) goto LAB_04981214;
  if ((long)sVar13 <= (long)uVar2) {
    cVar10 = DAT_0a48e028[0];
    plVar14 = plVar3;
    uVar18 = uVar2;
    do {
      if ((0xfffffffffffffffe < uVar18 - sVar13) ||
         (pvVar15 = _memchr(plVar14,(int)cVar10,(uVar18 - sVar13) + 1), pvVar15 == (void *)0x0))
      break;
      iVar12 = _memcmp(pvVar15,DAT_0a48e028,sVar13);
      if (iVar12 == 0) {
        if ((pvVar15 != pvVar1) && ((long)pvVar15 - (long)plVar3 != -1)) goto LAB_04981214;
        break;
      }
      plVar14 = (long *)((long)pvVar15 + 1);
      uVar18 = (long)pvVar1 - (long)plVar14;
    } while ((long)sVar13 <= (long)uVar18);
  }
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = (short *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_00068fa8(&local_78,plVar3,uVar2);
  psVar4 = DAT_0a48dff0;
  puVar7 = _DAT_0a48dff8;
  if (-1 < (char)DAT_0a48e007) {
    psVar4 = (short *)&DAT_0a48dff0;
    puVar7 = (undefined1 *)(ulong)DAT_0a48e007;
  }
  puVar19 = (undefined1 *)(long)(char)local_68._7_1_;
  if ((long)puVar19 < 0) {
    if (puVar7 == (undefined1 *)0xffffffffffffffff) goto LAB_04981274;
    pppppppsVar8 = local_78;
    puVar5 = local_70;
    puVar9 = local_70;
    if (puVar7 <= local_70) {
      puVar5 = puVar7;
      puVar9 = puVar7;
    }
  }
  else {
    if (puVar7 == (undefined1 *)0xffffffffffffffff) {
LAB_04981274:
      FUN_04981acc(&local_78);
                    /* WARNING: Does not return */
      pcVar11 = (code *)SoftwareBreakpoint(1,0x4981280);
      (*pcVar11)();
    }
    puVar5 = puVar19;
    if (puVar7 <= puVar19) {
      puVar5 = puVar7;
    }
    pppppppsVar8 = (short *******)&local_78;
    puVar9 = puVar5;
  }
  for (; puVar5 != (undefined1 *)0x0; puVar5 = puVar5 + -1) {
    if (*psVar4 != *(short *)pppppppsVar8) goto LAB_04981188;
    psVar4 = psVar4 + 1;
    pppppppsVar8 = (short *******)((long)pppppppsVar8 + 2);
  }
  if (puVar9 == puVar7) {
    puVar5 = local_70;
    if (-1 < (long)local_68) {
      puVar5 = puVar19;
    }
    if ((undefined1 *)(long)((int)puVar7 + 8) < puVar5) {
      iVar12 = (int)puVar7 + 4;
      iVar16 = 4;
      goto LAB_049811c4;
    }
  }
LAB_04981188:
  if ((long)local_68 < 0) {
    puVar19 = local_70;
    if ((undefined1 *)0x2 < local_70) goto LAB_049811b4;
  }
  else if (2 < local_68._7_1_) {
LAB_049811b4:
    iVar12 = 1;
    iVar16 = iVar12;
    if ((undefined1 *)0x4 < puVar19) {
      iVar12 = 2;
      iVar16 = iVar12;
    }
    goto LAB_049811c4;
  }
  iVar12 = 0;
  iVar16 = 0;
LAB_049811c4:
  FUN_049812a4(param_1,&local_78,iVar12,iVar16);
  if (-1 < (long)local_68) {
    return;
  }
  __ZdlPvm(local_78,(long)local_68 << 1);
  return;
}


