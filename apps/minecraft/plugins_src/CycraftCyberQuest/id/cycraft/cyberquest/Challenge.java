package id.cycraft.cyberquest;

public class Challenge {
    private final String id;
    private final String name;
    private final String category;
    private final String description;
    private final String hint;
    private final String flag;
    private final int cybits;
    private final int claimBlocks;
    private final int diamonds;

    public Challenge(String id, String name, String category, String description, String hint, String flag, int cybits, int claimBlocks, int diamonds) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.description = description;
        this.hint = hint;
        this.flag = flag;
        this.cybits = cybits;
        this.claimBlocks = claimBlocks;
        this.diamonds = diamonds;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public String getCategory() { return category; }
    public String getDescription() { return description; }
    public String getHint() { return hint; }
    public String getFlag() { return flag; }
    public int getCybits() { return cybits; }
    public int getClaimBlocks() { return claimBlocks; }
    public int getDiamonds() { return diamonds; }
}
