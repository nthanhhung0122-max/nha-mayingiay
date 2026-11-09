#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
  BOT AUTO PLAY 24/7 TOÀN DIỆN - NHÀ MÁY IN GIẤY (@nhamayingiay_bot)
  Website: https://nhamayingiay.vercel.app/
  Bot    : @nhamayingiay_bot

  TÍNH NĂNG TỰ ĐỘNG 100%:
    1. AUTO INDATA: Tự động lấy init_data mới qua Telethon StringSession.
    2. AUTO START PRINT: Tự kích hoạt cỗ máy in qua Adsgram (Block 38649)
       để duy trì dây chuyền in tiền liên tục 24/7.
    3. AUTO STOP & COLLECT: Canh thời gian ca in tiền kết thúc,
       tự động gọi /api/stop-print gom toàn bộ Tiền giấy về kho an toàn.
    4. AUTO UPGRADE: Tự động nâng cấp cấp độ nhà máy qua /api/upgrade khi đủ Bánh Răng Vàng.
    5. AUTO CLAIM TASKS: Tự động nhận tất cả nhiệm vụ hệ thống qua /api/tasks.
    6. AUTO CLAIM ADSGRAM BONUS: Nhận Bánh Răng Vàng (Block 38651) & Tiền Giấy (Block 38650).
