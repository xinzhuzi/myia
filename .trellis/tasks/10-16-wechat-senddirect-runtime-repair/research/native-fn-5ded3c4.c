// Ghidra inferred pseudocode; requested=0x5ded3c4
// entry=05ded3c4 end=05ded4eb

void FUN_05ded3c4(undefined8 *param_1,ulong param_2)

{
  ulong uVar1;
  void *pvVar2;
  ulong uVar3;
  size_t sVar4;
  
  if ((ulong)param_1[3] < param_2) {
    uVar3 = param_1[4];
    uVar1 = 0;
    if (uVar3 != 0) {
      uVar1 = ((param_2 + uVar3) - 1) / uVar3;
    }
    sVar4 = uVar1 * uVar3;
    pvVar2 = _realloc((void *)*param_1,sVar4);
    if (pvVar2 == (void *)0x0) {
      FUN_05ded150("autobuffer.cc",0x126,"__FitSize","p",
                   "_len=%llu, m_nMallocUnitSize=%llu, nMallocSize=%llu, m_nCapacity=%llu");
      _free((void *)*param_1);
      sVar4 = 0;
      *param_1 = 0;
    }
    else {
      *param_1 = pvVar2;
      if (0x3200000 < param_2) {
        FUN_05ded150("autobuffer.cc",0x130,"__FitSize","_len <= 50 * 1024 * 1024","%u");
        pvVar2 = (void *)*param_1;
        if (pvVar2 == (void *)0x0) {
          FUN_05decec8("autobuffer.cc",0x131,"__FitSize","parray_");
          pvVar2 = (void *)*param_1;
        }
      }
      _bzero((void *)((long)pvVar2 + param_1[3]),sVar4 - param_1[3]);
    }
    param_1[3] = sVar4;
  }
  return;
}


