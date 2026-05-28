import os, sys, subprocess, time, re, json, hashlib
import urllib.request, urllib.error

GITHUB_REPO  = 'Wumpusuhq/Wumpus-multitool'
BRANDING_URL = 'https://github.com/Wumpusuhq/Wumpus-multitool'

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
STAR_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'star')

# ── Colors ─────────────────────────────────────────────────
def c(text, color):
    r, g, b = color
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def purplepink(text):
    out = ""; red = 40
    for line in text.splitlines():
        out += f"\033[38;2;{red};0;220m{line}\033[0m\n"
        if red < 255: red = min(255, red + 15)
    return out

PINK   = (220,  80, 180)
WHITE  = (240, 240, 240)
GRAY   = (140, 140, 150)
GREEN  = ( 80, 220, 120)
YELLOW = (240, 200,  80)
CYAN   = ( 80, 200, 220)
RED    = (220,  60,  60)

BANNER = '''
██╗    ██╗██╗   ██╗███╗   ███╗██████╗ ██╗   ██╗███████╗
██║    ██║██║   ██║████╗ ████║██╔══██╗██║   ██║██╔════╝
██║ █╗ ██║██║   ██║██╔████╔██║██████╔╝██║   ██║███████╗
██║███╗██║██║   ██║██║╚██╔╝██║██╔═══╝ ██║   ██║╚════██║
╚███╔███╔╝╚██████╔╝██║ ╚═╝ ██║██║     ╚██████╔╝███████║
 ╚══╝╚══╝  ╚═════╝ ╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝
'''

# ── IP / Langue ────────────────────────────────────────────
_COUNTRY_CACHE = None