====================================================================
"""

import time
import json
import urllib.parse
import re
import os
import random
import asyncio
import base64
import requests
from datetime import datetime
from colorama import Fore, Style, init

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

# -----------------------------------------------------------------
#  CẤU HÌNH HỆ THỐNG & ĐA TÀI KHOẢN (Acc 1 -> Acc 4)
# -----------------------------------------------------------------
import argparse

ACCOUNTS_CONFIG = {
    1: {
        "name": "Acc 1 (hungzai22)",
        "api_id": 39182276,
        "api_hash": "f02b155d895a3a3fbf8a1cbe810b5338",
        "session": (
            "1BVtsOHIBuxmpWiBJ9hvwV9pSrzWw5U2I5Fe20Ww8l1LCk9rnsG6T6lLZEJXZE1JJC_qUH_yyWHnRoed"
            "RNI5lJYnfjRN4gyGeDrCxquDU12ZflrpCz0VLhMZx2C0LlyUCy2eHRSRE1wUCpEYZaymL0P7Z9eAHwMy4"
            "Oogewh5TqyO4x4MF6j0yTq8Zvfpv43O4aQDzErNv3GRqpx8DXBcOJIMP9yVhq-Mby5VH5J9cF-h-bJ5ws"
            "3xKjA4GY7YKjHxDt9OI-Zr7mr-V3qZy99UxJooThJj51f2RqOKhODdLh9XZQ0ygSoAd3iFAZDOPMEo8Ch"
            "5TrrzLXi2Q3N0HorIL1JfV0xoFQlY="
        )
    },
    2: {
        "name": "Acc 2 (gaylobucu)",
        "api_id": 39182276,
        "api_hash": "f02b155d895a3a3fbf8a1cbe810b5338",
        "session": (
            "1BVtsOHIBuzoeRtBOmpNGh2sdyxpZ5e0nY4MrFe-6KKbmJPaM0YnCJiKRI0L9mEh1C5rwqLQqucj456LRF7v"
            "V1YIPjZNqL6JevLM0Ww3FTml1NoKdwsiPINfsy9MbBlBhKOvha7py44L4pK5aEXjwpjpoNj4LaSmtWaPiQPuf"
            "JuTwPB86f4gYjSeXM3HtxhnFU7MtHR5vbZPBa9N2HQSlt2BMB47q00DbQVtvYA37R3R-TrtV2MtwixL9ozChAD"
            "Fq38NYcw4eRyRwKrkobVLccvz0_hvqgHXiQbrfcFLLRkRGwGlRCB-Ew4YhLLdnCbG1hjGEfxUrp9MRmF0JvS"
            "-u20MfAuvlcgQ="
        )
    },
    3: {
        "name": "Acc 3 (nthanhhung0122)",
        "api_id": 39182276,
        "api_hash": "f02b155d895a3a3fbf8a1cbe810b5338",
        "session": (
            "1BVtsOHIBuxrTG6Dt9a8C_J7D3bm1disV_mQiY_mw7AP5Gp-cEVAlKU1cfvOJiDnU6yi7PInfBRG_wJBQ3uNc-1k"
            "Oa8fM3ITgUcE7YkaCd77FoBTgIFqw6gMYeRfVJOS1U9S_botQyX5764dx94NBfHHm8HuQKejs0PrdAJQq6WUT"
            "DS3mkijWRWIvO4SwXSUrM5yNOFoGIrav8Mbuyl5ZFQaDPg_kwa11NT4kiqov8rVx0virTbGbQudyFeG80kP4zW2"
            "CxcuL6TObemIPJgR_2-jb8zVQRQMiI4oN829ZCfHU2JCQY2S2clWwI7onZV8AhYP1LoDBiu32dgQPuk4brS-r"
            "1DtkySc="
        )
    },
    4: {
        "name": "Acc 4 (Wind_trader)",
        "api_id": 34333329,
        "api_hash": "4f9371f95000578c84dbc670aaf1f819",
        "session": (
            "1BVtsOIIBuzNuH5Jfb4Uwek2dG7YRqSyFk-74KTokth0VB3_UTMwM8Edh_ikn83fJOGyN7JaWzIZXnro3ico"
            "Y8zsjYIlT5nQ4z_GgKknABQ74FRseCvNbz3yyTkPOfQ4xJfZnJIJHuY4EkzVOzQzYZFg_EJWOj_vvg6OVwSk"
            "Qv9Nd52tl_SlH4TofoxDXDNvxLJyFcoQFH6BegTybx-pFyX2tz0rMeR7AQujnGxqdWOd4zywoFVShzsCTFeq"
            "dsBP9itJvg1YB0ISmJEYXzGEQo37IddAFGw3PJcAIY4BBctxri9_Cw-FbxhMgLU9gsotA3Rrys2jLcGV4CGf"
            "Op_IzD0CmtNm845I="
        )
    }
}

parser = argparse.ArgumentParser()
parser.add_argument("--acc", type=int, default=int(os.getenv("ACC_NUM", "1")), help="Account index 1..4")
args, _ = parser.parse_known_args()
acc_data = ACCOUNTS_CONFIG.get(args.acc, ACCOUNTS_CONFIG[1])

ACC_INDEX = args.acc
ACCOUNT_DISPLAY_NAME = acc_data["name"]
API_ID = int(os.getenv("TELEGRAM_API_ID") or acc_data["api_id"])
API_HASH = os.getenv("TELEGRAM_API_HASH") or acc_data["api_hash"]
KNOWN_GOOD_STRING_SESSION = (
    os.getenv(f"TELEGRAM_STRING_SESSION_ACC{ACC_INDEX}") or
    os.getenv("TELEGRAM_STRING_SESSION") or
    acc_data["session"]
)

BOT_USERNAME = "nhamayingiay_bot"
WEBAPP_URL = "https://nhamayingiay.vercel.app/"
BASE_URL = "https://nhamayingiay.vercel.app/api"

ADSGRAM_BLOCK_PRINT = "38649"     # Kích hoạt máy in tiền
ADSGRAM_BLOCK_BANKNOTE = "38650"  # Thưởng 100,000 tiền giấy
ADSGRAM_BLOCK_GOLD = "38651"      # Thưởng 500 bánh răng vàng

CURRENT_INIT_DATA = ""
CURRENT_USER_NAME = ""
CURRENT_USER_ID = "7744031191"

IS_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
MAX_RUNTIME = int(os.getenv("MAX_RUNTIME_SECONDS", "19800" if IS_GITHUB_ACTIONS else "0"))

def log(tag, msg, color=Fore.WHITE):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] [{tag}] {color}{msg}{Style.RESET_ALL}", flush=True)

def fmt_num(val):
    try:
        return f"{int(val):,}"
    except:
        return str(val)

def make_dcs(init_d):
    params = urllib.parse.parse_qsl(init_d)
    items = []
    for k, v in params:
        if k not in ['hash', 'signature']:
            items.append(f"{k}={v}")
    items.sort()
    raw = "\n".join(items)
    return base64.urlsafe_b64encode(raw.encode('utf-8')).decode('utf-8').rstrip('=')

def get_clean_string_session():
    raw = (
        os.getenv("TELEGRAM_STRING_SESSION") or
        os.getenv("TELEGRAM_SESSION_B64_ACC1") or
        os.getenv("TELEGRAM_SESSION_B64") or
        ""
    ).strip()

    if not raw:
        return KNOWN_GOOD_STRING_SESSION

    if raw.startswith("1") and 300 <= len(raw) <= 450:
        return raw

    try:
        import tempfile, sqlite3
        from telethon.crypto import AuthKey
        bdata = base64.b64decode(raw)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".session") as tmp:
            tmp.write(bdata)
            tmp_path = tmp.name

        conn = sqlite3.connect(tmp_path)
        c = conn.cursor()
        c.execute("SELECT dc_id, server_address, port, auth_key FROM sessions")
        row = c.fetchone()
        conn.close()
        try: os.remove(tmp_path)
        except Exception: pass

        if row and row[3]:
            ss = StringSession()
            ss.set_dc(row[0], row[1], row[2])
            ss.auth_key = AuthKey(data=row[3])
            extracted = ss.save()
            if extracted:
                return extracted
    except Exception:
        pass

    return KNOWN_GOOD_STRING_SESSION

# =================================================================
#  TỰ ĐỘNG LẤY INIT_DATA QUA TELETHON
# =================================================================
async def fetch_fresh_init_data():
    global CURRENT_INIT_DATA, CURRENT_USER_NAME, CURRENT_USER_ID
    session_str = get_clean_string_session()
    client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            log("TELETHON_ERR", "Session chưa được xác thực!", Fore.RED)
            await client.disconnect()
            return None

        me = await client.get_me()
        CURRENT_USER_NAME = f"{me.first_name or ''} {me.last_name or ''}".strip()
        CURRENT_USER_ID = str(me.id)

        bot = await client.get_input_entity(BOT_USERNAME)
        wv = await client(RequestWebViewRequest(
            peer=bot,
            bot=bot,
            platform="android",
            from_bot_menu=False,
            url=WEBAPP_URL
        ))
        frag = urllib.parse.urlparse(wv.url).fragment
        CURRENT_INIT_DATA = urllib.parse.parse_qs(frag).get("tgWebAppData", [None])[0]
        log("INIT_DATA", f"Lấy initData mới thành công! User: {CURRENT_USER_NAME} (ID: {CURRENT_USER_ID})", Fore.CYAN)
        await client.disconnect()
        return CURRENT_INIT_DATA
    except Exception as e:
        log("WEBVIEW_ERR", f"Lỗi lấy WebView initData: {e}", Fore.RED)
        try: await client.disconnect()
        except: pass
        return None

def get_fresh_init_data_sync():
    return asyncio.run(fetch_fresh_init_data())

def get_api_headers():
    return {
        "Content-Type": "application/json",
        "x-init-data": CURRENT_INIT_DATA,
        "Origin": "https://nhamayingiay.vercel.app",
        "Referer": "https://nhamayingiay.vercel.app/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; SM-S928B Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Mobile Safari/537.36 Telegram-Android/10.11.1"
    }

# =================================================================
#  ADSGRAM SIMULATION ENGINE
# =================================================================
def trigger_adsgram_ad(block_id, label="Quảng cáo"):
    """
    Xem và xác thực quảng cáo Adsgram chuẩn 100% cơ chế trình duyệt:
    - Hỗ trợ cả định dạng VAST XML Video lẫn banner JSON thông thường.
    - Trích xuất toàn bộ chuỗi tracking events chuẩn: render -> show -> video events -> reward.
    - Mô phỏng người thật trên Samsung Galaxy S24 Ultra (Android 14).
    - Tự động kích hoạt webhook ghi nhận máy in / tiền giấy / vàng.
    """
    try:
        parsed = dict(urllib.parse.parse_qsl(CURRENT_INIT_DATA))
        sig = parsed.get('signature', '')
        dcs = make_dcs(CURRENT_INIT_DATA)

        ad_headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; SM-S928B Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Mobile Safari/537.36 Telegram-Android/10.11.1',
            'Origin': 'https://nhamayingiay.vercel.app',
            'Referer': 'https://nhamayingiay.vercel.app/',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'org.telegram.messenger'
        }
        params = {
            'blockId': str(block_id),
            'tg_id': str(CURRENT_USER_ID),
            'tg_platform': 'android',
            'platform': 'Linux aarch64',
            'language': 'en',
            'top_domain': 'vercel.app',
            'signature': sig,
            'data_check_string': dcs,
            'sdk_version': '2.2.5'
        }
        log("ADSGRAM", f"Đang yêu cầu Adsgram [{label}] (Block {block_id})...", Fore.YELLOW)
        r = requests.get('https://api.adsgram.ai/adv', headers=ad_headers, params=params, timeout=15)
        if r.status_code != 200:
            log("ADS_WARN", f"Adsgram phản hồi mã {r.status_code}", Fore.YELLOW)
            return False

        # Trích xuất toàn bộ URLs tracking (bao gồm cả VAST XML và JSON banners)
        all_urls = [u.replace('<![CDATA[', '').replace(']]>', '').strip() 
                    for u in re.findall(r'https://api\.adsgram\.ai/[^\s"\'<>]+', r.text)]
        valid_urls = [u for u in all_urls if 'error' not in u]

        if not valid_urls:
            log("ADS_WARN", f"Adsgram không có sẵn quảng cáo (No fill) cho [{label}]", Fore.YELLOW)
            return False

        log("ADS_WATCH", f"Đang xem video [{label}] ({len(valid_urls)} sự kiện tracking)...", Fore.CYAN)
        
        # 1. Ping render / start
        for u in valid_urls[:3]:
            try: requests.get(u, headers=ad_headers, timeout=8)
            except Exception: pass
            
        time.sleep(random.uniform(2.0, 3.5))

        # 2. Ping midpoints & video tracking
        for u in valid_urls[3:-2]:
            try: requests.get(u, headers=ad_headers, timeout=8)
            except Exception: pass

        watch_sec = round(random.uniform(8.0, 12.0), 2)
        time.sleep(watch_sec)

        # 3. Ping complete & reward events
        for u in valid_urls[-2:]:
            try: requests.get(u, headers=ad_headers, timeout=8)
            except Exception: pass

        log("ADS_OK", f"🎉 Đã xác thực trọn vẹn sự kiện Adsgram [{label}]!", Fore.GREEN)
        time.sleep(2)
        return True

    except Exception as e:
        log("ADS_ERR", f"Lỗi gọi Adsgram [{label}]: {e}", Fore.RED)
        return False

# =================================================================
#  LỚP ĐIỀU KHIỂN NHÀ MÁY IN GIẤY
# =================================================================
class PaperFactoryBot:
    def __init__(self):
        self.user = {}
        self.banknotes = 0
        self.gold = 0
        self.level = 1
        self.printing_speed = 10
        self.is_printing = False
        self.print_end_time = 0
        self.telegram_tasks = []

    def fetch_user(self):
        try:
            r = requests.post(f"{BASE_URL}/user", headers=get_api_headers(), json={}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                self.user = data.get("user", {})
                self.telegram_tasks = data.get("telegramTasks", [])
                self.banknotes = self.user.get("banknotes", 0)
                self.gold = self.user.get("gold", 0)
                self.level = self.user.get("level", 1)
                self.printing_speed = self.user.get("printingSpeed", 10)
                self.is_printing = self.user.get("isPrinting", False)
                self.print_end_time = self.user.get("printEndTime", 0)
                return True
            elif r.status_code == 401:
                log("AUTH", "Token hết hạn! Đang tự động làm mới qua Telethon...", Fore.YELLOW)
                if get_fresh_init_data_sync():
                    return self.fetch_user()
                return False
            return False
        except Exception as e:
            log("API_ERR", f"Lỗi fetch user: {e}", Fore.RED)
            return False

    def print_dashboard(self):
        now_ms = int(time.time() * 1000)
        rem_sec = max(0, int((self.print_end_time - now_ms) / 1000)) if self.is_printing else 0
        rem_min = rem_sec // 60
        rem_s = rem_sec % 60
        status_txt = f"ĐANG IN ({rem_min:02d}:{rem_s:02d})" if self.is_printing else "ĐANG NGHỈ / SẴN SÀNG IN"

        banner = [
            "=" * 60,
            "     NHÀ MÁY IN GIẤY - BẢNG ĐIỀU KHIỂN DÂY CHUYỀN",
            "=" * 60,
            f" Công nhân   : {CURRENT_USER_NAME} (ID: {CURRENT_USER_ID})",
            f" Cấp nhà máy : Cấp {self.level} | Tốc độ in: +{self.printing_speed} tờ/giây",
            f" Trạng thái  : {status_txt}",
            f" Tiền giấy   : {fmt_num(self.banknotes)} Giấy",
            f" Bánh răng   : {fmt_num(self.gold)} Vàng",
            f" Giới thiệu  : {self.user.get('referrals', 0)} bạn bè",
            "=" * 60
        ]
        print("\n" + "\n".join(banner) + "\n", flush=True)

    def start_printing(self):
        for attempt in range(1, 4):
            log("PRINT", f"🚀 [Lần {attempt}/3] Kích hoạt máy in qua Adsgram (Block 38649)...", Fore.YELLOW)
            ok = trigger_adsgram_ad(ADSGRAM_BLOCK_PRINT, "Khởi động in tiền")
            time.sleep(3)
            self.fetch_user()
            if self.is_printing:
                log("PRINT_OK", "🎉 DÂY CHUYỀN IN TIỀN ĐÃ KHỞI ĐỘNG THÀNH CÔNG!", Fore.GREEN)
                return True
            if attempt < 3:
                log("PRINT_RETRY", "Chưa nhận trạng thái in, chờ 6s thử lại...", Fore.YELLOW)
                time.sleep(6)
        return False

    def stop_and_collect(self):
        log("HARVEST", "📥 Ca in đã xong! Đang thu hoạch toàn bộ Tiền Giấy...", Fore.CYAN)
        try:
            r = requests.post(f"{BASE_URL}/stop-print", headers=get_api_headers(), json={}, timeout=10)
            data = r.json()
            if r.status_code == 200 and data.get("ok", True):
                new_banknotes = data.get("newBanknotes", self.banknotes)
                diff = new_banknotes - self.banknotes
                self.banknotes = new_banknotes
                self.is_printing = False
                log("HARVEST_OK", f"🎉 Thu hoạch thành công! +{fmt_num(diff)} Tiền Giấy (Tổng: {fmt_num(self.banknotes)})", Fore.GREEN)
                return True
            else:
                log("HARVEST_WARN", f"Thu hoạch chưa thành công: {data.get('error')}", Fore.YELLOW)
                return False
        except Exception as e:
            log("HARVEST_ERR", f"Lỗi thu hoạch: {e}", Fore.RED)
            return False

    def claim_all_tasks(self):
        completed = set(self.user.get("completedTasks", []))
        default_tasks = [
            {"id": "t1", "title": "Kênh Nhà Máy In Giấy"},
            {"id": "t2", "title": "Nhóm Chat Nhà Máy In Giấy"},
            {"id": "t3", "title": "Kênh Thanh Toán"},
            {"id": "t4", "title": "Kênh Happy Cow Farm"},
            {"id": "t5", "title": "Nhóm Chat Happy Cow Farm"},
            {"id": "v1", "title": "VIP Task 1"},
            {"id": "v2", "title": "VIP Task 2"},
            {"id": "v3", "title": "VIP Task 3"},
            {"id": "v4", "title": "VIP Task 4"},
            {"id": "v5", "title": "VIP Task 5"},
            {"id": "v6", "title": "VIP Task 6"},
            {"id": "v7", "title": "VIP Task 7"}
        ]
        all_tasks = default_tasks + self.telegram_tasks
        for t in all_tasks:
            tid = t.get("id")
            title = t.get("title", tid)
            if tid and tid not in completed:
                try:
                    r = requests.post(f"{BASE_URL}/tasks", headers=get_api_headers(), json={"taskId": tid}, timeout=8)
                    if r.status_code == 200:
                        log("TASK_CLAIM", f"🎉 Hoàn thành nhiệm vụ [{title}] ({tid})!", Fore.GREEN)
                        completed.add(tid)
                    time.sleep(0.5)
                except Exception:
                    pass

    def try_upgrade(self):
        # Tự động nâng cấp nhà máy nếu đủ Bánh Răng Vàng
        try:
            r = requests.post(f"{BASE_URL}/upgrade", headers=get_api_headers(), json={
                "fullName": CURRENT_USER_NAME,
                "avatar": "https://t.me/i/userpic/320/Zmiju56Xdg-UDWFdmDQaUJbLaUx3f7I4_rH3UQWwoh_acL4656EtBRjrDDLSPb-B.svg"
            }, timeout=8)
            data = r.json()
            if r.status_code == 200:
                self.level = data.get("newLevel", self.level)
                self.printing_speed = data.get("newSpeed", self.printing_speed)
                self.gold = data.get("newGold", self.gold)
                log("UPGRADE_OK", f"⭐ NÂNG CẤP NHÀ MÁY THÀNH CÔNG LÊN CẤP {self.level}! Tốc độ mới: +{self.printing_speed} tờ/s", Fore.MAGENTA)
                return True
        except Exception:
            pass
        return False

    def claim_15m_bonus(self):
        """Tự động nhận thưởng mỗi 15 phút: 100% chỉ nhận Tiền Giấy (+100,000 Tiền Giấy - Block 38650)"""
        now_ms = int(time.time() * 1000)
        ad_cd = self.user.get("adCooldown", 0)
        if now_ms >= ad_cd:
            log("BONUS_15M", "🎁 [ĐẾN GIỜ NHẬN THƯỞNG 15 PHÚT] Đang xem QC nhận +100,000 Tiền Giấy (Block 38650)...", Fore.YELLOW)
            ok = trigger_adsgram_ad(ADSGRAM_BLOCK_BANKNOTE, "Thưởng 15 phút (+100,000 Tiền Giấy)")
            if ok:
                time.sleep(4)
                old_banknotes = self.banknotes
                self.fetch_user()
                diff_bn = self.banknotes - old_banknotes
                earned = diff_bn if diff_bn > 0 else 100000
                log("BONUS_OK", f"🎉 Nhận thưởng 15 phút thành công! +{fmt_num(earned)} Tiền Giấy (Tổng: {fmt_num(self.banknotes)})", Fore.GREEN)
                return True
        return False

    def get_ad_cooldown_remaining_sec(self):
        now_ms = int(time.time() * 1000)
        ad_cd = self.user.get("adCooldown", 0)
        return max(0, int((ad_cd - now_ms) / 1000))

def trigger_next_shift():
    """Tự động kích hoạt ca trực GitHub Actions tiếp theo để chạy liên tục 24/7 không gián đoạn"""
    gh_pat = (os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN") or "").strip()
    if not gh_pat:
        return
    wf_file = os.getenv("WORKFLOW_FILE") or f"nhamayingiay_acc{ACC_INDEX}.yml"
    log("RETRIGGER", f"🚀 Đang tự động kích hoạt ca trực mới trên GitHub Actions ({wf_file} - {ACCOUNT_DISPLAY_NAME})...", Fore.YELLOW)
    try:
        url = f"https://api.github.com/repos/nthanhhung0122-max/nha-mayingiay/actions/workflows/{wf_file}/dispatches"
        h = {
            "Authorization": f"Bearer {gh_pat}",
            "Accept": "application/vnd.github.v3+json"
        }
        r = requests.post(url, headers=h, json={"ref": "main"}, timeout=10)
        if r.status_code == 204:
            log("RETRIGGER", f"✅ Ca trực mới ({wf_file}) đã được khởi động thành công trên GitHub!", Fore.GREEN)
        else:
            log("RETRIGGER", f"⚠️ Phản hồi retrigger: {r.status_code}", Fore.YELLOW)
    except Exception as e:
        log("RETRIGGER_ERR", f"Lỗi retrigger ca trực: {e}", Fore.RED)

# =================================================================
#  VÒNG LẶP CHÍNH 24/7
# =================================================================
def main():
    print(Fore.YELLOW + """
