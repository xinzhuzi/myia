// Bounded function inventory in a selected frozen-code region; no target execution.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class OfflineDispatchInventory extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 4) throw new IllegalArgumentException("out sha start end");
        if (!args[1].equals(currentProgram.getExecutableSHA256())) throw new IllegalStateException("wrong binary");
        long start = Long.decode(args[2]), end = Long.decode(args[3]);
        if (end <= start || end - start > 0x20000) throw new IllegalArgumentException("bounded region");
        FunctionIterator functions = currentProgram.getFunctionManager().getFunctions(toAddr(start), true);
        try (PrintWriter rows = new PrintWriter(Files.newBufferedWriter(Path.of(args[0]).resolve("inventory.tsv"), StandardOpenOption.CREATE_NEW))) {
            int count = 0;
            while (functions.hasNext()) {
                monitor.checkCancelled();
                Function function = functions.next();
                if (function.getEntryPoint().getOffset() >= end) break;
                if (++count > 256) throw new IllegalStateException("function limit");
                int indirect = 0;
                InstructionIterator insns = currentProgram.getListing().getInstructions(function.getBody(), true);
                while (insns.hasNext()) {
                    Instruction instruction = insns.next();
                    if (instruction.getMnemonicString().equals("blr")) indirect++;
                }
                rows.println(function.getEntryPoint() + "\t" + function.getBody().getNumAddresses() + "\t" + indirect);
            }
        }
    }
}
