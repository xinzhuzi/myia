// Ghidra inferred pseudocode; requested=0x4eafe18
// entry=04eafe18 end=04eb0363

/* WARNING: Type propagation algorithm not settling */

int FUN_04eafe18(long param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  uint uVar5;
  uint uVar6;
  long lVar7;
  byte bVar8;
  long lVar9;
  
  uVar6 = *(uint *)(param_1 + 0x74);
  if ((uVar6 & 0xff) == 0) {
    iVar2 = 0;
  }
  else {
    if ((uVar6 & 1) == 0) {
      iVar2 = 0;
    }
    else if (*(uint *)(param_1 + 8) < 0x80) {
      iVar2 = 2;
    }
    else {
      iVar2 = FUN_0571a3d8();
      uVar6 = *(uint *)(param_1 + 0x74);
      iVar2 = iVar2 + 1;
    }
    if ((uVar6 >> 1 & 1) != 0) {
      if (*(uint *)(param_1 + 0xc) < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8();
        uVar6 = *(uint *)(param_1 + 0x74);
      }
      iVar2 = iVar2 + iVar3 + 1;
    }
    if ((uVar6 >> 2 & 1) != 0) {
      lVar7 = *(long *)(param_1 + 0x10);
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a51f728 + 0x10);
      }
      uVar4 = FUN_04ea740c(lVar7);
      if ((uint)uVar4 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar4);
      }
      iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
      uVar6 = *(uint *)(param_1 + 0x74);
    }
    if ((uVar6 >> 3 & 1) != 0) {
      lVar7 = *(long *)(param_1 + 0x18);
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a51f728 + 0x18);
      }
      uVar4 = FUN_04ea80b8(lVar7);
      if ((uint)uVar4 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar4);
      }
      iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
      uVar6 = *(uint *)(param_1 + 0x74);
    }
    if ((uVar6 >> 4 & 1) != 0) {
      lVar7 = *(long *)(param_1 + 0x20);
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a51f728 + 0x20);
        bVar8 = *(byte *)(lVar7 + 0x18);
        if (bVar8 != 0) goto LAB_04eaff70;
