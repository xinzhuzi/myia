import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.File;
import java.io.PrintWriter;

public class HuntR27 extends GhidraScript {
    PrintWriter out;
    DecompInterface dec;
    long base;

    void findString(String needle, String label) {
        out.println();
        out.println("== find \"" + needle + "\" (" + label + ") ==");
        try {
            ghidra.program.model.mem.MemoryBlock[] blocks = currentProgram.getMemory().getBlocks();
            byte[] pat = needle.getBytes("UTF-8");
            byte[] buf = new byte[1 << 20];
            int found = 0;
            for (ghidra.program.model.mem.MemoryBlock b : blocks) {
                if (!b.isInitialized()) continue;
                long len = b.getSize();
                for (long off = 0; off < len && found < 4; off += buf.length) {
                    int n = (int) Math.min(buf.length, len - off);
                    try { b.getBytes(b.getStart().add(off), buf, 0, n); } catch (Exception e) { break; }
                    for (int i = 0; i <= n - pat.length && found < 4; i++) {
                        boolean m = true;
                        for (int j = 0; j < pat.length; j++) { if (buf[i + j] != pat[j]) { m = false; break; } }
                        if (m) {
                            Address sAddr = b.getStart().add(off + i);
                            out.println("  str at rva 0x" + Long.toHexString(sAddr.getOffset() - base));
                            ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(sAddr);
                            int c = 0;
                            while (it.hasNext() && c < 5) {
                                Reference r = it.next();
                                Function f = getFunctionContaining(r.getFromAddress());
                                out.println("    <- from rva 0x" + Long.toHexString(r.getFromAddress().getOffset() - base)
                                    + " in func 0x" + Long.toHexString(f != null ? f.getEntryPoint().getOffset() - base : 0));
                                c++;
                            }
                            found++;
                            i += pat.length;
                        }
                    }
                }
                if (found >= 4) break;
            }
            if (found == 0) out.println("  (not found)");
        } catch (Exception e) { out.println("  ERR " + e.getMessage()); }
        out.flush();
    }

    @Override
    public void run() throws Exception {
        out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r27_out.txt"), "UTF-8");
        dec = new DecompInterface();
        dec.openProgram(currentProgram);
        base = currentProgram.getImageBase().getOffset();
        // 1) Req2Buf 桥函数内找 BLR 指令与函数边界
        Function f = getFunctionContaining(toAddr(base + 0x5daad24L));
        if (f != null) {
            out.println("== Req2Buf func " + Long.toHexString(f.getEntryPoint().getOffset() - base)
                + " .. " + Long.toHexString(f.getBody().getMaxAddress().getOffset() - base) + " ==");
            InstructionIterator it = currentProgram.getListing().getInstructions(f.getBody(), true);
            while (it.hasNext()) {
                Instruction ins = it.next();
                String mn = ins.getMnemonicString();
                if (mn.startsWith("blr") || mn.equals("ret")) {
                    out.println("  " + mn + " at rva 0x" + Long.toHexString(ins.getAddress().getOffset() - base)
                        + "  " + ins.toString());
                }
            }
        }
        out.flush();
        // 2) Buf2Resp / AutoBuffer 字符串锚
        findString("Buf2Resp", "buf2resp");
        findString("AutoBuffer", "autobuffer");
        out.println();
        out.println("HUNT_R27_DONE");
        out.close();
        dec.dispose();
    }
}
