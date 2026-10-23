// Ghidra inferred pseudocode; requested=0x5699278
// entry=05699278 end=056992d7

undefined8 * FUN_05699278(undefined8 *param_1)

{
  long lVar1;
  
  lVar1 = FUN_0569fd80();
  *(undefined8 *)(lVar1 + 0x1b0) = 0;
  *(undefined8 *)(lVar1 + 0x198) = 0;
  *(undefined8 *)(lVar1 + 400) = 0;
  *(undefined8 *)(lVar1 + 0x1a8) = 0;
  *(undefined8 *)(lVar1 + 0x1a0) = 0;
  *(undefined8 *)(lVar1 + 0x188) = 0;
  *(undefined8 *)(lVar1 + 0x180) = 0;
  FUN_0562a69c(lVar1 + 0x180);
  *(undefined1 *)(param_1 + 0x33) = 0;
  param_1[0x35] = 0;
  param_1[0x36] = 0;
  param_1[0x34] = param_1 + 0x35;
  *param_1 = &PTR_FUN_09f1cbc0;
  param_1[0x30] = &PTR_FUN_09f1cc48;
  return param_1;
}


