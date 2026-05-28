import os, sys, subprocess, time, re, json, urllib.request, urllib.error

GITHUB_REPO  = 'Wumpusuhq/Wumpus-multitool'
BRANDING_URL = 'https://github.com/Wumpusuhq/Wumpus-multitool'

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
STAR_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'star')

# ── Colors - Style VOID ───────────────────────────────────
def c(text, color):
    r, g, b = color
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def void_red(text):
    out = ""
    red = 90
    for line in text.splitlines():
        out += f"\033[38;2;{red};0;0m{line}\033[0m\n"
        red = min(255, red + 18)
    return out

RED     = (220,  20,  60)
DARKRED = (140,  10,  30)
WHITE   = (240, 240, 240)
GRAY    = (110, 110, 120)
GREEN   = ( 80, 220, 120)
YELLOW  = (255, 190,  60)
CYAN    = ( 80, 220, 220)

BANNER = '''
╔══════════════════════════════════════════════════════════════╗
║                 WUMPUS MULTITOOL v2.0                        ║
║                   ★ Star to unlock All ★                     ║
╚══════════════════════════════════════════════════════════════╝
'''

# ── IP / Langue ────────────────────────────────────────────
_COUNTRY_CACHE = None
def get_country() -> str:
    global _COUNTRY_CACHE
    if _COUNTRY_CACHE is not None: return _COUNTRY_CACHE
    try:
        req = urllib.request.Request('https://ipinfo.io/json', headers={'User-Agent': 'wumpus-launcher'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        _COUNTRY_CACHE = data.get('country', 'EN').upper()
    except:
        _COUNTRY_CACHE = 'EN'
    return _COUNTRY_CACHE

# ── Traductions ────────────────────────────────────────────
_LANG_MAP = {'FR': 'fr', 'BE': 'fr', 'CH': 'fr', 'CA': 'fr', 'ES': 'es', 'PT': 'pt'}

STRINGS = {
    'fr': {
        'gh_title':      'CONFIGURATION GITHUB TOKEN + STAR',
        'gh_saved':      'Token sauvegardé trouvé',
        'gh_use':        'Utiliser ce token ? (O/n) :',
        'gh_confirmed':  '⭐ Star confirmé — STAR TOOLS DÉBLOQUÉS !',
        'gh_not_starred':'Tu n\'as pas encore starré le repo.',
        'gh_star_here':  '→ Mets une étoile ici :',
        'gh_paste':      'Colle ton token (vide pour annuler) :',
        'gh_step_star':  '1. Mets une ★ sur le repo (obligatoire)',
        'gh_step1':      '2. Va sur   https://github.com/settings/tokens',
        'gh_step2':      '3. Generate new token (classic)',
        'gh_step3':      '4. Scope    ✓ read:user',
        'gh_step4':      '5. Copie le token',
        'star_locked_msg':'Ce tool est réservé aux utilisateurs ayant mis une étoile',
        'star_hint':     '☆ Star le repo pour débloquer →',
        'exit':          'Quitter',
        'enter':         'ENTRÉE pour continuer',
        'invalid':       'Numéro invalide',
        'not_a_number':  'Entre un numéro',
        'page_next':     'Page Suivante',
        'page_prev':     'Page Précédente',
    },
    'en': {
        'gh_title':      'GITHUB TOKEN + STAR SETUP',
        'gh_saved':      'Saved token found',
        'gh_use':        'Use this token? (Y/n) :',
        'gh_confirmed':  '⭐ Star confirmed — STAR TOOLS UNLOCKED!',
        'gh_not_starred':"You haven't starred the repo yet.",
        'gh_star_here':  '→ Star it here:',
        'gh_paste':      'Paste your token (blank to cancel) :',
        'gh_step_star':  '1. Star the repository (required)',
        'gh_step1':      '2. Go to    https://github.com/settings/tokens',
        'gh_step2':      '3. Generate new token (classic)',
        'gh_step3':      '4. Scope    ✓ read:user',
        'gh_step4':      '5. Copy the token',
        'star_locked_msg':'This tool is for starrers only',
        'star_hint':     '☆ Star the repo to unlock →',
        'exit':          'Exit',
        'enter':         'ENTER to continue',
        'invalid':       'Invalid number',
        'not_a_number':  'Enter a number',
        'page_next':     'Next Page',
        'page_prev':     'Previous Page',
    }
}

def t(key: str) -> str:
    global _LANG_CACHE
    if '_LANG_CACHE' not in globals():
        country = get_country()
        lang = _LANG_MAP.get(country, 'en')
        globals()['_LANG_CACHE'] = STRINGS.get(lang, STRINGS['en'])
    return _LANG_CACHE.get(key, key)

# ── Helpers ────────────────────────────────────────────────
def cls(): os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    cls()
    print(void_red(BANNER))
    print(c(f"                       {BRANDING_URL}", RED))
    print(c("          ─────────────────────────────────────────────────────────", DARKRED))
    print()

def ask(prompt): return input(c(f"  [?] {prompt} ", CYAN)).strip().upper()
def ok(msg):   print(c(f"  [+] {msg}", GREEN))
def err(msg):  print(c(f"  [-] {msg}", RED))
def info(msg): print(c(f"  [i] {msg}", CYAN))

# ── Scan Tools ─────────────────────────────────────────────
def get_name(filepath):
    PAT = re.compile(r'''(?x) ^ \#? \s* NAME \s* = \s* (?P<q> ["']) (.+?) (?P=q) ''')
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = PAT.match(line.strip())
                if m: return m.group(2).strip()
    except: pass
    return os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()

def scan_folder(folder, is_star=False):
    if not os.path.isdir(folder): return []
    files = []
    for f in sorted([x for x in os.listdir(folder) if x.endswith('.py') and not x.startswith('_')]):
        files.append((os.path.join(folder, f), is_star))
    return files

# ── Star Check ─────────────────────────────────────────────
_STAR_CACHE = None

def _check_star_github() -> bool:
    global _STAR_CACHE
    if _STAR_CACHE is not None: return _STAR_CACHE

    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    if not os.path.isfile(token_path):
        _STAR_CACHE = False
        return False

    try:
        with open(token_path) as f:
            token = f.read().strip()
        if not token:
            _STAR_CACHE = False
            return False
    except:
        _STAR_CACHE = False
        return False

    req = urllib.request.Request(
        f"https://api.github.com/user/starred/{GITHUB_REPO}",
        headers={'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json', 'User-Agent': 'wumpus-launcher'}
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            _STAR_CACHE = (r.status == 204)
    except:
        _STAR_CACHE = False
    return _STAR_CACHE

def save_token(token):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    with open(path, 'w') as f:
        f.write(token.strip())
    ok(f"{t('gh_saved_ok')} → {path}")

# ── GitHub Setup avec boîte parfaitement carrée ────────────
def github_setup():
    global _STAR_CACHE
    cls()
    print(void_red(BANNER))
    print(c(f"  ─────  {t('gh_title')}  ─────────────────────────────────", RED))
    print()

    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    if os.path.isfile(token_path):
        with open(token_path) as f:
            saved = f.read().strip()
        if saved:
            info(f"{t('gh_saved')} : {saved[:8]}{'*'*(len(saved)-8)}")
            if ask(t('gh_use')).lower() not in ('N','NO','NON'):
                if _check_star_github():
                    ok(t('gh_confirmed'))
                else:
                    err(t('gh_not_starred'))
                input(c(f"  [{t('enter')}]", GRAY))
                return

    # Boîte parfaitement alignée (largeur fixe 67 caractères)
    print(c("  ┌───────────────────────────────────────────────────────────────────┐", RED))
    print(c("  │ 1. Mets une ★ sur le repo (obligatoire)                           │", WHITE))
    print(c(f"  │   https://github.com/{GITHUB_REPO:<45}│", YELLOW))
    print(c("  │                                                                   │", WHITE))
    print(c("  │ 2. Va sur   https://github.com/settings/tokens                    │", WHITE))
    print(c("  │ 3. Generate new token (classic)                                   │", WHITE))
    print(c("  │ 4. Scope    ✓ read:user                                           │", WHITE))
    print(c("  │ 5. Copie le token                                                 │", WHITE))
    print(c("  └───────────────────────────────────────────────────────────────────┘", RED))
    print()

    token = input(c(f"  {t('gh_paste')} ", CYAN)).strip()
    if not token: return

    save_token(token)
    print()
    if _check_star_github():
        ok(t('gh_confirmed'))
    else:
        err(t('gh_not_starred'))
        print(c(f"\n  {t('gh_star_here')} https://github.com/{GITHUB_REPO}", CYAN))
    input(c(f"  [{t('enter')}]", GRAY))

# ── Tuto Star ──────────────────────────────────────────────
def show_star_tutorial():
    cls()
    print(void_red(BANNER))
    print(c("  ─────  COMMENT DÉBLOQUER LES STAR TOOLS  ───────────────────────", RED))
    print()
    print(c("  ┌─────────────────────────────────────────────────────────────────┐", RED))
    print(c("  │ 1. Va sur le repo :                                             │", WHITE))
    print(c(f"  │    https://github.com/{GITHUB_REPO:<45}│", YELLOW))
    print(c("  │ 2. Clique sur le bouton ★ 'Star' en haut à droite               │", WHITE))
    print(c("  │ 3. Reviens ici et appuie sur [G] pour configurer ton token      │", WHITE))
    print(c("  └─────────────────────────────────────────────────────────────────┘", RED))
    print()
    info("Une fois la star mise, utilise [G] pour ajouter ton token.")
    input(c(f"\n  [{t('enter')}]", GRAY))

# ── Launch Tool ────────────────────────────────────────────
def launch(filepath):
    try:
        subprocess.run([sys.executable, filepath], check=False)
    except:
        err("Erreur lors du lancement du tool")
        time.sleep(1)

# ── Main Menu ──────────────────────────────────────────────
def main_menu():
    page = 1
    ITEMS_PER_PAGE = 12

    while True:
        star_tools = scan_folder(STAR_DIR, is_star=True)
        free_tools = scan_folder(TOOLS_DIR, is_star=False)
        all_tools = star_tools + free_tools

        star_ok = _check_star_github()

        total_items = len(all_tools)
        total_pages = max(1, (total_items - 1) // ITEMS_PER_PAGE + 1)
        start = (page - 1) * ITEMS_PER_PAGE
        current_page_tools = all_tools[start:start + ITEMS_PER_PAGE]

        show_banner()
        print(c(f"  ─────  PAGE {page}/{total_pages} ─────────────────────────────────────", RED))

        for i, (fp, is_star) in enumerate(current_page_tools, start + 1):
            name = get_name(fp)
            if is_star:
                color = YELLOW
                prefix = "★ " if star_ok else ""
                suffix = " [LOCKED]" if not star_ok else ""
                print(c(f"  [{i:>2}]", color) + c(f"  {prefix}{name}{suffix}", color))
            else:
                print(c(f"  [{i:>2}]", RED) + c(f"  {name}", WHITE))

        print(c("  ──────────────────────────────────────────────────────────────", DARKRED))
        print(c("  [G]", CYAN) + c("  GitHub Token / Star", WHITE))
        if total_pages > 1:
            print(c("  [N]", CYAN) + c(f"  {t('page_next')}", WHITE))
            print(c("  [P]", CYAN) + c(f"  {t('page_prev')}", WHITE))
        print(c("  [0]", GRAY) + c(f"  {t('exit')}", GRAY))
        print()

        choice = ask(">>")

        if choice == '0':
            cls()
            print(c(f"\n  Bye — {BRANDING_URL}\n", RED))
            sys.exit(0)

        elif choice == 'G':
            github_setup()
            global _STAR_CACHE
            _STAR_CACHE = None

        elif choice == 'N' and total_pages > 1:
            page = min(page + 1, total_pages)
        elif choice == 'P' and total_pages > 1:
            page = max(page - 1, 1)

        else:
            try:
                n = int(choice)
                if 1 <= n <= total_items:
                    idx = n - 1
                    filepath, is_star_tool = all_tools[idx]

                    if is_star_tool and not star_ok:
                        show_star_tutorial()
                    else:
                        launch(filepath)
                else:
                    err(t('invalid'))
                    time.sleep(0.4)
            except ValueError:
                err(t('not_a_number'))
                time.sleep(0.4)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        cls()
        print(c(f"\n  Bye — {BRANDING_URL}\n", RED))
        sys.exit(0)