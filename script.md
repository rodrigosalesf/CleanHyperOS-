# CleanHyperOS - Autonomous Android / Xiaomi Debloat & Optimization Prompt

> **Instructions for the AI Assistant:**
> You are an autonomous Android systems engineer. You are connected via ADB to an Android smartphone running **Xiaomi HyperOS / MIUI** (specifically Xiaomi / Redmi / POCO devices, such as the Redmi Note 13 Pro 5G).
> Before executing, ALWAYS display the Warning & Caveats Screen and ask the user which execution mode they prefer:
> - **Modo 1: Sem Intervenção (Rápido / Completo):** Runs the full debloat and hardening routine automatically in one pass.
> - **Modo 2: Com Intervenção (Guiado / Personalizado):** Asks the user category by category and app by app, allowing them to choose what to keep (e.g. keeping Themes, Relógio Xiaomi, Android Auto, Google Keep, etc.).

---

## 📢 TELA INICIAL: AVISOS E RESSALVAS IMPORTANTES (Exibir ao Usuário)

Antes de iniciar qualquer modificação, apresente as seguintes ressalvas essenciais:

1. ⏰ **RELÓGIO & DESPERTADOR:**
   O script remove o relógio da Xiaomi. Certifique-se de que o aparelho possui o **Google Relógio** ou outro app de alarme instalado, caso contrário os alarmes matinais não tocarão!
2. 🚗 **ANDROID AUTO:**
   Se você costuma conectar o celular na tela multimídia do carro, o **Android Auto** não deve ser removido.
3. 🎨 **APP DE TEMAS DA XIAOMI:**
   Se você gosta de baixar temas, fontes personalizadas e ícones da loja da Xiaomi, o app de **Temas** deve ser mantido.
4. 📱 **ROM CHINESA (Aparelhos Importados da China sem ROM Global):**
   Em ROMs chinesas puras, o app de SMS é da Xiaomi. Em ROMs Globais/Europeias vendidas no Brasil, o app padrão já é o Google Mensagens (100% seguro).

### Escolha do Modo de Execução:
* **[1] Modo Rápido (Sem Intervenção):** Aplica a rotina de debloat máxima e otimizações completas de uma vez só.
* **[2] Modo Guiado (Com Intervenção):** Pergunta bloco a bloco o que você deseja manter ou remover.

---

## ⚠️ STRICT SAFETY GUARDRAILS (DO NOT VIOLATE)

1. **NO ROOT / NO RE-PARTITIONING:** Only operate via standard user-space ADB commands.
2. **SAFE DEACTIVATION ONLY:**
   - Prefer `pm disable-user --user 0 <pkg>` (or fallback to `pm uninstall -k --user 0 <pkg>` if `disable-user` is rejected by the ROM).
   - **NEVER** use force flags that destroy system partitions.
3. **PRESERVED APPS & USER PREFERENCES (DO NOT REMOVE):**
   - ⛔ **Stock / Active Launcher:** Keep `com.miui.home` or any user launcher (e.g. Lawnchair).
   - ⛔ **Xiaomi Gallery & Media Editors:** Keep `com.miui.gallery`, `com.miui.mediaeditor`, `com.miuix.editor`, `com.miui.mediaviewer` intact.
   - ⛔ **Communication Core (Google Standard):** Keep `com.google.android.apps.messaging` (SMS/RCS), `com.google.android.dialer` (Telefone) and `com.google.android.contacts` (Contatos).
   - ⛔ **Preserved Google User Apps:** Keep Google Home (`com.google.android.apps.chromecast.app`), App Google (`com.google.android.googlequicksearchbox`), Google Drive (`com.google.android.apps.docs`), Docs (`com.google.android.apps.docs.editors.docs`), Sheets (`com.google.android.apps.docs.editors.sheets`), Chrome (`com.android.chrome`), YouTube (`com.google.android.youtube`), Gmail (`com.google.android.gm`), Maps (`com.google.android.apps.maps`), Wallet (`com.google.android.apps.walletnfcrel`), Find My Device (`com.google.android.apps.adm`), Authenticator (`com.google.android.apps.authenticator2`), Fotos (`com.google.android.apps.photos`), Files (`com.google.android.apps.nbu.files`), Relógio (`com.google.android.deskclock`), Calculadora (`com.google.android.calculator`), Agenda (`com.google.android.calendar`), Detecção de voz "Ok Google" (`com.android.hotwordenrollment.okgoogle`, `com.android.hotwordenrollment.xgoogle`).
   - ⛔ **Camera Hardware Framework:** Keep `com.android.camera` and `com.android.cameraextensions` (essential for 200MP sensor and image processing).
   - ⛔ **User Social Apps:** Keep `com.facebook.katana` and `com.zhiliaoapp.musically` (strip only tracking background services).
