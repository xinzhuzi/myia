import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.File;
import java.io.PrintWriter;

public class HuntR32 extends GhidraScript {
    @Override
    public void run() throws Exception {
        PrintWriter out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r32_out.txt"), "UTF-8");
        long base = currentProgram.getImageBase().getOffset();
        Function f = getFunctionContaining(toAddr(base + 0x5daa3e4L));
        if (f == null) { out.println("(no function)"); out.close(); return; }
        long entry = f.getEntryPoint().getOffset() - base;
        long end = f.getBody().getMaxAddress().getOffset() - base;
        out.println("FUNC entry=0x" + Long.toHexString(entry) + " end=0x" + Long.toHexString(end));
        InstructionIterator it = currentProgram.getListing().getInstructions(toAddr(base + entry), true);
        int n = 0;
        while (it.hasNext()) {
            Instruction ins = it.next();
            if (ins.getAddress().getOffset() - base > end) break;
            String mn = ins.getMnemonicString();
            if (n < 40 || mn.startsWith("blr") || mn.equals("ret")) {
                out.println(String.format("0x%x: %s", ins.getAddress().getOffset() - base, ins));
            }
            n++;
            if (n > 400) break;
        }
        out.close();
    }
}
