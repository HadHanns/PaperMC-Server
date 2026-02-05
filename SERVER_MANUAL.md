# PaperMC Server Manual

Panduan ringkas untuk mengoperasikan server Minecraft Paper pada macOS (Apple Silicon).

## 1. Struktur Direktori
```
Server Minecraft/
├── paper.jar              # Versi Paper terbaru
├── start.sh               # Skrip menjalankan server (Aikar flags)
├── backup.sh              # Backup manual (menyimpan world + plugins)
├── auto_backup.sh         # Loop auto-backup interval menit
├── server.properties      # Konfigurasi server
├── eula.txt               # Persetujuan EULA
├── config/, plugins/, logs/, world*, backups/
└── SETUP_GUIDE.md         # Panduan lengkap original
```

## 2. Persiapan & Menjalankan Server
1. Pastikan Java 21 sudah terpasang (`java -version`).
2. Buka terminal pada folder `Server Minecraft`.
3. Jalankan server:
   ```bash
   ./start.sh
   ```
4. Tunggu pesan `Done (...)! For help, type "help"`. Terminal harus tetap terbuka saat server aktif.

### Menghentikan Server
- Ketik `stop` di konsol server untuk shutdown bersih.
- Darurat (jika terminal hilang): `pkill -f "paper.jar --nogui"`.

## 3. Mengizinkan Player Bergabung
- **Mode Online (disarankan)**: `online-mode=true` (default). Semua pemain harus login akun resmi.
- **Mode Offline**: set `online-mode=false` bila ingin menerima pemain nonresmi. Pasang plugin autentikasi (mis. AuthMe) dan gunakan whitelist untuk keamanan.
- **Whitelist**: aktifkan dengan `white-list=true` di `server.properties`, lalu `whitelist add <nama>` di konsol.

## 4. Network & Port Forwarding
1. Temukan IP lokal Mac: `ipconfig getifaddr en0`.
2. Atur port forwarding router:
   - External/Internal Port: `25565`
   - Protocol: TCP/UDP
   - Internal IP: alamat lokal Mac
3. Bagikan IP publik (`curl ifconfig.me`) atau hostname DDNS ke teman.
4. Uji port menggunakan https://mcsrvstat.us atau https://yougetsignal.com/tools/open-ports/.

## 5. Backup
### 5.1 Backup Manual
1. (Opsional) ketik `stop` untuk memastikan data konsisten.
2. Jalankan: `./backup.sh`
3. Berkas baru akan muncul di `backups/backup_YYYY-MM-DD_HH-MM-SS.tar.gz` (hanya 7 arsip terakhir disimpan).

### 5.2 Auto-Backup Interval
1. Pastikan `backup.sh` executable (`chmod +x backup.sh`) – sudah dilakukan.
2. Jalankan loop otomatis (contoh setiap 60 menit):
   ```bash
   ./auto_backup.sh 60
   ```
3. Biarkan terminal berjalan atau gunakan `screen`/`tmux`. Tekan `Ctrl+C` untuk berhenti.
4. Bisa dijadwalkan lewat cron:
   ```bash
   crontab -e
   0 3 * * * /Users/YOUR_USER/Documents/Server\ Minecraft/backup.sh
   ```
   Ganti `YOUR_USER` dengan nama user macOS Anda.

## 6. Pemeliharaan
- **Update Paper**: unduh jar terbaru (https://papermc.io/downloads) dan timpa `paper.jar`, lalu jalankan `./start.sh` sekali untuk memastikan dunia naik tanpa error.
- **Update Plugin**: salin `.jar` baru ke folder `plugins/`, restart server.
- **Monitoring**: gunakan `/tps`, `/timings` (butuh plugin/perintah bawaan Paper) untuk mengecek performa.
- **Log**: lihat `logs/latest.log` untuk error/ketika pemain join.

## 7. Troubleshooting Singkat
| Gejala | Solusi |
| --- | --- |
| "Failed to verify username" | Pastikan pemain login akun resmi atau set `online-mode=false` (dengan risiko keamanan). |
| "Outdated server" | Pastikan `paper.jar` sesuai versi klien teman (mis. upgrade ke 1.21.11). |
| TPS rendah/lag | Kurangi `view-distance`, hapus plugin berat, tambah RAM (`-Xmx` di start.sh), jalankan `/timings`. |
| Tidak bisa join via internet | Pastikan port forwarding benar, firewall mengizinkan Java, IP publik terbaru dibagikan. |
| Backup tidak jalan | Pastikan `backup.sh` executable dan jalankan manual; cek output `auto_backup.sh` untuk error. |

## 8. Workflow Harian yang Disarankan
1. Jalankan `./start.sh` (bisa lewat `screen`/`tmux`).
2. Setelah sesi bermain: ketik `stop`.
3. Jalankan `./backup.sh` sebelum upgrade plugin/versi besar.
4. Secara berkala salin folder `backups/` ke media eksternal/cloud.

Selamat bermain! Manual ini bisa diperbarui bila ada script baru atau perubahan workflow.
