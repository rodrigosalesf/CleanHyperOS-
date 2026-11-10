import subprocess
import os
import sys

def run_adb(args):
    cmd = ["adb"] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout.strip(), p.stderr.strip(), p.returncode

def run_shell(cmd_str):
    return run_adb(["shell", cmd_str])

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("=" * 70)
    print("   🚀 CleanHyperOS - Otimizador e Debloat Inteligente para Xiaomi")
    print("      Compatível com MIUI 13/14 e HyperOS 1.0, 2.0 e 3.0")
    print("=" * 70)

def show_caveats():
    print("\n" + "!" * 70)
    print("   ⚠️  AVISOS E RESSALVAS IMPORTANTES ANTES DE EXECUTAR")
    print("!" * 70)
    print("1. ⏰ RELÓGIO & DESPERTADOR:")
    print("   O script remove o relógio da Xiaomi. Certifique-se de ter o")
    print("   'Google Relógio' ou outro app de alarme instalado no aparelho.")
    print("\n2. 🚗 ANDROID AUTO:")
    print("   Se você conecta o celular na central multimídia do seu carro,")
    print("   o Android Auto NÃO deve ser removido.")
    print("\n3. 🎨 APP DE TEMAS DA XIAOMI:")
    print("   Se você gosta de baixar temas, fontes e ícones na loja da Xiaomi,")
    print("   mantenha o app de Temas ativo.")
    print("\n4. 📱 ROM CHINESA (Aparelhos Importados da China sem ROM Global):")
    print("   Em ROMs chinesas puras, o app de SMS é da Xiaomi. Em ROMs Globais/EEA,")
    print("   o app padrão já é o Google Mensagens (100% seguro).")
    print("!" * 70 + "\n")

