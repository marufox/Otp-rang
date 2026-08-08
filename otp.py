import telebot
import os
import time
import threading
import requests
import json
import re
from telebot import types
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))
API_BASE = os.environ.get("API_URL", "https://api.2009.cloud/HXS47FLFX80U/tnews/@public/api")

bot = telebot.TeleBot(BOT_TOKEN)

# ================= 💎 PREMIUM EMOJIS (From Your Files) =================

FLAG_EMOJIS = {
    "1": {"emoji": "🇺🇸", "id": "5913463998522592692"},
    "880": {"emoji": "🇧🇩", "id": "5911365056594973179"},
    "91": {"emoji": "🇮🇳", "id": "5913754823643107921"},
    "92": {"emoji": "🇵🇰", "id": "5913705895375672082"},
    "44": {"emoji": "🇬🇧", "id": "5913443365499703513"},
    "261": {"emoji": "🇲🇬", "id": "5913766918271012920"},
    "232": {"emoji": "🇸🇱", "id": "5911210450657218661"},
    "90": {"emoji": "🇹🇷", "id": "5910995113881901195"},
    "49": {"emoji": "🇩🇪", "id": "5911096835887337583"},
    "81": {"emoji": "🇯🇵", "id": "5913293711659241040"},
    "86": {"emoji": "🇨🇳", "id": "5913779335021466780"},
    "55": {"emoji": "🇧🇷", "id": "5911148568768418614"},
    "7": {"emoji": "🇷🇺", "id": "5913274246867456342"},
    "33": {"emoji": "🇫🇷", "id": "5913605586414473124"},
    "39": {"emoji": "🇮🇹", "id": "5913688444923547525"},
    "34": {"emoji": "🇪🇸", "id": "5911193287967904547"},
    "31": {"emoji": "🇳🇱", "id": "5913367645226275100"},
    "46": {"emoji": "🇸🇪", "id": "5911156510162949403"},
    "47": {"emoji": "🇳🇴", "id": "5913617397574537046"},
    "41": {"emoji": "🇨🇭", "id": "5913271227505448072"},
    "351": {"emoji": "🇵🇹", "id": "5911023653939581472"},
    "54": {"emoji": "🇦🇷", "id": "5913573356979884082"},
    "52": {"emoji": "🇲🇽", "id": "5913687302462246518"},
    "57": {"emoji": "🇨🇴", "id": "5913773060074246009"},
    "60": {"emoji": "🇲🇾", "id": "5913654360063087453"},
    "62": {"emoji": "🇮🇩", "id": "5913479361620611038"},
    "63": {"emoji": "🇵🇭", "id": "5911268638874145162"},
    "61": {"emoji": "🇦🇺", "id": "5913632326880858455"},
    "64": {"emoji": "🇳🇿", "id": "5913640044937089340"},
    "66": {"emoji": "🇹🇭", "id": "5913617968805187987"},
    "82": {"emoji": "🇰🇷", "id": "5913371673905598425"},
    "84": {"emoji": "🇻🇳", "id": "5913428887164949581"},
    "98": {"emoji": "🇮🇷", "id": "5911308891307643032"},
    "212": {"emoji": "🇲🇦", "id": "5911482111633658301"},
    "213": {"emoji": "🇩🇿", "id": "5913782968563800236"},
    "216": {"emoji": "🇹🇳", "id": "5911332947419468671"},
    "218": {"emoji": "🇱🇾", "id": "5911236989260140996"},
    "220": {"emoji": "🇬🇲", "id": "5913657267755945883"},
    "221": {"emoji": "🇸🇳", "id": "5910995302860461643"},
    "222": {"emoji": "🇲🇷", "id": "5433859405898594234"},
    "223": {"emoji": "🇲🇱", "id": "5911305266355245916"},
    "224": {"emoji": "🇬🇳", "id": "5913471858312744319"},
    "225": {"emoji": "🇨🇮", "id": "5222233374948602940"},
    "226": {"emoji": "🇧🇫", "id": "5913407764515786948"},
    "227": {"emoji": "🇳🇪", "id": "5911270086278124251"},
    "228": {"emoji": "🇹🇬", "id": "5913423260757790970"},
    "229": {"emoji": "🇧🇯", "id": "5913735869952430547"},
    "230": {"emoji": "🇲🇺", "id": "5913291113204027321"},
    "231": {"emoji": "🇱🇷", "id": "5913324167272337727"},
    "233": {"emoji": "🇬🇭", "id": "5913391155877252952"},
    "234": {"emoji": "🇳🇬", "id": "5911143844304393105"},
    "235": {"emoji": "🇹🇩", "id": "5913299849167507310"},
    "236": {"emoji": "🇨🇫", "id": "5913443245240619222"},
    "237": {"emoji": "🇨🇲", "id": "5911172109484167745"},
    "238": {"emoji": "🇨🇻", "id": "5913571501554012193"},
    "239": {"emoji": "🇸🇹", "id": "5913574331937462345"},
    "240": {"emoji": "🇬🇶", "id": "5911306279967529251"},
    "241": {"emoji": "🇬🇦", "id": "5911037896051137264"},
    "242": {"emoji": "🇨🇬", "id": "5911338788574990168"},
    "243": {"emoji": "🇨🇩", "id": "5913770362834783827"},
    "244": {"emoji": "🇦🇴", "id": "5913753316109586411"},
    "245": {"emoji": "🇬🇼", "id": "5911398694778836149"},
    "248": {"emoji": "🇸🇨", "id": "5911185183364616913"},
    "249": {"emoji": "🇸🇩", "id": "5911387497799094470"},
    "250": {"emoji": "🇷🇼", "id": "5911455229433352234"},
    "251": {"emoji": "🇪🇹", "id": "5911078333168227043"},
    "252": {"emoji": "🇸🇴", "id": "5911397852965244436"},
    "253": {"emoji": "🇩🇯", "id": "5911407709915190157"},
    "254": {"emoji": "🇰🇪", "id": "5911154710571651231"},
    "255": {"emoji": "🇹🇿", "id": "5911418949844603556"},
    "256": {"emoji": "🇺🇬", "id": "5913488939397681980"},
    "257": {"emoji": "🇧🇮", "id": "5913766441529642752"},
    "258": {"emoji": "🇲🇿", "id": "5911333419865871464"},
    "260": {"emoji": "🇿🇲", "id": "5913564754160389778"},
    "263": {"emoji": "🇿🇼", "id": "5911092502265336396"},
    "264": {"emoji": "🇳🇦", "id": "5911108535378252443"},
    "265": {"emoji": "🇲🇼", "id": "5433968339154122439"},
    "266": {"emoji": "🇱🇸", "id": "5911059881988723711"},
    "267": {"emoji": "🇧🇼", "id": "5911513782722499475"},
    "268": {"emoji": "🇸🇿", "id": "5913374525763883286"},
    "269": {"emoji": "🇰🇲", "id": "5911338582416560604"},
    "290": {"emoji": "🇸🇭", "id": "5780471598922337683"},
    "291": {"emoji": "🇪🇷", "id": "5433723401464198287"},
    "297": {"emoji": "🇦🇼", "id": "5780471598922337683"},
    "298": {"emoji": "🇫🇴", "id": "5296469342039327674"},
    "299": {"emoji": "🇬🇱", "id": "5292014752283774878"},
    "350": {"emoji": "🇬🇮", "id": "5780471598922337683"},
    "352": {"emoji": "🇱🇺", "id": "5913390842344640293"},
    "353": {"emoji": "🇮🇪", "id": "5913440715504881532"},
    "354": {"emoji": "🇮🇸", "id": "5911047899029967246"},
    "355": {"emoji": "🇦🇱", "id": "5911357458797826163"},
    "356": {"emoji": "🇲🇹", "id": "5911023714069123567"},
    "357": {"emoji": "🇨🇾", "id": "5911023550860366409"},
    "358": {"emoji": "🇫🇮", "id": "5911041344909873378"},
    "359": {"emoji": "🇧🇬", "id": "5294329219965272288"},
    "370": {"emoji": "🇱🇹", "id": "5911172315642597775"},
    "371": {"emoji": "🇱🇻", "id": "5913738489882480243"},
    "372": {"emoji": "🇪🇪", "id": "5910986042910969906"},
    "373": {"emoji": "🇲🇩", "id": "5913456847402045950"},
    "374": {"emoji": "🇦🇲", "id": "5913272455866093666"},
    "375": {"emoji": "🇧🇾", "id": "5911011185649521599"},
    "376": {"emoji": "🇦🇩", "id": "5911314702398396902"},
    "377": {"emoji": "🇲🇨", "id": "5911245347266500057"},
    "378": {"emoji": "🇸🇲", "id": "5913587968458625465"},
    "379": {"emoji": "🇻🇦", "id": "5911211932420938860"},
    "380": {"emoji": "🇺🇦", "id": "5911406692007941050"},
    "381": {"emoji": "🇷🇸", "id": "5913592598433369871"},
    "382": {"emoji": "🇲🇪", "id": "5913239436157522151"},
    "383": {"emoji": "🇽🇰", "id": "5911433681582429010"},
    "385": {"emoji": "🇭🇷", "id": "5913692684056269311"},
    "386": {"emoji": "🇸🇮", "id": "5913431983836368644"},
    "387": {"emoji": "🇧🇦", "id": "5913700002680541032"},
    "389": {"emoji": "🇲🇰", "id": "5913394029210374721"},
    "420": {"emoji": "🇨🇿", "id": "5911198691036764307"},
    "421": {"emoji": "🇸🇰", "id": "5913751666842145020"},
    "423": {"emoji": "🇱🇮", "id": "5911166650580734660"},
    "500": {"emoji": "🇫🇰", "id": "5780471598922337683"},
    "501": {"emoji": "🇧🇿", "id": "5913355005137522807"},
    "502": {"emoji": "🇬🇹", "id": "5913324858762072330"},
    "503": {"emoji": "🇸🇻", "id": "5913238624408703010"},
    "504": {"emoji": "🇭🇳", "id": "5911406889576436289"},
    "505": {"emoji": "🇳🇮", "id": "5334807849418003620"},
    "506": {"emoji": "🇨🇷", "id": "5911261745451635030"},
    "507": {"emoji": "🇵🇦", "id": "5913428968769327174"},
    "509": {"emoji": "🇭🇹", "id": "5913459789454643194"},
    "591": {"emoji": "🇧🇴", "id": "5913638795101606133"},
    "592": {"emoji": "🇬🇾", "id": "5913579412883771480"},
    "593": {"emoji": "🇪🇨", "id": "5911273865849347408"},
    "595": {"emoji": "🇵🇾", "id": "5911014265141072316"},
    "597": {"emoji": "🇸🇷", "id": "5913275539652611719"},
    "598": {"emoji": "🇺🇾", "id": "5913623088406204470"},
    "670": {"emoji": "🇹🇱", "id": "5911141915864076479"},
    "673": {"emoji": "🇧🇳", "id": "5911336409163109113"},
    "674": {"emoji": "🇳🇷", "id": "5434131139889478358"},
    "675": {"emoji": "🇵🇬", "id": "5911107251183030903"},
    "676": {"emoji": "🇹🇴", "id": "5433640100573491806"},
    "677": {"emoji": "🇸🇧", "id": "5911482712929080608"},
    "678": {"emoji": "🇻🇺", "id": "5913511535220625585"},
    "679": {"emoji": "🇫🇯", "id": "5911393832875856716"},
    "680": {"emoji": "🇵🇼", "id": "5911283903187915549"},
    "681": {"emoji": "🇼🇫", "id": "5780471598922337683"},
    "682": {"emoji": "🇨🇰", "id": "5780471598922337683"},
    "683": {"emoji": "🇳🇺", "id": "5780471598922337683"},
    "685": {"emoji": "🇼🇸", "id": "5913325971158602854"},
    "686": {"emoji": "🇰🇮", "id": "5911294443037660118"},
    "687": {"emoji": "🇳🇨", "id": "5780471598922337683"},
    "688": {"emoji": "🇹🇻", "id": "5433684690923961019"},
    "689": {"emoji": "🇵🇫", "id": "5780471598922337683"},
    "690": {"emoji": "🇹🇰", "id": "5780471598922337683"},
    "691": {"emoji": "🇫🇲", "id": "5911271104185373336"},
    "692": {"emoji": "🇲🇭", "id": "5913235935759175692"},
    "850": {"emoji": "🇰🇵", "id": "5434142701941437163"},
    "852": {"emoji": "🇭🇰", "id": "5292166459118606932"},
    "853": {"emoji": "🇲🇴", "id": "6323557758096377611"},
    "855": {"emoji": "🇰🇭", "id": "5913699998385573485"},
    "856": {"emoji": "🇱🇦", "id": "5913718526874489279"},
    "886": {"emoji": "🇹🇼", "id": "5366187256937726720"},
    "960": {"emoji": "🇲🇻", "id": "5913501399097806832"},
    "961": {"emoji": "🇱🇧", "id": "5911504273664905447"},
    "962": {"emoji": "🇯🇴", "id": "5913234136167878475"},
    "963": {"emoji": "🇸🇾", "id": "5433910876786670092"},
    "964": {"emoji": "🇮🇶", "id": "5911382442622587735"},
    "965": {"emoji": "🇰🇼", "id": "5913290705182134003"},
    "966": {"emoji": "🇸🇦", "id": "4985897134424328239"},
    "967": {"emoji": "🇾🇪", "id": "5913346492512341993"},
    "968": {"emoji": "🇴🇲", "id": "5913570801474343473"},
    "970": {"emoji": "🇵🇸", "id": "5913684768431541668"},
    "971": {"emoji": "🇦🇪", "id": "5913726554168365343"},
    "972": {"emoji": "🇮🇱", "id": "5911471936856134692"},
    "973": {"emoji": "🇧🇭", "id": "5913581663446634403"},
    "974": {"emoji": "🇶🇦", "id": "5911260864983339619"},
    "975": {"emoji": "🇧🇹", "id": "5913236734623093021"},
    "976": {"emoji": "🇲🇳", "id": "5911041383564580038"},
    "977": {"emoji": "🇳🇵", "id": "5913496520014958723"},
    "992": {"emoji": "🇹🇯", "id": "5911287639809463107"},
    "993": {"emoji": "🇹🇲", "id": "5913315521503170180"},
    "994": {"emoji": "🇦🇿", "id": "5911197578640233518"},
    "995": {"emoji": "🇬🇪", "id": "5913434771270144023"},
    "996": {"emoji": "🇰🇬", "id": "5911202161370337549"},
    "998": {"emoji": "🇺🇿", "id": "5911051846104912282"}
}

