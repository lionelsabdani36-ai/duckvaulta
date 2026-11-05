package id.cycraft.cyberquest;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.Action;
import org.bukkit.event.entity.EntityDamageEvent;
import org.bukkit.event.player.PlayerCommandPreprocessEvent;
import org.bukkit.event.player.PlayerInteractEvent;
import org.bukkit.event.player.PlayerMoveEvent;
import org.bukkit.event.player.PlayerPortalEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.util.Vector;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class CycraftCyberQuest extends JavaPlugin implements CommandExecutor, TabCompleter, Listener {

    private final Map<String, Challenge> challenges = new LinkedHashMap<>();
    private File dataFile;
    private FileConfiguration playerData;
    private final Map<UUID, Long> portalCooldowns = new HashMap<>();
    private final Map<UUID, Long> liftCooldowns = new HashMap<>();

    @Override
    public void onEnable() {
        saveDefaultConfig();
        loadChallenges();
        loadPlayerData();

        Objects.requireNonNull(getCommand("challenge")).setExecutor(this);
        Objects.requireNonNull(getCommand("challenge")).setTabCompleter(this);

        Objects.requireNonNull(getCommand("submit")).setExecutor(this);
        Objects.requireNonNull(getCommand("submit")).setTabCompleter(this);

        Objects.requireNonNull(getCommand("ctfstats")).setExecutor(this);
        Objects.requireNonNull(getCommand("answer")).setExecutor(this);
        Objects.requireNonNull(getCommand("lift")).setExecutor(this);
        Objects.requireNonNull(getCommand("blueprint")).setExecutor(this);
        Objects.requireNonNull(getCommand("blueprint")).setTabCompleter(this);
        Objects.requireNonNull(getCommand("lift")).setTabCompleter(this);

        getServer().getPluginManager().registerEvents(this, this);

        // Periodic safety watchdog for void skyblock
        Bukkit.getScheduler().runTaskTimer(this, this::checkVoidFallingPlayers, 10L, 5L);

        getLogger().info("CycraftCyberQuest v1.7.0 with Instant Direct RTP Engine active!");
    }

    @Override
    public void onDisable() {
        savePlayerData();
        getLogger().info("CycraftCyberQuest data saved.");
    }

    private void rescuePlayerFromVoid(Player player) {
        Location nexus = new Location(Bukkit.getWorld("cyber_skyblock"), 0.5, 65.0, 0.5, 0.0f, 0.0f);
        player.teleport(nexus);
        player.setFallDistance(0.0f);
        player.setVelocity(new Vector(0, 0, 0));
        player.playSound(nexus, Sound.ENTITY_ENDERMAN_TELEPORT, 1.0f, 1.0f);
        player.playSound(nexus, Sound.BLOCK_BEACON_ACTIVATE, 1.0f, 1.5f);
        player.sendMessage(ChatColor.DARK_AQUA + "==================================================");
        player.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "⚡ [CYBER RESCUE STABILIZER ACTIVATED] ⚡");
        player.sendMessage(ChatColor.WHITE + "Sistem anti-gravitasi mendeteksi Anda jatuh ke void.");
        player.sendMessage(ChatColor.GREEN + "Anda berhasil diselamatkan dan diteleportasi kembali ke Hub Nexus.");
        player.sendMessage(ChatColor.DARK_AQUA + "==================================================");
    }

    private void checkVoidFallingPlayers() {
        for (Player p : Bukkit.getOnlinePlayers()) {
            if (p.isOnline() && p.isValid()) {
                if (p.getWorld().getName().equalsIgnoreCase("cyber_skyblock")) {
                    if (p.getLocation().getY() < 48.0) {
                        rescuePlayerFromVoid(p);
                    }
                }
            }
        }
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onEntityDamage(EntityDamageEvent event) {
        if (event.getEntity() instanceof Player) {
            Player p = (Player) event.getEntity();
            if (p.getWorld().getName().equalsIgnoreCase("cyber_skyblock")) {
                if (event.getCause() == EntityDamageEvent.DamageCause.VOID) {
                    event.setCancelled(true);
                    rescuePlayerFromVoid(p);
                } else if (event.getCause() == EntityDamageEvent.DamageCause.FALL) {
                    event.setCancelled(true);
                }
            }
        }
    }

    @EventHandler(priority = EventPriority.NORMAL)
    public void onPlayerInteract(PlayerInteractEvent event) {
        Block clickedBlock = event.getClickedBlock();
        if (clickedBlock == null) return;
        Player player = event.getPlayer();

        // 1. Kinetic Cyber Jump Pads
        if (event.getAction() == Action.PHYSICAL) {
            if (clickedBlock.getType() == Material.HEAVY_WEIGHTED_PRESSURE_PLATE) {
                Block below = clickedBlock.getRelative(0, -1, 0);
                if (below.getType() == Material.SEA_LANTERN && player.getWorld().getName().equalsIgnoreCase("cyber_skyblock")) {
                    double bx = clickedBlock.getX();
                    double bz = clickedBlock.getZ();
                    double vx = 0;
                    double vz = 0;
                    double vy = 0.55;

                    if (Math.abs(bx) < 20 && Math.abs(bz) < 20) {
                        if (bz < -5) vz = -2.4; // North
                        else if (bz > 5) vz = 2.4; // South
                        else if (bx > 5) vx = 2.4; // East
                        else if (bx < -5) vx = -2.4; // West
                    } else {
                        if (bz < -30) vz = 2.4;
                        else if (bz > 30) vz = -2.4;
                        else if (bx > 30) vx = -2.4;
                        else if (bx < -30) vx = 2.4;
                    }

                    if (vx != 0 || vz != 0) {
                        player.setVelocity(new Vector(vx, vy, vz));
                        player.playSound(clickedBlock.getLocation(), Sound.ENTITY_FIREWORK_ROCKET_LAUNCH, 1.0f, 1.4f);
                        player.playSound(clickedBlock.getLocation(), Sound.BLOCK_BEACON_POWER_SELECT, 1.0f, 1.8f);
                        player.sendTitle(ChatColor.AQUA + "⚡ KINETIC BOOST ⚡", ChatColor.YELLOW + "Transit Skybridge Berkecepatan Tinggi", 2, 20, 5);
                        return;
                    }
                }
            }
        }

        // 2. Elevator Interaction
        if (event.getAction() == Action.RIGHT_CLICK_BLOCK || event.getAction() == Action.PHYSICAL) {
            Location loc = clickedBlock.getLocation();
            if (loc.getWorld().getName().equalsIgnoreCase("cyber_skyblock")) {
                if ((loc.getBlockX() == 8 || loc.getBlockX() == 7 || loc.getBlockX() == 9) &&
                    (loc.getBlockZ() == 6 || loc.getBlockZ() == 7 || loc.getBlockZ() == 8)) {
                    int y = loc.getBlockY();
                    if (y >= 64 && y <= 93) {
                        sendElevatorMenu(player);
                    }
                }
            }
        }
    }

    // Direct Instant RTP Command Router: Handles /rtp, /wild, /survival, /smp, /warp survival
    @EventHandler(priority = EventPriority.HIGHEST)
    public void onPlayerCommand(PlayerCommandPreprocessEvent event) {
        String msg = event.getMessage().toLowerCase().trim();
        if (msg.equals("/rtp") || msg.startsWith("/rtp ") ||
            msg.equals("/wild") || msg.startsWith("/wild ") ||
            msg.equals("/randomtp") || msg.startsWith("/randomtp ") ||
            msg.equals("/warp survival") || msg.startsWith("/warp survival ") ||
            msg.equals("/survival") || msg.equals("/smp")) {

            event.setCancelled(true);
            Player player = event.getPlayer();
            player.sendMessage(ChatColor.DARK_AQUA + "==================================================");
            player.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "⚡ [CYCRAFT INSTANT RTP] ⚡");
            player.sendMessage(ChatColor.YELLOW + "Mencari safe zone instan di alam liar Survival Overworld...");
            player.sendMessage(ChatColor.DARK_AQUA + "==================================================");

            // Directly execute AsyncRTP from console to teleport player to pre-cached safe surface chunk in world
            Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "rtp " + player.getName() + " world world");
        }
    }

    // Portal Touch Handler: Stepping into Nether Portals
    @EventHandler(priority = EventPriority.HIGHEST)
    public void onPlayerPortal(PlayerPortalEvent event) {
        Player player = event.getPlayer();
        event.setCancelled(true);

        long now = System.currentTimeMillis();
        if (portalCooldowns.containsKey(player.getUniqueId()) && (now - portalCooldowns.get(player.getUniqueId()) < 3000)) {
            return;
        }
        portalCooldowns.put(player.getUniqueId(), now);

        String worldName = player.getWorld().getName();
        if (worldName.equalsIgnoreCase("cyber_skyblock")) {
            player.sendTitle(ChatColor.AQUA + "" + ChatColor.BOLD + "🌌 SANCTUARY SURVIVAL 🌌",
                             ChatColor.YELLOW + "Teleportasi instan ke alam liar...", 5, 30, 10);
            Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "rtp " + player.getName() + " world world");
        } else if (worldName.equalsIgnoreCase("world")) {
            World targetWorld = Bukkit.getWorld("cyber_skyblock");
            if (targetWorld != null) {
                Location dest = new Location(targetWorld, 0.5, 65.0, 0.5, 0.0f, 0.0f);
                player.teleport(dest);
                player.playSound(dest, Sound.ENTITY_ENDERMAN_TELEPORT, 1.0f, 1.0f);
                player.playSound(dest, Sound.BLOCK_BEACON_ACTIVATE, 0.7f, 1.4f);
                player.sendTitle(ChatColor.DARK_AQUA + "" + ChatColor.BOLD + "⚡ CYBER CITADEL ⚡",
                                 ChatColor.AQUA + "Kembali ke Pusat Nexus Skyblock", 10, 40, 10);
            }
        }
    }

    // Spatial Portal Trigger
    @EventHandler(priority = EventPriority.NORMAL)
    public void onPlayerMove(PlayerMoveEvent event) {
        Player player = event.getPlayer();
        Location loc = player.getLocation();
        String worldName = loc.getWorld().getName();

        long now = System.currentTimeMillis();
        if (portalCooldowns.containsKey(player.getUniqueId()) && (now - portalCooldowns.get(player.getUniqueId()) < 3000)) {
            return;
        }

        if (worldName.equalsIgnoreCase("cyber_skyblock")) {
            boolean inLobbyPortal = (loc.getX() >= -2.5 && loc.getX() <= 2.5 &&
                                     loc.getY() >= 64.0 && loc.getY() <= 70.0 &&
                                     loc.getZ() >= 9.5 && loc.getZ() <= 12.5);

            boolean inHighwayPortal = (loc.getX() >= -5.0 && loc.getX() <= 5.0 &&
                                       loc.getY() >= 64.0 && loc.getY() <= 74.0 &&
                                       loc.getZ() >= 62.0 && loc.getZ() <= 68.0);

            if (inLobbyPortal || inHighwayPortal) {
                portalCooldowns.put(player.getUniqueId(), now);
                player.sendTitle(ChatColor.AQUA + "" + ChatColor.BOLD + "🌌 SANCTUARY SURVIVAL 🌌",
                                 ChatColor.YELLOW + "Teleportasi instan ke alam liar...", 5, 30, 10);
                Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "rtp " + player.getName() + " world world");
            }
        } else if (worldName.equalsIgnoreCase("world")) {
            if (loc.getX() >= 60.0 && loc.getX() <= 69.0 &&
                loc.getY() >= 82.0 && loc.getY() <= 90.0 &&
                loc.getZ() >= -108.0 && loc.getZ() <= -102.0) {

                World targetWorld = Bukkit.getWorld("cyber_skyblock");
                if (targetWorld != null) {
                    portalCooldowns.put(player.getUniqueId(), now);
                    Location dest = new Location(targetWorld, 0.5, 65.0, 0.5, 0.0f, 0.0f);
                    player.teleport(dest);
                    player.playSound(dest, Sound.ENTITY_ENDERMAN_TELEPORT, 1.0f, 1.0f);
                    player.playSound(dest, Sound.BLOCK_BEACON_ACTIVATE, 0.7f, 1.4f);
                    player.sendTitle(ChatColor.DARK_AQUA + "" + ChatColor.BOLD + "⚡ CYBER CITADEL ⚡",
                                     ChatColor.AQUA + "Kembali ke Pusat Nexus Skyblock", 10, 40, 10);
                }
            }
        }
    }

    private void sendElevatorMenu(Player player) {
        player.sendMessage(ChatColor.DARK_AQUA + "==================================================");
        player.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "⚡ CYBER CITADEL EXPRESS LIFT ⚡");
        player.sendMessage(ChatColor.GRAY + "Gunakan perintah: " + ChatColor.YELLOW + "/lift <lantai>");
        player.sendMessage(ChatColor.WHITE + " • " + ChatColor.AQUA + "/lift 1 " + ChatColor.GRAY + "(Lobby & Grand Rotunda - Y: 65)");
        player.sendMessage(ChatColor.WHITE + " • " + ChatColor.AQUA + "/lift 2 " + ChatColor.GRAY + "(Cyber Security Operations Center - Y: 74)");
        player.sendMessage(ChatColor.WHITE + " • " + ChatColor.AQUA + "/lift 3 " + ChatColor.GRAY + "(Executive Lounge & Briefing - Y: 83)");
        player.sendMessage(ChatColor.WHITE + " • " + ChatColor.AQUA + "/lift 4 " + ChatColor.GRAY + "(Skyport Terminal & Helipad - Y: 92)");
        player.sendMessage(ChatColor.DARK_AQUA + "==================================================");
    }

    public void loadChallenges() {
        challenges.clear();
        FileConfiguration config = getConfig();
        if (config.isConfigurationSection("challenges")) {
            for (String key : Objects.requireNonNull(config.getConfigurationSection("challenges")).getKeys(false)) {
                String path = "challenges." + key + ".";
                String name = config.getString(path + "name", "Unnamed Challenge");
                String category = config.getString(path + "category", "General");
                String desc = config.getString(path + "description", "No description provided.");
                String hint = config.getString(path + "hint", "No hint available.");
                String flag = config.getString(path + "flag", "FLAG{default}");
                int cybits = config.getInt(path + "reward_cybits", 500);
                int blocks = config.getInt(path + "reward_claim_blocks", 50);
                int diamonds = config.getInt(path + "reward_diamonds", 5);

                challenges.put(key.toLowerCase(), new Challenge(key, name, category, desc, hint, flag, cybits, blocks, diamonds));
            }
        }
    }

    private void loadPlayerData() {
        dataFile = new File(getDataFolder(), "player_data.yml");
        if (!dataFile.exists()) {
            try {
                dataFile.getParentFile().mkdirs();
                dataFile.createNewFile();
            } catch (IOException e) {
                getLogger().severe("Could not create player_data.yml: " + e.getMessage());
            }
        }
        playerData = YamlConfiguration.loadConfiguration(dataFile);
    }

    private void savePlayerData() {
        if (dataFile != null && playerData != null) {
            try {
                playerData.save(dataFile);
            } catch (IOException e) {
                getLogger().severe("Could not save player_data.yml: " + e.getMessage());
            }
        }
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        String cmdName = command.getName().toLowerCase();

        if (cmdName.equals("challenge")) {
            return handleChallengeCommand(sender, args);
        } else if (cmdName.equals("submit")) {
            return handleSubmitCommand(sender, args);
        } else if (cmdName.equals("ctfstats")) {
            return handleStatsCommand(sender, args);
        }
        return false;
    }

    private boolean handleChallengeCommand(CommandSender sender, String[] args) {
        if (args.length == 0) {
            sendChallengeList(sender);
            return true;
        }

        String sub = args[0].toLowerCase();
        if (sub.equals("reload") && sender.hasPermission("cycraft.admin")) {
            reloadConfig();
            loadChallenges();
            sender.sendMessage(ChatColor.GREEN + "[CYCRAFT CTF] Konfigurasi challenge berhasil dimuat ulang (" + challenges.size() + " aktif)!");
            return true;
        }

        if (challenges.containsKey(sub)) {
            sendChallengeDetail(sender, challenges.get(sub));
            return true;
        }

        sender.sendMessage(ChatColor.RED + "Tantangan dengan ID '" + args[0] + "' tidak ditemukan. Ketik /challenge untuk daftar lengkap.");
        return true;
    }

    private void sendChallengeList(CommandSender sender) {
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
        sender.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "       ⚡ CYCRAFT SMP - CYBER CHALLENGE NEXUS ⚡");
        sender.sendMessage(ChatColor.GRAY + " Selesaikan misi cybersecurity dan raih reward CyBits & Claim Blocks!");
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");

        String playerUuid = (sender instanceof Player) ? ((Player) sender).getUniqueId().toString() : "CONSOLE";
        List<String> solved = playerData.getStringList("players." + playerUuid + ".solved");

        for (Challenge ch : challenges.values()) {
            boolean isSolved = solved.contains(ch.getId().toLowerCase());
            String status = isSolved ? ChatColor.GREEN + " [SELESAI ✔]" : ChatColor.YELLOW + " [TERBUKA 🔓]";
            sender.sendMessage(ChatColor.GOLD + "▶ " + ChatColor.WHITE + ChatColor.BOLD + ch.getId().toUpperCase() + ": " 
                    + ChatColor.AQUA + ch.getName() + status);
            sender.sendMessage(ChatColor.DARK_AQUA + "   Kategori: " + ChatColor.WHITE + ch.getCategory() 
                    + ChatColor.DARK_GRAY + " | " + ChatColor.GOLD + "Hadiah: " + ChatColor.YELLOW + ch.getCybits() + " CyBits, " 
                    + ChatColor.GREEN + "+" + ch.getClaimBlocks() + " Claim Blocks");
        }

        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
        sender.sendMessage(ChatColor.GRAY + "Ketik: " + ChatColor.YELLOW + "/challenge <id>" + ChatColor.GRAY + " untuk rincian soal.");
        sender.sendMessage(ChatColor.GRAY + "Ketik: " + ChatColor.AQUA + "/submit <flag>" + ChatColor.GRAY + " untuk mengirimkan jawaban.");
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
    }

    private void sendChallengeDetail(CommandSender sender, Challenge ch) {
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
        sender.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "MISI: " + ChatColor.WHITE + ch.getName().toUpperCase());
        sender.sendMessage(ChatColor.GRAY + "ID: " + ChatColor.YELLOW + ch.getId().toUpperCase() + ChatColor.DARK_GRAY + " | " 
                + ChatColor.GRAY + "Kategori: " + ChatColor.DARK_AQUA + ch.getCategory());
        sender.sendMessage("");
        sender.sendMessage(ChatColor.WHITE + ch.getDescription());
        sender.sendMessage("");
        sender.sendMessage(ChatColor.GOLD + "Petunjuk (Hint): " + ChatColor.ITALIC + ChatColor.GRAY + ch.getHint());
        sender.sendMessage(ChatColor.LIGHT_PURPLE + "Hadiah Eksekusi:");
        sender.sendMessage(ChatColor.YELLOW + " • " + ch.getCybits() + " CyBits (Saldo Server)");
        sender.sendMessage(ChatColor.GREEN + " • " + ch.getClaimBlocks() + " Bonus Claim Blocks (Proteksi Tanah)");
        sender.sendMessage(ChatColor.AQUA + " • " + ch.getDiamonds() + " Butir Berlian");
        sender.sendMessage("");
        sender.sendMessage(ChatColor.GRAY + "Kirim jawaban dengan: " + ChatColor.AQUA + "/submit " + ChatColor.YELLOW + "<flag>");
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
    }

    private boolean handleSubmitCommand(CommandSender sender, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(ChatColor.RED + "Perintah ini hanya dapat dijalankan oleh player in-game!");
            return true;
        }

        if (args.length == 0) {
            sender.sendMessage(ChatColor.RED + "Gunakan: /submit <flag>");
            sender.sendMessage(ChatColor.GRAY + "Contoh: /submit CYBER{sql_injection_bypass_2026}");
            return true;
        }

        Player player = (Player) sender;
        String rawInput = String.join(" ", args).trim();
        String playerUuid = player.getUniqueId().toString();

        List<String> solvedList = new ArrayList<>(playerData.getStringList("players." + playerUuid + ".solved"));

        Challenge matched = null;
        for (Challenge ch : challenges.values()) {
            if (ch.getFlag().equalsIgnoreCase(rawInput)) {
                matched = ch;
                break;
            }
        }

        if (matched == null) {
            player.playSound(player.getLocation(), Sound.ENTITY_VILLAGER_NO, 1.0f, 0.8f);
            player.sendMessage(ChatColor.RED + "" + ChatColor.BOLD + "[ACCESS DENIED] " 
                    + ChatColor.RED + "Flag tidak valid atau hash verifikasi tidak cocok. Coba periksa kembali payload Anda!");
            return true;
        }

        String challId = matched.getId().toLowerCase();
        if (solvedList.contains(challId)) {
            player.sendMessage(ChatColor.YELLOW + "[PERINGATAN] Anda sudah pernah menyelesaikan tantangan " + matched.getName() + " sebelumnya!");
            return true;
        }

        // Mark as solved
        solvedList.add(challId);
        playerData.set("players." + playerUuid + ".name", player.getName());
        playerData.set("players." + playerUuid + ".solved", solvedList);
        int totalSolved = solvedList.size();
        playerData.set("players." + playerUuid + ".total_solved", totalSolved);
        savePlayerData();

        // Award rewards
        // 1. Vault Money via console command
        Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "eco give " + player.getName() + " " + matched.getCybits());
        // 2. Claim Blocks via GriefPrevention
        Bukkit.dispatchCommand(Bukkit.getConsoleSender(), "adjustbonusclaimblocks " + player.getName() + " " + matched.getClaimBlocks());
        // 3. Diamonds item
        if (matched.getDiamonds() > 0) {
            player.getInventory().addItem(new ItemStack(Material.DIAMOND, matched.getDiamonds()));
        }

        // Sound & Effects
        player.playSound(player.getLocation(), Sound.UI_TOAST_CHALLENGE_COMPLETE, 1.0f, 1.2f);
        player.playSound(player.getLocation(), Sound.ENTITY_PLAYER_LEVELUP, 1.0f, 1.0f);

        // Individual notification
        player.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
        player.sendMessage(ChatColor.GREEN + "" + ChatColor.BOLD + "✔ [FLAG ACCEPTED] MISI BERHASIL DITEMBUS! ✔");
        player.sendMessage(ChatColor.AQUA + "Tantangan: " + ChatColor.WHITE + matched.getName());
        player.sendMessage(ChatColor.GOLD + "Reward yang diterima:");
        player.sendMessage(ChatColor.YELLOW + " + " + matched.getCybits() + " CyBits");
        player.sendMessage(ChatColor.GREEN + " + " + matched.getClaimBlocks() + " Claim Blocks");
        player.sendMessage(ChatColor.AQUA + " + " + matched.getDiamonds() + " Berlian");
        player.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");

        // Server-wide broadcast
        Bukkit.broadcastMessage(ChatColor.DARK_GRAY + "[" + ChatColor.AQUA + ChatColor.BOLD + "CYCRAFT CTF" 
                + ChatColor.DARK_GRAY + "] " + ChatColor.GREEN + ChatColor.BOLD + player.getName() 
                + ChatColor.GRAY + " berhasil memecahkan " + ChatColor.YELLOW + ChatColor.BOLD + matched.getName() 
                + ChatColor.GRAY + " (" + ChatColor.AQUA + matched.getCategory() + ChatColor.GRAY + ")!");

        return true;
    }

    private boolean handleStatsCommand(CommandSender sender, String[] args) {
        String targetName = (args.length > 0) ? args[0] : (sender instanceof Player ? sender.getName() : null);
        if (targetName == null) {
            sender.sendMessage(ChatColor.RED + "Gunakan: /ctfstats <player>");
            return true;
        }

        String targetUuid = null;
        Player targetPlayer = Bukkit.getPlayer(targetName);
        if (targetPlayer != null) {
            targetUuid = targetPlayer.getUniqueId().toString();
        } else {
            // search in config
            if (playerData.isConfigurationSection("players")) {
                for (String uid : Objects.requireNonNull(playerData.getConfigurationSection("players")).getKeys(false)) {
                    if (targetName.equalsIgnoreCase(playerData.getString("players." + uid + ".name"))) {
                        targetUuid = uid;
                        break;
                    }
                }
            }
        }

        if (targetUuid == null || !playerData.contains("players." + targetUuid)) {
            sender.sendMessage(ChatColor.RED + "Data statistik untuk player '" + targetName + "' tidak ditemukan.");
            return true;
        }

        List<String> solved = playerData.getStringList("players." + targetUuid + ".solved");
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
        sender.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "PROFIL HACKER CYCRAFT: " + ChatColor.YELLOW + targetName);
        sender.sendMessage(ChatColor.GRAY + "Total Misi Selesai: " + ChatColor.GREEN + solved.size() + " / " + challenges.size());
        sender.sendMessage(ChatColor.GRAY + "Daftar Solve: " + ChatColor.WHITE + (solved.isEmpty() ? "Belum ada" : String.join(", ", solved)));
        sender.sendMessage(ChatColor.DARK_GRAY + "--------------------------------------------------");
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        String cmdName = command.getName().toLowerCase();
        if (cmdName.equals("challenge")) {
            if (args.length == 1) {
                List<String> list = new ArrayList<>(challenges.keySet());
                if (sender.hasPermission("cycraft.admin")) list.add("reload");
                return list;
            }
        }
        return Collections.emptyList();
    }

    private boolean handleAnswerCommand(CommandSender sender) {
        if (!(sender instanceof Player)) return true;
        Player p = (Player) sender;
        p.sendMessage(ChatColor.DARK_AQUA + "==================================================");
        p.sendMessage(ChatColor.AQUA + "" + ChatColor.BOLD + "⚡ CYSEC VALIDATOR TERMINAL ⚡");
        p.sendMessage(ChatColor.GRAY + "Untuk mengirimkan flag bukti eksekusi, ketik:");
        p.sendMessage(ChatColor.YELLOW + "  /submit <flag>");
        p.sendMessage(ChatColor.GRAY + "Contoh: " + ChatColor.WHITE + "/submit CYBER{sql_injection_bypass_2026}");
        p.sendMessage(ChatColor.DARK_AQUA + "==================================================");
        return true;
    }

    private boolean handleLiftCommand(CommandSender sender, String[] args) {
        if (!(sender instanceof Player)) return true;
        Player p = (Player) sender;
        if (!p.getWorld().getName().equalsIgnoreCase("cyber_skyblock")) {
            p.sendMessage(ChatColor.RED + "Express Lift hanya tersedia di dalam Cyber Citadel!");
            return true;
        }
        if (args.length == 0) {
            sendElevatorMenu(p);
            return true;
        }
        String floor = args[0].toLowerCase();
        double targetY = 65.0;
        String floorName = "Lobby";
        if (floor.equals("1") || floor.equals("lobby")) {
            targetY = 65.0; floorName = "Lobby";
        } else if (floor.equals("2") || floor.equals("csoc")) {
            targetY = 74.0; floorName = "CSOC Hub";
        } else if (floor.equals("3") || floor.equals("lounge")) {
            targetY = 83.0; floorName = "Executive Lounge";
        } else if (floor.equals("4") || floor.equals("helipad") || floor.equals("skyport")) {
            targetY = 92.0; floorName = "Skyport Terminal";
        } else {
            p.sendMessage(ChatColor.RED + "Lantai tidak valid. Pilih 1, 2, 3, atau 4.");
            return true;
        }
        Location dest = new Location(p.getWorld(), 8.5, targetY, 7.5, p.getLocation().getYaw(), p.getLocation().getPitch());
        p.teleport(dest);
        p.playSound(dest, Sound.BLOCK_IRON_DOOR_OPEN, 1.0f, 1.2f);
        p.playSound(dest, Sound.BLOCK_BEACON_POWER_SELECT, 1.0f, 1.5f);
        p.sendTitle(ChatColor.AQUA + "⚡ EXPRESS LIFT ⚡", ChatColor.YELLOW + "Tiba di Lantai: " + floorName, 5, 25, 5);
        return true;
    }

    private boolean handleBlueprintCommand(CommandSender sender, String[] args) {
        sender.sendMessage(ChatColor.DARK_AQUA + "==================================================");
        sender.sendMessage(ChatColor.GOLD + "" + ChatColor.BOLD + "📐 CHIEF ARCHITECT SPADE - BLUEPRINTS 📐");
        sender.sendMessage(ChatColor.GRAY + "Megastruktur Terverifikasi di Cycraft SMP:");
        sender.sendMessage(ChatColor.YELLOW + " 1. Cyber Citadel Central Rotunda & Spire (X: 0, Z: 0)");
        sender.sendMessage(ChatColor.YELLOW + " 2. Roman-Cyber Colosseum & Porta Gladiatoria (X: 75, Z: 0)");
        sender.sendMessage(ChatColor.YELLOW + " 3. Valkyrie-01 Sky Dreadnought Carrier (X: 0, Y: 100, Z: 0)");
        sender.sendMessage(ChatColor.YELLOW + " 4. Sanctuary Survival Overworld Gateway (X: 64, Z: -96)");
        sender.sendMessage(ChatColor.DARK_AQUA + "==================================================");
        return true;
    }

}
