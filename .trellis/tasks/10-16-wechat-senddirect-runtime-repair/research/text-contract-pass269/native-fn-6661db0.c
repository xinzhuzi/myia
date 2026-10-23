// Ghidra inferred pseudocode; requested=0x6661db0
// entry=06661db0 end=06661e47

undefined8
FUN_06661db0(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
            undefined8 param_5)

{
  undefined8 uVar1;
  
  uVar1 = (**(code **)(*(long *)param_1[1] + 0x20))();
  (**(code **)(*(long *)param_1[1] + 0x30))
            ((long *)param_1[1],uVar1,param_2,param_3,param_4,param_5);
  (**(code **)(*param_1 + 0x28))(param_1,uVar1,param_2,param_4,param_5);
  return uVar1;
}


