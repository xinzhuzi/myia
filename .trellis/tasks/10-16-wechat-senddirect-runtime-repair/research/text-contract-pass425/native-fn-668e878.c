// Ghidra inferred pseudocode; requested=0x668e878
// entry=0668e878 end=0668ed17

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long FUN_0668e878(long param_1)

{
  char cVar1;
  size_t sVar2;
  undefined8 *******pppppppuVar3;
  undefined8 ******ppppppuVar4;
  undefined8 *******pppppppuVar5;
  ulong uVar6;
  undefined8 ******ppppppuVar7;
  undefined8 *****local_f0;
  size_t local_e8;
  undefined8 local_e0;
  undefined8 ******local_d8;
  size_t local_d0;
  undefined8 local_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  undefined1 *local_60;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  
  ppppppuVar4 = &local_f0;
  ppppppuVar7 = &local_f0;
  pppppppuVar5 = (undefined8 *******)&local_f0;
  if (*(int *)(param_1 + 0xc0) != 2) {
    if ((*(int *)(param_1 + 0xc0) == 1) && (*(long *)(param_1 + 0xb8) != 0)) {
      uVar6 = (ulong)*(char *)(param_1 + 0x4f);
      if ((long)uVar6 < 0) {
        uVar6 = *(ulong *)(param_1 + 0x40);
      }
      if (DAT_0a12d0f8 < uVar6) {
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
                  (param_1 + 0x38,DAT_0a12d0f8,0);
      }
      FUN_0668e058(*(undefined8 *)(param_1 + 0xb8),param_1 + 0x20);
    }
    if (*(char *)(param_1 + 0x97) < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x80),*(ulong *)(param_1 + 0x90) & 0x7fffffffffffffff);
      cVar1 = *(char *)(param_1 + 0x7f);
    }
    else {
      cVar1 = *(char *)(param_1 + 0x7f);
    }
    if (cVar1 < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x68),*(ulong *)(param_1 + 0x78) & 0x7fffffffffffffff);
      cVar1 = *(char *)(param_1 + 0x67);
    }
    else {
      cVar1 = *(char *)(param_1 + 0x67);
    }
    if (cVar1 < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x50),*(ulong *)(param_1 + 0x60) & 0x7fffffffffffffff);
      cVar1 = *(char *)(param_1 + 0x4f);
    }
    else {
      cVar1 = *(char *)(param_1 + 0x4f);
    }
    if (cVar1 < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x38),*(ulong *)(param_1 + 0x48) & 0x7fffffffffffffff);
    }
    return param_1;
  }
  if (*(long *)(param_1 + 0xb8) != 0) {
    uVar6 = (ulong)*(char *)(param_1 + 0x4f);
    if ((long)uVar6 < 0) {
      uVar6 = *(ulong *)(param_1 + 0x40);
    }
    if (DAT_0a12d0f8 < uVar6) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
                (param_1 + 0x38,DAT_0a12d0f8,0);
    }
    FUN_0668e058(*(undefined8 *)(param_1 + 0xb8),param_1 + 0x20);
  }
  local_58 = 0;
  uStack_50 = 0;
  local_48 = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7reserveEm(&local_58,0x400);
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a518d01 & 1) == 0) {
    _DAT_0a518cc8 = CONCAT44((int)DAT_09688318,(int)DAT_09688310);
    uRam000000000a518cd0 = CONCAT44((int)DAT_09688328,(int)DAT_09688320);
    _DAT_0a518cd8 = CONCAT44((int)DAT_09688338,(int)DAT_09688330);
    uRam000000000a518ce0 = CONCAT44((int)DAT_09688340,(int)DAT_08b612c8);
    _DAT_0a518ce8 = CONCAT44((int)DAT_09688350,(int)DAT_09688348);
    uRam000000000a518cf0 = CONCAT44((int)DAT_09688358,(int)DAT_08495970);
    DAT_0a518cf8 = CONCAT44((int)DAT_09688368,(int)DAT_09688360);
    DAT_0a518d00 = 0;
    DAT_0a518d01 = 1;
  }
  sVar2 = _strlen(&DAT_0a518cc8);
  if (0x7ffffffffffffff7 < sVar2) {
    pppppppuVar5 = &local_d8;
    goto LAB_0668ed14;
  }
  if (sVar2 < 0x17) {
    local_c8 = CONCAT17((char)sVar2,(undefined7)local_c8);
    pppppppuVar3 = &local_d8;
    if (sVar2 != 0) goto LAB_0668ea94;
  }
  else {
    uVar6 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar6 = (sVar2 | 7) + 1;
    }
    pppppppuVar3 = (undefined8 *******)__Znwm(uVar6);
    local_c8 = uVar6 | 0x8000000000000000;
    local_d8 = pppppppuVar3;
    local_d0 = sVar2;
LAB_0668ea94:
    _memcpy(pppppppuVar3,&DAT_0a518cc8,sVar2);
  }
  *(undefined1 *)((long)pppppppuVar3 + sVar2) = 0;
  if ((DAT_0a518d23 & 1) == 0) {
    uRam000000000a518d18 = _UNK_09688538;
    _DAT_0a518d10 = _DAT_09688530;
    DAT_0a518d20 = 0x7d64;
    DAT_0a518d22 = 0;
    DAT_0a518d23 = 1;
  }
  sVar2 = _strlen(&DAT_0a518d10);
  if (0x7ffffffffffffff7 < sVar2) {
LAB_0668ed14:
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(pppppppuVar5);
  }
  if (sVar2 < 0x17) {
    local_e0 = CONCAT17((char)sVar2,(undefined7)local_e0);
    if (sVar2 == 0) goto LAB_0668eb4c;
  }
  else {
    uVar6 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar6 = (sVar2 | 7) + 1;
    }
    ppppppuVar4 = (undefined8 ******)__Znwm(uVar6);
    local_e0 = uVar6 | 0x8000000000000000;
    local_f0 = ppppppuVar4;
    local_e8 = sVar2;
  }
  _memcpy(ppppppuVar4,&DAT_0a518d10,sVar2);
  ppppppuVar7 = ppppppuVar4;
LAB_0668eb4c:
  *(undefined1 *)((long)ppppppuVar7 + sVar2) = 0;
  FUN_0668a544(&local_c0,&local_d8,&local_f0);
  if ((long)local_e0 < 0) {
    __ZdlPvm(local_f0,local_e0 & 0x7fffffffffffffff);
  }
  if ((long)local_c8 < 0) {
    __ZdlPvm(local_d8,local_c8 & 0x7fffffffffffffff);
  }
  FUN_0668cd88(&local_c0,param_1 + 0x20,&local_58);
                    /* WARNING: Subroutine does not return */
  FUN_00023b4c(&local_58);
}


