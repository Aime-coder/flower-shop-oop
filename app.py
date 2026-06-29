# AI Flower Shop - OOP Project
# Author  : Ndacyayisenga Parfait
# Course  : Object-Oriented Programming
# School  : University of Lodz

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# BASE CLASS
class Flower:
    """Base class representing a flower. Demonstrates encapsulation and inheritance."""

    kingdom = "Plantae"  # class variable shared by all flowers

    def __init__(self, name, color, petals, price, emoji, description):
        self.name         = name
        self.color        = color
        self.petals       = petals
        self.__price      = price   # private attribute - encapsulation
        self.emoji        = emoji
        self.description  = description
        self._is_blooming = True

    def get_price(self):
        return self.__price

    def set_price(self, new_price):
        if new_price >= 0:
            self.__price = new_price

    def special_feature(self):
        """Base version - overridden by each child class (polymorphism)."""
        return f"{self.name} is a beautiful flower."

    def to_dict(self):
        return {
            "name"        : self.name,
            "color"       : self.color,
            "petals"      : self.petals,
            "price"       : self.__price,
            "emoji"       : self.emoji,
            "description" : self.description,
            "feature"     : self.special_feature(),
        }

    def __str__(self):
        return f"{self.emoji} {self.name} ({self.color}) — ${self.__price:.2f}"

    def __repr__(self):
        return f"Flower(name={self.name}, color={self.color}, price={self.__price})"

    def __eq__(self, other):
        return isinstance(other, Flower) and self.name == other.name and self.color == other.color

    def __lt__(self, other):
        return self.__price < other.get_price()


# CHILD CLASSES - each overrides special_feature() with genuinely different behavior

class Rose(Flower):
    """
    Rose class - inherits from Flower.
    special_feature() calculates a discount based on quantity ordered.
    This is real polymorphism: different logic, not just a different string.
    """
    def __init__(self, color, price, has_thorns=True):
        super().__init__(
            name        = "Rose",
            color       = color,
            petals      = 32,
            price       = price,
            emoji       = "🌹",
            description = f"A classic {color.lower()} rose, symbol of love and passion."
        )
        self.has_thorns = has_thorns

    def special_feature(self, quantity=1):
        """
        Calculates a bulk discount based on quantity.
        Buy 6+ roses: 10% off. Buy 12+: 20% off.
        Different logic from Sunflower and Tulip.
        """
        price = self.get_price()
        if quantity >= 12:
            discount = 0.20
        elif quantity >= 6:
            discount = 0.10
        else:
            discount = 0.0

        discounted = price * quantity * (1 - discount)
        thorn_note = "with thorns" if self.has_thorns else "thornless variety"
        if discount > 0:
            return (f"Rose bulk discount: buy {quantity} and get {int(discount*100)}% off! "
                    f"Total: ${discounted:.2f} instead of ${price * quantity:.2f}. "
                    f"This is a {thorn_note}.")
        return (f"No bulk discount yet — buy 6+ roses to save 10%, or 12+ to save 20%. "
                f"This is a {thorn_note}.")


class Sunflower(Flower):
    """
    Sunflower class - inherits from Flower.
    special_feature() calculates how many days until the flower needs watering
    based on its height (taller sunflowers need more water).
    """
    def __init__(self, price, height_cm):
        super().__init__(
            name        = "Sunflower",
            color       = "Yellow",
            petals      = 34,
            price       = price,
            emoji       = "🌻",
            description = f"A bright sunflower standing {height_cm}cm tall, always facing the sun."
        )
        self.height_cm     = height_cm
        self._last_watered = 0  # days since last watered

    def special_feature(self, days_since_watered=0):
        """
        Calculates watering schedule based on height.
        Taller sunflowers (>200cm) need water every 2 days.
        Shorter ones every 3 days.
        Returns a specific care action the user should take.
        """
        if self.height_cm > 200:
            water_every = 2
        else:
            water_every = 3

        days_until_water = max(0, water_every - days_since_watered)

        if days_since_watered >= water_every:
            return (f"⚠️ Water immediately! This {self.height_cm}cm sunflower is overdue. "
                    f"Tall sunflowers need water every {water_every} days.")
        return (f"Next watering in {days_until_water} day(s). "
                f"At {self.height_cm}cm tall, this sunflower needs water every {water_every} days. "
                f"Sunflowers follow the sun — place near a south-facing window.")


