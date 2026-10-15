import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.File;
import java.io.PrintWriter;

public class HuntR30 extends GhidraScript {
    PrintWriter out;
    long base;

    void disasm(long rva, String label) {
        out.println();
        out.println("== " + label + " disasm ==");
        try {
            Function f = getFunctionContaining(toAddr(base + rva));
            if (f == null) { out.println("(no function)"); return; }
            long entry = f.getEntryPoint().getOffset() - base;
            long end = f.getBody().getMaxAddress().getOffset() - base;
            out.println("-- entry=0x" + Long.toHexString(entry) + " end=0x" + Long.toHexString(end));
            InstructionIterator it = currentProgram.getListing().getInstructions(toAddr(base + entry), true);
            int n = 0;
            while (it.hasNext() && n < 90) {
                Instruction ins = it.next();
                if (ins.getAddress().getOffset() - base > end) break;
                String mn = ins.getMnemonicString();
                if (n < 30 || mn.startsWith("blr") || mn.equals("ret") || mn.startsWith("cbz") || mn.startsWith("cbnz") || mn.startsWith("tbz") || mn.startsWith("tbnz")) {
                    out.println(String.format("  0x%x: %s", ins.getAddress().getOffset() - base, ins));
                }
                n++;
            }
            out.println("  (total ins shown cap 90)");
        } catch (Exception e) { out.println("ERR " + e); }
        out.flush();
    }

    @Override
    public void run() throws Exception {
        out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r30_out.txt"), "UTF-8");
        base = currentProgram.getImageBase().getOffset();
        disasm(0x5980a6cL, "CAND_A_05980a6c");
        disasm(0x5db0db8L, "CAND_B_05db0db8");
        out.println("HUNT_R30_DONE");
        out.close();
    }
}
