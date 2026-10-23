// Ghidra inferred pseudocode; requested=0x4eaea88
// entry=04eaea88 end=04eaeeb7

void FUN_04eaea88(long param_1)

{
  byte bVar1;
  uint uVar2;
  long lVar3;
  undefined8 *puVar4;
  long lVar5;
  
  uVar2 = *(uint *)(param_1 + 0x74);
  if ((uVar2 & 0xff) != 0) {
    *(undefined8 *)(param_1 + 8) = 0;
    if (((uVar2 >> 2 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x10), lVar3 != 0)) {
      if (*(byte *)(lVar3 + 0x24) != 0) {
        *(undefined8 *)(lVar3 + 8) = 0;
        if (((*(byte *)(lVar3 + 0x24) >> 2 & 1) != 0) &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x10), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
        if (((*(byte *)(lVar3 + 0x24) >> 3 & 1) != 0) &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x18), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
      }
      *(undefined4 *)(lVar3 + 0x24) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 3 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x18), lVar3 != 0)) {
      if (*(byte *)(lVar3 + 0x38) != 0) {
        *(undefined8 *)(lVar3 + 8) = 0;
        *(undefined8 *)(lVar3 + 0x10) = 0;
        *(undefined8 *)(lVar3 + 0x15) = 0;
        if (((*(byte *)(lVar3 + 0x38) >> 6 & 1) != 0) &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x20), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
        if ((*(char *)(lVar3 + 0x38) < '\0') &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x28), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
      }
      if (*(char *)(lVar3 + 0x39) != '\0') {
        *(undefined4 *)(lVar3 + 0x30) = 0;
      }
      *(undefined4 *)(lVar3 + 0x38) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 4 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x20), lVar3 != 0)) {
      if ((*(byte *)(lVar3 + 0x18) != 0) &&
         ((*(undefined4 *)(lVar3 + 0x10) = 0, (*(byte *)(lVar3 + 0x18) >> 1 & 1) != 0 &&
          (puVar4 = *(undefined8 **)(lVar3 + 8), puVar4 != &DAT_0a524ad0)))) {
        if (*(char *)((long)puVar4 + 0x17) < '\0') {
          *(undefined1 *)*puVar4 = 0;
          puVar4[1] = 0;
        }
        else {
          *(undefined1 *)puVar4 = 0;
          *(undefined1 *)((long)puVar4 + 0x17) = 0;
        }
      }
      *(undefined4 *)(lVar3 + 0x18) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 5 & 1) != 0) && (*(long *)(param_1 + 0x28) != 0)) {
      FUN_04eaa17c();
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 6 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x30), lVar3 != 0)) {
      if ((*(uint *)(lVar3 + 0x30) & 0x1fe) != 0) {
        if (((*(uint *)(lVar3 + 0x30) >> 1 & 1) != 0) &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x20), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
        *(undefined4 *)(lVar3 + 0x28) = 0;
      }
      if (0 < *(int *)(lVar3 + 0x10)) {
        lVar5 = 0;
        do {
          (**(code **)(**(long **)(*(long *)(lVar3 + 8) + lVar5 * 8) + 0x20))();
          lVar5 = lVar5 + 1;
        } while (lVar5 < *(int *)(lVar3 + 0x10));
      }
      *(undefined4 *)(lVar3 + 0x10) = 0;
      *(undefined4 *)(lVar3 + 0x30) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 7 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x38), lVar3 != 0)) {
      uVar2 = *(uint *)(lVar3 + 0x38);
      if ((uVar2 & 0xff) != 0) {
        *(undefined8 *)(lVar3 + 8) = 0;
        *(undefined8 *)(lVar3 + 0x10) = 0;
        if (((uVar2 >> 4 & 1) != 0) &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x18), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
        if (((*(byte *)(lVar3 + 0x38) >> 5 & 1) != 0) &&
           (puVar4 = *(undefined8 **)(lVar3 + 0x20), puVar4 != &DAT_0a524ad0)) {
          if (*(char *)((long)puVar4 + 0x17) < '\0') {
            *(undefined1 *)*puVar4 = 0;
            puVar4[1] = 0;
          }
          else {
            *(undefined1 *)puVar4 = 0;
            *(undefined1 *)((long)puVar4 + 0x17) = 0;
          }
        }
        *(undefined8 *)(lVar3 + 0x28) = 0;
        uVar2 = *(uint *)(lVar3 + 0x38);
      }
      if ((uVar2 & 0xff00) != 0) {
        *(undefined4 *)(lVar3 + 0x30) = 0;
      }
      *(undefined4 *)(lVar3 + 0x38) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
  }
  if ((uVar2 & 0xff00) != 0) {
    if (((uVar2 >> 8 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x40), lVar3 != 0)) {
      if (((*(byte *)(lVar3 + 0x14) & 1) != 0) &&
         (puVar4 = *(undefined8 **)(lVar3 + 8), puVar4 != &DAT_0a524ad0)) {
        if (*(char *)((long)puVar4 + 0x17) < '\0') {
          *(undefined1 *)*puVar4 = 0;
          puVar4[1] = 0;
        }
        else {
          *(undefined1 *)puVar4 = 0;
          *(undefined1 *)((long)puVar4 + 0x17) = 0;
        }
      }
      *(undefined4 *)(lVar3 + 0x14) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 9 & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x48), lVar3 != 0)) {
      if (*(char *)(lVar3 + 0x10) != '\0') {
        *(undefined4 *)(lVar3 + 8) = 0;
      }
      *(undefined4 *)(lVar3 + 0x10) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    *(undefined8 *)(param_1 + 0x50) = 0;
    if (((uVar2 >> 0xb & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x58), lVar3 != 0)) {
      bVar1 = *(byte *)(lVar3 + 0x2c);
      uVar2 = (uint)bVar1;
      if (bVar1 != 0) {
        *(undefined4 *)(lVar3 + 0x10) = 0;
        *(undefined8 *)(lVar3 + 8) = 0;
        *(undefined1 *)(lVar3 + 0x14) = 0;
        if (((bVar1 >> 3 & 1) != 0) && (lVar5 = *(long *)(lVar3 + 0x18), lVar5 != 0)) {
          if (*(char *)(lVar5 + 0x10) != '\0') {
            *(undefined4 *)(lVar5 + 8) = 0;
          }
          *(undefined4 *)(lVar5 + 0x10) = 0;
          uVar2 = *(uint *)(lVar3 + 0x2c);
        }
        if (((uVar2 >> 4 & 1) != 0) && (lVar5 = *(long *)(lVar3 + 0x20), lVar5 != 0)) {
          if (*(char *)(lVar5 + 0x10) != '\0') {
            *(undefined4 *)(lVar5 + 8) = 0;
          }
          *(undefined4 *)(lVar5 + 0x10) = 0;
        }
      }
      *(undefined4 *)(lVar3 + 0x2c) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 0xc & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x60), lVar3 != 0)) {
      if (*(char *)(lVar3 + 0x10) != '\0') {
        *(undefined2 *)(lVar3 + 8) = 0;
      }
      *(undefined4 *)(lVar3 + 0x10) = 0;
      uVar2 = *(uint *)(param_1 + 0x74);
    }
    if (((uVar2 >> 0xd & 1) != 0) && (lVar3 = *(long *)(param_1 + 0x68), lVar3 != 0)) {
      if (*(char *)(lVar3 + 0x10) != '\0') {
        *(undefined1 *)(lVar3 + 8) = 0;
      }
      *(undefined4 *)(lVar3 + 0x10) = 0;
    }
  }
  *(undefined4 *)(param_1 + 0x74) = 0;
  return;
}