class Tulip(Flower):
    """
    Tulip class - inherits from Flower.
    special_feature() generates a personalized care schedule
    based on the season the tulip blooms in.
    """
    def __init__(self, color, price, season="Spring"):
        super().__init__(
            name        = "Tulip",
            color       = color,
            petals      = 6,
            price       = price,
            emoji       = "🌷",
            description = f"A delicate {color.lower()} tulip that blooms in {season}."
        )
        self.season = season

    def special_feature(self, current_month=None):
        """
        Generates a care schedule based on the tulip's bloom season.
        Spring tulips need cold storage now. Summer tulips need sun.
        Completely different logic from Rose and Sunflower.
        """
        import datetime
        if current_month is None:
            current_month = datetime.datetime.now().month

        season_months = {
            "Spring" : [3, 4, 5],
            "Summer" : [6, 7, 8],
            "Autumn" : [9, 10, 11],
            "Winter" : [12, 1, 2],
        }

        bloom_months = season_months.get(self.season, [3, 4, 5])

        if current_month in bloom_months:
            return (f"🌷 Perfect timing! {self.color} Tulips are in their bloom season ({self.season}). "
                    f"Keep them in a bright spot and water every 2 days.")
        else:
            months_away = min((m - current_month) % 12 for m in bloom_months)
            return (f"📅 {self.color} Tulips bloom in {self.season} — about {months_away} month(s) away. "
                    f"Store bulbs in a cool dry place (5–10°C) until then. "
                    f"Originally from Central Asia, they need a cold rest period.")


class Lavender(Flower):
    """
    Lavender class - inherits from Flower.
    special_feature() calculates aromatherapy benefit score
    based on scent level and suggests uses.
    """
    def __init__(self, price, scent_level="Strong"):
        super().__init__(
            name        = "Lavender",
            color       = "Purple",
            petals      = 4,
            price       = price,
            emoji       = "💜",
            description = "Calming purple lavender known for its relaxing fragrance."
        )
        self.scent_level = scent_level

    def special_feature(self, room_size_sqm=20):
        """
        Calculates how many lavender plants are needed for a room
        based on scent level and room size.
        Returns a practical recommendation.
        """
        coverage = {"Strong": 15, "Mild": 8, "Light": 4}
        sqm_per_plant = coverage.get(self.scent_level, 8)
        plants_needed = max(1, round(room_size_sqm / sqm_per_plant))

        uses = {
            "Strong": "sleep aid, anxiety relief, and repelling insects",
            "Mild"  : "light relaxation and room freshening",
            "Light" : "subtle decoration and mild calming effect",
        }
        use_case = uses.get(self.scent_level, "general wellness")

        return (f"{self.scent_level} scent lavender: you need about {plants_needed} plant(s) "
                f"for a {room_size_sqm}sqm room. "
                f"Best used for {use_case}. "
                f"Lavender loves dry, well-drained soil — do not overwater!")


# CART CLASS - demonstrates composition
class Cart:
    """Manages items the customer wants to buy. Uses composition with Flower objects."""

    def __init__(self):
        self.items = []  # list of (Flower, quantity) tuples

    def add(self, flower, quantity=1):
        for i, (f, q) in enumerate(self.items):
            if f.name == flower.name and f.color == flower.color:
                self.items[i] = (f, q + quantity)
                return
        self.items.append((flower, quantity))

    def remove(self, flower_name):
        self.items = [(f, q) for f, q in self.items if f.name != flower_name]

    def total(self):
        return sum(f.get_price() * q for f, q in self.items)

    def total_items(self):
        return sum(q for _, q in self.items)

    def clear(self):
        self.items = []

    def __len__(self):
        return len(self.items)


