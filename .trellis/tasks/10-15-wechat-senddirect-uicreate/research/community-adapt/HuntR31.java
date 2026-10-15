import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.File;
import java.io.PrintWriter;

public class HuntR31 extends GhidraScript {
    @Override
    public void run() throws Exception {
        PrintWriter out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r31_out.txt"), "UTF-8");
        long base = currentProgram.getImageBase().getOffset();
        Address start = toAddr(base + 0x5db0e20L);
        Address end = toAddr(base + 0x5db0e80L);
        InstructionIterator it = currentProgram.getListing().getInstructions(start, true);
        while (it.hasNext()) {
            Instruction ins = it.next();
            if (ins.getAddress().getOffset() > end.getOffset()) break;
            out.println(String.format("0x%x: %s", ins.getAddress().getOffset() - base, ins));
        }
        out.close();
    }
}