APP_EMOJIS = {
    "facebook": {"emoji": "📘", "id": "5334807341109908955"},
    "whatsapp": {"emoji": "💬", "id": "5334759662677957452"},
    "telegram": {"emoji": "✈️", "id": "5337010556253543833"},
    "whatsapp_business": {"emoji": "💼", "id": "5336814486701514414"},
    "imo": {"emoji": "💭", "id": "5337155807752524558"},
    "instagram": {"emoji": "📸", "id": "5334868205091459431"},
    "apple": {"emoji": "🍎", "id": "5334637951894722661"},
    "google": {"emoji": "🔍", "id": "5335010201005231986"},
    "microsoft": {"emoji": "🪟", "id": "5334880948259427772"},
    "teams": {"emoji": "🧑‍🤝‍🧑", "id": "5334590977837403844"},
    "tiktok": {"emoji": "🎵", "id": "5339213256001102461"},
    "bkash": {"emoji": "🏦", "id": "5348469219761626211"},
    "rocket": {"emoji": "🚀", "id": "5346042941196507141"},
    "bybit": {"emoji": "📈", "id": "5348372939479751825"},
    "binance": {"emoji": "💱", "id": "5348212415077064131"},
    "melbet": {"emoji": "🌟", "id": "5337102391244263212"},
    "snapchat": {"emoji": "👻", "id": "5359441366554255082"},
    "uber": {"emoji": "🚗", "id": "5298715455316303708"},
    "paypal": {"emoji": "💵", "id": "5776103539872896061"},
    "discord": {"emoji": "🎬", "id": "5116246243646898866"},
    "amazon": {"emoji": "🌟", "id": "4995019580536524226"},
    "viber": {"emoji": "💜", "id": "5463060437572528782"},
    "linkedin": {"emoji": "💼", "id": "6224222994265279792"},
    "line": {"emoji": "🔒", "id": "5399818044866327279"},
    "wechat": {"emoji": "🌟", "id": "5782757599560602950"},
    "twitter": {"emoji": "🐦", "id": "5215726959056662534"},
    "reddit": {"emoji": "👽", "id": "4992421103847604984"},
    "pinterest": {"emoji": "📌", "id": "5346103513120258857"},
    "twitch": {"emoji": "🎮", "id": "5233333563306301418"},
    "zoom": {"emoji": "📹", "id": "5881799193219043268"},
    "signal": {"emoji": "💬", "id": "5293998404404272267"},
    "slack": {"emoji": "💻", "id": "4994972469040251302"},
    "skype": {"emoji": "☎️", "id": "4992613535562334989"},
    "netflix": {"emoji": "🎥", "id": "6255738712664050133"},
    "spotify": {"emoji": "🎵", "id": "5411392711146095115"},
    "amazon_prime": {"emoji": "📺", "id": "6111801057061374810"},
    "hoichoi": {"emoji": "🍿", "id": "6104822598493801746"},
    "daraz": {"emoji": "📦", "id": "5336879280578138635"},
    "foodpanda": {"emoji": "🐼", "id": "5336879280578138635"},
    "pathao": {"emoji": "🛵", "id": "5336879280578138635"},
    "aliexpress": {"emoji": "🛒", "id": "5336879280578138635"},
    "shopee": {"emoji": "🛍️", "id": "5336879280578138635"},
    "payoneer": {"emoji": "💳", "id": "5336879280578138635"},
    "wise": {"emoji": "🦉", "id": "5336879280578138635"},
    "chatgpt": {"emoji": "🤖", "id": "5296516998996445955"},
    "notion": {"emoji": "📓", "id": "5336879280578138635"},
    "github": {"emoji": "🐙", "id": "5417836094098007862"},
    "canva": {"emoji": "🖌️", "id": "5111661409008092227"},
    "figma": {"emoji": "🎨", "id": "5336879280578138635"},
    "upwork": {"emoji": "💼", "id": "5336879280578138635"},
    "fiverr": {"emoji": "🟢", "id": "5336879280578138635"},
    "yahoo": {"emoji": "🌐", "id": "5336879280578138635"},
    "dropbox": {"emoji": "☁️", "id": "5336879280578138635"},
    "coursera": {"emoji": "📚", "id": "5336879280578138635"},
    "duolingo": {"emoji": "🗣️", "id": "5336879280578138635"}
}

