# ============================================================
#  🌸 AI FLOWER SHOP — OOP + AI + Streamlit
#  Author  : Ndacyayisenga Parfait
#  Course  : Object-Oriented Programming
#  School  : University of Lodz
# ============================================================

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
#  OOP CLASSES  (the entire backend)
# ─────────────────────────────────────────────

class Flower:
    """Base class — encapsulation, constructors, methods."""
    kingdom = "Plantae"

    def __init__(self, name, color, petals, price, emoji, description):
        self.name        = name
        self.color       = color
        self.petals      = petals
        self.__price     = price   # private — encapsulation
        self.emoji       = emoji
        self.description = description
        self._is_blooming = True

    def get_price(self):
        return self.__price

    def set_price(self, new_price):
        if new_price >= 0:
            self.__price = new_price

    def special_feature(self):
        return f"{self.name} is a beautiful flower."

    def to_dict(self):
        return {
            "name"       : self.name,
            "color"      : self.color,
            "petals"     : self.petals,
            "price"      : self.__price,
            "emoji"      : self.emoji,
            "description": self.description,
            "feature"    : self.special_feature(),
        }

    def __str__(self):
        return f"{self.emoji} {self.name} ({self.color}) — ${self.__price:.2f}"


class Rose(Flower):
    """Child class — inherits Flower, adds has_thorns."""
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

    def special_feature(self):
        t = "has thorns" if self.has_thorns else "thornless"
        return f"Roses are the symbol of love and romance — this one is {t}."


class Sunflower(Flower):
    """Child class — inherits Flower, adds height."""
    def __init__(self, price, height_cm):
        super().__init__(
            name        = "Sunflower",
            color       = "Yellow",
            petals      = 34,
            price       = price,
            emoji       = "🌻",
            description = f"A bright sunflower standing {height_cm}cm tall, always facing the sun."
        )
        self.height_cm = height_cm

    def special_feature(self):
        return f"Sunflowers follow the sun (heliotropism) and grow up to {self.height_cm}cm tall!"


class Tulip(Flower):
    """Child class — inherits Flower, adds season."""
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

    def special_feature(self):
        return f"Tulips bloom in {self.season} and originally came from Central Asia."


class Lavender(Flower):
    """Child class — inherits Flower, adds scent_level."""
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

    def special_feature(self):
        return f"Lavender has a {self.scent_level.lower()} calming scent used in aromatherapy."


class Cart:
    """
    Cart class — manages items the user wants to buy.
    Demonstrates: composition, list management, aggregation.
    """
    def __init__(self):
        self.items = []   # list of (Flower, quantity) tuples

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


class FlowerShop:
    """
    FlowerShop class — manages the full catalog.
    Demonstrates: class methods, static methods, composition.
    """
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
        tips = {
            "Rose"      : "💧 Water roses every 2 days and give them full sunlight.",
            "Sunflower" : "☀️ Sunflowers need 6–8 hours of direct sun daily.",
            "Tulip"     : "❄️ Tulip bulbs need a cold period before blooming.",
            "Lavender"  : "🪨 Lavender loves dry, well-drained soil — don't overwater!",
        }
        return tips.get(flower_name, "🌱 Keep your flower watered and in good light.")

    @classmethod
    def create_default_shop(cls):
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


# ─────────────────────────────────────────────
#  AI ASSISTANT  (OpenRouter)
# ─────────────────────────────────────────────

def get_ai_client():
    return OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key  = os.getenv("OPENROUTER_API_KEY")
    )

def ask_flower_ai(question, chat_history):
    client = get_ai_client()
    system = """You are Flora, an expert AI flower assistant for Parfait's Flower Shop.
You help customers choose flowers, explain care tips, suggest bouquets for occasions,
and answer any flower-related questions. Be warm, friendly, and knowledgeable.
Keep answers concise (2–4 sentences). Use flower emojis occasionally."""

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
              f"Available flowers: Red Rose ($5.99), White Rose ($4.99), Pink Rose ($5.49), "
              f"Sunflower ($3.50–$4.25), Purple Tulip ($2.99), Yellow Tulip ($3.25), "
              f"Orange Tulip ($3.10), Lavender ($3.75–$4.50). "
              f"Give a specific combination with quantities and explain why. Be concise.")
    client2 = get_ai_client()
    response = client2.chat.completions.create(
        model    = "openrouter/free",
        messages = [{"role": "user", "content": prompt}],
        max_tokens = 250
    )
    return response.choices[0].message.content


# ─────────────────────────────────────────────
#  STREAMLIT UI
# ─────────────────────────────────────────────

st.set_page_config(
    page_title = "🌸 Parfait's Flower Shop",
    page_icon  = "🌸",
    layout     = "wide"
)