def get_country() -> str:
    global _COUNTRY_CACHE
    if _COUNTRY_CACHE is not None:
        return _COUNTRY_CACHE
    try:
        req = urllib.request.Request(
            'https://ipinfo.io/json',
            headers={'User-Agent': 'existentielle-launcher'}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        _COUNTRY_CACHE = data.get('country', 'EN').upper()
    except Exception:
        _COUNTRY_CACHE = 'EN'
    return _COUNTRY_CACHE

# ── Traductions Complètes ──────────────────────────────────
_LANG_MAP = {
    'FR': 'fr', 'BE': 'fr', 'CH': 'fr', 'CA': 'fr', 'LU': 'fr', 'MC': 'fr',
    'SN': 'fr', 'CI': 'fr', 'CM': 'fr', 'MG': 'fr', 'BF': 'fr', 'ML': 'fr',
    'GN': 'fr', 'TG': 'fr', 'BJ': 'fr', 'NE': 'fr', 'CD': 'fr', 'CG': 'fr',
    'GA': 'fr', 'TD': 'fr', 'DZ': 'fr', 'MA': 'fr', 'TN': 'fr', 'HT': 'fr',
    'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es', 'CL': 'es', 'PE': 'es',
    'VE': 'es', 'EC': 'es', 'GT': 'es', 'CU': 'es', 'BO': 'es', 'DO': 'es',
    'HN': 'es', 'PY': 'es', 'SV': 'es', 'NI': 'es', 'CR': 'es', 'PA': 'es',
    'UY': 'es', 'GQ': 'es',
    'PT': 'pt', 'BR': 'pt', 'AO': 'pt', 'MZ': 'pt',
    'DE': 'de', 'AT': 'de', 'LI': 'de',
    'IT': 'it', 'SM': 'it', 'VA': 'it',
    'RU': 'ru', 'BY': 'ru', 'KZ': 'ru', 'KG': 'ru',
    'SA': 'ar', 'AE': 'ar', 'EG': 'ar', 'IQ': 'ar',
    'TR': 'tr', 'NL': 'nl', 'PL': 'pl', 'JP': 'ja',
    'KR': 'ko', 'CN': 'zh', 'TW': 'zh', 'HK': 'zh',
}

STRINGS = {
    'fr': {
        'gh_label':      'Comment créer un token',
        'gh_title':      'COMMENT CRÉER UN TOKEN GITHUB',
        'gh_saved':      'Token sauvegardé trouvé',
        'gh_use':        'Utiliser ce token ? (O/n) :',
        'gh_confirmed':  'Star confirmé — STAR TOOLS DÉBLOQUÉS !',
        'gh_not_starred':'Tu n\'as pas encore starré {repo}.',
        'gh_star_here':  '→ Mets une étoile ici :',
        'gh_paste':      'Colle ton token (vide pour annuler) :',
        'gh_step1':      '1. Va sur   https://github.com/settings/tokens',
        'gh_step2':      '2. Clique   Generate new token (classic)',
        'gh_step3':      '3. Scope    ✓ read:user   (uniquement)',
        'gh_step4':      '4. Copie le token — GitHub le montre une seule fois !',
        'gh_saved_ok':   'Token sauvegardé',
        'gh_gitignore':  'Ajoute .gh_token à ton .gitignore !',
        'star_unlock':   'STAR TOOLS  (débloqués)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Mets une étoile pour débloquer →',
        'star_locked_msg':'Ce tool est réservé aux starrers de {repo}',
        'star_info':     'Mets une étoile →',
        'star_token':    'Lance [G] pour configurer ton token GitHub.',
        'exit':          'Exit',
        'enter':         'ENTRÉE pour continuer',
        'invalid':       'Numéro invalide',
        'not_a_number':  'Entre un numéro',
        'page_next':     'Page Suivante',
        'page_prev':     'Page Précédente',
    },
    'es': {
        'gh_label':      'Cómo crear un token',
        'gh_title':      'CÓMO CREAR UN TOKEN DE GITHUB',
        'gh_saved':      'Token guardado encontrado',
        'gh_use':        '¿Usar este token? (S/n) :',
        'gh_confirmed':  '¡Estrella confirmada — STAR TOOLS DESBLOQUEADOS!',
        'gh_not_starred':'Aún no has dado estrella a {repo}.',
        'gh_star_here':  '→ Dale estrella aquí:',
        'gh_paste':      'Pega tu token (vacío para cancelar) :',
        'gh_step1':      '1. Ve a    https://github.com/settings/tokens',
        'gh_step2':      '2. Clic en Generate new token (classic)',
        'gh_step3':      '3. Scope   ✓ read:user   (solo este)',
        'gh_step4':      '4. Copia el token — ¡GitHub lo muestra solo una vez!',
        'gh_saved_ok':   'Token guardado',
        'gh_gitignore':  '¡Añade .gh_token a tu .gitignore!',
        'star_unlock':   'STAR TOOLS  (desbloqueados)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Da una estrella para desbloquear →',
        'star_locked_msg':'Este tool es solo para starrers de {repo}',
        'star_info':     'Estrella aquí →',
        'star_token':    'Ejecuta [G] para configurar tu token de GitHub.',
        'exit':          'Salir',
        'enter':         'ENTER para continuar',
        'invalid':       'Número inválido',
        'not_a_number':  'Introduce un número',
        'page_next':     'Página Siguiente',
        'page_prev':     'Página Anterior',
    },
    'pt': {
        'gh_label':      'Como criar um token',
        'gh_title':      'COMO CRIAR UM TOKEN DO GITHUB',
        'gh_saved':      'Token salvo encontrado',
        'gh_use':        'Usar este token? (S/n) :',
        'gh_confirmed':  'Estrela confirmada — STAR TOOLS DESBLOQUEADOS!',
        'gh_not_starred':'Você ainda não deu estrela em {repo}.',
        'gh_star_here':  '→ Dê uma estrela aqui:',
        'gh_paste':      'Cole seu token (vazio para cancelar) :',
        'gh_step1':      '1. Acesse  https://github.com/settings/tokens',
        'gh_step2':      '2. Clique  Generate new token (classic)',
        'gh_step3':      '3. Scope   ✓ read:user   (apenas este)',
        'gh_step4':      '4. Copie o token — o GitHub mostra apenas uma vez!',
        'gh_saved_ok':   'Token salvo',
        'gh_gitignore':  'Adicione .gh_token ao seu .gitignore!',
        'star_unlock':   'STAR TOOLS  (desbloqueados)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Dê uma estrela para desbloquear →',
        'star_locked_msg':'Este tool é apenas para starrers de {repo}',
        'star_info':     'Estrela aqui →',
        'star_token':    'Execute [G] para configurar seu token do GitHub.',
        'exit':          'Sair',
        'enter':         'ENTER para continuar',
        'invalid':       'Número inválido',
        'not_a_number':  'Digite um número',
        'page_next':     'Próxima Página',
        'page_prev':     'Página Anterior',
    },
    'en': {
        'gh_label':      'How to create a token',
        'gh_title':      'HOW TO CREATE A GITHUB TOKEN',
        'gh_saved':      'Saved token found',
        'gh_use':        'Use this token? (Y/n) :',
        'gh_confirmed':  'Star confirmed — STAR TOOLS UNLOCKED!',
        'gh_not_starred':"You haven't starred {repo} yet.",
        'gh_star_here':  '→ Star it here:',
        'gh_paste':      'Paste your token (blank to cancel) :',
        'gh_step1':      '1. Go to    https://github.com/settings/tokens',
        'gh_step2':      '2. Click    Generate new token (classic)',
        'gh_step3':      '3. Scope    ✓ read:user   (only this one)',
        'gh_step4':      '4. Copy the token — GitHub shows it only once!',
        'gh_saved_ok':   'Token saved',
        'gh_gitignore':  'Add .gh_token to your .gitignore!',
        'star_unlock':   'STAR TOOLS  (unlocked)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Star the repo to unlock →',
        'star_locked_msg':'This tool is for starrers of {repo} only',
        'star_info':     'Star here →',
        'star_token':    'Run [G] to configure your GitHub token.',
        'exit':          'Exit',
        'enter':         'ENTER to continue',
        'invalid':       'Invalid number',
        'not_a_number':  'Enter a number',
        'page_next':     'Next Page',
        'page_prev':     'Previous Page',
    }
    # Tu peux ajouter les autres langues (de, it, ru, ar, tr, nl, pl, ja, ko, zh) si besoin
}

_LANG_CACHE = None
def t(key: str) -> str:
    global _LANG_CACHE
    if _LANG_CACHE is None:
        country = get_country()
        lang = _LANG_MAP.get(country, 'en')
        _LANG_CACHE = STRINGS.get(lang, STRINGS['en'])
    s = _LANG_CACHE.get(key, STRINGS['en'].get(key, key))
    return s.replace('{repo}', GITHUB_REPO)

# ── Helpers ────────────────────────────────────────────────
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    cls()
    print(purplepink(BANNER))
    print(c(f"                       {BRANDING_URL}", PINK))
    print(c("          ─────────────────────────────────────────────────────────", GRAY))
    print()

def ask(prompt):
    return input(c(f"  [?] {prompt} ", CYAN)).strip().upper()

def ok(msg):   print(c(f"  [+] {msg}", GREEN))
def err(msg):  print(c(f"  [-] {msg}", RED))
def info(msg): print(c(f"  [i] {msg}", CYAN))

# ── Scan & Name ────────────────────────────────────────────
def get_name(filepath):
    PAT = re.compile(r'''(?x) ^ \#? \s* NAME \s* = \s* (?P<q> ["']) (.+?) (?P=q) ''')
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = PAT.match(line.strip())
                if m:
                    return m.group(2).strip()
    except:
        pass
    return os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()

def scan_folder(folder, is_star=False):
    if not os.path.isdir(folder):
        return []
    files = []
    for f in sorted([x for x in os.listdir(folder) if x.endswith('.py') and not x.startswith('_')]):
        path = os.path.join(folder, f)
        files.append((path, is_star))
    return files

# ── Star Check ─────────────────────────────────────────────
_STAR_CACHE = None

def _check_star_github() -> bool:
    global _STAR_CACHE
    if _STAR_CACHE is not None:
        return _STAR_CACHE

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
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'wumpus-launcher',
        }
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
    info(t('gh_gitignore'))

