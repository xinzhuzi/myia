// Ghidra inferred pseudocode; requested=0x4c876bc
// entry=04c876bc end=04c8836b

void FUN_04c876bc(undefined8 param_1,long *param_2,undefined8 param_3)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  int iVar4;
  long *plVar5;
  long *plVar6;
  ulong uVar7;
  ulong uVar8;
  long lVar9;
  long local_90;
  long *local_88;
  undefined1 auStack_80 [16];
  long local_70;
  long *plStack_68;
  long local_60;
  long *local_58;
  long *local_50;
  long *local_48;
  
  local_50 = (long *)0x0;
  local_48 = (long *)0x0;
  lVar9 = *param_2;
  uVar7 = (ulong)*(uint *)(lVar9 + 8);
  if (*(uint *)(lVar9 + 8) == 0x31) {
    uVar7 = (ulong)*(uint *)(lVar9 + 0xc) << 0x20 | 0x31;
  }
  if ((long)uVar7 < 0x2100000031) {
    if ((long)uVar7 < 0x200000031) {
      if ((long)uVar7 < 0x2f) {
        if ((long)uVar7 < 0x22) {
          if (uVar7 == 1) goto LAB_04c87c30;
          if (uVar7 == 3) goto LAB_04c87e58;
        }
        else {
          if (uVar7 == 0x22) {
            plVar5 = (long *)__Znwm(0x60);
            plVar5[1] = 0;
            plVar5[2] = 0;
            *plVar5 = (long)&PTR_FUN_09eadb28;
            local_60 = CONCAT71(local_60._1_7_,0xaa);
            FUN_04c8dd08(&local_60,plVar5 + 3,param_3);
            plVar3 = local_48;
            local_50 = plVar5 + 3;
            goto joined_r0x04c88354;
          }
          if (uVar7 == 0x2a) goto LAB_04c87dac;
          if (uVar7 == 0x2b) goto LAB_04c87acc;
        }
LAB_04c881bc:
        plVar5 = (long *)__Znwm(0x60);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09eadd58;
        local_60 = CONCAT71(local_60._1_7_,0xaa);
        FUN_04c8eff4(&local_60,plVar5 + 3,param_3);
        plVar3 = local_48;
        local_50 = plVar5 + 3;
      }
      else if ((long)uVar7 < 0x3e) {
        if (uVar7 == 0x2f) {
LAB_04c87d34:
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eae088;
          local_60 = CONCAT71(local_60._1_7_,0xaa);
          FUN_04c90864(&local_60,plVar5 + 3,param_3);
          plVar3 = local_48;
          local_50 = plVar5 + 3;
        }
        else {
          if (uVar7 != 0x30) goto LAB_04c881bc;
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eadbc8;
          local_60 = CONCAT71(local_60._1_7_,0xaa);
          FUN_04c8e270(&local_60,plVar5 + 3,param_3);
          plVar3 = local_48;
          local_50 = plVar5 + 3;
        }
      }
      else if (uVar7 == 0x3e) {
LAB_04c87acc:
        plVar5 = (long *)__Znwm(0x60);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09eadad8;
        local_60 = CONCAT71(local_60._1_7_,0xaa);
        FUN_04c8da54(&local_60,plVar5 + 3,param_3);
        plVar3 = local_48;
        local_50 = plVar5 + 3;
      }
      else {
        if (uVar7 != 0x43) {
          uVar8 = 0x100000031;
          goto LAB_04c87ac0;
        }
LAB_04c87dac:
        if ((*(long *)(lVar9 + 0x218) == 0) ||
           (local_60 = ___dynamic_cast(*(long *)(lVar9 + 0x218),&PTR_DAT_09eb1040,&PTR_DAT_09eb5e50,
                                       0), local_60 == 0)) {
          local_60 = 0;
          local_58 = (long *)0x0;
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eadd58;
          local_70 = CONCAT71(local_70._1_7_,0xaa);
          plVar1 = plVar5 + 3;
          FUN_04c8eff4(&local_70,plVar1,param_3);
          plVar6 = local_48;
          plVar3 = local_58;
          local_50 = plVar1;
          if (local_48 != (long *)0x0) {
            LOAcquire();
            lVar9 = local_48[1];
            local_48[1] = lVar9 + -1;
            LORelease();
            if (lVar9 == 0) {
              lVar9 = *local_48;
              local_48 = plVar5;
              (**(code **)(lVar9 + 0x10))(plVar6);
              goto LAB_04c8834c;
            }
          }
        }
        else {
          local_58 = *(long **)(lVar9 + 0x220);
          lVar9 = 0;
          if (local_58 != (long *)0x0) {
            lVar9 = local_58[1];
            local_58[1] = lVar9 + 1;
          }
          lVar2 = *(long *)(local_60 + 0x1a8);
          plVar6 = *(long **)(local_60 + 0x1b0);
          if (plVar6 != (long *)0x0) {
            lVar9 = plVar6[1];
            plVar6[1] = lVar9 + 1;
          }
          local_70 = lVar2;
          plStack_68 = plVar6;
          if (lVar2 == 0) {
            FUN_04c88ba8(auStack_80,param_3);
LAB_04c88310:
            FUN_002652cc(&local_50,auStack_80);
            FUN_00129f68(auStack_80);
          }
          else {
            iVar4 = FUN_04d1b4ec(lVar9,lVar2);
            if (((iVar4 != 3) && (iVar4 = FUN_04d1b4ec(lVar2), iVar4 != 4)) &&
               (iVar4 = FUN_04d1b4ec(lVar2), iVar4 != 5)) {
              FUN_04c88ba8(auStack_80,param_3);
              goto LAB_04c88310;
            }
            FUN_04c88c38(auStack_80,param_3);
            FUN_002652cc(&local_50,auStack_80);
            FUN_00129f68(auStack_80);
          }
          plVar3 = local_58;
          plVar5 = local_48;
          if (plVar6 != (long *)0x0) {
            LOAcquire();
            lVar9 = plVar6[1];
            plVar6[1] = lVar9 + -1;
            LORelease();
            if (lVar9 == 0) {
              (**(code **)(*plVar6 + 0x10))(plVar6);
LAB_04c8834c:
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
              plVar3 = local_58;
              plVar5 = local_48;
            }
          }
        }
      }
    }
    else if ((long)uVar7 < 0x700000031) {
      if ((long)uVar7 < 0x400000031) {
        if (uVar7 != 0x200000031) {
          if (uVar7 == 0x300000031) goto LAB_04c87c8c;
          goto LAB_04c881bc;
        }
LAB_04c87e58:
        plVar5 = (long *)__Znwm(0x60);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09eada38;
        local_60 = CONCAT71(local_60._1_7_,0xaa);
        FUN_04c8d4ec(&local_60,plVar5 + 3,param_3);
        plVar3 = local_48;
        local_50 = plVar5 + 3;
      }
      else {
        if (uVar7 == 0x400000031) goto LAB_04c87acc;
        if (uVar7 == 0x500000031) goto LAB_04c87d70;
        if (uVar7 != 0x600000031) goto LAB_04c881bc;
        plVar5 = (long *)__Znwm(0x60);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09eada88;
        local_60 = CONCAT71(local_60._1_7_,0xaa);
        FUN_04c8d7a0(&local_60,plVar5 + 3,param_3);
        plVar3 = local_48;
        local_50 = plVar5 + 3;
      }
    }
    else if ((long)uVar7 < 0xa00000031) {
      if (uVar7 != 0x700000031) {
        if (uVar7 == 0x800000031) goto LAB_04c87d34;
        goto LAB_04c881bc;
      }
LAB_04c87d70:
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eadb78;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8dfbc(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else if (uVar7 == 0xa00000031) {
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eadc18;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8e524(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else if (uVar7 == 0x1300000031) {
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eadf38;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c9002c(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else {
      if (uVar7 != 0x1800000031) goto LAB_04c881bc;
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eadfe0;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c904e8(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
  }
  else if ((long)uVar7 < 0x4c00000031) {
    if ((long)uVar7 < 0x3500000031) {
      if ((long)uVar7 < 0x2c00000031) {
        if (uVar7 == 0x2100000031) {
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eade48;
          local_60 = CONCAT71(local_60._1_7_,0xaa);
          FUN_04c8f810(&local_60,plVar5 + 3,param_3);
          plVar3 = local_48;
          local_50 = plVar5 + 3;
        }
        else {
          if (uVar7 != 0x2400000031) goto LAB_04c881bc;
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eaddf8;
          local_60 = CONCAT71(local_60._1_7_,0xaa);
          FUN_04c8f55c(&local_60,plVar5 + 3,param_3);
          plVar3 = local_48;
          local_50 = plVar5 + 3;
        }
      }
      else {
        if (uVar7 == 0x2c00000031) {
          iVar4 = FUN_048abf50(lVar9);
          if (iVar4 != 0) {
            FUN_04c88cc8(&local_60,param_3);
            FUN_002652cc(&local_50,&local_60);
            FUN_00129f68(&local_60);
            goto LAB_04c88228;
          }
          FUN_04c88ba8(&local_60,param_3);
LAB_04c882ec:
          FUN_002652cc(&local_50,&local_60);
          FUN_00129f68(&local_60);
          goto LAB_04c88228;
        }
        if (uVar7 == 0x3200000031) {
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eadda8;
          local_60 = CONCAT71(local_60._1_7_,0xaa);
          FUN_04c8f2a8(&local_60,plVar5 + 3,param_3);
          plVar3 = local_48;
          local_50 = plVar5 + 3;
        }
        else {
          if (uVar7 != 0x3300000031) goto LAB_04c881bc;
          plVar5 = (long *)__Znwm(0x60);
          plVar5[1] = 0;
          plVar5[2] = 0;
          *plVar5 = (long)&PTR_FUN_09eadcb8;
          local_60 = CONCAT71(local_60._1_7_,0xaa);
          FUN_04c8ea8c(&local_60,plVar5 + 3,param_3);
          plVar3 = local_48;
          local_50 = plVar5 + 3;
        }
      }
    }
    else if ((long)uVar7 < 0x3f00000031) {
      if (uVar7 == 0x3500000031) goto LAB_04c87c30;
      if (uVar7 != 0x3900000031) goto LAB_04c881bc;
      plVar5 = (long *)__Znwm(0x68);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09ead998;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8cf80(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else if (uVar7 == 0x3f00000031) {
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eadd08;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8ed40(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else {
      if (uVar7 == 0x4400000031) goto LAB_04c87d70;
      if (uVar7 != 0x4a00000031) goto LAB_04c881bc;
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09ead9e8;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8d238(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
  }
  else if ((long)uVar7 < 0x5d00000031) {
    if ((long)uVar7 < 0x5700000031) {
      if (uVar7 == 0x4c00000031) {
LAB_04c87c8c:
        plVar5 = (long *)__Znwm(0x60);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09eadc68;
        local_60 = CONCAT71(local_60._1_7_,0xaa);
        FUN_04c8e7d8(&local_60,plVar5 + 3,param_3);
        plVar3 = local_48;
        local_50 = plVar5 + 3;
      }
      else {
        if (uVar7 != 0x5200000031) goto LAB_04c881bc;
        plVar5 = (long *)__Znwm(0x60);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09eae178;
        local_60 = CONCAT71(local_60._1_7_,0xaa);
        FUN_04c91080(&local_60,plVar5 + 3,param_3);
        plVar3 = local_48;
        local_50 = plVar5 + 3;
      }
    }
    else if (uVar7 == 0x5700000031) {
LAB_04c87c30:
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09ead948;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8cbe0(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else {
      if (uVar7 == 0x5800000031) {
        iVar4 = FUN_048a91e0(lVar9);
        if (iVar4 != 0) {
          FUN_04c88b18(&local_60,param_3);
          FUN_002652cc(&local_50,&local_60);
          FUN_00129f68(&local_60);
          goto LAB_04c88228;
        }
        FUN_04c88ba8(&local_60,param_3);
        goto LAB_04c882ec;
      }
      if (uVar7 != 0x5c00000031) goto LAB_04c881bc;
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eade98;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8fac4(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
  }
  else if ((long)uVar7 < 0x8400000031) {
    if (uVar7 == 0x5d00000031) {
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eadee8;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c8fd78(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else if (uVar7 == 0x6f00000031) {
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eae128;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c90dcc(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
    else {
      if (uVar7 != 0x7300000031) goto LAB_04c881bc;
      plVar5 = (long *)__Znwm(0x60);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09eae1c8;
      local_60 = CONCAT71(local_60._1_7_,0xaa);
      FUN_04c91334(&local_60,plVar5 + 3,param_3);
      plVar3 = local_48;
      local_50 = plVar5 + 3;
    }
  }
  else if (uVar7 == 0x8400000031) {
    plVar5 = (long *)__Znwm(0x60);
    plVar5[1] = 0;
    plVar5[2] = 0;
    *plVar5 = (long)&PTR_FUN_09eae268;
    local_60 = CONCAT71(local_60._1_7_,0xaa);
    FUN_04c9189c(&local_60,plVar5 + 3,param_3);
    plVar3 = local_48;
    local_50 = plVar5 + 3;
  }
  else {
    if (uVar7 != 0x8700000031) {
      uVar8 = 0x8b00000031;
LAB_04c87ac0:
      if (uVar7 == uVar8) goto LAB_04c87c30;
      goto LAB_04c881bc;
    }
    plVar5 = (long *)__Znwm(0x60);
    plVar5[1] = 0;
    plVar5[2] = 0;
    *plVar5 = (long)&PTR_FUN_09eae2b8;
    local_60 = CONCAT71(local_60._1_7_,0xaa);
    FUN_04c91b50(&local_60,plVar5 + 3,param_3);
    plVar3 = local_48;
    local_50 = plVar5 + 3;
  }
joined_r0x04c88354:
  local_48 = plVar5;
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar9 = plVar3[1];
    plVar3[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
LAB_04c88228:
  local_90 = *param_2;
  local_88 = (long *)param_2[1];
  if (local_88 != (long *)0x0) {
    local_88[1] = local_88[1] + 1;
  }
  (**(code **)(*local_50 + 0x10))(param_1,local_50,&local_90);
  plVar3 = local_88;
  if (local_88 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_88[1];
    local_88[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_88 + 0x10))(local_88);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_48[1];
    local_48[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  return;
}


