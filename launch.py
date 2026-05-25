import os, sys, subprocess, time, re, json
import urllib.request, urllib.error

GITHUB_REPO  = 'Wumpusuhq/Wumpus-multitool'
BRANDING_URL = 'https://github.com/Wumpusuhq/Wumpus-multitool'

TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
STAR_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'star')

if os.name == 'nt': os.system("")

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

# ── IP / langue ────────────────────────────────────────────
_COUNTRY_CACHE = None

def get_country() -> str:
    """Retourne le code pays de l'IP publique (ex: 'FR', 'US'). Fallback 'EN'."""
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

# Textes localisés par pays
# Format : { 'CODE_PAYS': { 'clé': 'texte' } }
# Les pays non listés tombent sur 'EN' (anglais)
_LANG_MAP = {
    # ── Français ──────────────────────────────────────────
    'FR': 'fr', 'BE': 'fr', 'CH': 'fr', 'CA': 'fr',
    'LU': 'fr', 'MC': 'fr', 'SN': 'fr', 'CI': 'fr',
    'CM': 'fr', 'MG': 'fr', 'BF': 'fr', 'ML': 'fr',
    'GN': 'fr', 'TG': 'fr', 'BJ': 'fr', 'NE': 'fr',
    'CD': 'fr', 'CG': 'fr', 'GA': 'fr', 'TD': 'fr',
    'DZ': 'fr', 'MA': 'fr', 'TN': 'fr', 'HT': 'fr',
    # ── Espagnol ──────────────────────────────────────────
    'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es',
    'CL': 'es', 'PE': 'es', 'VE': 'es', 'EC': 'es',
    'GT': 'es', 'CU': 'es', 'BO': 'es', 'DO': 'es',
    'HN': 'es', 'PY': 'es', 'SV': 'es', 'NI': 'es',
    'CR': 'es', 'PA': 'es', 'UY': 'es', 'GQ': 'es',
    # ── Portugais ─────────────────────────────────────────
    'PT': 'pt', 'BR': 'pt', 'AO': 'pt', 'MZ': 'pt',
    'CV': 'pt', 'GW': 'pt', 'ST': 'pt', 'TL': 'pt',
    # ── Allemand ──────────────────────────────────────────
    'DE': 'de', 'AT': 'de', 'LI': 'de',
    # ── Italien ───────────────────────────────────────────
    'IT': 'it', 'SM': 'it', 'VA': 'it',
    # ── Russe ─────────────────────────────────────────────
    'RU': 'ru', 'BY': 'ru', 'KZ': 'ru', 'KG': 'ru',
    # ── Arabe ─────────────────────────────────────────────
    'SA': 'ar', 'AE': 'ar', 'EG': 'ar', 'IQ': 'ar',
    'SY': 'ar', 'JO': 'ar', 'LB': 'ar', 'LY': 'ar',
    'SD': 'ar', 'YE': 'ar', 'KW': 'ar', 'QA': 'ar',
    'BH': 'ar', 'OM': 'ar', 'MR': 'ar', 'SO': 'ar',
    # ── Turc ──────────────────────────────────────────────
    'TR': 'tr',
    # ── Néerlandais ───────────────────────────────────────
    'NL': 'nl', 'SR': 'nl',
    # ── Polonais ──────────────────────────────────────────
    'PL': 'pl',
    # ── Japonais ──────────────────────────────────────────
    'JP': 'ja',
    # ── Coréen ────────────────────────────────────────────
    'KR': 'ko',
    # ── Chinois ───────────────────────────────────────────
    'CN': 'zh', 'TW': 'zh', 'HK': 'zh', 'MO': 'zh', 'SG': 'zh',
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
    },
    'de': {
        'gh_label':      'Token erstellen',
        'gh_title':      'GITHUB TOKEN ERSTELLEN',
        'gh_saved':      'Gespeicherter Token gefunden',
        'gh_use':        'Diesen Token verwenden? (J/n) :',
        'gh_confirmed':  'Star bestätigt — STAR TOOLS ENTSPERRT!',
        'gh_not_starred':'Du hast {repo} noch nicht mit einem Stern markiert.',
        'gh_star_here':  '→ Hier einen Stern vergeben:',
        'gh_paste':      'Token einfügen (leer zum Abbrechen) :',
        'gh_step1':      '1. Gehe zu  https://github.com/settings/tokens',
        'gh_step2':      '2. Klicke   Generate new token (classic)',
        'gh_step3':      '3. Scope    ✓ read:user   (nur dieser)',
        'gh_step4':      '4. Token kopieren — GitHub zeigt ihn nur einmal!',
        'gh_saved_ok':   'Token gespeichert',
        'gh_gitignore':  'Füge .gh_token zu deiner .gitignore hinzu!',
        'star_unlock':   'STAR TOOLS  (entsperrt)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Stern vergeben zum Entsperren →',
        'star_locked_msg':'Dieses Tool ist nur für Starrer von {repo}',
        'star_info':     'Stern hier →',
        'star_token':    'Starte [G] um deinen GitHub Token zu konfigurieren.',
        'exit':          'Beenden',
        'enter':         'ENTER zum Fortfahren',
        'invalid':       'Ungültige Nummer',
        'not_a_number':  'Gib eine Nummer ein',
    },
    'it': {
        'gh_label':      'Come creare un token',
        'gh_title':      'COME CREARE UN TOKEN GITHUB',
        'gh_saved':      'Token salvato trovato',
        'gh_use':        'Usare questo token? (S/n) :',
        'gh_confirmed':  'Stella confermata — STAR TOOLS SBLOCCATI!',
        'gh_not_starred':'Non hai ancora messo una stella a {repo}.',
        'gh_star_here':  '→ Metti una stella qui:',
        'gh_paste':      'Incolla il tuo token (vuoto per annullare) :',
        'gh_step1':      '1. Vai su   https://github.com/settings/tokens',
        'gh_step2':      '2. Clicca   Generate new token (classic)',
        'gh_step3':      '3. Scope    ✓ read:user   (solo questo)',
        'gh_step4':      '4. Copia il token — GitHub lo mostra solo una volta!',
        'gh_saved_ok':   'Token salvato',
        'gh_gitignore':  'Aggiungi .gh_token al tuo .gitignore!',
        'star_unlock':   'STAR TOOLS  (sbloccati)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Metti una stella per sbloccare →',
        'star_locked_msg':'Questo tool è solo per gli starrers di {repo}',
        'star_info':     'Stella qui →',
        'star_token':    'Esegui [G] per configurare il tuo token GitHub.',
        'exit':          'Esci',
        'enter':         'INVIO per continuare',
        'invalid':       'Numero non valido',
        'not_a_number':  'Inserisci un numero',
    },
    'ru': {
        'gh_label':      'Как создать токен',
        'gh_title':      'КАК СОЗДАТЬ ТОКЕН GITHUB',
        'gh_saved':      'Найден сохранённый токен',
        'gh_use':        'Использовать этот токен? (Д/н) :',
        'gh_confirmed':  'Звезда подтверждена — STAR TOOLS РАЗБЛОКИРОВАНЫ!',
        'gh_not_starred':'Ты ещё не поставил звезду на {repo}.',
        'gh_star_here':  '→ Поставь звезду здесь:',
        'gh_paste':      'Вставь токен (пусто = отмена) :',
        'gh_step1':      '1. Открой  https://github.com/settings/tokens',
        'gh_step2':      '2. Нажми   Generate new token (classic)',
        'gh_step3':      '3. Scope   ✓ read:user   (только это)',
        'gh_step4':      '4. Скопируй токен — GitHub показывает его только раз!',
        'gh_saved_ok':   'Токен сохранён',
        'gh_gitignore':  'Добавь .gh_token в .gitignore!',
        'star_unlock':   'STAR TOOLS  (разблокированы)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Поставь звезду для разблокировки →',
        'star_locked_msg':'Этот инструмент только для starrers {repo}',
        'star_info':     'Звезда здесь →',
        'star_token':    'Запусти [G] чтобы настроить GitHub токен.',
        'exit':          'Выход',
        'enter':         'ENTER для продолжения',
        'invalid':       'Неверный номер',
        'not_a_number':  'Введи число',
    },
    'ar': {
        'gh_label':      'إنشاء توكن',
        'gh_title':      'كيفية إنشاء توكن GitHub',
        'gh_saved':      'تم العثور على توكن محفوظ',
        'gh_use':        'استخدام هذا التوكن؟ (ن/لا) :',
        'gh_confirmed':  'تم تأكيد النجمة — STAR TOOLS مفعّلة!',
        'gh_not_starred':'لم تضع نجمة على {repo} بعد.',
        'gh_star_here':  '→ ضع نجمة هنا:',
        'gh_paste':      'الصق التوكن (فارغ للإلغاء) :',
        'gh_step1':      '1. اذهب إلى  https://github.com/settings/tokens',
        'gh_step2':      '2. انقر       Generate new token (classic)',
        'gh_step3':      '3. النطاق     ✓ read:user   (هذا فقط)',
        'gh_step4':      '4. انسخ التوكن — GitHub يعرضه مرة واحدة فقط!',
        'gh_saved_ok':   'تم حفظ التوكن',
        'gh_gitignore':  'أضف .gh_token إلى .gitignore!',
        'star_unlock':   'STAR TOOLS  (مفعّلة)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  ضع نجمة لفتح الأدوات →',
        'star_locked_msg':'هذه الأداة للمستخدمين الذين وضعوا نجمة على {repo}',
        'star_info':     'نجمة هنا →',
        'star_token':    'شغّل [G] لإعداد توكن GitHub.',
        'exit':          'خروج',
        'enter':         'ENTER للمتابعة',
        'invalid':       'رقم غير صحيح',
        'not_a_number':  'أدخل رقماً',
    },
    'tr': {
        'gh_label':      'Token nasıl oluşturulur',
        'gh_title':      'GITHUB TOKEN NASIL OLUŞTURULUR',
        'gh_saved':      'Kayıtlı token bulundu',
        'gh_use':        'Bu tokeni kullan? (E/h) :',
        'gh_confirmed':  'Yıldız onaylandı — STAR TOOLS AÇILDI!',
        'gh_not_starred':'{repo} reposuna henüz yıldız vermedin.',
        'gh_star_here':  '→ Buraya yıldız ver:',
        'gh_paste':      'Tokenini yapıştır (boş = iptal) :',
        'gh_step1':      '1. Git      https://github.com/settings/tokens',
        'gh_step2':      '2. Tıkla    Generate new token (classic)',
        'gh_step3':      '3. Kapsam   ✓ read:user   (sadece bu)',
        'gh_step4':      '4. Tokeni kopyala — GitHub yalnızca bir kez gösterir!',
        'gh_saved_ok':   'Token kaydedildi',
        'gh_gitignore':  '.gh_token dosyasını .gitignore\'a ekle!',
        'star_unlock':   'STAR TOOLS  (açıldı)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Açmak için yıldız ver →',
        'star_locked_msg':'Bu tool yalnızca {repo} starrers içindir',
        'star_info':     'Yıldız ver →',
        'star_token':    'GitHub tokenini ayarlamak için [G] çalıştır.',
        'exit':          'Çıkış',
        'enter':         'Devam için ENTER',
        'invalid':       'Geçersiz numara',
        'not_a_number':  'Bir numara gir',
    },
    'nl': {
        'gh_label':      'Token aanmaken',
        'gh_title':      'GITHUB TOKEN AANMAKEN',
        'gh_saved':      'Opgeslagen token gevonden',
        'gh_use':        'Dit token gebruiken? (J/n) :',
        'gh_confirmed':  'Ster bevestigd — STAR TOOLS ONTGRENDELD!',
        'gh_not_starred':'Je hebt {repo} nog geen ster gegeven.',
        'gh_star_here':  '→ Geef hier een ster:',
        'gh_paste':      'Plak je token (leeg = annuleren) :',
        'gh_step1':      '1. Ga naar  https://github.com/settings/tokens',
        'gh_step2':      '2. Klik op  Generate new token (classic)',
        'gh_step3':      '3. Scope    ✓ read:user   (alleen dit)',
        'gh_step4':      '4. Kopieer de token — GitHub toont hem maar één keer!',
        'gh_saved_ok':   'Token opgeslagen',
        'gh_gitignore':  'Voeg .gh_token toe aan je .gitignore!',
        'star_unlock':   'STAR TOOLS  (ontgrendeld)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Geef een ster om te ontgrendelen →',
        'star_locked_msg':'Dit tool is alleen voor starrers van {repo}',
        'star_info':     'Ster hier →',
        'star_token':    'Start [G] om je GitHub token in te stellen.',
        'exit':          'Afsluiten',
        'enter':         'ENTER om door te gaan',
        'invalid':       'Ongeldig nummer',
        'not_a_number':  'Voer een nummer in',
    },
    'pl': {
        'gh_label':      'Jak stworzyć token',
        'gh_title':      'JAK STWORZYĆ TOKEN GITHUB',
        'gh_saved':      'Znaleziono zapisany token',
        'gh_use':        'Użyć tego tokena? (T/n) :',
        'gh_confirmed':  'Gwiazdka potwierdzona — STAR TOOLS ODBLOKOWANE!',
        'gh_not_starred':'Nie dałeś jeszcze gwiazdki {repo}.',
        'gh_star_here':  '→ Daj gwiazdkę tutaj:',
        'gh_paste':      'Wklej swój token (puste = anuluj) :',
        'gh_step1':      '1. Idź do   https://github.com/settings/tokens',
        'gh_step2':      '2. Kliknij  Generate new token (classic)',
        'gh_step3':      '3. Zakres   ✓ read:user   (tylko to)',
        'gh_step4':      '4. Skopiuj token — GitHub pokazuje go tylko raz!',
        'gh_saved_ok':   'Token zapisany',
        'gh_gitignore':  'Dodaj .gh_token do swojego .gitignore!',
        'star_unlock':   'STAR TOOLS  (odblokowane)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  Daj gwiazdkę aby odblokować →',
        'star_locked_msg':'To narzędzie jest tylko dla starrers {repo}',
        'star_info':     'Gwiazdka tutaj →',
        'star_token':    'Uruchom [G] aby skonfigurować token GitHub.',
        'exit':          'Wyjście',
        'enter':         'ENTER aby kontynuować',
        'invalid':       'Nieprawidłowy numer',
        'not_a_number':  'Wpisz numer',
    },
    'ja': {
        'gh_label':      'トークンの作成方法',
        'gh_title':      'GITHUB トークンの作成方法',
        'gh_saved':      '保存済みトークンが見つかりました',
        'gh_use':        'このトークンを使用しますか？(Y/n) :',
        'gh_confirmed':  'スター確認済 — STAR TOOLS アンロック！',
        'gh_not_starred':'{repo} にまだスターをつけていません。',
        'gh_star_here':  '→ こちらでスターをつけてください:',
        'gh_paste':      'トークンを貼り付け（空白でキャンセル）:',
        'gh_step1':      '1. 開く     https://github.com/settings/tokens',
        'gh_step2':      '2. クリック Generate new token (classic)',
        'gh_step3':      '3. スコープ ✓ read:user   (これだけ)',
        'gh_step4':      '4. トークンをコピー — GitHubは一度しか表示しません！',
        'gh_saved_ok':   'トークンを保存しました',
        'gh_gitignore':  '.gh_token を .gitignore に追加してください！',
        'star_unlock':   'STAR TOOLS  (アンロック済)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  スターをつけてアンロック →',
        'star_locked_msg':'このツールは {repo} のスタラー限定です',
        'star_info':     'スターはこちら →',
        'star_token':    '[G] を実行してGitHubトークンを設定してください。',
        'exit':          '終了',
        'enter':         'ENTER で続ける',
        'invalid':       '無効な番号',
        'not_a_number':  '番号を入力してください',
    },
    'ko': {
        'gh_label':      '토큰 생성 방법',
        'gh_title':      'GITHUB 토큰 생성 방법',
        'gh_saved':      '저장된 토큰을 찾았습니다',
        'gh_use':        '이 토큰을 사용하시겠습니까? (Y/n) :',
        'gh_confirmed':  '별 확인됨 — STAR TOOLS 잠금 해제!',
        'gh_not_starred':'{repo}에 아직 별을 주지 않았습니다.',
        'gh_star_here':  '→ 여기서 별을 주세요:',
        'gh_paste':      '토큰 붙여넣기 (빈칸 = 취소) :',
        'gh_step1':      '1. 이동     https://github.com/settings/tokens',
        'gh_step2':      '2. 클릭     Generate new token (classic)',
        'gh_step3':      '3. 범위     ✓ read:user   (이것만)',
        'gh_step4':      '4. 토큰 복사 — GitHub는 한 번만 표시합니다!',
        'gh_saved_ok':   '토큰이 저장되었습니다',
        'gh_gitignore':  '.gh_token을 .gitignore에 추가하세요!',
        'star_unlock':   'STAR TOOLS  (잠금 해제)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  잠금 해제하려면 별 주기 →',
        'star_locked_msg':'이 툴은 {repo} 스타러 전용입니다',
        'star_info':     '별은 여기 →',
        'star_token':    '[G]를 실행해 GitHub 토큰을 설정하세요.',
        'exit':          '종료',
        'enter':         '계속하려면 ENTER',
        'invalid':       '잘못된 번호',
        'not_a_number':  '번호를 입력하세요',
    },
    'zh': {
        'gh_label':      '如何创建令牌',
        'gh_title':      '如何创建 GITHUB 令牌',
        'gh_saved':      '找到已保存的令牌',
        'gh_use':        '使用此令牌？(Y/n) :',
        'gh_confirmed':  '星标已确认 — STAR TOOLS 已解锁！',
        'gh_not_starred':'你还没有给 {repo} 加星标。',
        'gh_star_here':  '→ 在这里加星标:',
        'gh_paste':      '粘贴令牌（空白取消）:',
        'gh_step1':      '1. 前往     https://github.com/settings/tokens',
        'gh_step2':      '2. 点击     Generate new token (classic)',
        'gh_step3':      '3. 权限     ✓ read:user   (仅此一项)',
        'gh_step4':      '4. 复制令牌 — GitHub 只显示一次！',
        'gh_saved_ok':   '令牌已保存',
        'gh_gitignore':  '将 .gh_token 添加到 .gitignore！',
        'star_unlock':   'STAR TOOLS  (已解锁)',
        'star_locked':   'STAR TOOLS',
        'star_hint':     '☆  加星标以解锁 →',
        'star_locked_msg':'此工具仅限 {repo} 的星标用户',
        'star_info':     '星标在此 →',
        'star_token':    '运行 [G] 配置 GitHub 令牌。',
        'exit':          '退出',
        'enter':         '按 ENTER 继续',
        'invalid':       '无效编号',
        'not_a_number':  '请输入一个数字',
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
    },
}

