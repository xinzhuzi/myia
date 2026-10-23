// Ghidra inferred pseudocode; requested=0x5037c
// entry=0005037c end=000503c3

void FUN_0005037c(undefined8 param_1,undefined8 *param_2)

{
  if (param_2 != (undefined8 *)0x0) {
    FUN_0005037c(param_1,*param_2);
    FUN_0005037c(param_1,param_2[1]);
    __ZdlPvm(param_2,0x28);
    return;
  }
  return;
}


