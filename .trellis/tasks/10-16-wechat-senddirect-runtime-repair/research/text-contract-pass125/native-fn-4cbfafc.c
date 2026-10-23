// Ghidra inferred pseudocode; requested=0x4cbfafc
// entry=04cbfafc end=04cbfb57

void FUN_04cbfafc(long param_1)

{
  int iVar1;
  long lVar2;
  long lVar3;
  
  lVar2 = *(long *)(param_1 + 0x178);
  if ((lVar2 != *(long *)(param_1 + 0x180)) &&
     (iVar1 = FUN_05ab3ab8(param_1 + 400,lVar2,(int)*(long *)(param_1 + 0x180) - (int)lVar2),
     iVar1 != 0)) {
    lVar2 = *(long *)(param_1 + 0x178);
    *(undefined8 *)(param_1 + 0x178) = 0;
    *(undefined8 *)(param_1 + 0x180) = 0;
    lVar3 = *(long *)(param_1 + 0x188);
    *(undefined8 *)(param_1 + 0x188) = 0;
    if (lVar2 != 0) {
      __ZdlPvm(lVar2,lVar3 - lVar2);
      return;
    }
  }
  return;
}


