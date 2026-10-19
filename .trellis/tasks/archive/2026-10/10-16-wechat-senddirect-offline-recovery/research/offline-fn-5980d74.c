// Ghidra inferred pseudocode; requested=0x5980d74
// entry=05980d74 end=05980deb

void FUN_05980d74(undefined8 *param_1,long param_2,undefined4 param_3)

{
  long lVar1;
  long lVar2;
  undefined4 local_34;
  
  __ZNSt3__15mutex4lockEv(param_2 + 8);
  local_34 = param_3;
  lVar2 = FUN_0598201c(param_2 + 0x70,&local_34);
  if (lVar2 == 0) {
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    lVar1 = *(long *)(lVar2 + 0x20);
    *param_1 = *(undefined8 *)(lVar2 + 0x18);
    param_1[1] = lVar1;
    if (lVar1 != 0) {
      *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
    }
  }
  __ZNSt3__15mutex6unlockEv(param_2 + 8);
  return;
}