# ================= 🔍 DETECT SERVICE & COUNTRY =================

def detect_service(msg):
    msg = msg.lower()
    for name, data in APP_EMOJIS.items():
        if name in msg:
            return name.title(), data["emoji"], data["id"]
    return "OTP Service", "📱", None

def get_country_from_number(number):
    for code, data in FLAG_EMOJIS.items():
        if number.startswith(code):
            return data["emoji"], data["id"]
    return "🌍", None

# ================= 🧾 EXTRACT OTP =================

def extract_otp(msg):
    match = re.search(r'\b\d{4,8}\b', msg)
    if match:
        return match.group()
    return "******"

# ================= 📩 FORMAT OTP MESSAGE =================

def format_otp_message(number, service_name, service_emoji, service_id, otp_code):
    masked = number[:3] + "xxxx" + number[-4:] if len(number) > 7 else number
    flag_emoji, flag_id = get_country_from_number(number)
    
    service_tag = f'<tg-emoji emoji-id="{service_id}">{service_emoji}</tg-emoji>' if service_id else service_emoji
    flag_tag = f'<tg-emoji emoji-id="{flag_id}">{flag_emoji}</tg-emoji>' if flag_id else flag_emoji
    
    return f"""✅ <b>Message OTP Received</b> ✅

{service_tag} <b>Service:</b> {service_name}
📱 <b>Number:</b> <code>{masked}</code>
🌍 <b>Country:</b> {flag_tag}

🔐 <b>OTP Code:</b> <code>{otp_code}</code>

━━━━━━━━━━━━━━━━━━━━
⚠️ <i>Please don't share this code with anyone!</i>
🛡 <b>Secure • Fast • Reliable</b>"""

