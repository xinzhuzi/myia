// Ghidra inferred pseudocode; requested=0x6680b64
// entry=06680b64 end=06681697

/* WARNING: Removing unreachable block (ram,0x06680e1c) */
/* WARNING: Removing unreachable block (ram,0x06680dec) */
/* WARNING: Removing unreachable block (ram,0x066815e8) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 * FUN_06680b64(long param_1)

{
  undefined1 **ppuVar1;
  uint3 uVar2;
  long lVar3;
  int iVar4;
  undefined1 *puVar5;
  ulong uVar6;
  undefined4 *puVar7;
  undefined8 uVar8;
  long *plVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  undefined1 *local_190;
  long *plStack_188;
  undefined7 local_180;
  char cStack_179;
  undefined1 auStack_158 [48];
  undefined8 *******local_128 [2];
  char local_111;
  ulong local_c0;
  undefined8 uStack_b8;
  ulong local_b0;
  undefined1 *local_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined1 *local_90;
  undefined8 local_88;
  undefined1 *puStack_80;
  undefined8 local_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_a8 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)(param_1 + 0x97) < '\0') {
    FUN_00018d20(&local_a0,*(undefined8 *)(param_1 + 0x80),*(undefined8 *)(param_1 + 0x88));
  }
  else {
    uStack_98 = *(undefined8 *)(param_1 + 0x88);
    local_a0 = *(ulong **)(param_1 + 0x80);
    local_90 = *(undefined1 **)(param_1 + 0x90);
  }
  if ((DAT_0a518349 & 1) == 0) {
    DAT_0a518340 = DAT_09685c48;
    DAT_0a518348 = 0;
    DAT_0a518349 = 1;
  }
  if ((DAT_0a51835a & 1) == 0) {
    DAT_0a518350 = DAT_09685c50;
    DAT_0a518358 = 0x22;
    DAT_0a51835a = 1;
  }
  FUN_06666718(&local_190,&DAT_0a518340,&DAT_0a518350,&local_a0);
  ppuVar1 = (undefined1 **)local_190;
  if (-1 < cStack_179) {
    ppuVar1 = &local_190;
  }
  local_b0 = local_b0 & 0xffffffffffffff;
  local_c0 = local_c0 & 0xffffffffffffff00;
  if ((DAT_0a5181e5 & 1) == 0) {
    DAT_0a5181e0 = (undefined4)ram0x08782918;
    DAT_0a5181e4 = 0;
    DAT_0a5181e5 = 1;
  }
  if ((DAT_0a518349 & 1) == 0) {
    DAT_0a518340 = DAT_09685c48;
    DAT_0a518348 = 0;
    DAT_0a518349 = 1;
  }
  if ((DAT_0a518203 & 1) == 0) {
    DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
    DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
    DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
    DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
    DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
    DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
    DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
    DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
    DAT_0a518200 = 0x7070;
    DAT_0a518202 = 0;
    DAT_0a518203 = 1;
  }
  thunk_FUN_0668f12c(&local_a8,&DAT_0a5181e0,&DAT_0a518340,&DAT_0a5181f8,ppuVar1,0xc000000000,
                     &local_c0);
  if (cStack_179 < '\0') {
    __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
  }
  FUN_06673848(&local_190);
  puVar5 = local_190;
  if (plStack_188 == (long *)0x0) {
LAB_06680d4c:
    if (local_190 != (undefined1 *)0x0) goto LAB_06680d50;
LAB_06680e4c:
    lVar3 = FUN_06662530();
    if (lVar3 != 0) {
      if (lVar3 != *(long *)(param_1 + 0xf8)) {
        iVar4 = FUN_0668dad0(0);
        if (iVar4 != 0) {
          if ((DAT_0a5181e5 & 1) == 0) {
            DAT_0a5181e0 = (undefined4)ram0x08782918;
            DAT_0a5181e4 = 0;
            DAT_0a5181e5 = 1;
          }
          if ((DAT_0a518349 & 1) == 0) {
            DAT_0a518348 = 0;
            DAT_0a518349 = 1;
            DAT_0a518340 = DAT_09685c48;
          }
          if ((DAT_0a518203 & 1) == 0) {
            DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
            DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
            DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
            DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
            DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
            DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
            DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
            DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
            DAT_0a518200 = 0x7070;
            DAT_0a518202 = 0;
            DAT_0a518203 = 1;
          }
          FUN_0668db5c(&local_190,&DAT_0a5181e0,&DAT_0a518340,&DAT_0a5181f8,0xd400000800);
          if ((DAT_0a518432 & 1) == 0) {
            _DAT_0a518410 = CONCAT44((int)ram0x084cd9a0,(int)DAT_087faf40);
            uRam000000000a518418 = CONCAT44((int)DAT_084d7818,(int)DAT_08486af0);
            _DAT_0a518420 = CONCAT44((int)DAT_09685c68,(int)DAT_084d58f8);
            uRam000000000a518428 = CONCAT44((int)DAT_08492618,(int)DAT_084f1768);
            DAT_0a518430 = 0x74;
            DAT_0a518432 = 1;
          }
          plVar9 = (long *)(local_190 + 0x68);
          if ((char)local_190[0x7f] < '\0') {
            plVar9 = (long *)*plVar9;
          }
          uStack_98 = 0xaaaaaaaa00000006;
          local_a0 = (ulong *)&DAT_aaaaaaaa00000000;
          FUN_0668e1e4(local_190 + 0x38,&DAT_0a518410,plVar9,&local_a0,0);
          goto LAB_066810b0;
        }
        goto LAB_066810bc;
      }
      if ((DAT_0a5181e5 & 1) == 0) {
        DAT_0a5181e0 = (undefined4)ram0x08782918;
        DAT_0a5181e4 = 0;
        DAT_0a5181e5 = 1;
      }
      if ((DAT_0a518349 & 1) == 0) {
        DAT_0a518348 = 0;
        DAT_0a518349 = 1;
        DAT_0a518340 = DAT_09685c48;
      }
      if ((DAT_0a518203 & 1) == 0) {
        DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
        DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
        DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
        DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
        DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
        DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
        DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
        DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
        DAT_0a518200 = 0x7070;
        DAT_0a518202 = 0;
        DAT_0a518203 = 1;
      }
      FUN_0668db5c(&local_190,&DAT_0a5181e0,&DAT_0a518340,&DAT_0a5181f8,0xcc0000b000);
      if ((DAT_0a51838e & 1) == 0) {
        DAT_0a518380._0_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[0];
        DAT_0a518380._1_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[1];
        DAT_0a518380._2_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[2];
        DAT_0a518380._3_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[3];
        DAT_0a518380._4_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[4];
        DAT_0a518380._5_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[5];
        DAT_0a518380._6_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[6];
        DAT_0a518380._7_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[7];
        DAT_0a518388 = (undefined4)DAT_084d8788;
        DAT_0a51838c = 0x20;
        DAT_0a51838e = 1;
      }
      if (-1 < local_111) {
        local_128[0] = local_128;
      }
      uStack_98 = 0xaaaaaaaa00000006;
      local_a0 = (ulong *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(auStack_158,&DAT_0a518380,local_128[0],&local_a0,0);
      if ((DAT_0a5183ea & 1) == 0) {
        uVar6 = 0;
        do {
          uVar10 = *(undefined4 *)((long)&DAT_09686043 + uVar6);
          uVar2 = CONCAT12((char)((uint)uVar10 >> 8),(short)uVar10) & 0xff00ff;
          uVar11 = *(undefined4 *)((long)&DAT_0968602f + uVar6 % 0x14);
          *(uint *)((long)&DAT_0a51838f + uVar6) =
               CONCAT13((char)((uint)uVar10 >> 0x18) + 0x8aU ^ (byte)((uint)uVar11 >> 0x18),
                        CONCAT12((char)((uint)uVar10 >> 0x10) + 0x8aU ^ (byte)((uint)uVar11 >> 0x10)
                                 ,CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar11 >> 8)
                                           ,(char)uVar2 + 0x8aU ^ (byte)uVar11)));
          uVar6 = uVar6 + 4;
        } while (uVar6 != 0x58);
        DAT_0a5183e7 = 0x2172;
        DAT_0a5183e9 = 0;
        DAT_0a5183ea = 1;
      }
      plVar9 = (long *)(local_190 + 0x68);
      if ((char)local_190[0x7f] < '\0') {
        plVar9 = (long *)*plVar9;
      }
      uStack_98 = 0xaaaaaaaa00000006;
      local_a0 = (ulong *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_190 + 0x38,&DAT_0a51838f,plVar9,&local_a0,0);
LAB_066813a8:
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_190);
      puVar5 = (undefined1 *)0x0;
      goto joined_r0x066813bc;
    }
    iVar4 = FUN_0668dad0();
    if (iVar4 != 0) {
      if ((DAT_0a5181e5 & 1) == 0) {
        DAT_0a5181e0 = (undefined4)ram0x08782918;
        DAT_0a5181e4 = 0;
        DAT_0a5181e5 = 1;
      }
      if ((DAT_0a518349 & 1) == 0) {
        DAT_0a518348 = 0;
        DAT_0a518349 = 1;
        DAT_0a518340 = DAT_09685c48;
      }
      if ((DAT_0a518203 & 1) == 0) {
        DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
        DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
        DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
        DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
        DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
        DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
        DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
        DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
        DAT_0a518200 = 0x7070;
        DAT_0a518202 = 0;
        DAT_0a518203 = 1;
      }
      FUN_0668db5c(&local_190,&DAT_0a5181e0,&DAT_0a518340,&DAT_0a5181f8,0xd100000800);
      if ((DAT_0a51840c & 1) == 0) {
        _DAT_0a5183ec = CONCAT44((int)ram0x084cd9a0,(int)DAT_087faf40);
        uRam000000000a5183f4 = CONCAT44((int)DAT_084d7818,(int)DAT_08486af0);
        _DAT_0a5183fc = CONCAT44((int)DAT_084cf918,(int)ram0x0875ae18);
        uRam000000000a518404 = CONCAT44((int)DAT_084d0070,(int)DAT_08486a60);
        DAT_0a51840c = 1;
      }
      plVar9 = (long *)(local_190 + 0x68);
      if ((char)local_190[0x7f] < '\0') {
        plVar9 = (long *)*plVar9;
      }
      uStack_98 = 0xaaaaaaaa00000006;
      local_a0 = (ulong *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_190 + 0x38,&DAT_0a5183ec,plVar9,&local_a0,0);
LAB_066810b0:
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_190);
    }
LAB_066810bc:
    puVar7 = (undefined4 *)FUN_02c620c8(param_1 + 200);
    uVar10 = *puVar7;
    uVar6 = FUN_0668dad0(0);
    if ((uVar6 & 1) != 0) {
      if ((DAT_0a5181e5 & 1) == 0) {
        DAT_0a5181e0 = (undefined4)ram0x08782918;
        DAT_0a5181e4 = 0;
        DAT_0a5181e5 = 1;
      }
      if ((DAT_0a518349 & 1) == 0) {
        DAT_0a518348 = 0;
        DAT_0a518349 = 1;
        DAT_0a518340 = DAT_09685c48;
      }
      if ((DAT_0a518203 & 1) == 0) {
        DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
        DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
        DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
        DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
        DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
        DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
        DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
        DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
        DAT_0a518200 = 0x7070;
        DAT_0a518202 = 0;
        DAT_0a518203 = 1;
      }
      FUN_0668db5c(&local_190,&DAT_0a5181e0,&DAT_0a518340,&DAT_0a5181f8,0xd700000800);
      if ((DAT_0a51844e & 1) == 0) {
        _DAT_0a518434 = CONCAT44((int)DAT_0860f288,(int)DAT_087faf40);
        uRam000000000a51843c = CONCAT44((int)DAT_084e3fc0,(int)DAT_08489290);
        DAT_0a518444 = CONCAT44((int)DAT_08598098,(int)DAT_085b0820);
        DAT_0a51844c = 0x5f;
        DAT_0a51844e = 1;
      }
      plVar9 = (long *)(local_190 + 0x68);
      if ((char)local_190[0x7f] < '\0') {
        plVar9 = (long *)*plVar9;
      }
      uStack_98 = 0xaaaaaaaa00000006;
      local_a0 = (ulong *)CONCAT44(0xaaaaaaaa,uVar10);
      local_88 = 0xaaaaaaaa00000006;
      local_90 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_190 + 0x38,&DAT_0a518434,plVar9,&local_a0,1);
      goto LAB_066813a8;
    }
  }
  else {
    LOAcquire();
    lVar3 = plStack_188[1];
    plStack_188[1] = lVar3 + -1;
    LORelease();
    if (lVar3 != 0) goto LAB_06680d4c;
    (**(code **)(*plStack_188 + 0x10))(plStack_188);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plStack_188);
    if (puVar5 == (undefined1 *)0x0) goto LAB_06680e4c;
LAB_06680d50:
    puVar5 = (undefined1 *)FUN_06674d5c(param_1 + 200);
    if ((long)puVar5 < 0) {
      uVar6 = FUN_0668dad0(1);
      if ((uVar6 & 1) != 0) {
        if ((DAT_0a5181e5 & 1) == 0) {
          DAT_0a5181e0 = (undefined4)ram0x08782918;
          DAT_0a5181e4 = 0;
          DAT_0a5181e5 = 1;
        }
        if ((DAT_0a518349 & 1) == 0) {
          DAT_0a518348 = 0;
          DAT_0a518349 = 1;
          DAT_0a518340 = DAT_09685c48;
        }
        if ((DAT_0a518203 & 1) == 0) {
          DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
          DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
          DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
          DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
          DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
          DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
          DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
          DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
          DAT_0a518200 = 0x7070;
          DAT_0a518202 = 0;
          DAT_0a518203 = 1;
        }
        FUN_0668db5c(&local_190,&DAT_0a5181e0,&DAT_0a518340,&DAT_0a5181f8,0xc700002800);
        if (*(char *)(param_1 + 0x97) < '\0') {
          FUN_00018d20(&local_c0,*(undefined8 *)(param_1 + 0x80),*(undefined8 *)(param_1 + 0x88));
        }
        else {
          uStack_b8 = *(undefined8 *)(param_1 + 0x88);
          local_c0 = *(ulong *)(param_1 + 0x80);
          local_b0 = *(ulong *)(param_1 + 0x90);
        }
        if ((DAT_0a51837f & 1) == 0) {
          _DAT_0a51835c = CONCAT44((int)DAT_09685c58,(int)DAT_087faf40);
          uRam000000000a518364 = CONCAT44((int)DAT_084d8738,(int)DAT_09685c60);
          _DAT_0a51836c = CONCAT44((int)DAT_084a5d18,(int)DAT_08486af0);
          uRam000000000a518374 = CONCAT44((int)DAT_085ad310,(int)DAT_0848a1c0);
          DAT_0a51837c = 0x5f25;
          DAT_0a51837e = 0;
          DAT_0a51837f = 1;
        }
        plVar9 = (long *)(local_190 + 0x68);
        if ((char)local_190[0x7f] < '\0') {
          plVar9 = (long *)*plVar9;
        }
        uStack_98 = 0xaaaaaaaa00000010;
        local_a0 = &local_c0;
        local_78 = 0xaaaaaaaa00000006;
        local_88 = 0xaaaaaaaa0000000a;
        puStack_80 = &DAT_aaaaaaaa00000000;
        local_90 = puVar5;
        FUN_0668e1e4(local_190 + 0x38,&DAT_0a51835c,plVar9,&local_a0,2);
        FUN_0668dbac();
        thunk_FUN_0668e878(&local_190);
      }
      goto joined_r0x066813bc;
    }
  }
  puVar5 = (undefined1 *)0x0;
joined_r0x066813bc:
  if (local_a8 != (undefined1 *)0x0) {
    uVar8 = thunk_FUN_0668ef88();
    __ZdlPvm(uVar8,0xf8);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return puVar5;
}


