package id.cycraft.cyberquest;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class CycraftCyberQuest extends JavaPlugin implements CommandExecutor, TabCompleter {

    private final Map<String, Challenge> challenges = new LinkedHashMap<>();
    private File dataFile;
    private FileConfiguration playerData;

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

        getLogger().info("CycraftCyberQuest initialized successfully with " + challenges.size() + " challenges!");
    }

    @Override
    public void onDisable() {
        savePlayerData();
        getLogger().info("CycraftCyberQuest data saved and disabled.");
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
}
