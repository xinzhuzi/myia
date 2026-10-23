// Ghidra inferred pseudocode; requested=0x6684444
// entry=06684444 end=06684527

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_06684444(void)

{
  ulong uVar1;
  undefined8 local_38 [2];
  undefined7 local_28;
  char cStack_21;
  
  if (((DAT_0a518848 & 1) == 0) && (uVar1 = FUN_0713404c(local_38), (uVar1 & 1) == 0)) {
    FUN_00255b9c(local_38,&DAT_0a518860);
    FUN_066819f4(&DAT_0a518708,local_38);
    DAT_0a518700 = &PTR_FUN_09fb2f78;
    uRam000000000a518808 = 0;
    _DAT_0a518800 = 0;
    uRam000000000a518818 = 0;
    _DAT_0a518810 = 0;
    uRam000000000a518828 = 0;
    _DAT_0a518820 = 0;
    DAT_0a518830 = 0;
    DAT_0a518838 = 0x80000000ffffffff;
    DAT_0a518840 = 2;
    DAT_0a5187f8 = 0;
    if (cStack_21 < '\0') {
      __ZdlPvm(local_38[0],CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
    }
    ___cxa_atexit(FUN_06684558,&DAT_0a518700,0);
    ___cxa_guard_release(&DAT_0a518848);
  }
  return &DAT_0a518700;
}