# ── GitHub Setup ───────────────────────────────────────────
def github_setup():
    global _STAR_CACHE
    cls()
    print(purplepink(BANNER))
    print(c(f"  ─────  {t('gh_title')}  ─────────────────────────────────", PINK))
    print()

    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    if os.path.isfile(token_path):
        with open(token_path) as f:
            saved = f.read().strip()
        if saved:
            info(f"{t('gh_saved')} : {saved[:8]}{'*'*(len(saved)-8)}")
            if ask(t('gh_use')).lower() not in ('N','NO','NON','НЕТ','لا','HAYIR','NEE','NIE'):
                if _check_star_github():
                    ok(t('gh_confirmed'))
                else:
                    err(t('gh_not_starred'))
                    print(c(f"\n  {t('gh_star_here')} https://github.com/{GITHUB_REPO}", CYAN))
                input(c(f"  [{t('enter')}]", GRAY))
                return

    print(c("  ┌───────────────────────────────────────────────────────────────┐", PINK))
    for step in [t('gh_step1'), t('gh_step2'), t('gh_step3'), t('gh_step4')]:
        print(c(f"  │  {step:<63}│", WHITE))
    print(c("  └───────────────────────────────────────────────────────────────┘", PINK))
    print()

    token = input(c(f"  {t('gh_paste')} ", CYAN)).strip()
    if not token:
        return

    save_token(token)
    print()
    if _check_star_github():
        ok(t('gh_confirmed'))
    else:
        err(t('gh_not_starred'))
        print(c(f"\n  {t('gh_star_here')} https://github.com/{GITHUB_REPO}\n", CYAN))
    input(c(f"  [{t('enter')}]", GRAY))

