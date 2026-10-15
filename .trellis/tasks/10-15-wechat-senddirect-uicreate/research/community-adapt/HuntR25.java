import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.data.StringDataType;
import java.io.File;
import java.io.PrintWriter;

public class HuntR25 extends GhidraScript {
    PrintWriter out;
    long base;

    void findString(String needle, String label) {
        out.println();
        out.println("== find \"" + needle + "\" (" + label + ") ==");
        try {
            Address start = toAddr(base);
            int found = 0;
            byte[] pat = needle.getBytes("UTF-8");
            // 在前 0x10000000 的地址空间线性搜内存太慢;用 Ghidra defined data:
            // 遍历 memory,块搜
            ghidra.program.model.mem.Memory mem = currentProgram.getMemory();
            ghidra.program.model.mem.MemoryBlock[] blocks = mem.getBlocks();
            byte[] buf = new byte[1 << 20];
            for (ghidra.program.model.mem.MemoryBlock b : blocks) {
                if (!b.isInitialized()) continue;
                long len = b.getSize();
                for (long off = 0; off < len && found < 6; off += buf.length) {
                    int n = (int) Math.min(buf.length, len - off);
                    try { b.getBytes(b.getStart().add(off), buf, 0, n); } catch (Exception e) { break; }
                    for (int i = 0; i <= n - pat.length && found < 6; i++) {
                        boolean m = true;
                        for (int j = 0; j < pat.length; j++) { if (buf[i + j] != pat[j]) { m = false; break; } }
                        if (m) {
                            Address sAddr = b.getStart().add(off + i);
                            out.println("  str at rva 0x" + Long.toHexString(sAddr.getOffset() - base));
                            // xrefs to this address
                            ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(sAddr);
                            int c = 0;
                            while (it.hasNext() && c < 6) {
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
                if (found >= 6) break;
            }
            if (found == 0) out.println("  (not found)");
        } catch (Exception e) { out.println("  ERR " + e.getMessage()); }
        out.flush();
    }

    @Override
    public void run() throws Exception {
        out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r25_out.txt"), "UTF-8");
        base = currentProgram.getImageBase().getOffset();
        findString("MMStartTask", "anchor");
        findString("startTask", "mars-mangled-chunk");
        findString("Req2Buf", "req2buf");
        findString("N4mars3stn", "mars-stn-mangled");
        out.println();
        out.println("HUNT_R25_DONE");
        out.close();
    }
}
