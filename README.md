# 🚀 CleanHyperOS

> **Otimizador, Debloater e Proteção de Privacidade em 1 Clique para celulares Xiaomi, Redmi e POCO (HyperOS & MIUI).**
> Deixe seu celular mais rápido, sem anúncios do sistema, livre de aplicativos inúteis de fábrica (bloatware) e com muito mais bateria — sem precisar de root!

[![Download ZIP](https://img.shields.io/badge/Download-Baixar%20Vers%C3%A3o%20Pronta%20(ZIP)-success?style=for-the-badge&logo=windows)](https://github.com/rodrigosalesf/CleanHyperOS-/archive/refs/heads/main.zip)
[![Releases](https://img.shields.io/badge/Releases-Vers%C3%A3o%201.0.0-blue?style=for-the-badge&logo=github)](https://github.com/rodrigosalesf/CleanHyperOS-/releases)

[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20HyperOS%20%7C%20MIUI-orange.svg)](https://www.mi.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![ADB Safe](https://img.shields.io/badge/Root-NÃO%20Necessário-success.svg)](#-seguran%C3%A7a)
[![Python](https://img.shields.io/badge/Python-Auto--Instalado-brightgreen.svg)](https://www.python.org/)

---

## 🎯 Guia Rápido para o Usuário Comum (3 Passos)

Não entende de programação? Não se preocupe! O **CleanHyperOS** foi feito para você só dar dois cliques e esperar a mágica acontecer:

### 📥 1. Baixar o Projeto
* Clique no botão verde acima ou [**Clique Aqui para Baixar o ZIP**](https://github.com/rodrigosalesf/CleanHyperOS-/archive/refs/heads/main.zip).
* Extraia a pasta baixada em qualquer lugar do seu computador (por exemplo, na Área de Trabalho ou Downloads).

### 🔌 2. Conectar o Celular no PC
1. No seu Xiaomi, abra **Configurações** > **Sobre o telefone**.
2. Toque 7 vezes seguidas em **Versão do HyperOS** (ou Versão da MIUI) até aparecer: *"Você agora é um desenvolvedor!"*.
3. Volte para a tela inicial das Configurações, vá em **Configurações adicionais** > **Opções do desenvolvedor**.
4. Ative a opção **Depuração USB**.
5. Conecte o cabo USB do celular no computador. Quando aparecer uma mensagem na tela do aparelho, marque a caixinha **"Sempre permitir a partir deste computador"** e confirme.

### ⚡ 3. Rodar a Otimização
* Entre na pasta que você extraiu e dê **duplo clique no arquivo `run.bat`**.
* **Pronto!** O inicializador cuida de tudo:
  - Se seu PC não tiver o Python ou o ADB instalados, ele baixa e instala tudo de forma transparente.
  - Na tela, você escolhe se quer o **Modo Rápido [1]** (faz tudo sozinho em segundos) ou o **Modo Guiado [2]** (pergunta o que você quer manter).
  - Um backup de segurança é criado antes de qualquer ação. Se um dia quiser reverter, basta rodar o restaurador gerado!

---

## 📖 O que é o CleanHyperOS?

O **CleanHyperOS** é uma ferramenta completa e automatizada via **ADB (Android Debug Bridge)** desenvolvida para transformar a experiência em dispositivos Xiaomi:
- Elimina anúncios do sistema, rastreadores e serviços ocultos de telemetria.
- Remove mais de 80 aplicativos redundantes e bloatwares (Xiaomi e Google).
- Isola o consumo em segundo plano de redes sociais (TikTok, X, Instagram, Facebook) e apps de corrida (Uber, 99, inDriver).
- Configura bloqueio de anúncios a nível de rede (AdGuard Private DNS).
- Aumenta a autonomia de bateria, reduz uso de memória RAM e preserva a vida útil da memória flash interna.
- **100% Reversível:** Gera scripts automáticos de restauração antes de qualquer alteração.

---

## ✨ Recursos Principais

* 🛡️ **Zero Root & Zero Risco de Bootloop:** Opera estritamente no espaço de usuário do Android (`pm disable-user` e `pm uninstall -k --user 0`). Componentes vitais do sistema (Security Center, PowerKeeper, Câmera nativa de alta resolução, Play Store) são rigidamente blindados.
* ⚡ **Dois Modos de Execução:**
  1. **Modo Rápido (Sem Intervenção):** Aplica o perfil completo recomendado em uma única passagem.
  2. **Modo Guiado (Com Intervenção):** Interface interativa que pergunta categoria por categoria o que você deseja manter (Temas, Relógio, Android Auto, etc.).
* 🔒 **Supressão Total de Telemetria:**
  * **Xiaomi:** Desativa serviços silenciosos de ativação de chip por SMS (`simactivate`), `misightservice`, `audiomonitor`, telemetria de operadora e diagnósticos.
  * **Google:** Desativa o Privacy Sandbox do Android (Topics API, AdServices, Cobalt logging), upload silencioso de APKs pelo Play Protect e o Bem-Estar Digital.
  * **Meta & Redes Sociais:** Desativa os serviços de instalação silenciosa do Facebook e isola processos de fundo do TikTok, X/Twitter, Instagram, Threads e Spotify.
* 🚗 **GPS Inteligente para Apps de Corrida:** Uber, 99 e inDriver têm sua localização travada para funcionar **apenas enquanto o aplicativo está em primeiro plano** (permitindo pedir corridas normalmente, mas cortando qualquer rastreamento quando fechados).
* 🌐 **Bloqueio de Anúncios Nativo:** Ativa o DNS Privado com DNS-over-TLS (`dns.adguard-dns.com`), bloqueando anúncios em navegadores e apps sem precisar de aplicativos VPN adicionais.
* 💨 **Fluidez e Longevidade:** Reduz as escalas de animação para `0.5x` e diminui o buffer do Logcat para `64K`, poupando ciclos de escrita na memória Flash (UFS).

---

## ⚠️ Ressalvas Importantes Antes de Usar

Antes de rodar a ferramenta em qualquer aparelho, fique atento:

1. ⏰ **Relógio & Despertador:**
   O script remove o relógio da Xiaomi por padrão. Certifique-se de ter o **Google Relógio** (ou outro app de despertador) instalado no aparelho.
2. 🚗 **Android Auto:**
   Se você conecta o celular na central multimídia do seu carro, escolha o **Modo Guiado** e opte por **MANTER** o Android Auto.
3. 🎨 **App de Temas Xiaomi:**
   Se você gosta de baixar papéis de parede, fontes e temas personalizados pela loja da Xiaomi, opte por manter o aplicativo de Temas.
4. 📱 **ROMs Importadas da China (China ROM):**
   Aparelhos com ROM chinesa pura usam o app de SMS da Xiaomi. Em aparelhos com ROM Global ou Europeia (vendidos no Brasil e internacionalmente), o padrão já é o Google Mensagens (100% seguro).

---

## 🛠️ Pré-requisitos & Instalação Automática

> [!TIP]
> **Zero Dificuldade no Windows:** Você não precisa se preocupar em instalar nada manualmente. O inicializador `run.bat` detecta automaticamente se o **Python** ou o **ADB** estão faltando e realiza o download e a instalação silenciosa para você!

### Requisitos Gerais:
1. **Computador:** Windows 10/11, Linux ou macOS.
   - *Windows (Manual via terminal, se desejar):*
     ```powershell
     winget install Python.Python.3.12
     winget install Google.PlatformTools --version 37.0.1
     ```
   - *Linux (Ubuntu/Debian):*
     ```bash
     sudo apt update && sudo apt install -y python3 adb
     ```
   - *macOS:*
     ```bash
     brew install python3 android-platform-tools
     ```
2. **Cabo USB** para conectar o smartphone ao PC.
3. **Depuração USB ativada no celular:**
   * Vá em **Configurações** > **Sobre o telefone** e toque repetidamente em **Versão do HyperOS / MIUI** até virar um desenvolvedor.
   * Volte, vá em **Configurações Adicionais** > **Opções do desenvolvedor**.
   * Ative a opção **Depuração USB** (e se disponível, *Depuração USB (Configurações de Segurança)*).
   * Conecte o cabo ao PC e, na tela do celular, marque **"Sempre permitir a partir deste computador"** e confirme.

---

## 🚀 Como Executar

### No Windows (1 Clique - 100% Automático):
Basta dar **duplo clique** no arquivo:
```cmd
run.bat
```
*(Ele verifica o ambiente, instala as dependências necessárias se faltarem e abre a tela de escolha de modo).*

### Via Terminal (Windows / Linux / macOS):
Abra o terminal na pasta do projeto e execute:
```bash
python run_clean_hyperos.py
```

*Para rodar direto no modo rápido sem perguntas via linha de comando:*
```bash
python run_clean_hyperos.py --auto
```

---

## 🔄 Como Reverter (Rollback / Restauração)

Sempre que a ferramenta é executada, ela cria automaticamente uma pasta `backup_hyperos` com a lista dos seus pacotes originais e scripts de restauração instantânea.

Para desfazer as alterações e restaurar os aplicativos originais:
* **No Windows:** Dê duplo clique em `backup_hyperos\restore.bat`.
* **No Linux / macOS:** Execute no terminal `./backup_hyperos/restore.sh`.

---

## 📂 Estrutura do Repositório

```text
CleanHyperOS/
├── run_clean_hyperos.py   # Script principal com interface interativa e automação
├── run.bat                # Launcher de 1 clique para Windows
├── script.md              # Manual técnico completo e prompt de referência
├── README.md              # Documentação oficial
├── LICENSE                # Licença MIT
└── .gitignore             # Arquivos ignorados pelo Git
```

---

## 🤝 Contribuições

Contribuições são muito bem-vindas! Se você encontrou novos pacotes de telemetria ou melhorias para o HyperOS:
1. Faça um Fork do projeto.
2. Crie uma branch para sua modificação (`git checkout -b feature/novo-recurso`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona novo recurso'`).
4. Envie para o branch (`git push origin feature/novo-recurso`).
5. Abra um Pull Request.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.
