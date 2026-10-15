import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.File;
import java.io.PrintWriter;

public class HuntR33 extends GhidraScript {
    @Override
    public void run() throws Exception {
        PrintWriter out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r33_out.txt"), "UTF-8");
        long base = currentProgram.getImageBase().getOffset();
        Address start = toAddr(base + 0x5980a6cL);
        Address end = toAddr(base + 0x5980d73L);
        InstructionIterator it = currentProgram.getListing().getInstructions(start, true);
        while (it.hasNext()) {
            Instruction ins = it.next();
            if (ins.getAddress().getOffset() > end.getOffset()) break;
            out.println(String.format("0x%x: %s", ins.getAddress().getOffset() - base, ins));
        }
        out.close();
    }
}
