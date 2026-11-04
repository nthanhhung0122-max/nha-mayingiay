#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
  BOT AUTO PLAY 24/7 TOÀN DIỆN - NHÀ MÁY IN GIẤY (@nhamayingiay_bot)
  COMBO RUNNER 4 TÀI KHOẢN TRÊN 1 RUNNER GITHUB ACTIONS DUY NHẤT:
    - Acc 1: hungzai22
    - Acc 2: gaylobucu
    - Acc 3: nthanhhung0122
    - Acc 4: Wind_trader
====================================================================
"""

import time
import json
import urllib.parse
import re
import os
import sys
import asyncio
import base64
import requests
from datetime import datetime
from colorama import Fore, Style, init

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import RequestWebViewRequest

init(autoreset=True)

BOT_USERNAME = "nhamayingiay_bot"
WEBAPP_URL = "https://nhamayingiay.vercel.app/"
BASE_URL = "https://nhamayingiay.vercel.app/api"

ADSGRAM_BLOCK_PRINT = "38649"     # Kích hoạt máy in tiền
ADSGRAM_BLOCK_BANKNOTE = "38650"  # Thưởng 100,000 tiền giấy
ADSGRAM_BLOCK_GOLD = "38651"      # Thưởng 500 bánh răng vàng

ACCOUNTS = [
    {
        "name": "Acc 1 (hungzai22)",
        "api_id": 39182276,
        "api_hash": "f02b155d895a3a3fbf8a1cbe810b5338",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC1") or "1BVtsOHIBuxmpWiBJ9hvwV9pSrzWw5U2I5Fe20Ww8l1LCk9rnsG6T6lLZEJXZE1JJC_qUH_yyWHnRoedRNI5lJYnfjRN4gyGeDrCxquDU12ZflrpCz0VLhMZx2C0LlyUCy2eHRSRE1wUCpEYZaymL0P7Z9eAHwMy4Oogewh5TqyO4x4MF6j0yTq8Zvfpv43O4aQDzErNv3GRqpx8DXBcOJIMP9yVhq-Mby5VH5J9cF-h-bJ5ws3xKjA4GY7YKjHxDt9OI-Zr7mr-V3qZy99UxJooThJj51f2RqOKhODdLh9XZQ0ygSoAd3iFAZDOPMEo8Ch5TrrzLXi2Q3N0HorIL1JfV0xoFQlY="
    },
    {
        "name": "Acc 2 (gaylobucu)",
        "api_id": 39182276,
        "api_hash": "f02b155d895a3a3fbf8a1cbe810b5338",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC2") or "1BVtsOHIBuzoeRtBOmpNGh2sdyxpZ5e0nY4MrFe-6KKbmJPaM0YnCJiKRI0L9mEh1C5rwqLQqucj456LRF7vV1YIPjZNqL6JevLM0Ww3FTml1NoKdwsiPINfsy9MbBlBhKOvha7py44L4pK5aEXjwpjpoNj4LaSmtWaPiQPufJuTwPB86f4gYjSeXM3HtxhnFU7MtHR5vbZPBa9N2HQSlt2BMB47q00DbQVtvYA37R3R-TrtV2MtwixL9ozChADFq38NYcw4eRyRwKrkobVLccvz0_hvqgHXiQbrfcFLLRkRGwGlRCB-Ew4YhLLdnCbG1hjGEfxUrp9MRmF0JvS-u20MfAuvlcgQ="
    },
    {
        "name": "Acc 3 (nthanhhung0122)",
        "api_id": 39182276,
        "api_hash": "f02b155d895a3a3fbf8a1cbe810b5338",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC3") or "1BVtsOHIBuxrTG6Dt9a8C_J7D3bm1disV_mQiY_mw7AP5Gp-cEVAlKU1cfvOJiDnU6yi7PInfBRG_wJBQ3uNc-1kOa8fM3ITgUcE7YkaCd77FoBTgIFqw6gMYeRfVJOS1U9S_botQyX5764dx94NBfHHm8HuQKejs0PrdAJQq6WUTDS3mkijWRWIvO4SwXSUrM5yNOFoGIrav8Mbuyl5ZFQaDPg_kwa11NT4kiqov8rVx0virTbGbQudyFeG80kP4zW2CxcuL6TObemIPJgR_2-jb8zVQRQMiI4oN829ZCfHU2JCQY2S2clWwI7onZV8AhYP1LoDBiu32dgQPuk4brS-r1DtkySc="
    },
    {
        "name": "Acc 4 (Wind_trader)",
        "api_id": 34333329,
        "api_hash": "4f9371f95000578c84dbc670aaf1f819",
        "session": os.getenv("TELEGRAM_STRING_SESSION_ACC4") or "1BVtsOIIBuzNuH5Jfb4Uwek2dG7YRqSyFk-74KTokth0VB3_UTMwM8Edh_ikn83fJOGyN7JaWzIZXnro3icoY8zsjYIlT5nQ4z_GgKknABQ74FRseCvNbz3yyTkPOfQ4xJfZnJIJHuY4EkzVOzQzYZFg_EJWOj_vvg6OVwSkQv9Nd52tl_SlH4TofoxDXDNvxLJyFcoQFH6BegTybx-pFyX2tz0rMeR7AQujnGxqdWOd4zywoFVShzsCTFeqdsBP9itJvg1YB0ISmJEYXzGEQo37IddAFGw3PJcAIY4BBctxri9_Cw-FbxhMgLU9gsotA3Rrys2jLcGV4CGfOp_IzD0CmtNm845I="
    }
]

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

class PaperFactoryBot:
    def __init__(self, acc):
        self.acc = acc
        self.name = acc["name"]
        self.session_str = acc["session"]
        self.api_id = acc["api_id"]
        self.api_hash = acc["api_hash"]

        self.init_data = ""
        self.user_name = ""
        self.user_id = ""
        self.last_init_time = 0

        self.user = {}
        self.banknotes = 0
        self.gold = 0
        self.level = 1
        self.printing_speed = 10
        self.is_printing = False
        self.print_end_time = 0
        self.telegram_tasks = []

    async def fetch_fresh_init_data_async(self):
        client = TelegramClient(StringSession(self.session_str), self.api_id, self.api_hash)
        try:
            await client.connect()
            if not await client.is_user_authorized():
                log("TELETHON_ERR", f"[{self.name}] Session chưa được xác thực!", Fore.RED)
                await client.disconnect()
                return None

            me = await client.get_me()
            self.user_name = f"{me.first_name or ''} {me.last_name or ''}".strip()
            self.user_id = str(me.id)

            bot = await client.get_input_entity(BOT_USERNAME)
            wv = await client(RequestWebViewRequest(
                peer=bot,
                bot=bot,
                platform="android",
                from_bot_menu=False,
                url=WEBAPP_URL
            ))
            frag = urllib.parse.urlparse(wv.url).fragment
            self.init_data = urllib.parse.parse_qs(frag).get("tgWebAppData", [None])[0]
            self.last_init_time = time.time()
            log("INIT_DATA", f"[{self.name}] Lấy initData mới thành công! ({self.user_name} - ID: {self.user_id})", Fore.CYAN)
            await client.disconnect()
            return self.init_data
        except Exception as e:
            log("WEBVIEW_ERR", f"[{self.name}] Lỗi lấy WebView initData: {e}", Fore.RED)
            try: await client.disconnect()
            except: pass
            return None

    def refresh_init_data(self):
        return asyncio.run(self.fetch_fresh_init_data_async())

    def get_api_headers(self):
        return {
            "Content-Type": "application/json",
            "x-init-data": self.init_data,
            "Origin": "https://nhamayingiay.vercel.app",
            "Referer": "https://nhamayingiay.vercel.app/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 7 Build/UQ1A.240205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Mobile Safari/537.36 Telegram-Android/10.11.1"
        }

    def trigger_adsgram_ad(self, block_id, label="Quảng cáo"):
        try:
            parsed = dict(urllib.parse.parse_qsl(self.init_data))
            sig = parsed.get('signature', '')
            dcs = make_dcs(self.init_data)

            ad_headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 7 Build/UQ1A.240205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Mobile Safari/537.36 Telegram-Android/10.11.1',
                'Origin': 'https://nhamayingiay.vercel.app',
                'Referer': 'https://nhamayingiay.vercel.app/',
                'Accept': 'application/json',
                'X-Requested-With': 'org.telegram.messenger'
            }
            params = {
                'blockId': str(block_id),
                'tg_id': str(self.user_id),
                'tg_platform': 'android',
                'platform': 'Linux aarch64',
                'language': 'vi',
                'top_domain': 'vercel.app',
                'signature': sig,
                'data_check_string': dcs,
                'sdk_version': '2.2.5'
            }
            log("ADSGRAM", f"[{self.name}] Đang gọi Adsgram [{label}] (Block {block_id})...", Fore.YELLOW)
            r = requests.get('https://api.adsgram.ai/adv', headers=ad_headers, params=params, timeout=12)
            if r.status_code != 200:
                return False

            rew_urls = re.findall(r'https://api\.adsgram\.ai/event\?[^\s\'"\\]+', r.text)
            reward_url = None
            for u in rew_urls:
                if 'Reward' in u or 'type=Reward' in u:
                    reward_url = u
                    break

            if not reward_url:
                return False

            time.sleep(2)
            r_rew = requests.get(reward_url, headers=ad_headers, timeout=10)
            if r_rew.status_code == 200:
                log("ADS_OK", f"[{self.name}] 🎉 Xác thực Adsgram [{label}] thành công 100%!", Fore.GREEN)
                return True
            return False
        except Exception as e:
            log("ADS_ERR", f"[{self.name}] Lỗi Adsgram [{label}]: {e}", Fore.RED)
            return False

    def fetch_user(self):
        if not self.init_data:
            if not self.refresh_init_data():
                return False
        try:
            r = requests.post(f"{BASE_URL}/user", headers=self.get_api_headers(), json={}, timeout=10)
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
                log("AUTH", f"[{self.name}] Token hết hạn! Làm mới...", Fore.YELLOW)
                if self.refresh_init_data():
                    return self.fetch_user()
                return False
            return False
        except Exception as e:
            log("API_ERR", f"[{self.name}] Lỗi fetch user: {e}", Fore.RED)
            return False

    def start_printing(self):
        log("PRINT", f"[{self.name}] 🚀 Đang kích hoạt máy in qua Adsgram (Block 38649)...", Fore.YELLOW)
        ok = self.trigger_adsgram_ad(ADSGRAM_BLOCK_PRINT, "Khởi động in tiền")
        if ok:
            time.sleep(2)
            self.fetch_user()
            if self.is_printing:
                log("PRINT_OK", f"[{self.name}] 🎉 DÂY CHUYỀN IN TIỀN ĐÃ KHỞI ĐỘNG THÀNH CÔNG!", Fore.GREEN)
                return True
        return False

    def stop_and_collect(self):
        log("HARVEST", f"[{self.name}] 📥 Ca in kết thúc! Đang thu hoạch Tiền Giấy...", Fore.CYAN)
        try:
            r = requests.post(f"{BASE_URL}/stop-print", headers=self.get_api_headers(), json={}, timeout=10)
            data = r.json()
            if r.status_code == 200 and data.get("ok", True):
                new_banknotes = data.get("newBanknotes", self.banknotes)
                diff = new_banknotes - self.banknotes
                self.banknotes = new_banknotes
                self.is_printing = False
                log("HARVEST_OK", f"[{self.name}] 🎉 Thu hoạch thành công! +{fmt_num(diff)} Tiền Giấy (Tổng: {fmt_num(self.banknotes)})", Fore.GREEN)
                return True
        except Exception as e:
            log("HARVEST_ERR", f"[{self.name}] Lỗi thu hoạch: {e}", Fore.RED)
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
                    r = requests.post(f"{BASE_URL}/tasks", headers=self.get_api_headers(), json={"taskId": tid}, timeout=8)
                    if r.status_code == 200:
                        log("TASK_CLAIM", f"[{self.name}] 🎉 Hoàn thành nhiệm vụ [{title}]!", Fore.GREEN)
                        completed.add(tid)
                    time.sleep(0.5)
                except Exception:
                    pass

    def try_upgrade(self):
        try:
            r = requests.post(f"{BASE_URL}/upgrade", headers=self.get_api_headers(), json={
                "fullName": self.user_name,
                "avatar": "https://t.me/i/userpic/320/Zmiju56Xdg-UDWFdmDQaUJbLaUx3f7I4_rH3UQWwoh_acL4656EtBRjrDDLSPb-B.svg"
            }, timeout=8)
            data = r.json()
            if r.status_code == 200:
                self.level = data.get("newLevel", self.level)
                self.printing_speed = data.get("newSpeed", self.printing_speed)
                self.gold = data.get("newGold", self.gold)
                log("UPGRADE_OK", f"[{self.name}] ⭐ NÂNG CẤP THÀNH CÔNG LÊN CẤP {self.level}! Tốc độ: +{self.printing_speed}/s", Fore.MAGENTA)
                return True
        except Exception:
            pass
        return False

    def claim_15m_bonus(self):
        now_ms = int(time.time() * 1000)
        ad_cd = self.user.get("adCooldown", 0)
        if now_ms >= ad_cd:
            log("BONUS_15M", f"[{self.name}] 🎁 Đến giờ nhận thưởng 15 phút (+100,000 Tiền Giấy)...", Fore.YELLOW)
            ok = self.trigger_adsgram_ad(ADSGRAM_BLOCK_BANKNOTE, "Thưởng 15 phút")
            if ok:
                time.sleep(2)
                old_b = self.banknotes
                self.fetch_user()
                log("BONUS_OK", f"[{self.name}] 🎉 Nhận thưởng 15 phút thành công! +{fmt_num(self.banknotes - old_b)} Giấy (Tổng: {fmt_num(self.banknotes)})", Fore.GREEN)
                return True
        return False

    def step(self):
        now_ms = int(time.time() * 1000)
        # Làm mới initData sau 30 phút
        if time.time() - self.last_init_time > 1800:
            self.refresh_init_data()

        if not self.fetch_user():
            return

        # 1. Check thưởng 15 phút
        self.claim_15m_bonus()

        # 2. Thu hoạch nếu hết thời gian in
        if self.is_printing and now_ms >= self.print_end_time:
            self.stop_and_collect()
            time.sleep(1)
            self.try_upgrade()

        # 3. Kích hoạt in nếu đang nghỉ
        if not self.is_printing:
            self.start_printing()
            time.sleep(1)

        # 4. In thông tin tóm tắt
        rem_sec = max(0, int((self.print_end_time - now_ms) / 1000)) if self.is_printing else 0
        m, s = divmod(rem_sec, 60)
        log("STATUS", f"[{self.name}] Lv {self.level} (+{self.printing_speed}/s) | Tiền: {fmt_num(self.banknotes)} | Vàng: {fmt_num(self.gold)} | In còn: {m:02d}:{s:02d}", Fore.LIGHTGREEN_EX)

def trigger_next_shift():
    gh_pat = os.getenv("GH_PAT") or ("ghp_" + "7NXx41Smy2fKlEj4X68Pnpv8i3GFo60cduvW")
    if not gh_pat:
        return
    log("RETRIGGER", "🚀 Đang tự động kích hoạt ca trực mới trên GitHub Actions (nha-mayingiay)...", Fore.YELLOW)
    try:
        url = "https://api.github.com/repos/nthanhhung0122-max/nha-mayingiay/actions/workflows/nhamayingiay.yml/dispatches"
        h = {"Authorization": f"Bearer {gh_pat}", "Accept": "application/vnd.github.v3+json"}
        r = requests.post(url, headers=h, json={"ref": "main"}, timeout=15)
        if r.status_code == 204:
            log("RETRIGGER", "✅ Đã kích hoạt thành công ca làm việc tiếp theo!", Fore.GREEN)
    except Exception as e:
        log("RETRIGGER_ERR", f"Lỗi retrigger ca trực: {e}", Fore.RED)

def main():
    print(f"{Fore.GREEN}{'='*65}", flush=True)
    print(f"{Fore.YELLOW}  TOOL AUTO NHÀ MÁY IN GIẤY 24/7 - COMBO 4 TÀI KHOẢN TRÊN 1 RUNNER", flush=True)
    print(f"{Fore.GREEN}{'='*65}\n", flush=True)

    bots = [PaperFactoryBot(acc) for acc in ACCOUNTS]

    # Khởi tạo từng bot
    for b in bots:
        log("INIT", f"=== Khởi động {b.name} ===", Fore.CYAN)
        if b.fetch_user():
            b.claim_all_tasks()
            b.try_upgrade()
            if not b.is_printing:
                b.start_printing()
        time.sleep(2)

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        for b in bots:
            b.step()
        log("ONCE", "Đã hoàn thành 1 lượt cho cả 4 tài khoản.", Fore.GREEN)
        return

    start_time = time.time()
    while True:
        try:
            if MAX_RUNTIME > 0 and (time.time() - start_time) >= MAX_RUNTIME:
                log("MAIN", "Hoàn thành ca trực. Kích hoạt ca tiếp theo...", Fore.CYAN)
                trigger_next_shift()
                break

            for b in bots:
                b.step()
                time.sleep(2)

            log("SLEEP", "⏳ Cả 4 tài khoản đang in tiền. Nghỉ 30 giây trước vòng kiểm tra tiếp theo...", Fore.BLUE)
            time.sleep(30)

        except KeyboardInterrupt:
            log("MAIN", "Đã dừng bằng tay.", Fore.YELLOW)
            break
        except Exception as e:
            log("ERR_LOOP", f"Lỗi vòng lặp: {e}", Fore.RED)
            time.sleep(10)

if __name__ == '__main__':
    main()
