import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import java.io.File;
import java.io.PrintWriter;

public class HuntR26 extends GhidraScript {
    PrintWriter out;
    DecompInterface dec;
    long base;

    void decompile(long rva, String label, int maxLines) {
        out.println();
        out.println("======== " + label + " rva=0x" + Long.toHexString(rva) + " ========");
        try {
            Function f = getFunctionContaining(toAddr(base + rva));
            if (f == null) { out.println("  (no function)"); return; }
            out.println("-- func entry=0x" + Long.toHexString(f.getEntryPoint().getOffset() - base));
            DecompileResults res = dec.decompileFunction(f, 180, monitor);
            if (res.decompileCompleted()) {
                String[] lines = res.getDecompiledFunction().getC().split("\n");
                for (int i = 0; i < lines.length && i < maxLines; i++) out.println(lines[i]);
                if (lines.length > maxLines) out.println("/* truncated " + lines.length + " */");
            } else out.println("  DECOMP FAILED: " + res.getErrorMessage());
        } catch (Exception e) { out.println("  ERR " + e.getMessage()); }
        out.flush();
    }

    @Override
    public void run() throws Exception {
        out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r26_out.txt"), "UTF-8");
        dec = new DecompInterface();
        dec.openProgram(currentProgram);
        base = currentProgram.getImageBase().getOffset();
        decompile(0x597eda0L, "MMST_REF_A", 120);
        decompile(0x5973938L, "MMST_REF_B", 150);
        decompile(0x5daad24L, "REQ2BUF_REF_A", 120);
        out.println();
        out.println("HUNT_R26_DONE");
        out.close();
        dec.dispose();
    }
}
