// Ghidra inferred pseudocode; requested=0x335fdd8
// entry=0335fdd8 end=0335fec7

void FUN_0335fdd8(undefined8 *param_1,long param_2)

{
  byte bVar1;
  long *plVar2;
  undefined1 local_2c8 [632];
  byte local_50;
  long *local_48;
  
  local_2c8[0] = 0;
  local_50 = 0;
  bVar1 = *(byte *)(param_2 + 0x278);
  if (bVar1 == 1) {
    FUN_02a0cf30(local_2c8);
  }
  local_50 = bVar1 == 1;
  local_48 = (long *)__Znwm(0x298);
  *local_48 = (long)&PTR_FUN_09df3c00;
  plVar2 = local_48 + 1;
  *(undefined1 *)plVar2 = 0;
  *(undefined1 *)(local_48 + 0x50) = 0;
  if ((bVar1 & 1) == 0) {
    local_48[0x51] = (long)&PTR_DAT_09df3cd8;
    local_48[0x52] = (long)plVar2;
  }
  else {
    FUN_02a0cf30(plVar2,local_2c8);
    *(undefined1 *)(local_48 + 0x50) = 1;
    local_48[0x51] = (long)&PTR_DAT_09df3cd8;
    local_48[0x52] = (long)plVar2;
    if ((local_50 & 1) != 0) {
      FUN_00ac6290(local_2c8);
    }
  }
  FUN_066696dc(*param_1,&local_48);
  if (local_48 != (long *)0x0) {
    (**(code **)(*local_48 + 8))();
  }
  return;
}