# FLOWERSHOP CLASS - demonstrates class methods, static methods, composition
class FlowerShop:
    """Manages the full flower catalog. Demonstrates static and class methods."""

    def __init__(self, name, owner):
        self.name    = name
        self.owner   = owner
        self.catalog = []

    def add_to_catalog(self, flower):
        self.catalog.append(flower)

    def get_by_name(self, name):
        return [f for f in self.catalog if f.name == name]

    def get_cheapest(self):
        return min(self.catalog, key=lambda f: f.get_price())

    def get_most_expensive(self):
        return max(self.catalog, key=lambda f: f.get_price())

    @staticmethod
    def care_tip(flower_name):
        """Static method - does not need self or cls."""
        tips = {
            "Rose"      : "Water roses every 2 days and give them full sunlight.",
            "Sunflower" : "Sunflowers need 6-8 hours of direct sun daily.",
            "Tulip"     : "Tulip bulbs need a cold period before blooming.",
            "Lavender"  : "Lavender loves dry, well-drained soil — do not overwater!",
        }
        return tips.get(flower_name, "Keep your flower watered and in good light.")

    @classmethod
    def create_default_shop(cls):
        """Class method - creates a shop instance without needing an existing one."""
        shop = cls("Parfait's Flower Shop", "Ndacyayisenga Parfait")
        shop.add_to_catalog(Rose("Red",    5.99, has_thorns=True))
        shop.add_to_catalog(Rose("White",  4.99, has_thorns=False))
        shop.add_to_catalog(Rose("Pink",   5.49, has_thorns=True))
        shop.add_to_catalog(Sunflower(3.50, height_cm=180))
        shop.add_to_catalog(Sunflower(4.25, height_cm=220))
        shop.add_to_catalog(Tulip("Purple", 2.99, "Spring"))
        shop.add_to_catalog(Tulip("Yellow", 3.25, "Summer"))
        shop.add_to_catalog(Tulip("Orange", 3.10, "Autumn"))
        shop.add_to_catalog(Lavender(4.50, "Strong"))
        shop.add_to_catalog(Lavender(3.75, "Mild"))
        return shop


# AI ASSISTANT (secondary feature - OOP is the main focus)
def get_ai_client():
    return OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key  = os.getenv("OPENROUTER_API_KEY")
    )

def ask_flower_ai(question, chat_history):
    client = get_ai_client()
    system = """You are Flora, an expert AI flower assistant for Parfait's Flower Shop.
Help customers choose flowers, explain care tips, and suggest bouquets.
Be warm and friendly. Keep answers to 2-4 sentences. Use flower emojis occasionally."""
    messages = [{"role": "system", "content": system}]
    messages += chat_history
    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model      = "openrouter/free",
        messages   = messages,
        max_tokens = 300
    )
    return response.choices[0].message.content

def get_ai_bouquet(occasion, budget):
    client = get_ai_client()
    prompt = (f"Suggest a flower bouquet for '{occasion}' with a budget of ${budget:.2f}. "
              f"Available: Red Rose ($5.99), White Rose ($4.99), Pink Rose ($5.49), "
              f"Sunflower ($3.50-$4.25), Purple/Yellow/Orange Tulip ($2.99-$3.25), "
              f"Lavender ($3.75-$4.50). Give a specific combination with quantities. Be concise.")
    response = client.chat.completions.create(
        model    = "openrouter/free",
        messages = [{"role": "user", "content": prompt}],
        max_tokens = 250
    )
    return response.choices[0].message.content


# STREAMLIT UI

st.set_page_config(
    page_title = "Parfait's Flower Shop",
    page_icon  = "🌸",
    layout     = "wide"
)

# session state - keeps cart and chat alive across interactions
if "shop"         not in st.session_state:
    st.session_state.shop = FlowerShop.create_default_shop()
if "cart"         not in st.session_state:
    st.session_state.cart = Cart()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

shop = st.session_state.shop
cart = st.session_state.cart

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #ff9a9e, #fecfef, #ffecd2);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .flower-card {
        background: white;
        border: 2px solid #ffd6e7;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(255,150,180,0.15);
    }
    .oop-badge {
        background: #e8f4f8;
        border-left: 4px solid #4a90d9;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.85em;
        margin: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🌸 Parfait's Flower Shop 🌸</h1>
    <p style="color:#666; font-size:1.1em;">
        Python OOP Project &nbsp;|&nbsp; University of Lodz &nbsp;|&nbsp; Ndacyayisenga Parfait 🇷🇼
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🌺 Flower Shop",
    "🛒 My Cart",
    "🤖 AI Assistant",
    "📚 OOP Concepts"
])