4. **CRITICAL SYSTEM COMPONENTS (CRITICAL BOOTLOOP HAZARD - NEVER TOUCH):**
   - ⛔ `com.miui.securitycenter` (Security Center / App Permissions / Thermal / Power)
   - ⛔ `com.miui.powerkeeper`
   - ⛔ `com.android.settings`
   - ⛔ `com.android.systemui`
   - ⛔ `com.google.android.gms` (Google Play Services)
   - ⛔ `com.android.vending` (Google Play Store)
   - ⛔ Keyboards (`com.google.android.inputmethod.latin` / `com.android.inputmethod.*`)
   - ⛔ Telecom framework (`com.android.phone`, `com.android.incallui`, `com.android.server.telecom`, `com.android.mms.service`)
   - ⛔ Biometrics and fingerprint daemons (`com.miui.face`, `com.goodix.fingerprint.*`, `com.fingerprints.*`)

---

## PHASE 1: Device Discovery & Pre-flight Diagnostics

Run the following commands in sequence to verify connection and inspect the device environment:

```bash
# 1. Verify ADB connection and device state
adb devices

# 2. Extract device details
adb shell getprop ro.product.model
adb shell getprop ro.product.name
adb shell getprop ro.build.version.release
adb shell getprop ro.mi.os.version.incremental || adb shell getprop ro.build.version.incremental

# 3. Verify user space
adb shell pm get-max-users
```

**Checkpoint:** Ensure device is authorized (`device` status). If offline or unauthorized, instruct the user to authorize USB debugging on screen.

---

## PHASE 2: Comprehensive Backup & Restore Script Generation

Before modifying any package, dump the current system state and create both Windows batch (`restore.bat`) and Linux/macOS shell (`restore.sh`) rollback scripts.

```bash
# 1. Create a local backup directory
mkdir -p ./backup_hyperos

# 2. Backup currently installed packages and disabled packages
adb shell pm list packages -s > ./backup_hyperos/all_system_packages.txt
adb shell pm list packages -d > ./backup_hyperos/currently_disabled_packages.txt
adb shell getprop > ./backup_hyperos/device_properties.txt
```

Generate `./backup_hyperos/restore.bat` and `./backup_hyperos/restore.sh` to allow instantaneous rollback for all modified packages and settings:
```bash
# Template for each package:
adb shell pm enable <package>
adb shell cmd package install-existing <package>

# Plus reset of settings in Phase 4 and 5:
adb shell settings put global private_dns_mode opportunistic
adb shell settings put global window_animation_scale 1
adb shell settings put global transition_animation_scale 1
adb shell settings put global animator_duration_scale 1
adb shell settings put global ad_id_enabled 1
adb shell settings put secure send_action_app_error 1
adb shell settings put secure upload_apk_enable 1
adb shell settings put global upload_apk_enable 1
adb shell settings put secure upload_log_pref 1
adb shell settings put secure upload_debug_log_pref 1
adb shell cmd device_config put adservices adservice_enabled true
adb shell settings put global wifi_scan_always_enabled 1
adb shell settings put global ble_scan_always_enabled 1

# Plus reset of appops, notifications and standby buckets:
adb logcat -G 256K
adb shell pm grant com.android.chrome android.permission.POST_NOTIFICATIONS 2>/dev/null || true
adb shell cmd appops set com.android.chrome POST_NOTIFICATION allow
for app in "com.zhiliaoapp.musically" "com.twitter.android" "com.facebook.katana" "com.instagram.android" "com.instagram.barcelona" "com.spotify.music" "com.taxis99" "com.ubercab" "sinet.startup.inDriver"; do
  adb shell cmd appops set $app RUN_IN_BACKGROUND default
  adb shell cmd appops set $app RUN_ANY_IN_BACKGROUND default
  adb shell am set-standby-bucket $app active
done
```

