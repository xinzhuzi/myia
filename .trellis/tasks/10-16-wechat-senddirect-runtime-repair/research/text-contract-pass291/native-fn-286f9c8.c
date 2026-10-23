// Ghidra inferred pseudocode; requested=0x286f9c8
// entry=0286f9c8 end=0286fb13

/* WARNING: Removing unreachable block (ram,0x0286fa6c) */
/* WARNING: Removing unreachable block (ram,0x0286fac4) */

void FUN_0286f9c8(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  undefined8 uVar1;
  long local_80;
  long local_78;
  long local_70;
  long local_68;
  long local_60;
  long local_58;
  undefined8 local_50;
  undefined8 uStack_48;
  
  uVar1 = __Znwm(0x28);
  FUN_00033c40(uVar1,FUN_0286fb58,FUN_02870520);
  uStack_48 = 0;
  local_50 = uVar1;
  FUN_0291cd74(&local_80);
  FUN_028569a4(param_1,param_2,param_3,param_4,&local_50,0,&local_80);
  if (local_68 != 0) {
    for (; local_60 != local_68; local_60 = local_60 + -0x18) {
    }
    local_60 = local_68;
    __ZdlPvm(local_68,local_58 - local_68);
  }
  if (local_80 != 0) {
    for (; local_78 != local_80; local_78 = local_78 + -0x18) {
    }
    local_78 = local_80;
    __ZdlPvm(local_80,local_70 - local_80);
  }
  FUN_00033d2c(&local_50);
  FUN_00033d2c(&uStack_48);
  return;
}