# ================= 🧵 CACHE =================

last_otps = set()
subscribed_users = set()

# ================= 📡 API CALLS =================

def fetch_otps():
    try:
        res = requests.get(f"{API_BASE}/success-otp", timeout=5)
        data = res.json()
        if data.get("meta", {}).get("code") == 208:
            return data.get("data", {}).get("otps", [])
    except:
        pass
    return []

# ================= 🤖 USER BOT =================

@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📡 Live OTP", "🔔 Subscribe")
    kb.row("🔕 Unsubscribe", "ℹ️ Help")
    bot.send_message(m.chat.id, f"""⭐ <b>OTP Live Monitor</b> ⭐

👋 Welcome to OTP Live Monitor Bot!

🔹 Get real-time OTP notifications
🔹 Support for all services
🔹 Premium emoji design

📍 <b>Select an option below</b>

🛡 <b>Secure • Fast • Reliable</b>""", reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📡 Live OTP")
def live_otp(m):
    otps = fetch_otps()
    if not otps:
        bot.send_message(m.chat.id, f"❌ No OTPs found!")
        return
    for otp in otps[:3]:
        num = otp.get("number", "N/A")
        msg_text = otp.get("message", "")
        service_name, service_emoji, service_id = detect_service(msg_text)
        otp_code = extract_otp(msg_text)
        formatted = format_otp_message(num, service_name, service_emoji, service_id, otp_code)
        
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton(f"📋 Copy {otp_code}", copy_text={"text": otp_code}, callback_data="copy_otp"))
        kb.add(types.InlineKeyboardButton("📱 Get Number", url="https://t.me/MX_Number1_Bot"))
        kb.add(types.InlineKeyboardButton("🆘 Support", url="https://t.me/max_supportar"))
        
        bot.send_message(m.chat.id, formatted, reply_markup=kb, parse_mode="HTML")
        time.sleep(0.5)