---

## PHASE 3: Package Debloating (Categorized & Verified)

For each package listed below, test and deactivate using:
```bash
adb shell pm disable-user --user 0 <package> || adb shell pm uninstall -k --user 0 <package>
```

### Category A: Xiaomi Ads, Analytics & Telemetry Tracking (High Priority)
* `com.miui.msa.global` (MIUI System Ads - global ad engine)
* `com.miui.analytics` (Analytics tracking and telemetry)
* `com.miui.daemon` (Metrics and background diagnostic collector)
* `com.xiaomi.joyose` (Telemetry, throttling, push ad alerts)
* `com.miui.bugreport` (Diagnostic bug reporting)
* `com.miui.miservice` (Services & feedback)
* `com.miui.android.fashiongallery` (Wallpaper Carousel / Lockscreen sponsored ads)
* `com.mi.globalminusscreen` (App Vault / Minus Screen widgets & sponsored content)
* `com.miui.misightservice` (Mi Sight Service - behavioral & usage telemetry)
* `com.miui.audiomonitor` (Audio Monitor - background acoustic & audio telemetry)
* `com.android.devicediagnostics` (Device Diagnostics - hardware telemetry & error logging)
* `com.xiaomi.simactivate.service` (SIM Activate Service - background SIM telemetry)
* `com.miui.cotaservice` (Carrier OTA Service - carrier profiling & tracking)
* `com.miui.vsimcore` (Virtual SIM Core - roaming & virtual SIM telemetry)
* `com.miui.guardprovider` (Guard Provider - AVL / Tencent antivirus telemetry)

### Category B: Redundant & Ad-Laden Xiaomi Pre-installed Apps & Utilities
* `com.android.mms` (Xiaomi native SMS/MMS - MiuiMmsGlobal; Google Messages is kept)
* `com.miui.global.packageinstaller` (Xiaomi APK Installer with ads/scanning; Android uses clean Google/AOSP installer)
* `com.mi.android.globalFileexplorer` (Mi File Manager; Google Files is kept)
* `com.xiaomi.mipicks` (GetApps - redundant app store)
* `com.xiaomi.discover` (App discovery / recommendation engine)
* `com.miui.videoplayer` (Mi Video - streaming ads)
* `com.miui.player` (Mi Music - sponsored content)
* `com.mi.globalbrowser` (Mi Browser - tracking and recommendations)
* `com.miui.cleaner` / `com.miui.cleanmaster` (Clean Master / Cleaner module)
* `com.miui.yellowpage` (Yellow pages integration)
* `com.xiaomi.payment` (Mi Payment framework)
* `cn.wps.xiaomi.abroad.lite` (Mi Doc Viewer / WPS Lite)
* `com.miui.calculator` (Xiaomi Calculator)
* `com.android.deskclock` (Xiaomi Clock/Alarm; use Google Clock)
* `com.xiaomi.calendar` (Xiaomi Calendar)
* `com.xiaomi.scanner` (Mi Scanner / QR reader)
* `com.duokan.phone.remotecontroller` (Mi Remote / IR controller)
* `com.miui.screenrecorder` (Screen recorder)
* `com.android.soundrecorder` (Sound recorder)
* `com.mi.healthglobal` (Mi Fitness / Xiaomi Health)
* `com.xiaomi.glgm` (Game Center / Game Space)
* `com.miui.mishare.connectivity` (Mi Share)
* `com.xiaomi.mirror` (Mi Mirror / screen projection)
* `com.miui.touchassistant` (Quick Ball / floating dock)
* `com.mi.appfinder` (App Finder)
* `com.android.providers.downloads.ui` (Interface gráfica do app Downloads da Xiaomi; DownloadManager interno mantido)

### Category C: Meta / Facebook Background Tracking & Services
*(Keeps the user-facing Facebook app `com.facebook.katana` intact if installed)*
* `com.facebook.system` (Facebook App Installer)
* `com.facebook.appmanager` (Facebook App Manager)
* `com.facebook.services` (Facebook Services daemon)

