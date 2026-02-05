# PaperMC Server Setup (macOS)

Repo ini menyimpan konfigurasi dan skrip untuk menjalankan server Minecraft Java berbasis PaperMC di macOS (Apple Silicon). Fokusnya adalah kemudahan start/stop server, manajemen plugin, serta backup otomatis.

## Prasyarat
- macOS dengan akses Terminal.
- Java 21 (OpenJDK 21). Cek dengan `java -version`.
- PaperMC `paper.jar` (versi terbaru diletakkan di root repo).

## Struktur Penting
| File/Folder | Deskripsi |
| ----------- | --------- |
| `start.sh` | Skrip menjalankan PaperMC dengan Aikar flags untuk performa optimal. |
| `server.properties` | Konfigurasi utama server. Perbarui MOTD, seed, mode online/offline, dll. |
| `backup.sh` | Backup manual dunia + plugins (retensi 7 arsip). |
| `auto_backup.sh` | Loop auto-backup dengan interval menit. |
| `SERVER_MANUAL.md` | Manual lengkap operasi server (jalankan, port forwarding, troubleshooting). |
| `SETUP_GUIDE.md` | Panduan awal pembuatan server secara detail. |

## Menjalankan Server
```bash
./start.sh
```
Tunggu sampai muncul `Done (...)! For help, type "help"`. Terminal harus tetap terbuka. Ketik `stop` untuk mematikan secara bersih.

## Backup
- **Manual**: `./backup.sh` (disarankan setelah sesi bermain atau sebelum update plugin).
- **Otomatis**: `./auto_backup.sh 60` untuk backup tiap 60 menit. Jalankan di `screen/tmux` atau jadwalkan lewat `cron`.

## Mengatur Seed/World
1. Edit `server.properties` → set `level-seed=<angka>` (atau kosong untuk random).
2. Hentikan server dan hapus folder `world`, `world_nether`, `world_the_end` (backup dulu!).
3. Jalankan `./start.sh` untuk membuat dunia baru.

## Port Forwarding & Akses Teman
- Temukan IP lokal: `ipconfig getifaddr en0`.
- Forward port 25565 TCP/UDP ke IP tersebut pada router.
- Bagikan IP publik (`curl ifconfig.me`) atau hostname DDNS ke teman.

## Git Workflow
```bash
git status
git add <file>
git commit -m "pesan"
git push origin master
```

Selengkapnya: baca `SERVER_MANUAL.md` untuk tips whitelist, mode online/offline, troubleshooting, dan workflow harian.
