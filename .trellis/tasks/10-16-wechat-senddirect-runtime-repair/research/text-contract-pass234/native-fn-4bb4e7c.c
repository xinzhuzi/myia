// Ghidra inferred pseudocode; requested=0x4bb4e7c
// entry=04bb4e7c end=04bb4ef3

undefined8 * FUN_04bb4e7c(void)

{
  ulong uVar1;
  
  if (((DAT_0a4a5298 & 1) == 0) && (uVar1 = FUN_0711b288(), (uVar1 & 1) == 0)) {
    FUN_00255b9c(&DAT_0a4a5280,&DAT_0a4a5490);
    ___cxa_atexit(PTR___ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEED1Ev_09b364f8,
                  &DAT_0a4a5280,0);
    ___cxa_guard_release(&DAT_0a4a5298);
  }
  return &DAT_0a4a5280;
}