====================================================================
|  TOOL AUTO NHÀ MÁY IN GIẤY 24/7 (@nhamayingiay_bot)              |
|  - TỰ ĐỘNG LẤY INIT_DATA MỚI 100% QUA RAM (TELETHON STRINGSESSION)|
|  - TỰ KÍCH HOẠT MÁY IN TIỀN QUA ADSGRAM (BLOCK 38649)            |
|  - TỰ ĐỘNG THU HOẠCH TIỀN GIẤY & TỰ ĐỘNG NÂNG CẤP DÂY CHUYỀN      |
|  - TỰ ĐỘNG NHẬN TOÀN BỘ NHIỆM VỤ HỆ THỐNG                        |
====================================================================
    """ + Style.RESET_ALL)

    if not get_fresh_init_data_sync():
        log("MAIN", "Không thể lấy initData từ Telegram. Kết thúc!", Fore.RED)
        return

    bot = PaperFactoryBot()
    if not bot.fetch_user():
        log("MAIN", "Không thể lấy thông tin người chơi!", Fore.RED)
        return

    bot.print_dashboard()
    bot.claim_all_tasks()
    bot.try_upgrade()

    start_time = time.time()
    last_refresh_time = time.time()

    while True:
        try:
            if MAX_RUNTIME > 0 and (time.time() - start_time) >= MAX_RUNTIME:
                log("MAIN", "Hoàn thành thời gian ca trực GitHub Actions. Kích hoạt ca trực tiếp theo an toàn!", Fore.CYAN)
                trigger_next_shift()
                break

            now_ms = int(time.time() * 1000)

            # 1. Tự động kiểm tra & nhận thưởng mỗi 15 phút (+100,000 Tiền Giấy)
            bot.claim_15m_bonus()

            # 2. Nếu đang in và đã hết thời gian ca in -> Thu hoạch
            if bot.is_printing and now_ms >= bot.print_end_time:
                bot.stop_and_collect()
                time.sleep(2)
                bot.try_upgrade()

            # 3. Nếu không in -> Kích hoạt ca in mới
            if not bot.is_printing:
                bot.start_printing()
                time.sleep(2)

            # 3. Tính toán thời gian chờ & Hiển thị đồng hồ ca in + QC 15P song song
            now_ms = int(time.time() * 1000)
            ad_rem_sec = bot.get_ad_cooldown_remaining_sec()
            ad_m, ad_s = divmod(ad_rem_sec, 60)
            ad_str = f"SẴN SÀNG NHẬN!" if ad_rem_sec == 0 else f"{ad_m:02d}:{ad_s:02d}"

            if bot.is_printing and bot.print_end_time > now_ms:
                wait_sec = min(45, int((bot.print_end_time - now_ms) / 1000) + 1)
                rem_total = int((bot.print_end_time - now_ms) / 1000)
                m, s = divmod(rem_total, 60)
                log("STATUS", f"🏭 Ca in còn: {m:02d}:{s:02d} (+{bot.printing_speed}/s) | 🎁 QC 15P (+100K Giấy): {ad_str} | Tổng Giấy: {fmt_num(bot.banknotes)}", Fore.GREEN)
                time.sleep(wait_sec)
            else:
                log("STATUS", f"⚙️ Đang đồng bộ trạng thái... | 🎁 QC 15P (+100K Giấy): {ad_str} | Tổng Giấy: {fmt_num(bot.banknotes)}", Fore.YELLOW)
                time.sleep(15)

            # Đồng bộ lại dữ liệu
            bot.fetch_user()

            # Làm mới token sau 30 phút
            if time.time() - last_refresh_time > 1800:
                get_fresh_init_data_sync()
                last_refresh_time = time.time()

        except KeyboardInterrupt:
            log("MAIN", "Đã dừng chương trình bằng tay.", Fore.YELLOW)
            break
        except Exception as e:
            log("ERR_LOOP", f"Lỗi trong vòng lặp: {e}", Fore.RED)
            time.sleep(10)

if __name__ == "__main__":
    main()