# ── Launch Tool ────────────────────────────────────────────
def launch(filepath):
    try:
        subprocess.run([sys.executable, filepath], check=False)
    except Exception:
        err("Erreur lors du lancement du tool")
        time.sleep(1)

# ── Main Menu (STAR TOOLS EN PREMIER) ──────────────────────
def main_menu():
    page = 1
    ITEMS_PER_PAGE = 12

    while True:
        star_tools = scan_folder(STAR_DIR, is_star=True)
        free_tools = scan_folder(TOOLS_DIR, is_star=False)
        all_tools = star_tools + free_tools   # ← STAR TOOLS EN PREMIER

        star_ok = _check_star_github()

        total_items = len(all_tools)
        total_pages = max(1, (total_items - 1) // ITEMS_PER_PAGE + 1)
        start = (page - 1) * ITEMS_PER_PAGE
        current_page_tools = all_tools[start:start + ITEMS_PER_PAGE]

        show_banner()
        print(c(f"  ─────  PAGE {page}/{total_pages} ─────────────────────────────────────", PINK))

        for i, (fp, is_star) in enumerate(current_page_tools, start + 1):
            name = get_name(fp)
            if is_star:
                color = YELLOW
                prefix = "★ " if star_ok else ""
                suffix = " [★ LOCKED]" if not star_ok else ""
                print(c(f"  [{i:>2}]", color) + c(f"  {prefix}{name}{suffix}", color))
            else:
                print(c(f"  [{i:>2}]", PINK) + c(f"  {name}", WHITE))

        print(c("  ──────────────────────────────────────────────────────────────", GRAY))
        print(c("  [G]", CYAN) + c("  GitHub Token / Star", WHITE))
        if total_pages > 1:
            print(c("  [N]", CYAN) + c(f"  {t('page_next')}", WHITE))
            print(c("  [P]", CYAN) + c(f"  {t('page_prev')}", WHITE))
        print(c("  [0]", GRAY) + c(f"  {t('exit')}", GRAY))
        print()

        choice = ask(">>")

        if choice == '0':
            cls()
            print(c(f"\n  Bye — {BRANDING_URL}\n", PINK))
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
                        err(t('star_locked_msg'))
                        info(t('star_info') + f" https://github.com/{GITHUB_REPO}")
                        info(t('star_token'))
                        time.sleep(2.5)
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
        print(c(f"\n  Bye — {BRANDING_URL}\n", PINK))
        sys.exit(0)