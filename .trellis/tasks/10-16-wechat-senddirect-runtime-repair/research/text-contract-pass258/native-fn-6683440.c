// Ghidra inferred pseudocode; requested=0x6683440
// entry=06683440 end=06683467

bool FUN_06683440(long *param_1,long *param_2)

{
  return (param_1[1] == param_2[1] ||
         (((uint)param_2[1] | (uint)param_1[1]) & 1) == 0 && *param_1 == 0) && *param_1 == *param_2;
}


