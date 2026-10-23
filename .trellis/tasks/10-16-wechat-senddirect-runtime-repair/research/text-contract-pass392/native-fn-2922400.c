// Ghidra inferred pseudocode; requested=0x2922400
// entry=02922400 end=029227d7

void FUN_02922400(undefined8 *param_1,undefined8 *param_2,undefined8 param_3)

{
  size_t sVar1;
  size_t sVar2;
  ulong uVar3;
  ulong uVar4;
  byte bVar5;
  char cVar6;
  char *******pppppppcVar7;
  ulong uVar8;
  int iVar9;
  undefined8 *puVar10;
  undefined8 *puVar11;
  void *pvVar12;
  undefined8 *puVar13;
  ulong uVar14;
  long lVar15;
  undefined8 local_b8 [2];
  undefined7 local_a8;
  char cStack_a1;
  char ******local_a0;
  size_t sStack_98;
  ulong local_90;
  char ******local_80;
  size_t sStack_78;
  ulong local_70;
  
  if ((DAT_0a3a61b0 & 1) == 0) {
    DAT_0a3a61ae = 0x3c;
    DAT_0a3a61b0 = 1;
  }
  __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
            (&local_a0,&DAT_0a3a61ae,param_3);
  if ((DAT_0a3a61b3 & 1) == 0) {
    DAT_0a3a61b1 = 0x3e;
    DAT_0a3a61b3 = 1;
  }
  puVar10 = (undefined8 *)
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                      (&local_a0,&DAT_0a3a61b1);
  sStack_78 = puVar10[1];
  local_80 = (char ******)*puVar10;
  local_70 = puVar10[2];
  puVar10[1] = 0;
  puVar10[2] = 0;
  *puVar10 = 0;
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,local_90 & 0x7fffffffffffffff);
  }
  if ((DAT_0a3a61b7 & 1) == 0) {
    DAT_0a3a61b4 = 0x2f3c;
    DAT_0a3a61b6 = 0;
    DAT_0a3a61b7 = 1;
  }
  __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
            (local_b8,&DAT_0a3a61b4,param_3);
  if ((DAT_0a3a61b3 & 1) == 0) {
    DAT_0a3a61b1 = 0x3e;
    DAT_0a3a61b3 = 1;
  }
  puVar10 = (undefined8 *)
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                      (local_b8,&DAT_0a3a61b1);
  sStack_98 = puVar10[1];
  local_a0 = (char ******)*puVar10;
  local_90 = puVar10[2];
  puVar10[1] = 0;
  puVar10[2] = 0;
  *puVar10 = 0;
  if (cStack_a1 < '\0') {
    __ZdlPvm(local_b8[0],CONCAT17(cStack_a1,local_a8) & 0x7fffffffffffffff);
  }
  bVar5 = *(byte *)((long)param_2 + 0x17);
  puVar10 = (undefined8 *)*param_2;
  uVar4 = param_2[1];
  uVar3 = uVar4;
  puVar13 = puVar10;
  if (-1 < (char)bVar5) {
    uVar3 = (ulong)bVar5;
    puVar13 = param_2;
  }
  sVar1 = sStack_78;
  pppppppcVar7 = (char *******)local_80;
  if (-1 < (long)local_70) {
    sVar1 = local_70 >> 0x38;
    pppppppcVar7 = &local_80;
  }
  if (sVar1 == 0) {
    lVar15 = 0;
LAB_02922600:
    sVar2 = sStack_98;
    pppppppcVar7 = (char *******)local_a0;
    if (-1 < (long)local_90) {
      sVar2 = local_90 >> 0x38;
      pppppppcVar7 = &local_a0;
    }
    uVar14 = lVar15 + sVar1;
    lVar15 = uVar3 - uVar14;
    if (uVar14 <= uVar3) {
      uVar8 = uVar14;
      if (sVar2 == 0) {
joined_r0x02922758:
        if (uVar8 != 0xffffffffffffffff) {
          if (-1 < (char)bVar5) {
            puVar10 = param_2;
            uVar4 = (ulong)bVar5;
          }
          if (uVar4 < uVar14) {
                    /* WARNING: Subroutine does not return */
            FUN_0020edd0(param_1);
          }
          uVar3 = uVar4 - uVar14;
          if (uVar8 - uVar14 <= uVar4 - uVar14) {
            uVar3 = uVar8 - uVar14;
          }
          if (0x7ffffffffffffff7 < uVar3) {
                    /* WARNING: Subroutine does not return */
            FUN_00018d9c(param_1);
          }
          if (uVar3 < 0x17) {
            *(char *)((long)param_1 + 0x17) = (char)uVar3;
            puVar13 = param_1;
            if (uVar3 != 0) goto LAB_02922730;
          }
          else {
            uVar4 = 0x19;
            if ((uVar3 | 7) != 0x17) {
              uVar4 = (uVar3 | 7) + 1;
            }
            puVar13 = (undefined8 *)__Znwm(uVar4);
            param_1[1] = uVar3;
            param_1[2] = uVar4 | 0x8000000000000000;
            *param_1 = puVar13;
LAB_02922730:
            _memmove(puVar13,(void *)((long)puVar10 + uVar14),uVar3);
            param_1 = puVar13;
          }
          param_1 = (undefined8 *)((long)param_1 + uVar3);
          goto LAB_02922764;
        }
      }
      else if ((long)sVar2 <= lVar15) {
        pvVar12 = (void *)((long)puVar13 + uVar14);
        cVar6 = *(char *)pppppppcVar7;
        do {
          if ((0xfffffffffffffffe < lVar15 - sVar2) ||
             (pvVar12 = _memchr(pvVar12,(int)cVar6,(lVar15 - sVar2) + 1), pvVar12 == (void *)0x0))
          break;
          iVar9 = _memcmp(pvVar12,pppppppcVar7,sVar2);
          if (iVar9 == 0) {
            if (pvVar12 != (void *)((long)puVar13 + uVar3)) {
              uVar8 = (long)pvVar12 - (long)puVar13;
              goto joined_r0x02922758;
            }
            break;
          }
          pvVar12 = (void *)((long)pvVar12 + 1);
          lVar15 = (long)((long)puVar13 + uVar3) - (long)pvVar12;
        } while ((long)sVar2 <= lVar15);
      }
    }
  }
  else if ((long)sVar1 <= (long)uVar3) {
    cVar6 = *(char *)pppppppcVar7;
    puVar11 = puVar13;
    uVar14 = uVar3;
    do {
      if ((0xfffffffffffffffe < uVar14 - sVar1) ||
         (pvVar12 = _memchr(puVar11,(int)cVar6,(uVar14 - sVar1) + 1), pvVar12 == (void *)0x0))
      break;
      iVar9 = _memcmp(pvVar12,pppppppcVar7,sVar1);
      if (iVar9 == 0) {
        if ((pvVar12 != (void *)((long)puVar13 + uVar3)) &&
           (lVar15 = (long)pvVar12 - (long)puVar13, lVar15 != -1)) goto LAB_02922600;
        break;
      }
      puVar11 = (undefined8 *)((long)pvVar12 + 1);
      uVar14 = (long)((long)puVar13 + uVar3) - (long)puVar11;
    } while ((long)sVar1 <= (long)uVar14);
  }
  *(undefined1 *)((long)param_1 + 0x17) = 0;
LAB_02922764:
  *(undefined1 *)param_1 = 0;
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,local_90 & 0x7fffffffffffffff);
  }
  if ((long)local_70 < 0) {
    __ZdlPvm(local_80,local_70 & 0x7fffffffffffffff);
  }
  return;
}


