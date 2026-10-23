// Ghidra inferred pseudocode; requested=0x667f534
// entry=0667f534 end=0667f61b

void FUN_0667f534(long param_1)

{
  undefined8 uVar1;
  long *plVar2;
  long *plVar3;
  code *pcVar4;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  
  *(undefined1 *)(param_1 + 0x150) = 1;
  if ((*(byte *)(param_1 + 0x143) & 1) == 0) {
    uVar1 = FUN_0667fa1c(param_1);
    *(undefined8 *)(param_1 + 0x148) = uVar1;
    FUN_0668435c();
    plVar2 = *(long **)(*(long *)(param_1 + 0x118) + 0x18);
    if (plVar2 != (long *)0x0) {
      (**(code **)(*plVar2 + 0x30))();
    }
    FUN_066823c4(*(long *)(param_1 + 0x148) + 8);
  }
  *(undefined1 *)(param_1 + 0x141) = 0;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_06676adc(&local_100);
  plVar2 = *(long **)(param_1 + 0x118);
  if (plVar2 == (long *)0x0) goto LAB_0667f5ec;
  plVar3 = (long *)plVar2[3];
  if (plVar3 == plVar2) {
    pcVar4 = *(code **)(*plVar3 + 0x20);
LAB_0667f5d8:
    (*pcVar4)();
  }
  else if (plVar3 != (long *)0x0) {
    pcVar4 = *(code **)(*plVar3 + 0x28);
    goto LAB_0667f5d8;
  }
  __ZdlPvm(plVar2,0x20);
  *(undefined8 *)(param_1 + 0x118) = 0;
LAB_0667f5ec:
  FUN_06676b84(&local_100);
  FUN_0667fc38(param_1,*(byte *)(param_1 + 0x143) & 1);
  return;
}


