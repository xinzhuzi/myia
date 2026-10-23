// Ghidra inferred pseudocode; requested=0x56459bc
// entry=056459bc end=056459ff

undefined8 FUN_056459bc(undefined8 param_1)

{
  undefined8 uVar1;
  ulong uVar2;
  
  uVar1 = FUN_05692dc0();
  if ((int)uVar1 != 0) {
    uVar2 = FUN_05645a00(param_1);
    if ((uVar2 & 1) == 0) {
      FUN_05645da4(param_1);
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
  }
  return uVar1;
}