@bot.message_handler(func=lambda m: m.text == "🔔 Subscribe")
def subscribe(m):
    subscribed_users.add(m.chat.id)
    bot.send_message(m.chat.id, f"✅ You are now subscribed to live OTP updates!")

@bot.message_handler(func=lambda m: m.text == "🔕 Unsubscribe")
def unsubscribe(m):
    subscribed_users.discard(m.chat.id)
    bot.send_message(m.chat.id, f"❌ You have unsubscribed.")

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_cmd(m):
    bot.send_message(m.chat.id, f"""💬 <b>Help</b>

🔹 <b>Live OTP</b> – দেখুন আপনার লেটেস্ট OTP
🔹 <b>Subscribe</b> – নতুন OTP এলে নোটিফিকেশন পাবেন
🔹 <b>Unsubscribe</b> – নোটিফিকেশন বন্ধ করুন

🛡 <b>Secure • Fast • Reliable</b>""", parse_mode="HTML")

# ================= 👑 ADMIN =================

@bot.message_handler(commands=['admin'])
def admin(m):
    if m.from_user.id != OWNER_ID:
        bot.send_message(m.chat.id, f"❌ Unauthorized!")
        return
    bot.send_message(m.chat.id, f"👑 <b>Admin Panel</b>\n\n👥 Subscribers: {len(subscribed_users)}", parse_mode="HTML")

