// Bounded read-only inspection of typed data surrounding a proven table slot.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class OfflineContractTable extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 4) throw new IllegalArgumentException("out sha table count");
        if (!args[1].equals(currentProgram.getExecutableSHA256())) throw new IllegalStateException("wrong binary");
        long start = Long.decode(args[2]);
        int count = Integer.decode(args[3]);
        if (count < 1 || count > 64) throw new IllegalArgumentException("bounded count");
        Path out = Path.of(args[0]).resolve("table.tsv");
        try (PrintWriter rows = new PrintWriter(Files.newBufferedWriter(out, StandardOpenOption.CREATE_NEW))) {
            for (int i = 0; i < count; i++) {
                monitor.checkCancelled();
                Address address = toAddr(start + i * 8);
                Data data = getDataAt(address);
                rows.println("DATA\t" + address + "\t" + (data == null ? "NO_DATA" : data.getDefaultValueRepresentation()));
                Reference[] refs = getReferencesTo(address);
                rows.println("REFS\t" + address + "\t" + refs.length);
                for (int j = 0; j < Math.min(refs.length, 32); j++) {
                    Reference ref = refs[j];
                    Function function = getFunctionContaining(ref.getFromAddress());
                    rows.println(ref.getFromAddress() + "\t" + ref.getReferenceType() + "\t"
                        + (function == null ? "NO_FUNCTION" : function.getEntryPoint() + " " + function.getName()));
                }
            }
        }
    }
}
