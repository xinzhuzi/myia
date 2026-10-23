// Ghidra inferred pseudocode; requested=0x30dcee4
// entry=030dcee4 end=030dcefb

void FUN_030dcee4(long param_1)

{
                    /* WARNING: Could not recover jumptable at 0x030dcef8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(param_1 + 0x10))
            (*(undefined8 *)(param_1 + 8),param_1 + 0x18,param_1 + 0x60,param_1 + 0x68);
  return;
}