_LANG_CACHE = None
def t(key: str) -> str:
    """Retourne la chaîne traduite selon le pays détecté."""
    global _LANG_CACHE
    if _LANG_CACHE is None:
        country = get_country()
        lang    = _LANG_MAP.get(country, 'en')
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
    return input(c(f"  [?] {prompt} ", CYAN)).strip()

def ok(msg):   print(c(f"  [+] {msg}", GREEN))
def err(msg):  print(c(f"  [-] {msg}", RED))
def info(msg): print(c(f"  [i] {msg}", CYAN))

# ── Scan folders ───────────────────────────────────────────
def get_name(filepath):
    import re as _re
    PAT = _re.compile(r'''(?x) ^ \#? \s* NAME \s* = \s* (?P<q> ["']) (.+?) (?P=q) ''')
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = PAT.match(line.strip())
                if m:
                    val = m.group(2).strip()
                    if val: return val
    except Exception:
        pass
    return os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()

def scan_folder(folder):
    if not os.path.isdir(folder):
        return []
    files = sorted([
        f for f in os.listdir(folder)
        if f.endswith('.py') and not f.startswith('_')
    ])
    return [os.path.join(folder, f) for f in files]

# ── Star gate ──────────────────────────────────────────────
_STAR_CACHE = None

def _check_star_github() -> bool:
    global _STAR_CACHE
    if _STAR_CACHE is not None:
        return _STAR_CACHE
    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    if not os.path.isfile(token_path):
        _STAR_CACHE = False; return False
    try:
        with open(token_path) as f: token = f.read().strip()
        if not token: _STAR_CACHE = False; return False
    except Exception:
        _STAR_CACHE = False; return False
    req = urllib.request.Request(
        f"https://api.github.com/user/starred/{GITHUB_REPO}",
        headers={
            'Authorization':        f'Bearer {token}',
            'Accept':               'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent':           'existentielle-launcher',
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            _STAR_CACHE = (r.status == 204)
    except urllib.error.HTTPError:
        _STAR_CACHE = False
    except Exception:
        _STAR_CACHE = False
    return _STAR_CACHE

def _STAR_CACHE_reset():
    global _STAR_CACHE
    _STAR_CACHE = None

def save_token(token):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    with open(path, 'w') as f: f.write(token.strip())
    ok(f"{t('gh_saved_ok')}  →  {path}")
    info(t('gh_gitignore'))

# ── GitHub setup ───────────────────────────────────────────
def github_setup():
    global _STAR_CACHE
    cls(); print(purplepink(BANNER)); print()
    print(c(f"  ─────  {t('gh_title')}  ─────────────────────────────────", PINK)); print()

    token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.gh_token')
    if os.path.isfile(token_path):
        with open(token_path) as f: saved = f.read().strip()
        if saved:
            info(f"{t('gh_saved')} : {saved[:8]}{'*'*(len(saved)-8)}")
            if ask(t('gh_use')).lower() not in ('n','no','non','нет','لا','hayır','nee','nie','いいえ','아니오','否'):
                _STAR_CACHE = None
                if _check_star_github():
                    ok(t('gh_confirmed'))
                else:
                    err(t('gh_not_starred'))
                    print(c(f"\n  {t('gh_star_here')} https://github.com/{GITHUB_REPO}\n", CYAN))
                input(c(f"  [{t('enter')}]", GRAY)); return

    print(c("  ┌───────────────────────────────────────────────────────────────┐", PINK))
    print(c(f"  │  {t('gh_step1'):<63}│", WHITE))
    print(c(f"  │  {t('gh_step2'):<63}│", WHITE))
    print(c(f"  │  {t('gh_step3'):<63}│", WHITE))
    print(c(f"  │  {t('gh_step4'):<63}│", WHITE))
    print(c("  └───────────────────────────────────────────────────────────────┘", PINK))
    print()
    token = ask(t('gh_paste'))
    if not token: return
    _STAR_CACHE = None
    save_token(token)
    print()
    if _check_star_github():
        ok(t('gh_confirmed'))
    else:
        err(t('gh_not_starred'))
        print(c(f"\n  {t('gh_star_here')} https://github.com/{GITHUB_REPO}\n", CYAN))
    input(c(f"  [{t('enter')}]", GRAY))

# ── Launch ─────────────────────────────────────────────────
def launch(filepath):
    try:
        subprocess.run([sys.executable, filepath], check=False)
    except FileNotFoundError:
        err("Python not found"); time.sleep(0.8)
    except KeyboardInterrupt:
        pass

# ── Main menu ──────────────────────────────────────────────
def main_menu():
    while True:
        free_tools = scan_folder(TOOLS_DIR)
        star_tools = scan_folder(STAR_DIR)
        star_ok    = _check_star_github()

        show_banner()

        # ── Free tools ──────────────────────────────────
        if free_tools:
            print(c("  ─────  TOOLS  ──────────────────────────────────────────────────", PINK))
            for i, fp in enumerate(free_tools, 1):
                name = get_name(fp)
                print(c(f"  [{i:>2}]", PINK) + c(f"  {name}", WHITE))
            print()
        else:
            print(c("  [tools/]  empty — drop your .py files here", GRAY))
            print()

        # ── Star tools ──────────────────────────────────
        if star_tools:
            if star_ok:
                print(c(f"  ─────  ★  {t('star_unlock')}  ─────────────────────────────────", YELLOW))
                offset = len(free_tools)
                for i, fp in enumerate(star_tools, offset + 1):
                    name = get_name(fp)
                    print(c(f"  [{i:>2}]", YELLOW) + c(f"  {name}", YELLOW))
            else:
                print(c(f"  ─────  ★  {t('star_locked')}  ──────────────────────────────────────", YELLOW))
                offset = len(free_tools)
                for i, fp in enumerate(star_tools, offset + 1):
                    name = get_name(fp)
                    print(c(f"  [{i:>2}]", YELLOW) + c(f"  {name}  ", YELLOW) + c("[ ★ ]", YELLOW))
                print()
                print(c(f"  {t('star_hint')} https://github.com/{GITHUB_REPO}", YELLOW))
            print()

        # ── Bottom ──────────────────────────────────────
        print(c("  ─────────────────────────────────────────────────────────────────", GRAY))
        print(c("  [ G]", CYAN) + c(f"  {t('gh_label')}", WHITE))
        print(c("  [ 0]", GRAY) + c(f"  {t('exit')}", GRAY))
        print()

        choice = ask(">>")

        if choice == '0':
            cls(); sys.exit(0)

        elif choice.upper() == 'G':
            github_setup()
            _STAR_CACHE_reset()

        else:
            try:
                n          = int(choice)
                total_free = len(free_tools)
                total_star = len(star_tools)

                if 1 <= n <= total_free:
                    launch(free_tools[n - 1])

                elif total_free < n <= total_free + total_star:
                    if not star_ok:
                        print()
                        err(t('star_locked_msg'))
                        info(f"{t('star_info')} https://github.com/{GITHUB_REPO}")
                        info(t('star_token'))
                        time.sleep(2.5)
                    else:
                        launch(star_tools[n - total_free - 1])
                else:
                    err(t('invalid')); time.sleep(0.4)

            except ValueError:
                err(t('not_a_number')); time.sleep(0.4)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        cls()
        print(c(f"\n  Bye — {BRANDING_URL}\n", PINK))
        sys.exit(0)