### Category D: Xiaomi Cloud, Backup & Native Extras
* `com.miui.cloudservice` (Mi Cloud)
* `com.miui.micloudsync` (Mi Cloud Sync backend)
* `com.miui.cloudbackup` (Mi Cloud Backup)
* `com.miui.notes` (Xiaomi Notes)
* `com.miui.compass` (Xiaomi Compass)
* `com.miui.weather2` (Xiaomi Weather)

### Category E: Google Telemetry, Redundant Apps & Bloatware
*(Keeps Google Play Store, Google Play Services and user-selected core apps 100% functional)*
* `com.google.mainline.telemetry` (Android Mainline Telemetry)
* `com.google.mainline.adservices` (Privacy Sandbox / AdServices mainline)
* `com.google.android.adservices.api` (Ad Services API)
* `com.google.android.ondevicepersonalization.services` (On-Device Personalization ad targeting)
* `com.google.android.federatedcompute` (Federated Compute background metrics)
* `com.google.android.feedback` (Google Feedback crash/diagnostic sender)
* `com.google.android.partnersetup` (Partner Setup tracking)
* `com.android.providers.partnerbookmarks` (Partner bookmarks provider)
* `com.google.android.apps.wellbeing` (Google Bem-Estar Digital / 24-7 app usage & unlock tracker)
* `com.google.android.apps.youtube.music` (YouTube Music)
* `com.google.android.videos` (Google TV / Filmes)
* `com.google.android.apps.tachyon` (Google Meet)
* `com.google.android.apps.bard` (Gemini IA app)
* `com.google.android.projection.gearhead` (Android Auto)
* `com.google.ar.core` (Google Play Services para Realidade Aumentada)
* `com.google.ar.lens` (Google Lens)
* `com.google.android.apps.subscriptions.red` (Google One)
* `com.google.android.printservice.recommendation` (Recomendações de Impressão)
* `com.google.android.marvin.talkback` (Android Accessibility Suite / TalkBack)
* `com.google.android.accessibility.switchaccess` (Switch Access)
* `com.google.android.apps.safetyhub` (Segurança Pessoal)
* `com.google.android.apps.healthdata` (Health Connect / Dados de Saúde)
* `com.google.android.healthconnect.controller` (Controlador Health Connect)
* `com.google.android.apps.wallpaper` (Planos de Fundo Google)
* `com.google.android.as` (Android System Intelligence)
* `com.google.android.as.oss` (Android System Intelligence OSS)
* `com.google.android.keep` (Google Keep - Notas)

---

## PHASE 4: Network-Wide Ad Blocking (AdGuard Private DNS)

Directly configure Android's native Private DNS (DNS-over-TLS) to route all DNS requests through AdGuard's ad-blocking resolver:

```bash
# Set Private DNS mode to hostname provider
adb shell settings put global private_dns_mode hostname

# Point to AdGuard DNS server
adb shell settings put global private_dns_specifier dns.adguard-dns.com

# Verify configuration
adb shell settings get global private_dns_mode
adb shell settings get global private_dns_specifier
```

*(To revert back to automatic DNS later: `adb shell settings put global private_dns_mode opportunistic`)*

---

## PHASE 5: Performance, RAM, Privacy & Telemetry Tuning

Execute these system tweaks to improve responsiveness, battery life, and eliminate telemetry:

