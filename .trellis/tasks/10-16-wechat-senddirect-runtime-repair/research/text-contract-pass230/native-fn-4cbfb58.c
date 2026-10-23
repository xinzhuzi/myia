// Ghidra inferred pseudocode; requested=0x4cbfb58
// entry=04cbfb58 end=04cbfbbb

void FUN_04cbfb58(long param_1)

{
  int iVar1;
  long lVar2;
  ulong uVar3;
  ulong uVar4;
  
  iVar1 = FUN_04eafe18(param_1 + 400);
  uVar4 = (ulong)iVar1;
  lVar2 = *(long *)(param_1 + 0x178);
  uVar3 = *(long *)(param_1 + 0x180) - lVar2;
  if (uVar4 < uVar3 || uVar4 - uVar3 == 0) {
    if (uVar4 < uVar3) {
      *(ulong *)(param_1 + 0x180) = lVar2 + uVar4;
    }
  }
  else {
    FUN_000196dc(param_1 + 0x178,uVar4 - uVar3);
    lVar2 = *(long *)(param_1 + 0x178);
  }
  thunk_FUN_05ab3f9c(param_1 + 400,lVar2,*(int *)(param_1 + 0x188) - (int)lVar2);
  return;
}


