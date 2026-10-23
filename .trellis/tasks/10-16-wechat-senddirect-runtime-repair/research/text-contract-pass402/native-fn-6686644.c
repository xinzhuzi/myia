// Ghidra inferred pseudocode; requested=0x6686644
// entry=06686644 end=0668667b

bool FUN_06686644(long param_1)

{
  pthread_t p_Var1;
  pthread_t p_Var2;
  
  p_Var1 = _pthread_self();
  p_Var2 = *(pthread_t *)(param_1 + 0x90);
  if (p_Var2 != p_Var1) {
    *(pthread_t *)(param_1 + 0x90) = p_Var1;
  }
  return p_Var2 != p_Var1;
}