# ── Session state ─────────────────────────────
if "shop"         not in st.session_state:
    st.session_state.shop = FlowerShop.create_default_shop()
if "cart"         not in st.session_state:
    st.session_state.cart = Cart()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

shop = st.session_state.shop
cart = st.session_state.cart

# ── Custom CSS ────────────────────────────────
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
    .cart-box {
        background: #fff9fc;
        border: 2px solid #ffb3c6;
        border-radius: 12px;
        padding: 15px;
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

# ── Header ────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌸 Parfait's AI Flower Shop 🌸</h1>
    <p style="color:#666; font-size:1.1em;">
        Built with Python OOP + AI &nbsp;|&nbsp; University of Lodz OOP Project
        &nbsp;|&nbsp; By Ndacyayisenga Parfait 🇷🇼
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🌺 Flower Shop",
    "🛒 My Cart",
    "🤖 AI Flower Assistant",
    "📚 OOP Concepts"
])


# ════════════════════════════════════════════
#  TAB 1 — SHOP
# ════════════════════════════════════════════
with tab1:
    st.subheader(f"🏪 {shop.name}  |  Owner: {shop.owner}")
    st.caption(f"We have {len(shop.catalog)} beautiful flowers for you today!")

    col_left, col_right = st.columns([3, 1])

    with col_right:
        st.markdown("### 🔍 Filter")
        flower_types = ["All"] + sorted(set(f.name for f in shop.catalog))
        selected_type = st.selectbox("Flower type", flower_types)

        max_price = max(f.get_price() for f in shop.catalog)
        price_range = st.slider("Max price ($)", 0.0, max_price + 1, max_price + 1)

        st.markdown("---")
        st.markdown("### 📊 Shop Stats")
        st.metric("Total flowers",    len(shop.catalog))
        st.metric("Cheapest",  f"${shop.get_cheapest().get_price():.2f}")
        st.metric("Most expensive", f"${shop.get_most_expensive().get_price():.2f}")

    with col_left:
        filtered = [
            f for f in shop.catalog
            if (selected_type == "All" or f.name == selected_type)
            and f.get_price() <= price_range
        ]

        if not filtered:
            st.info("No flowers match your filter.")
        else:
            # Group by type for display
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
                            <p style="color:#888; font-size:0.85em">{flower.description}</p>
                            <p>🌿 {flower.petals} petals &nbsp;|&nbsp;
                               🌍 {flower.kingdom}</p>
                            <h4 style="color:#e75480">${flower.get_price():.2f}</h4>
                        </div>
                        """, unsafe_allow_html=True)

                        qty = st.number_input(
                            "Qty", min_value=1, max_value=20, value=1,
                            key=f"qty_{flower.name}_{flower.color}_{flower.get_price()}"
                        )
                        if st.button(f"🛒 Add to Cart",
                                     key=f"add_{flower.name}_{flower.color}_{flower.get_price()}"):
                            cart.add(flower, qty)
                            st.success(f"Added {qty}× {flower.emoji} {flower.color} {flower.name}!")

                        with st.expander("💡 Care tip"):
                            st.write(FlowerShop.care_tip(flower.name))
                        with st.expander("✨ Special feature"):
                            st.write(flower.special_feature())


# ════════════════════════════════════════════
#  TAB 2 — CART
# ════════════════════════════════════════════
with tab2:
    st.subheader("🛒 Your Shopping Cart")

    if len(cart) == 0:
        st.info("Your cart is empty — go to the Shop tab to add flowers! 🌸")
    else:
        st.markdown('<div class="cart-box">', unsafe_allow_html=True)

        for flower, qty in cart.items:
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1:
                st.write(f"{flower.emoji} **{flower.color} {flower.name}**")
            with c2:
                st.write(f"${flower.get_price():.2f} each")
            with c3:
                st.write(f"× {qty}")
            with c4:
                subtotal = flower.get_price() * qty
                st.write(f"**${subtotal:.2f}**")

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
                st.success("🎉 Thank you for your order! Your flowers will bloom soon!")
                cart.clear()

        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════
#  TAB 3 — AI ASSISTANT
# ════════════════════════════════════════════
with tab3:
    st.subheader("🤖 Flora — Your AI Flower Assistant")
    st.caption("Ask me anything about flowers, care tips, or let me suggest a bouquet!")

    # ── Bouquet suggester ─────────────────────
    with st.expander("🎁 AI Bouquet Suggester", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            occasion = st.selectbox("What's the occasion?", [
                "Birthday 🎂", "Wedding 💍", "Anniversary ❤️",
                "Valentine's Day 💕", "Graduation 🎓", "Get Well Soon 🏥",
                "Mother's Day 🌷", "Just Because 😊"
            ])
        with col2:
            budget = st.slider("Budget ($)", 5.0, 100.0, 25.0, step=5.0)

        if st.button("🌸 Suggest a Bouquet with AI"):
            with st.spinner("Flora is thinking..."):
                suggestion = get_ai_bouquet(occasion, budget)
                st.success("🌸 Flora's Bouquet Suggestion:")
                st.write(suggestion)

    st.markdown("---")

    # ── Chat ──────────────────────────────────
    st.markdown("### 💬 Chat with Flora")

    for msg in st.session_state.chat_history:
        role = "🧑 You" if msg["role"] == "user" else "🌸 Flora"
        with st.chat_message(msg["role"]):
            st.write(f"{msg['content']}")

    user_input = st.chat_input("Ask Flora anything about flowers...")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.chat_history.append({
            "role": "user", "content": user_input
        })

        with st.chat_message("assistant"):
            with st.spinner("Flora is thinking..."):
                reply = ask_flower_ai(user_input, st.session_state.chat_history[:-1])
                st.write(reply)

        st.session_state.chat_history.append({
            "role": "assistant", "content": reply
        })

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()


# ════════════════════════════════════════════
#  TAB 4 — OOP CONCEPTS
# ════════════════════════════════════════════
with tab4:
    st.subheader("📚 OOP Concepts Used in This Project")
    st.caption("This is the educational breakdown for the University of Lodz OOP course.")

    concepts = [
        ("🏗️ Classes & Objects",
         "5 classes: `Flower`, `Rose`, `Sunflower`, `Tulip`, `Lavender`, `Cart`, `FlowerShop`. "
         "Every flower displayed is an *object* created from a class."),

        ("🔒 Encapsulation",
         "`__price` is a **private attribute** in `Flower`. "
         "It can only be read via `get_price()` and changed via `set_price()`. "
         "Direct access like `flower.__price` is blocked."),

        ("👪 Inheritance",
         "`Rose`, `Sunflower`, `Tulip`, and `Lavender` all **inherit** from `Flower`. "
         "They get all parent methods for free and only add their own extras like "
         "`has_thorns`, `height_cm`, `season`, `scent_level`."),

        ("🔄 Polymorphism",
         "`special_feature()` is defined in the parent `Flower` but **overridden** in every "
         "child class. Same method name — completely different behavior per class. "
         "You can see this in each flower card's 'Special Feature' section."),

        ("⚡ super()",
         "Every child class calls `super().__init__(...)` to **reuse** the parent constructor "
         "instead of rewriting it. Clean and DRY (Don't Repeat Yourself)."),

        ("🔮 Magic / Dunder Methods",
         "`__str__` formats how a flower prints. `__len__` lets `len(cart)` work naturally. "
         "These are Python's special methods that integrate with built-in functions."),

        ("🧩 Composition",
         "`Cart` contains a list of `Flower` objects. `FlowerShop` contains a catalog of "
         "`Flower` objects. Neither inherits — they just *use* flowers. This is composition."),

        ("📌 Class & Static Methods",
         "`FlowerShop.create_default_shop()` is a **class method** — it creates a shop without "
         "needing an existing instance. `FlowerShop.care_tip()` is a **static method** — "
         "it doesn't need `self` or `cls`, just pure logic."),

        ("🤖 AI Integration (Modern Extension)",
         "The `ask_flower_ai()` and `get_ai_bouquet()` functions connect the OOP system to "
         "a real AI API (OpenRouter). This shows how classical OOP and modern AI work together "
         "— the AI assistant uses the same `FlowerShop` class data to give smart suggestions."),
    ]

    for title, explanation in concepts:
        st.markdown(f"""
        <div class="oop-badge">
            <strong>{title}</strong><br>
            {explanation}
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    st.markdown("---")
    st.markdown("### 🗂️ Class Hierarchy Diagram")
    st.code("""
Flower  ← Base / Parent Class
│   ├── name, color, petals, __price (private), emoji, description
│   ├── get_price(), set_price()          ← encapsulation
│   ├── special_feature()                 ← overridden (polymorphism)
│   └── __str__(), to_dict()              ← magic methods
│
├── Rose(Flower)
│       └── + has_thorns
├── Sunflower(Flower)
│       └── + height_cm
├── Tulip(Flower)
│       └── + season
└── Lavender(Flower)
        └── + scent_level

Cart                                       ← Composition
│   └── contains list of (Flower, qty)
│   └── __len__()

FlowerShop                                 ← Composition
    └── contains list of Flower objects
    └── @classmethod create_default_shop()
    └── @staticmethod care_tip()
    """, language="text")

    st.markdown("---")
    st.info("🎓 **Project by Ndacyayisenga Parfait** — University of Lodz, Poland 🇵🇱 | From Rwanda 🇷🇼")