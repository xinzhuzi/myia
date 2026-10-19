// Ghidra inferred pseudocode; requested=0x5ab3f98
// entry=05ab3f98 end=05ab3f9b

bool thunk_FUN_05ab3f9c(long *param_1,long param_2,int param_3)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  undefined8 uVar4;
  
  uVar2 = (**(code **)(*param_1 + 0x48))();
  iVar1 = (int)uVar2;
  if (iVar1 <= param_3) {
    lVar3 = (**(code **)(*param_1 + 0x58))(param_1,param_2);
    if (lVar3 - param_2 != (long)iVar1) {
      uVar4 = (**(code **)(*param_1 + 0x48))(param_1);
      FUN_05ab3d94(uVar2,uVar4,lVar3 - param_2);
    }
  }
  return iVar1 <= param_3;
}


