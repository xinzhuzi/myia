// Ghidra inferred pseudocode; requested=0x5643aa4
// entry=05643aa4 end=05643b4f

void FUN_05643aa4(undefined8 *param_1)

{
  undefined8 *puVar1;
  undefined8 *puVar2;
  
  puVar2 = (undefined8 *)__Znwm(0x2d0);
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = &PTR_FUN_09f18548;
  puVar1 = puVar2 + 3;
  _bzero(puVar1,0x2b8);
  FUN_0562a69c(puVar1);
  puVar2[8] = 0;
  puVar2[3] = &PTR_FUN_09f18598;
  *(undefined1 *)(puVar2 + 6) = 0;
  puVar2[9] = 0;
  puVar2[7] = puVar2 + 8;
  FUN_056455cc(puVar2 + 10);
  puVar2[3] = &PTR_FUN_09f1c788;
  puVar2[10] = &PTR_FUN_09f1c7e8;
  puVar2[0x59] = 0;
  puVar2[0x58] = 0;
  puVar2[0x57] = puVar2 + 0x58;
  *param_1 = puVar1;
  param_1[1] = puVar2;
  return;
}


