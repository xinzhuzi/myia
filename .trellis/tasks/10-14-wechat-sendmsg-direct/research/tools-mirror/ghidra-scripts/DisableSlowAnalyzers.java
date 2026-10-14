import ghidra.app.script.GhidraScript;

public class DisableSlowAnalyzers extends GhidraScript {
    @Override
    public void run() throws Exception {
        var opts = currentProgram.getOptions("Analysis");
        String[] off = {
            "Decompiler Switch Analysis",
            "Decompiler Parameter ID",
            "Non-Returning Functions - Discovered"
        };
        for (String name : off) {
            try { opts.setBoolean(name, false); println("disabled: " + name); }
            catch (Exception e) { println("skip: " + name + " (" + e.getClass().getSimpleName() + ")"); }
        }
    }
}