# ================= 🔄 OTP MONITOR THREAD =================

def otp_monitor():
    while True:
        try:
            otps = fetch_otps()
            for otp in otps:
                otp_id = otp.get("otp_id", "")
                if otp_id in last_otps:
                    continue
                last_otps.add(otp_id)
                if len(last_otps) > 300:
                    last_otps.clear()

                num = otp.get("number", "N/A")
                msg_text = otp.get("message", "")
                service_name, service_emoji, service_id = detect_service(msg_text)
                otp_code = extract_otp(msg_text)
                formatted = format_otp_message(num, service_name, service_emoji, service_id, otp_code)

                kb = types.InlineKeyboardMarkup(row_width=2)
                kb.add(types.InlineKeyboardButton(f"📋 Copy {otp_code}", copy_text={"text": otp_code}))
                kb.add(types.InlineKeyboardButton("📱 Get Number", url="https://t.me/MX_Number1_Bot"))
                kb.add(types.InlineKeyboardButton("🆘 Support", url="https://t.me/max_supportar"))

                for uid in list(subscribed_users):
                    try:
                        bot.send_message(uid, formatted, reply_markup=kb, parse_mode="HTML")
                    except:
                        pass
        except:
            pass
        time.sleep(3)

# ================= 🚀 START =================

if __name__ == "__main__":
    print("🚀 OTP Live Monitor Bot Started...")
    threading.Thread(target=otp_monitor, daemon=True).start()
    bot.infinity_polling()