def main():
    clear_screen()
    banner()
    show_caveats()

    # Pre-flight device check
    print(">>> Verificando conexão do dispositivo...")
    dev_out, _, _ = run_adb(["devices"])
    lines = [l for l in dev_out.splitlines() if l.strip() and not l.startswith("*")]
    devices = [l.split("\t")[0] for l in lines[1:] if "device" in l]

    if not devices:
        print("\n❌ ERRO: Nenhum dispositivo detectado via ADB.")
        print("   Certifique-se de que:")
        print("   1. O cabo USB está conectado.")
        print("   2. A Depuração USB está ativada nas Opções do Desenvolvedor.")
        print("   3. A autorização foi confirmada na tela do celular.")
        input("\nPressione ENTER para sair...")
        return

    model, _, _ = run_shell("getprop ro.product.model")
    pname, _, _ = run_shell("getprop ro.product.name")
    os_ver, _, _ = run_shell("getprop ro.mi.os.version.incremental || getprop ro.build.version.incremental")
    print(f"✓ Dispositivo conectado: {model} ({pname}) - HyperOS/MIUI: {os_ver}\n")

    # Mode selection
    print("Escolha o modo de execução:")
    print(" [1] ⚡ Modo Rápido (Sem Intervenção)")
    print("     Aplica a otimização completa recomendada de uma só vez.")
    print("     (Remove telemetrias Xiaomi/Google, bloatware e aplica hardening)")
    print("")
    print(" [2] 🛠️  Modo Guiado (Com Intervenção)")
    print("     Pergunta bloco por bloco o que você deseja manter ou remover,")
    print("     permitindo escolher itens como Temas, Android Auto, Relógio, etc.")
    print("")
    print(" [0] Cancelar e Sair")

    # If --auto argument is passed, run mode 1 directly
    if "--auto" in sys.argv:
        choice = "1"
        print("\nExecutando automaticamente via parâmetro --auto...")
    else:
        choice = input("\nDigite a opção desejada [1, 2 ou 0]: ").strip()

    if choice == "0":
        print("\nOperação cancelada pelo usuário.")
        return

    # Configuration flags
    config = {
        "cat_a_xiaomi_ads": True,
        "cat_b_xiaomi_apps": True,
        "keep_xiaomi_themes": True,
        "keep_xiaomi_clock": False,
        "cat_c_meta": True,
        "cat_d_cloud": True,
        "cat_e_google_telemetry": True,
        "keep_android_auto": False,
        "keep_google_keep": False,
        "dns_adguard": True,
        "tweaks_animation": True,
        "tweaks_system_telemetry": True,
        "harden_social": True,
        "harden_rides": True,
        "reduce_logcat": True,
        "silence_chrome_notifs": True
    }

    if choice == "2":
        clear_screen()
        banner()
        print("\n--- 🛠️  MODO GUIADO: CONFIGURAÇÃO PERSONALIZADA ---\n")

        # Xiaomi Ads & Telemetry
        r = input("1. Desativar Telemetria, Anúncios e Coleta da Xiaomi (Categoria A)? [S/n]: ").strip().lower()
        config["cat_a_xiaomi_ads"] = r != "n"

        # Xiaomi Apps
        r = input("2. Remover Utilitários e Apps Redundantes da Xiaomi (GetApps, Mi Video, Mi Browser, etc.)? [S/n]: ").strip().lower()
        config["cat_b_xiaomi_apps"] = r != "n"

        if config["cat_b_xiaomi_apps"]:
            r = input("   -> Deseja MANTER o app de Temas da Xiaomi? [s/N]: ").strip().lower()
            config["keep_xiaomi_themes"] = r == "s"

            r = input("   -> Deseja MANTER o Relógio nativo da Xiaomi? (Responda 's' se NÃO usa o Google Relógio) [s/N]: ").strip().lower()
            config["keep_xiaomi_clock"] = r == "s"

        # Meta
        r = input("3. Desativar Serviços de Fundo da Meta/Facebook (App Installer, Manager, Services)? [S/n]: ").strip().lower()
        config["cat_c_meta"] = r != "n"

        # Xiaomi Cloud
        r = input("4. Desativar Xiaomi Mi Cloud, Sincronização em Nuvem e Notas/Bússola/Clima nativos? [S/n]: ").strip().lower()
        config["cat_d_cloud"] = r != "n"

        # Google Telemetry & Extra Apps
        r = input("5. Desativar Telemetria Google, Bem-Estar Digital e Apps Extras (YT Music, Meet, TV)? [S/n]: ").strip().lower()
        config["cat_e_google_telemetry"] = r != "n"

        if config["cat_e_google_telemetry"]:
            r = input("   -> Deseja MANTER o Android Auto (conexão com multimídia do carro)? [s/N]: ").strip().lower()
            config["keep_android_auto"] = r == "s"

            r = input("   -> Deseja MANTER o Google Keep (Notas)? [s/N]: ").strip().lower()
            config["keep_google_keep"] = r == "s"

        # Network Adblock
        r = input("6. Ativar Bloqueio de Anúncios a Nível de Rede via AdGuard DNS Privado? [S/n]: ").strip().lower()
        config["dns_adguard"] = r != "n"

        # Hardening
        r = input("7. Aplicar Hardening (bloqueio de execução em background) em Redes Sociais (TikTok, X, Instagram, etc.)? [S/n]: ").strip().lower()
        config["harden_social"] = r != "n"

        r = input("8. Aplicar Hardening em Apps de Corrida (99, Uber, InDriver) com GPS apenas em primeiro plano? [S/n]: ").strip().lower()
        config["harden_rides"] = r != "n"

        print("\nConfigurações personalizadas definidas com sucesso!")

    # ---------------------------------------------------------
    # EXECUTION PIPELINE
    # ---------------------------------------------------------
    print("\n" + "=" * 70)
    print("   INICIANDO EXECUÇÃO")
    print("=" * 70)

    # Backup State
    print("\n>>> Criando backup do estado atual do sistema...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = os.path.join(script_dir, "backup_hyperos")
    os.makedirs(backup_dir, exist_ok=True)
    sys_pkgs, _, _ = run_shell("pm list packages -s")
    with open(os.path.join(backup_dir, "all_system_packages.txt"), "w", encoding="utf-8") as f:
        f.write(sys_pkgs)
    dis_pkgs, _, _ = run_shell("pm list packages -d")
    with open(os.path.join(backup_dir, "currently_disabled_packages.txt"), "w", encoding="utf-8") as f:
        f.write(dis_pkgs)
    props, _, _ = run_shell("getprop")
    with open(os.path.join(backup_dir, "device_properties.txt"), "w", encoding="utf-8") as f:
        f.write(props)
    print("✓ Backup salvo em ./backup_hyperos")

    # Build target packages list
    targets = []

    if config["cat_a_xiaomi_ads"]:
        targets.extend([
            ("com.miui.msa.global", "MIUI System Ads"),
            ("com.miui.analytics", "Analytics Tracking"),
            ("com.miui.daemon", "Metrics Collector Daemon"),
            ("com.xiaomi.joyose", "Joyose Telemetry"),
            ("com.miui.bugreport", "Bug Report Telemetry"),
            ("com.miui.miservice", "Services & Feedback"),
            ("com.miui.android.fashiongallery", "Wallpaper Carousel Ads"),
            ("com.mi.globalminusscreen", "App Vault Ads"),
            ("com.miui.misightservice", "Mi Sight Service Telemetry"),
            ("com.miui.audiomonitor", "Audio Monitor Telemetry"),
            ("com.android.devicediagnostics", "Device Diagnostics"),
            ("com.xiaomi.simactivate.service", "SIM Activation Telemetry"),
            ("com.miui.cotaservice", "Carrier OTA Telemetry"),
            ("com.miui.vsimcore", "Virtual SIM Roaming Telemetry"),
            ("com.miui.guardprovider", "Guard Provider AVL/Tencent Engine")
        ])

    if config["cat_b_xiaomi_apps"]:
        b_list = [
            ("com.android.mms", "Xiaomi Native SMS"),
            ("com.miui.global.packageinstaller", "Xiaomi Package Installer"),
            ("com.mi.android.globalFileexplorer", "Mi File Manager"),
            ("com.xiaomi.mipicks", "GetApps App Store"),
            ("com.xiaomi.discover", "App Discovery Engine"),
            ("com.miui.videoplayer", "Mi Video"),
            ("com.miui.player", "Mi Music"),
            ("com.miui.globalbrowser", "Mi Browser"),
            ("com.miui.cleaner", "Cleaner Module"),
            ("com.miui.cleanmaster", "Clean Master"),
            ("com.miui.yellowpage", "Yellow Pages"),
            ("com.xiaomi.payment", "Mi Payment"),
            ("cn.wps.xiaomi.abroad.lite", "Mi Doc Viewer (WPS Lite)"),
            ("com.miui.calculator", "Xiaomi Calculator"),
            ("com.xiaomi.calendar", "Xiaomi Calendar"),
            ("com.xiaomi.scanner", "Mi Scanner"),
            ("com.duokan.phone.remotecontroller", "Mi Remote"),
            ("com.miui.screenrecorder", "Screen Recorder"),
            ("com.android.soundrecorder", "Sound Recorder"),
            ("com.mi.healthglobal", "Mi Fitness"),
            ("com.xiaomi.glgm", "Game Center"),
            ("com.miui.mishare.connectivity", "Mi Share"),
            ("com.xiaomi.mirror", "Mi Mirror"),
            ("com.miui.touchassistant", "Quick Ball"),
            ("com.mi.appfinder", "App Finder"),
            ("com.android.providers.downloads.ui", "Downloads UI App")
        ]
        if not config["keep_xiaomi_clock"]:
            b_list.append(("com.android.deskclock", "Xiaomi Clock"))
        if not config["keep_xiaomi_themes"]:
            b_list.extend([
                ("com.android.thememanager", "Xiaomi Themes App"),
                ("com.android.thememanager.customizethemeconfig.config.overlay", "Theme Config Overlay")
            ])
        targets.extend(b_list)

    if config["cat_c_meta"]:
        targets.extend([
            ("com.facebook.system", "Facebook App Installer"),
            ("com.facebook.appmanager", "Facebook App Manager"),
            ("com.facebook.services", "Facebook Services Daemon")
        ])

    if config["cat_d_cloud"]:
        targets.extend([
            ("com.miui.cloudservice", "Mi Cloud"),
            ("com.miui.micloudsync", "Mi Cloud Sync"),
            ("com.miui.cloudbackup", "Mi Cloud Backup"),
            ("com.miui.notes", "Xiaomi Notes"),
            ("com.miui.compass", "Xiaomi Compass"),
            ("com.miui.weather2", "Xiaomi Weather")
        ])

    if config["cat_e_google_telemetry"]:
        g_list = [
            ("com.google.mainline.telemetry", "Android Mainline Telemetry"),
            ("com.google.mainline.adservices", "Android Mainline AdServices"),
            ("com.google.android.adservices.api", "Ad Services API"),
            ("com.google.android.ondevicepersonalization.services", "On-Device Personalization"),
            ("com.google.android.federatedcompute", "Federated Compute Metrics"),
            ("com.google.android.feedback", "Google Feedback"),
            ("com.google.android.partnersetup", "Partner Setup"),
            ("com.android.providers.partnerbookmarks", "Partner Bookmarks"),
            ("com.google.android.apps.wellbeing", "Google Bem-Estar Digital"),
            ("com.google.android.apps.youtube.music", "YouTube Music"),
            ("com.google.android.videos", "Google TV / Filmes"),
            ("com.google.android.apps.tachyon", "Google Meet"),
            ("com.google.android.apps.bard", "Gemini IA"),
            ("com.google.ar.core", "Google AR Core"),
            ("com.google.ar.lens", "Google Lens"),
            ("com.google.android.apps.subscriptions.red", "Google One"),
            ("com.google.android.printservice.recommendation", "Recomendador de Impressao"),
            ("com.google.android.marvin.talkback", "TalkBack"),
            ("com.google.android.accessibility.switchaccess", "Switch Access"),
            ("com.google.android.apps.safetyhub", "Seguranca Pessoal"),
            ("com.google.android.apps.healthdata", "Health Connect Dados"),
            ("com.google.android.healthconnect.controller", "Health Connect Controlador"),
            ("com.google.android.apps.wallpaper", "Planos de Fundo Google"),
            ("com.google.android.as", "Android System Intelligence"),
            ("com.google.android.as.oss", "Android System Intelligence OSS")
        ]
        if not config["keep_android_auto"]:
            g_list.append(("com.google.android.projection.gearhead", "Android Auto"))
        if not config["keep_google_keep"]:
            g_list.append(("com.google.android.keep", "Google Keep (Notas)"))
        targets.extend(g_list)

    # Process Debloat Targets
    print(f"\n>>> Processando debloat de {len(targets)} pacotes selecionados...")
    inst_out, _, _ = run_shell("pm list packages")
    installed_set = set(line.strip().replace("package:", "") for line in inst_out.splitlines() if line.strip())

    deactivated = 0
    for pkg, label in targets:
        if pkg in installed_set:
            dis_out, dis_err, _ = run_shell(f"pm disable-user --user 0 {pkg}")
            comb_dis = (dis_out + " " + dis_err).strip()
            if "disabled" in comb_dis:
                print(f"  ✓ [DESATIVADO] {label} ({pkg})")
                deactivated += 1
            else:
                un_out, un_err, _ = run_shell(f"pm uninstall -k --user 0 {pkg}")
                comb_un = (un_out + " " + un_err).strip()
                if "Success" in comb_un:
                    print(f"  ✓ [REMOVIDO] {label} ({pkg})")
                    deactivated += 1
                else:
                    print(f"  ❌ [FALHA] {label} ({pkg}): {comb_un}")
        else:
            print(f"  - [JÁ INATIVO] {label} ({pkg})")
            deactivated += 1

    # DNS AdGuard
    if config["dns_adguard"]:
        print("\n>>> Configurando Bloqueador de Anúncios AdGuard DNS...")
        run_shell("settings put global private_dns_mode hostname")
        run_shell("settings put global private_dns_specifier dns.adguard-dns.com")
        print("  ✓ DNS Privado configurado para dns.adguard-dns.com")

    # Tweaks
    print("\n>>> Aplicando Otimizações de Fluidez, Bateria e Privacidade...")
    if config["tweaks_animation"]:
        run_shell("settings put global window_animation_scale 0.5")
        run_shell("settings put global transition_animation_scale 0.5")
        run_shell("settings put global animator_duration_scale 0.5")
        print("  ✓ Escala de animações reduzida para 0.5x")

    if config["tweaks_system_telemetry"]:
        run_shell("settings put global ad_id_enabled 0")
        run_shell("settings put secure send_action_app_error 0")
        for flag, val in [("adservice_enabled", "false"), ("topics_kill_switch", "true"),
                          ("adid_kill_switch", "true"), ("cobalt_logging_enabled", "false"),
                          ("measurement_kill_switch", "true"), ("fledge_select_ads_kill_switch", "true")]:
            run_shell(f"cmd device_config put adservices {flag} {val}")
        for ns, k, v in [("secure", "upload_apk_enable", "0"), ("global", "upload_apk_enable", "0"),
                         ("secure", "upload_log_pref", "0"), ("secure", "upload_debug_log_pref", "0"),
                         ("secure", "upload_log_pref_last_status_for_passport", "0"),
                         ("global", "passport_ad_status", "OFF"), ("global", "personalized_ad_enabled", "0"),
                         ("global", "wifi_scan_always_enabled", "0"), ("global", "ble_scan_always_enabled", "0")]:
            run_shell(f"settings put {ns} {k} {v}")
        print("  ✓ Telemetria de sistema, Privacy Sandbox e varreduras Wi-Fi/BLE desativadas")

    if config["harden_social"]:
        socials = ["com.zhiliaoapp.musically", "com.twitter.android", "com.facebook.katana",
                   "com.instagram.android", "com.instagram.barcelona", "com.spotify.music"]
        print(">>> Aplicando isolamento de telemetria em Redes Sociais...")
        for app in socials:
            for op in ["RUN_IN_BACKGROUND ignore", "RUN_ANY_IN_BACKGROUND ignore",
                       "READ_CLIPBOARD ignore", "READ_CONTACTS ignore",
                       "COARSE_LOCATION ignore", "FINE_LOCATION ignore",
                       "ACTIVITY_RECOGNITION ignore"]:
                run_shell(f"cmd appops set {app} {op}")
            run_shell(f"am set-standby-bucket {app} restricted")
            run_shell(f"dumpsys deviceidle whitelist -{app}")
        print("  ✓ Redes sociais isoladas e com execução de fundo cortada")

    if config["harden_rides"]:
        rides = ["com.taxis99", "com.ubercab", "sinet.startup.inDriver"]
        print(">>> Aplicando isolamento em Apps de Corrida (99, Uber, InDriver)...")
        for app in rides:
            for op in ["RUN_IN_BACKGROUND ignore", "RUN_ANY_IN_BACKGROUND ignore",
                       "READ_CLIPBOARD ignore", "READ_CONTACTS ignore",
                       "ACTIVITY_RECOGNITION ignore",
                       "COARSE_LOCATION foreground", "FINE_LOCATION foreground"]:
                run_shell(f"cmd appops set {app} {op}")
            run_shell(f"am set-standby-bucket {app} restricted")
            run_shell(f"dumpsys deviceidle whitelist -{app}")
        print("  ✓ Apps de corrida protegidos com GPS apenas em primeiro plano")

    if config["reduce_logcat"]:
        run_adb(["logcat", "-G", "64K"])
        print("  ✓ Buffer de logs reduzido para 64K (alivia RAM e desgaste de memória Flash)")

    if config["silence_chrome_notifs"]:
        run_shell("pm revoke com.android.chrome android.permission.POST_NOTIFICATIONS")
        run_shell("cmd appops set com.android.chrome POST_NOTIFICATION ignore")
        print("  ✓ Notificações de spam do Chrome silenciadas")

    # Final Verification
    print("\n" + "=" * 70)
    print("   VERIFICAÇÃO FINAL & ESTABILIDADE DO SISTEMA")
    print("=" * 70)
    focus, _, _ = run_shell("dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
    print(focus)
    print("\n✓ OTIMIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("  Caso deseje reverter qualquer mudança, utilize o script de restauração:")
    print(f"  {os.path.join(backup_dir, 'restore.bat')} (Windows)")
    print(f"  {os.path.join(backup_dir, 'restore.sh')} (Linux/macOS)")
    print("=" * 70)

if __name__ == "__main__":
    main()