# TAB 1 - SHOP
with tab1:
    st.subheader(f"🏪 {shop.name}  |  Owner: {shop.owner}")
    st.caption(f"We have {len(shop.catalog)} flowers available today!")

    col_left, col_right = st.columns([3, 1])

    with col_right:
        st.markdown("### 🔍 Filter")
        flower_types  = ["All"] + sorted(set(f.name for f in shop.catalog))
        selected_type = st.selectbox("Flower type", flower_types)
        max_price     = max(f.get_price() for f in shop.catalog)
        price_range   = st.slider("Max price ($)", 0.0, max_price + 1, max_price + 1)

        st.markdown("---")
        st.markdown("### 📊 Shop Stats")
        st.metric("Total flowers",    len(shop.catalog))
        st.metric("Cheapest",         f"${shop.get_cheapest().get_price():.2f}")
        st.metric("Most expensive",   f"${shop.get_most_expensive().get_price():.2f}")

    with col_left:
        filtered = [
            f for f in shop.catalog
            if (selected_type == "All" or f.name == selected_type)
            and f.get_price() <= price_range
        ]

        if not filtered:
            st.info("No flowers match your filter.")
        else:
            groups = {}
            for f in filtered:
                groups.setdefault(f.name, []).append(f)

            for flower_name, flowers in groups.items():
                st.markdown(f"### {flowers[0].emoji} {flower_name}s")
                cols = st.columns(min(len(flowers), 3))

                for i, flower in enumerate(flowers):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="flower-card">
                            <h3 style="margin:0">{flower.emoji} {flower.color} {flower.name}</h3>
                            <p style="color:#888;font-size:0.85em">{flower.description}</p>
                            <p>🌿 {flower.petals} petals &nbsp;|&nbsp; 🌍 {flower.kingdom}</p>
                            <h4 style="color:#e75480">${flower.get_price():.2f}</h4>
                        </div>
                        """, unsafe_allow_html=True)

                        qty = st.number_input(
                            "Qty", min_value=1, max_value=20, value=1,
                            key=f"qty_{flower.name}_{flower.color}_{flower.get_price()}"
                        )
                        if st.button("🛒 Add to Cart",
                                     key=f"add_{flower.name}_{flower.color}_{flower.get_price()}"):
                            cart.add(flower, qty)
                            st.success(f"Added {qty}× {flower.emoji} {flower.color} {flower.name}!")

                        with st.expander("💡 Care tip"):
                            st.write(FlowerShop.care_tip(flower.name))

                        with st.expander("✨ Special feature (polymorphism demo)"):
                            # each flower class runs different logic here - that is polymorphism
                            if isinstance(flower, Rose):
                                st.write(flower.special_feature(quantity=qty))
                            elif isinstance(flower, Sunflower):
                                days = st.slider("Days since watered", 0, 5, 1,
                                                 key=f"days_{flower.name}_{flower.get_price()}")
                                st.write(flower.special_feature(days_since_watered=days))
                            elif isinstance(flower, Tulip):
                                st.write(flower.special_feature())
                            elif isinstance(flower, Lavender):
                                room = st.slider("Room size (sqm)", 5, 50, 20,
                                                 key=f"room_{flower.name}_{flower.get_price()}")
                                st.write(flower.special_feature(room_size_sqm=room))

# TAB 2 - CART
with tab2:
    st.subheader("🛒 Your Shopping Cart")

    if len(cart) == 0:
        st.info("Your cart is empty — go to the Shop tab to add flowers! 🌸")
    else:
        for flower, qty in cart.items:
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1: st.write(f"{flower.emoji} **{flower.color} {flower.name}**")
            with c2: st.write(f"${flower.get_price():.2f} each")
            with c3: st.write(f"× {qty}")
            with c4: st.write(f"**${flower.get_price() * qty:.2f}**")

            if st.button(f"❌ Remove", key=f"remove_{flower.name}_{flower.color}"):
                cart.remove(flower.name)
                st.rerun()

        st.markdown("---")
        st.markdown(f"### 💰 Total: **${cart.total():.2f}**")
        st.caption(f"{cart.total_items()} items in cart")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Cart"):
                cart.clear()
                st.rerun()
        with col2:
            if st.button("✅ Checkout (Demo)"):
                st.balloons()
                st.success("Thank you for your order! Your flowers will bloom soon!")
                cart.clear()

# TAB 3 - AI ASSISTANT
with tab3:
    st.subheader("🤖 Flora — AI Flower Assistant")
    st.caption("Ask me anything about flowers or let me suggest a bouquet!")

    with st.expander("🎁 AI Bouquet Suggester", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            occasion = st.selectbox("Occasion?", [
                "Birthday 🎂", "Wedding 💍", "Anniversary ❤️",
                "Valentine's Day 💕", "Graduation 🎓", "Get Well Soon 🏥",
                "Mother's Day 🌷", "Just Because 😊"
            ])
        with col2:
            budget = st.slider("Budget ($)", 5.0, 100.0, 25.0, step=5.0)

        if st.button("🌸 Suggest a Bouquet"):
            with st.spinner("Flora is thinking..."):
                st.write(get_ai_bouquet(occasion, budget))

    st.markdown("---")
    st.markdown("### 💬 Chat with Flora")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask Flora anything about flowers...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Flora is thinking..."):
                reply = ask_flower_ai(user_input, st.session_state.chat_history[:-1])
                st.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# TAB 4 - OOP CONCEPTS
with tab4:
    st.subheader("📚 OOP Concepts Used in This Project")

    concepts = [
        ("🏗️ Classes & Objects",
         "7 classes total: Flower, Rose, Sunflower, Tulip, Lavender, Cart, FlowerShop. "
         "Every flower displayed in the shop is an object created from one of these classes."),

        ("🔒 Encapsulation",
         "__price is a private attribute in Flower. It cannot be accessed directly from outside "
         "the class. You must use get_price() to read it and set_price() to change it."),

        ("👪 Inheritance",
         "Rose, Sunflower, Tulip, and Lavender all inherit from Flower using super().__init__(). "
         "They reuse all parent attributes and only add their own: has_thorns, height_cm, season, scent_level."),

        ("🔄 Polymorphism",
         "special_feature() is defined in the parent Flower class but overridden in every child. "
         "Each child runs completely different logic: "
         "Rose calculates a bulk discount, "
         "Sunflower calculates a watering schedule based on height, "
         "Tulip checks the bloom season against the current month, "
         "Lavender calculates how many plants you need for a room. "
         "Same method name — four different behaviors."),

        ("⚡ super()",
         "Every child class calls super().__init__() to reuse the parent constructor. "
         "This avoids rewriting the same code in every child class (DRY principle)."),

        ("🔮 Magic / Dunder Methods",
         "__str__ controls how a flower prints. __repr__ gives a technical representation. "
         "__eq__ lets you compare two flowers with ==. __lt__ lets you sort flowers by price. "
         "__len__ makes len(cart) work on the Cart class."),

        ("🧩 Composition",
         "Cart contains a list of Flower objects. FlowerShop contains a catalog of Flower objects. "
         "Neither inherits from Flower — they use flowers as components. This is composition."),

        ("📌 Class & Static Methods",
         "FlowerShop.create_default_shop() is a class method — creates a shop without an existing instance. "
         "FlowerShop.care_tip() is a static method — pure logic with no need for self or cls."),
    ]

    for title, explanation in concepts:
        st.markdown(f"""
        <div class="oop-badge">
            <strong>{title}</strong><br>{explanation}
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    st.markdown("---")
    st.markdown("### 🗂️ Class Hierarchy")
    st.code("""
Flower  (Base Class)
│   attributes : name, color, petals, __price (private), emoji, description
│   methods    : get_price(), set_price(), special_feature(), to_dict()
│   dunder     : __str__, __repr__, __eq__, __lt__
│
├── Rose(Flower)        → special_feature() calculates bulk discount
├── Sunflower(Flower)   → special_feature() calculates watering schedule
├── Tulip(Flower)       → special_feature() checks bloom season vs current month
└── Lavender(Flower)    → special_feature() calculates plants needed per room size

Cart                    (Composition — contains Flower objects)
│   __len__() makes len(cart) work naturally

FlowerShop              (Composition — contains Flower catalog)
    @classmethod  create_default_shop()
    @staticmethod care_tip()
    """, language="text")

    st.info("🎓 Project by Ndacyayisenga Parfait — University of Lodz 🇵🇱 | From Rwanda 🇷🇼")