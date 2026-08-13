import threading
import requests
import json
import uuid

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

SERVER_LOGIN_URL = "https://smsm3030.pythonanywhere.com/api/login"

PRODUCTS_MAPPING = [
    {"id": "Fakka_2.5_Unite", "display": "فكة 2.5 ج | 45 وحدة | يوم"},
    {"id": "Fakka_3_Unite", "display": "فكة 3 ج | 125 وحدة | يوم"},
    {"id": "Fakka_4.25_Unite", "display": "فكة 4.25 ج | 190 وحدة | يوم"},
    {"id": "Fakka_5_Unite", "display": "فكة 5 ج | 225 وحدة | يوم"},
    {"id": "Fakka_7_Unite", "display": "فكة 7 ج | 300 وحدة | 3 أيام"},
    {"id": "Fakka_9_Unite", "display": "فكة 9 ج | 400 وحدة | 4 أيام"},
    {"id": "Fakka_10_Unite", "display": "فكة 10 ج | 450 وحدة | 7 أيام"},
    {"id": "Fakka_10.5_Unite", "display": "فكة 10.5 ج | 400 وحدة + 50MB"},
    {"id": "Fakka_12_Unite", "display": "فكة 12 ج | 425 وحدة | 7 أيام"},
    {"id": "Fakka_13.5_Unite", "display": "فكة 13.5 ج | 625 وحدة | 7 أيام"},
    {"id": "Fakka_15_Unite", "display": "فكة 15 ج | 550 وحدة | 7 أيام"},
    {"id": "Fakka_15.5_Unite", "display": "فكة 15.5 ج | 625 وحدة | 7 أيام"},
    {"id": "Fakka_17.5_Unite", "display": "فكة 17.5 ج | 650 وحدة | 10 أيام"},
    {"id": "Fakka_20_Unite", "display": "فكة 20 ج | 750 وحدة | 10 أيام"},
    {"id": "Fakka_26_Unite", "display": "فكة 26 ج | 750 وحدة | 10 أيام"},
    {"id": "Mared_10_Minuts", "display": "مارد 10 دقائق | دقائق"},
    {"id": "Mared_10_Flexs", "display": "مارد 10 فليكس | فليكس"},
    {"id": "Mared_10_Social", "display": "مارد 10 سوشيال | سوشيال"}
]

def make_bg(widget, color, radius=[12,]):
    with widget.canvas.before:
        Color(*color)
        widget.rect = RoundedRectangle(size=widget.size, pos=widget.pos, radius=radius)
    widget.bind(size=lambda w, val: setattr(w.rect, 'size', val),
                pos=lambda w, val: setattr(w.rect, 'pos', val))

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=[30, 50], spacing=20)
        make_bg(main_layout, [0.05, 0.07, 0.09, 1])

        title = Label(text="📱 تطبيق شحن كروت فكة", font_size='24sp', bold=True, size_hint_y=None, height=60, color=[0.9, 0.2, 0.2, 1])
        subtitle = Label(text="سجل دخولك لتفعيل خدمة الشحن المباشر", font_size='14sp', size_hint_y=None, height=30, color=[0.7, 0.7, 0.7, 1])
        main_layout.add_widget(title)
        main_layout.add_widget(subtitle)

        card = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None, height=220)
        make_bg(card, [0.09, 0.11, 0.13, 1], radius=[15,])

        self.user_input = TextInput(hint_text="اسم المستخدم", multiline=False, size_hint_y=None, height=45)
        self.pass_input = TextInput(hint_text="كلمة المرور", password=True, multiline=False, size_hint_y=None, height=45)

        card.add_widget(self.user_input)
        card.add_widget(self.pass_input)
        main_layout.add_widget(card)

        self.btn_login = Button(text="🚀 تسجيل الدخول", font_size='18sp', bold=True, size_hint_y=None, height=50, background_normal='', background_color=[0, 0, 0, 0])
        make_bg(self.btn_login, [0.14, 0.52, 0.21, 1], radius=[10,])
        self.btn_login.bind(on_press=self.do_login)
        main_layout.add_widget(self.btn_login)

        self.status_label = Label(text="", font_size='14sp', size_hint_y=None, height=40, color=[1, 0.3, 0.3, 1])
        main_layout.add_widget(self.status_label)

        self.add_widget(main_layout)

    def do_login(self, instance):
        username = self.user_input.text.strip()
        password = self.pass_input.text.strip()
        if not username or not password:
            self.status_label.text = "⚠️ يرجى كتابة اسم المستخدم وكلمة المرور"
            return

        self.status_label.text = "🔄 جاري التحقق من السيرفر..."

        def check_thread():
            try:
                resp = requests.post(SERVER_LOGIN_URL, json={"username": username, "password": password}, timeout=8)
                data = resp.json()
                if resp.status_code == 200 and data.get("success"):
                    Clock.schedule_once(lambda dt: self.on_success(data.get("expire_date")))
                else:
                    msg = data.get("message", "❌ فشل تسجيل الدخول")
                    Clock.schedule_once(lambda dt: self.on_error(msg))
            except Exception:
                Clock.schedule_once(lambda dt: self.on_error("❌ تعذر الاتصال بالسيرفر"))

        threading.Thread(target=check_thread).start()

    def on_success(self, expire_date):
        self.status_label.text = "✅ تم تسجيل الدخول!"
        app = App.get_running_app()
        app.charge_screen.set_user_info(self.user_input.text, expire_date)
        app.root.current = 'charge'

    def on_error(self, msg):
        self.status_label.text = msg

class ChargeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_product_id = None
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        make_bg(main_layout, [0.05, 0.07, 0.09, 1])

        self.header_label = Label(text="مرحباً بك", font_size='14sp', size_hint_y=None, height=30, color=[0.2, 0.8, 0.2, 1], bold=True)
        main_layout.add_widget(self.header_label)

        lbl_title = Label(text="🛒 اختر الكارت المراد شحنه:", font_size='16sp', bold=True, size_hint_y=None, height=25, color=[1, 1, 1, 1])
        main_layout.add_widget(lbl_title)

        scroll = ScrollView(size_hint=(1, 1))
        self.grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.card_buttons = []
        for prod in PRODUCTS_MAPPING:
            btn = Button(text=prod['display'], size_hint_y=None, height=45, background_normal='', background_color=[0, 0, 0, 0], color=[0.9, 0.9, 0.9, 1])
            make_bg(btn, [0.09, 0.11, 0.13, 1], radius=[8,])
            btn.bind(on_press=lambda b, p=prod: self.select_product(b, p))
            self.grid.add_widget(btn)
            self.card_buttons.append((btn, prod))

        scroll.add_widget(self.grid)
        main_layout.add_widget(scroll)

        inputs_card = BoxLayout(orientation='vertical', padding=10, spacing=8, size_hint_y=None, height=120)
        make_bg(inputs_card, [0.09, 0.11, 0.13, 1], radius=[10,])

        self.receiver_input = TextInput(hint_text="📱 رقم هاتف المستلم (11 رقم)", multiline=False, size_hint_y=None, height=40)
        self.pin_input = TextInput(hint_text="🔐 الرقم السري لفودافون كاش (6 أرقام)", password=True, multiline=False, size_hint_y=None, height=40)

        inputs_card.add_widget(self.receiver_input)
        inputs_card.add_widget(self.pin_input)
        main_layout.add_widget(inputs_card)

        self.btn_charge = Button(text="⚡ تنفيذ الخصم والشحن الان", font_size='16sp', bold=True, size_hint_y=None, height=50, background_normal='', background_color=[0, 0, 0, 0])
        make_bg(self.btn_charge, [0.9, 0.2, 0.2, 1], radius=[10,])
        self.btn_charge.bind(on_press=self.execute_charge)
        main_layout.add_widget(self.btn_charge)

        self.status_label = Label(text="اختر كارت ثم ادخل البيانات لتنفيذ الشحن", font_size='13sp', size_hint_y=None, height=30, color=[0.8, 0.8, 0.8, 1])
        main_layout.add_widget(self.status_label)

        self.add_widget(main_layout)

    def set_user_info(self, username, expire_date):
        self.header_label.text = f"👤 الحساب: {username}  |  📅 ينتهي: {expire_date[:10]}"

    def select_product(self, btn_obj, prod):
        self.selected_product_id = prod['id']
        for btn, _ in self.card_buttons:
            make_bg(btn, [0.09, 0.11, 0.13, 1], radius=[8,])
            btn.color = [0.9, 0.9, 0.9, 1]
        make_bg(btn_obj, [0.14, 0.52, 0.21, 1], radius=[8,])
        btn_obj.color = [1, 1, 1, 1]
        self.status_label.text = f"✅ اخترت: {prod['display']}"

    def execute_charge(self, instance):
        if not self.selected_product_id:
            self.status_label.text = "⚠️ يرجى اختيار كارت من القائمة أولاً!"
            return

        receiver = self.receiver_input.text.strip()
        pin = self.pin_input.text.strip()

        if len(receiver) != 11 or not receiver.isdigit():
            self.status_label.text = "❌ رقم المستلم يجب أن يتكون من 11 رقم"
            return
        if len(pin) != 6 or not pin.isdigit():
            self.status_label.text = "❌ الرقم السري يجب أن يكون 6 أرقام"
            return

        self.status_label.text = "🔄 جاري الاتصال وتأكيد الطلب..."

        def charge_thread():
            try:
                url1 = "http://mobile.vodafone.com.eg/checkSeamless/realms/vf-realm/protocol/openid-connect/auth"
                h1 = {'User-Agent': "okhttp/4.12.0", 'clientId': "AnaVodafoneAndroid"}
                r1 = requests.get(url1, params={'client_id': "cash-app"}, headers=h1, timeout=10)
                data1 = r1.json()
                seamless_token = data1.get("seamlessToken")
                raw_msisdn = data1.get("msisdn")
                msisdn_sender = ('0' + raw_msisdn) if (raw_msisdn and raw_msisdn.startswith('1')) else raw_msisdn

                url2 = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
                p2 = {'grant_type': "password", 'client_secret': "b86e30a8-ae29-467a-a71f-65c73f2ff5e3", 'client_id': "cash-app"}
                h2 = {'User-Agent': "okhttp/4.12.0", 'seamlessToken': seamless_token, 'clientId': "AnaVodafoneAndroid"}
                r2 = requests.post(url2, data=p2, headers=h2, timeout=10)
                access_token = r2.json().get("access_token")

                url3 = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"
                payload3 = {
                    "channel": {"name": "MobileApp"},
                    "orderItem": [{
                        "action": "insert",
                        "id": self.selected_product_id,
                        "product": {
                            "characteristic": [
                                {"name": "PaymentMethod", "value": "VFCash"},
                                {"name": "USE_EMONEY", "value": "False"},
                                {"name": "MerchantCode", "value": "81841829"}
                            ],
                            "id": self.selected_product_id,
                            "relatedParty": [
                                {"id": msisdn_sender, "name": "MSISDN", "role": "Subscriber"},
                                {"id": receiver, "name": "Receiver", "role": "Receiver"}
                            ]
                        },
                        "@type": self.selected_product_id,
                        "eCode": 0
                    }],
                    "relatedParty": [{"id": pin, "name": "pin", "role": "Requestor"}],
                    "@type": "CashFakkaAndMared"
                }

                h3 = {
                    'User-Agent': "okhttp/4.12.0", 'Accept': "application/json",
                    'X-Request-ID': str(uuid.uuid4()), 'msisdn': msisdn_sender,
                    'Authorization': f"Bearer {access_token}", 'clientId': "AnaVodafoneAndroid",
                    'Content-Type': "application/json; charset=UTF-8"
                }

                r3 = requests.post(url3, data=json.dumps(payload3), headers=h3, timeout=15)
                if r3.status_code in [200, 201]:
                    Clock.schedule_once(lambda dt: self.on_order_success(msisdn_sender, receiver))
                else:
                    Clock.schedule_once(lambda dt: self.on_order_failed("فشلت العملية، تحقق من الرصيد والبيانات"))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.on_order_failed(str(e)))

        threading.Thread(target=charge_thread).start()

    def on_order_success(self, sender, receiver):
        self.status_label.text = f"🎉 تم الشحن بنجاح إلى ({receiver})!"

    def on_order_failed(self, err_msg):
        self.status_label.text = f"❌ {err_msg}"

class VodafoneFakkaApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        self.login_screen = LoginScreen(name='login')
        self.charge_screen = ChargeScreen(name='charge')
        sm.add_widget(self.login_screen)
        sm.add_widget(self.charge_screen)
        return sm

if __name__ == '__main__':
    VodafoneFakkaApp().run()