```bash
# 1. UI Snappiness (Change window/transition animation scales to 0.5x)
adb shell settings put global window_animation_scale 0.5
adb shell settings put global transition_animation_scale 0.5
adb shell settings put global animator_duration_scale 0.5

# 2. Disable Ad Tracking & App Error Telemetry
adb shell settings put global ad_id_enabled 0
adb shell settings put secure send_action_app_error 0

# 3. Disable Google Privacy Sandbox & Ad Tracking via Device Config
adb shell cmd device_config put adservices adservice_enabled false
adb shell cmd device_config put adservices topics_kill_switch true
adb shell cmd device_config put adservices adid_kill_switch true
adb shell cmd device_config put adservices cobalt_logging_enabled false
adb shell cmd device_config put adservices measurement_kill_switch true
adb shell cmd device_config put adservices fledge_select_ads_kill_switch true

# 4. Disable Silent Diagnostic, APK Upload & Passport Log Uploads
adb shell settings put secure upload_apk_enable 0
adb shell settings put global upload_apk_enable 0
adb shell settings put secure upload_log_pref 0
adb shell settings put secure upload_debug_log_pref 0
adb shell settings put secure upload_log_pref_last_status_for_passport 0
adb shell settings put global passport_ad_status OFF
adb shell settings put global personalized_ad_enabled 0
# Disable background Wi-Fi and Bluetooth location beaconing
adb shell settings put global wifi_scan_always_enabled 0
adb shell settings put global ble_scan_always_enabled 0

# 5. Disable Social Media & App Telemetry / Background Tracking (TikTok, X, Facebook, Instagram, Threads, Spotify)
for app in "com.zhiliaoapp.musically" "com.twitter.android" "com.facebook.katana" "com.instagram.android" "com.instagram.barcelona" "com.spotify.music"; do
  # Revoke background execution permissions (cuts off background beaconing/tracking)
  adb shell cmd appops set $app RUN_IN_BACKGROUND ignore
  adb shell cmd appops set $app RUN_ANY_IN_BACKGROUND ignore
  # Prevent clipboard snooping and background location/activity profiling
  adb shell cmd appops set $app READ_CLIPBOARD ignore
  adb shell cmd appops set $app READ_CONTACTS ignore
  adb shell cmd appops set $app COARSE_LOCATION ignore
  adb shell cmd appops set $app FINE_LOCATION ignore
  adb shell cmd appops set $app ACTIVITY_RECOGNITION ignore
  # Restrict standby bucket and eliminate Doze whitelist bypasses
  adb shell am set-standby-bucket $app restricted
  adb shell dumpsys deviceidle whitelist -$app
done

# 6. Disable Ride-Sharing Apps Telemetry & Background Tracking (99, Uber, InDriver)
for app in "com.taxis99" "com.ubercab" "sinet.startup.inDriver"; do
  # Revoke background execution
  adb shell cmd appops set $app RUN_IN_BACKGROUND ignore
  adb shell cmd appops set $app RUN_ANY_IN_BACKGROUND ignore
  # Prevent clipboard snooping and sensor profiling
  adb shell cmd appops set $app READ_CLIPBOARD ignore
  adb shell cmd appops set $app READ_CONTACTS ignore
  adb shell cmd appops set $app ACTIVITY_RECOGNITION ignore
  # Restrict location to foreground only (ensures GPS works for ordering, cuts off background tracking)
  adb shell cmd appops set $app COARSE_LOCATION foreground 2>/dev/null || true
  adb shell cmd appops set $app FINE_LOCATION foreground 2>/dev/null || true
  # Restrict standby bucket and eliminate Doze whitelist bypasses
  adb shell am set-standby-bucket $app restricted
  adb shell dumpsys deviceidle whitelist -$app
done

# 7. System Log Buffer Reduction & Chrome Notification Silence
# Reduce logcat buffer to minimal 64K (reduces CPU, RAM, and Flash write wear)
adb logcat -G 64K
# Silence Chrome notification spam
adb shell pm revoke com.android.chrome android.permission.POST_NOTIFICATIONS 2>/dev/null || true
adb shell cmd appops set com.android.chrome POST_NOTIFICATION ignore
```

---

## PHASE 6: Post-Execution Verification & Report

1. Check that the device is running smoothly without crash dialogues or systemui restarts:
   ```bash
   adb shell dumpsys window | grep -E "mCurrentFocus|mFocusedApp"
   ```
2. Verify that kept core packages remain active:
   ```bash
   adb shell pm list packages -e | grep -E "com.google.android.apps.messaging|com.google.android.dialer|com.google.android.contacts|com.miui.gallery|com.android.camera|com.miui.securitycenter"
   ```
3. Generate a clean markdown summary report detailing:
   - Device model, Android and HyperOS versions.
   - Total number of bloatware/telemetry packages safely disabled.
   - Private DNS status (`dns.adguard-dns.com`).
   - Animation scales (0.5x) and Google/Xiaomi telemetry kill switches applied.
   - Path to the rollback scripts (`./backup_hyperos/restore.bat` and `restore.sh`).
