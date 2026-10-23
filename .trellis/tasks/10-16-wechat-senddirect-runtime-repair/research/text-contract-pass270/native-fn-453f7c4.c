// Ghidra inferred pseudocode; requested=0x453f7c4
// entry=0453f7c4 end=0453f897

void FUN_0453f7c4(undefined8 param_1,long param_2)

{
  undefined8 *puVar1;
  int iVar2;
  undefined4 local_80;
  undefined4 uStack_7c;
  long lStack_78;
  undefined8 *puStack_70;
  long local_68;
  undefined4 local_60;
  undefined4 uStack_5c;
  undefined1 auStack_58 [16];
  undefined1 *puStack_48;
  undefined1 *puStack_40;
  undefined1 *local_38;
  undefined1 *local_30;
  
  iVar2 = thunk_FUN_05e1d97c(*(undefined4 *)(param_2 + 0xc));
  if (iVar2 != 0) {
    local_30 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
    auStack_58._8_8_ = &SUB_aaaaaaaaaaaaaaaa;
    local_38 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_40 = &SUB_aaaaaaaaaaaaaaaa;
    auStack_58._0_8_ = &SUB_aaaaaaaaaaaaaaaa;
    _local_80 = CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_2 + 0xc));
    lStack_78 = *(long *)(param_2 + 0x30);
    if (-1 < *(char *)(param_2 + 0x47)) {
      lStack_78 = param_2 + 0x30;
    }
    puStack_70 = *(undefined8 **)(param_2 + 0x60);
    if (-1 < *(char *)(param_2 + 0x77)) {
      puStack_70 = (undefined8 *)(param_2 + 0x60);
    }
    local_68 = *(long *)(param_2 + 0x48);
    if (-1 < *(char *)(param_2 + 0x5f)) {
      local_68 = param_2 + 0x48;
    }
    _local_60 = CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_2 + 0x78));
    _gettimeofday((timeval *)auStack_58,(void *)0x0);
    puStack_40 = *(undefined1 **)(param_2 + 0x88);
    puStack_48 = *(undefined1 **)(param_2 + 0x80);
    local_38 = (undefined1 *)0xffffffffffffffff;
    puVar1 = *(undefined8 **)(param_2 + 0x18);
    if (-1 < *(char *)(param_2 + 0x2f)) {
      puVar1 = (undefined8 *)(param_2 + 0x18);
    }
    thunk_FUN_05e1d9b8(&local_80,puVar1);
  }
  return;
}


