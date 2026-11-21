# TamaPoke 1.19-pika

皮卡丘內建圖像版的公開備份，適用 **Waveshare ESP32-S3-Touch-AMOLED-1.75**（16 MB Flash、8 MB OPI PSRAM）。

基於 [socquique/TamaPoke](https://github.com/socquique/TamaPoke) 的 [`00136942`](https://github.com/socquique/TamaPoke/commit/00136942f42c651ceb75fbfef8499a2df945cde7)，保留原作者授權與署名。

這版將皮卡丘 #25、雷丘 #26 的一般與異色動畫放進韌體，缺少 microSD 圖像時直接使用內建資料。`SPEC 25` 指令會切換成一般皮卡丘、離開初始選角畫面並立即存檔。其他未內建的角色仍需 microSD 圖像。

![內建皮卡丘動畫的第一幀](assets/p025-preview.png)

## 已保存的版本

[v1.19-pika 下載頁](https://github.com/MAXXTANG/TamaPoke-Pikachu-Public/releases/tag/archive-2026-11-21) 提供韌體與完整留存 ZIP。

| 檔案 | 燒錄位址 | 用途與驗證 |
| --- | --- | --- |
| `firmware/tamapoke-1.19-pika-app.bin` | `0x10000` | 本次實際刷入的檔案；寫入雜湊校驗、開機及重開機後角色保存已驗證。適用已有相同 TamaPoke 分割表的板子。 |
| `firmware/tamapoke-1.19-pika-factory.bin` | `0x0` | 原版 v1.19 開機區與分割表，加上相同自訂應用程式；供全新安裝。這個整合檔尚未整包重刷驗證。 |
| `firmware/SHA256SUMS` | — | 兩個韌體檔的 SHA-256。 |

實機驗證的應用程式 SHA-256：

```text
d5da1d790d8794f92d8db0ff8cbbcffaaeb5ca0e3b7642451944a94e2133edbe
```

## 刷回這版

在倉庫根目錄執行。將連接埠換成電腦實際辨識到的名稱；macOS 例如 `/dev/cu.usbmodem1101`。

```bash
python3 -m pip install esptool==5.3.0 pyserial
cd firmware
shasum -a 256 -c SHA256SUMS
cd ..
```

已有相同 TamaPoke 分割表時，更新應用程式可保留現有存檔：

```bash
python3 -m esptool --chip esp32s3 --port /dev/cu.usbmodem1101 \
  write-flash 0x10000 firmware/tamapoke-1.19-pika-app.bin
python3 tools/select_pikachu.py --port /dev/cu.usbmodem1101
```

全新安裝會清除板內存檔與設定；使用相容的 1.75 板型：

```bash
python3 -m esptool --chip esp32s3 --port /dev/cu.usbmodem1101 \
  write-flash --erase-all 0x0 firmware/tamapoke-1.19-pika-factory.bin
python3 tools/select_pikachu.py --port /dev/cu.usbmodem1101
```

韌體檔包含遊戲程式與內建圖像。全新安裝後執行選角工具，才會直接設定為皮卡丘。公開韌體不含個人的遊戲存檔；原機 Flash 與存檔由擁有者另行私下備份。

## 2026-11-21 公開專案封存

[archive-2026-11-21](https://github.com/MAXXTANG/TamaPoke-Pikachu-Public/releases/tag/archive-2026-11-21) 提供公開專案 ZIP 與 SHA-256 校驗檔，保存原始碼、固定版本韌體、圖像、署名與重建說明。

本公開倉庫與附件不含原機完整 Flash、個人遊戲存檔、操作環境設定或還原金鑰；這些資料由擁有者另行私下備份。Arduino 套件、編譯工具、build 與 ELF/map 等可再產生內容不納入公開封存。

## 原始碼與重建

`TamaPoke/` 為實際編譯使用的原始碼；`assets/` 保存四份原始 TPK2 圖像。以下版本對應這次建置：

- ESP32 Arduino core：`3.3.12`。
- GFX Library for Arduino：`1.6.9`。
- SensorLib：`0.5.1`。
- XPowersLib：`0.3.3`。
- U8g2：`2.36.19`。

```bash
arduino-cli core update-index --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core install esp32:esp32@3.3.12 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli lib install 'GFX Library for Arduino@1.6.9' 'SensorLib@0.5.1' 'XPowersLib@0.3.3' 'U8g2@2.36.19'
bash tools/build.sh
```

若使用獨立的 Arduino CLI 設定，可執行 `bash tools/build.sh --config-file /path/to/arduino-cli.yaml`。重建輸出位於 `build/output/`；不同環境重建的檔案可能有不同雜湊，`firmware/` 保存的是本次留存的固定檔案。

## 驗證紀錄

- 2026-11-12：應用程式刷入後雜湊校驗通過。
- 實際開機版本為 `1.19-pika`，角色為 #25；無 microSD 時圖像載入成功。
- 實際重開機後仍為 #25，內建圖像再次載入成功。
- 162 項主機遊戲測試通過；同一套測試在 AddressSanitizer 與 UndefinedBehaviorSanitizer 下亦通過。
- 原版畫面與觸控已由使用者確認；皮卡丘修改版的目視畫面與觸控狀態仍待使用者回報。

詳細資訊見 `evidence/`。`STATS` 的 `mon` 僅代表舊圖像載入器；本版動畫是否載入應參考 `HEALTH` 的 `mon=1`。

執行主機測試：

```bash
make -C TamaPoke/test run asan
```

## 授權

程式碼沿用上游 MIT 授權，見 [LICENSE](LICENSE)。圖像來自 PMD SpriteCollab，沿用其非商業使用與署名條件；Pokémon 角色權利屬 Nintendo / Game Freak / The Pokémon Company。見 [第三方標示](THIRD_PARTY_NOTICES.md) 與 [上游署名](docs/UPSTREAM_CREDITS.md)。