LAB_04eaff94:
        uVar6 = 0;
        *(undefined4 *)(lVar7 + 0x14) = 0;
        iVar3 = 1;
      }
      else {
        bVar8 = *(byte *)(lVar7 + 0x18);
        if (bVar8 == 0) goto LAB_04eaff94;
LAB_04eaff70:
        if ((bVar8 & 1) == 0) {
          uVar6 = 0;
joined_r0x04eaffb4:
          if ((bVar8 >> 1 & 1) != 0) {
LAB_04eaffcc:
            lVar9 = *(long *)(lVar7 + 8);
            bVar8 = *(byte *)(lVar9 + 0x17);
            uVar5 = (uint)*(undefined8 *)(lVar9 + 8);
            uVar1 = uVar5;
            if (-1 < (char)bVar8) {
              uVar1 = (uint)bVar8;
            }
            if (uVar1 < 0x80) {
              iVar3 = 1;
            }
            else {
              iVar3 = FUN_0571a3d8();
              bVar8 = *(byte *)(lVar9 + 0x17);
              uVar5 = (uint)*(undefined8 *)(lVar9 + 8);
            }
            if (-1 < (char)bVar8) {
              uVar5 = (uint)bVar8;
            }
            uVar6 = uVar6 + iVar3 + uVar5 + 1;
          }
        }
        else {
          if (*(uint *)(lVar7 + 0x10) < 0x80) {
            uVar6 = 2;
            goto joined_r0x04eaffb4;
          }
          iVar3 = FUN_0571a3d8();
          uVar6 = iVar3 + 1;
          if ((*(uint *)(lVar7 + 0x18) >> 1 & 1) != 0) goto LAB_04eaffcc;
        }
        *(uint *)(lVar7 + 0x14) = uVar6;
        if (uVar6 < 0x80) {
          iVar3 = 1;
        }
        else {
          iVar3 = FUN_0571a3d8(uVar6);
        }
      }
      iVar2 = iVar2 + uVar6 + iVar3 + 1;
      uVar6 = *(uint *)(param_1 + 0x74);
    }
    if ((uVar6 >> 5 & 1) != 0) {
      lVar7 = *(long *)(param_1 + 0x28);
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a51f728 + 0x28);
      }
      uVar4 = FUN_04eaa60c(lVar7);
      if ((uint)uVar4 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar4);
      }
      iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
      uVar6 = *(uint *)(param_1 + 0x74);
    }
    if ((uVar6 >> 6 & 1) != 0) {
      lVar7 = *(long *)(param_1 + 0x30);
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a51f728 + 0x30);
      }
      uVar4 = FUN_04ea931c(lVar7);
      if ((uint)uVar4 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar4);
      }
      iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
      uVar6 = *(uint *)(param_1 + 0x74);
    }
    if ((uVar6 >> 7 & 1) != 0) {
      lVar7 = *(long *)(param_1 + 0x38);
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a51f728 + 0x38);
      }
      uVar4 = FUN_04eab3bc(lVar7);
      if ((uint)uVar4 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar4);
      }
      iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
      uVar6 = *(uint *)(param_1 + 0x74);
    }
  }
  if ((uVar6 & 0xff00) == 0) goto LAB_04eb0328;
  if ((uVar6 >> 8 & 1) != 0) {
    lVar7 = *(long *)(param_1 + 0x40);
    if (lVar7 == 0) {
      lVar7 = *(long *)(DAT_0a51f728 + 0x40);
      if ((*(byte *)(lVar7 + 0x14) & 1) == 0) goto LAB_04eb0154;
LAB_04eb0178:
      lVar9 = *(long *)(lVar7 + 8);
      bVar8 = *(byte *)(lVar9 + 0x17);
      uVar6 = (uint)*(undefined8 *)(lVar9 + 8);
      uVar1 = uVar6;
      if (-1 < (char)bVar8) {
        uVar1 = (uint)bVar8;
      }
      if (uVar1 < 0x80) {
        iVar3 = 2;
      }
      else {
        iVar3 = FUN_0571a3d8();
        bVar8 = *(byte *)(lVar9 + 0x17);
        uVar6 = (uint)*(undefined8 *)(lVar9 + 8);
        iVar3 = iVar3 + 1;
      }
      if (-1 < (char)bVar8) {
        uVar6 = (uint)bVar8;
      }
      uVar6 = iVar3 + uVar6;
      *(uint *)(lVar7 + 0x10) = uVar6;
      if (uVar6 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar6);
      }
    }
    else {
      if ((*(byte *)(lVar7 + 0x14) & 1) != 0) goto LAB_04eb0178;
LAB_04eb0154:
      uVar6 = 0;
      *(undefined4 *)(lVar7 + 0x10) = 0;
      iVar3 = 1;
    }
    iVar2 = iVar2 + uVar6 + iVar3 + 1;
    uVar6 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar6 >> 9 & 1) != 0) {
    lVar7 = *(long *)(param_1 + 0x48);
    if (lVar7 == 0) {
      lVar7 = *(long *)(DAT_0a51f728 + 0x48);
      if ((*(byte *)(lVar7 + 0x10) & 1) == 0) goto LAB_04eb0204;
LAB_04eb0220:
      if ((int)*(uint *)(lVar7 + 8) < 0) {
        uVar6 = 0xb;
        goto LAB_04eb023c;
      }
      if (*(uint *)(lVar7 + 8) < 0x80) {
        uVar6 = 2;
        goto LAB_04eb023c;
      }
      iVar3 = FUN_0571a3d8();
      uVar6 = iVar3 + 1;
      *(uint *)(lVar7 + 0xc) = uVar6;
      if (uVar6 < 0x80) goto LAB_04eb0240;
      iVar3 = FUN_0571a3d8(uVar6);
    }
    else {
      if ((*(byte *)(lVar7 + 0x10) & 1) != 0) goto LAB_04eb0220;
LAB_04eb0204:
      uVar6 = 0;
LAB_04eb023c:
      *(uint *)(lVar7 + 0xc) = uVar6;
LAB_04eb0240:
      iVar3 = 1;
    }
    iVar2 = iVar2 + uVar6 + iVar3 + 1;
    uVar6 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar6 >> 10 & 1) != 0) {
    iVar3 = FUN_05ab36b8(*(undefined8 *)(param_1 + 0x50));
    iVar2 = iVar2 + iVar3 + 1;
    uVar6 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar6 >> 0xb & 1) != 0) {
    lVar7 = *(long *)(param_1 + 0x58);
    if (lVar7 == 0) {
      lVar7 = *(long *)(DAT_0a51f728 + 0x58);
    }
    uVar4 = FUN_04ead4d8(lVar7);
    if ((uint)uVar4 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8(uVar4);
    }
    iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
    uVar6 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar6 >> 0xc & 1) != 0) {
    lVar7 = *(long *)(param_1 + 0x60);
    if (lVar7 == 0) {
      lVar7 = *(long *)(DAT_0a51f728 + 0x60);
    }
    uVar6 = *(uint *)(lVar7 + 0x10);
    iVar3 = 0;
    if ((uVar6 & 0xff) != 0) {
      iVar3 = (uVar6 & 1) * 2 + (uVar6 & 2);
    }
    *(int *)(lVar7 + 0xc) = iVar3;
    iVar2 = iVar2 + iVar3 + 2;
    uVar6 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar6 >> 0xd & 1) != 0) {
    lVar7 = *(long *)(param_1 + 0x68);
    if (lVar7 == 0) {
      lVar7 = *(long *)(DAT_0a51f728 + 0x68);
    }
    iVar3 = 0;
    if ((*(uint *)(lVar7 + 0x10) & 0xff) != 0) {
      iVar3 = (*(uint *)(lVar7 + 0x10) & 1) << 1;
    }
    *(int *)(lVar7 + 0xc) = iVar3;
    iVar2 = iVar2 + iVar3 + 2;
  }
LAB_04eb0328:
  *(int *)(param_1 + 0x70) = iVar2;
  return iVar2;
}


