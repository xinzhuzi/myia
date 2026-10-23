// Ghidra inferred pseudocode; requested=0x668e174
// entry=0668e174 end=0668e1cf

void FUN_0668e174(long param_1)

{
  long *plVar1;
  long *plVar2;
  
  __ZNSt3__115recursive_mutex4lockEv(param_1 + 0xa0);
  plVar1 = *(long **)(param_1 + 0x78);
  for (plVar2 = *(long **)(param_1 + 0x70); plVar2 != plVar1; plVar2 = plVar2 + 2) {
    if ((long *)*plVar2 != (long *)0x0) {
      (**(code **)(*(long *)*plVar2 + 0x18))();
    }
  }
  __ZNSt3__115recursive_mutex6unlockEv(param_1 + 0xa0);
  return;
}


