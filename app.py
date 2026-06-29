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

    def care_instructions(self):
        """
        Returns care instructions for this flower.
        Overridden by each child class with data-dependent behavior (polymorphism).
        The base version is a generic fallback.
        """
        return f"Keep {self.name} in a bright spot and water regularly."

    def to_dict(self):
        return {
            "name"        : self.name,
            "color"       : self.color,
            "petals"      : self.petals,
            "price"       : self.__price,
            "emoji"       : self.emoji,
            "description" : self.description,
            "feature"     : self.care_instructions(),
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
    Extra attribute: has_thorns (bool).
    care_instructions() gives different handling advice depending on whether
    the rose has thorns or not. Data drives the behavior.
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

    def care_instructions(self):
        """
        Care depends on has_thorns.
        Thorny roses need protective gloves and specific pruning technique.
        Thornless roses are easier to handle but still need careful watering.
        """
        if self.has_thorns:
            return (
                "🧤 Always wear thick gloves when handling — thorns can cause injury. "
                "Prune at a 45° angle just above a leaf node to encourage new growth. "
                "Water at the base every 2 days, never wet the leaves to avoid fungus. "
                "Remove dead petals regularly to promote blooming."
            )
        else:
            return (
                "✋ Thornless variety — safe to handle without gloves. "
                "Still prune at a 45° angle to keep the plant healthy. "
                "Water at the base every 2 days and place in full sunlight. "
                "Easier to arrange in bouquets — great for beginners."
            )


class Sunflower(Flower):
    """
    Sunflower class - inherits from Flower.
    Extra attribute: height_cm (int).
    care_instructions() gives different support and watering advice
    depending on how tall the sunflower grows.
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
        self.height_cm = height_cm

    def care_instructions(self):
        """
        Care depends on height_cm.
        Taller sunflowers need stronger stakes and more frequent watering.
        Shorter ones are more self-supporting and need less water.
        """
        if self.height_cm > 200:
            return (
                f"🪵 At {self.height_cm}cm, this sunflower needs a strong bamboo stake "
                f"tied at two points to prevent wind damage. "
                f"Water deeply every 2 days — tall plants have large root systems. "
                f"Place in full sun for at least 8 hours daily. "
                f"Fertilize once a week during the growing season."
            )
        else:
            return (
                f"🌱 At {self.height_cm}cm, this sunflower is compact and largely self-supporting. "
                f"A light stake is enough if needed. "
                f"Water every 3 days — smaller plants need less moisture. "
                f"Full sun for 6 hours daily is sufficient. "
                f"Great for indoor pots or small garden spaces."
            )


class Tulip(Flower):
    """
    Tulip class - inherits from Flower.
    Extra attribute: season (str).
    care_instructions() gives different storage and planting advice
    depending on which season the tulip is meant to bloom in.
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

    def care_instructions(self):
        """
        Care depends on season.
        Spring tulips need cold storage before planting.
        Summer tulips go straight into warm soil.
        Autumn tulips need planting in late summer.
        Each season means a completely different preparation routine.
        """
        instructions = {
            "Spring": (
                "❄️ Spring tulip: plant bulbs in autumn (October–November) "
                "after storing them at 5–10°C for at least 8 weeks. "
                "This cold period is essential — without it the bulb will not bloom. "
                "Plant 15cm deep in well-drained soil and water lightly after planting."
            ),
            "Summer": (
                "☀️ Summer tulip: plant bulbs in spring once the ground warms above 10°C. "
                "No cold storage needed — these varieties prefer warmth from the start. "
                "Plant 10cm deep, water every 3 days, and ensure full sun exposure. "
                "Ideal for outdoor beds and large containers."
            ),
            "Autumn": (
                "🍂 Autumn tulip: plant bulbs in mid-summer (July–August) "
                "so they establish before the first frost. "
                "Store bulbs in a cool dry place until planting time. "
                "Water weekly and protect from heavy rain to prevent bulb rot."
            ),
            "Winter": (
                "🌨️ Winter tulip: a hardy variety that tolerates frost. "
                "Plant in early autumn and mulch heavily to insulate the bulbs. "
                "No watering needed in winter — rain is sufficient. "
                "They will push through snow and bloom in late winter."
            ),
        }
        return instructions.get(self.season, f"Plant in well-drained soil and water regularly.")


class Lavender(Flower):
    """
    Lavender class - inherits from Flower.
    Extra attribute: scent_level (str).
    care_instructions() gives different watering and pruning advice
    depending on the intensity of the scent, which reflects the plant's oil content.
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

    def care_instructions(self):
        """
        Care depends on scent_level.
        Strong-scented lavender has high oil content — it needs drier conditions.
        Mild-scented lavender is more tolerant of moisture.
        Light-scented lavender is the most adaptable but needs the most pruning.
        """
        if self.scent_level == "Strong":
            return (
                "🪨 Strong scent means high essential oil content — do not overwater. "
                "Water only when the top 5cm of soil is completely dry (every 10–14 days). "
                "Plant in sandy, well-drained soil with full sun. "
                "Prune by one third after flowering to keep the plant compact and maximize oil production."
            )
        elif self.scent_level == "Mild":
            return (
                "💧 Mild scent variety — slightly more tolerant of moisture than strong varieties. "
                "Water every 7–10 days, allowing soil to partially dry between waterings. "
                "Works well in regular garden soil with good drainage. "
                "Prune lightly after flowering — avoid cutting into old woody stems."
            )
        else:
            return (
                "🌿 Light scent variety — the most adaptable lavender for beginners. "
                "Water every 5–7 days and tolerates slightly heavier soil. "
                "Can grow in partial shade, though full sun produces better fragrance. "
                "Prune regularly throughout the season to encourage bushy growth."
            )


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

                        with st.expander("🌿 Care Instructions (polymorphism)"):
                            # care_instructions() is defined in Flower but overridden
                            # in every child class with data-dependent logic.
                            # The same method call produces different behavior per class.
                            st.write(flower.care_instructions())

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
         "Every flower displayed in the shop is a real object created from one of these classes."),

        ("🔒 Encapsulation",
         "__price is a private attribute in the Flower class. "
         "It cannot be accessed or changed directly from outside the class. "
         "You must use get_price() to read it and set_price() to modify it. "
         "This protects the data from accidental or unauthorized changes."),

        ("👪 Inheritance",
         "Rose, Sunflower, Tulip, and Lavender all inherit from Flower using super().__init__(). "
         "They automatically get all parent attributes (name, color, petals, price, emoji) "
         "and only define their own extras: has_thorns, height_cm, season, scent_level."),

        ("🔄 Polymorphism — care_instructions()",
         "care_instructions() is defined once in the Flower base class. "
         "Every child class overrides it with behavior that depends on its own unique data: "
         "Rose uses has_thorns — thorny roses need gloves and specific pruning; thornless ones do not. "
         "Sunflower uses height_cm — tall sunflowers (>200cm) need strong stakes and water every 2 days; short ones every 3. "
         "Tulip uses season — Spring tulips need 8 weeks of cold storage; Summer tulips go straight into warm soil; each season is a different routine. "
         "Lavender uses scent_level — Strong scent means high oil content and very dry soil; Mild is more tolerant; Light needs the most pruning. "
         "This is the correct use of polymorphism: one method name, one shared theme (care), "
         "but each class provides its own data-driven implementation."),

        ("⚡ super()",
         "Every child class calls super().__init__() to reuse the parent constructor. "
         "This avoids rewriting the same 6 attributes in every child class (DRY principle — Don't Repeat Yourself)."),

        ("🔮 Magic / Dunder Methods",
         "__str__ controls how a flower prints as a string. "
         "__repr__ gives a technical developer-friendly representation. "
         "__eq__ lets you compare two flowers with == based on name and color. "
         "__lt__ lets you sort a list of flowers by price using sorted(). "
         "__len__ makes len(cart) work naturally on the Cart class."),

        ("🧩 Composition",
         "Cart contains a list of Flower objects. FlowerShop contains a catalog of Flower objects. "
         "Neither Cart nor FlowerShop inherits from Flower — they simply use flowers as components. "
         "This is composition: building complex objects from simpler ones."),

        ("📌 Class & Static Methods",
         "FlowerShop.create_default_shop() is a @classmethod — it creates a complete shop "
         "without needing an existing instance. "
         "FlowerShop.care_tip() is a @staticmethod — it contains pure logic with no need "
         "for self or cls. Both are called directly on the class, not on an object."),
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
│   methods    : get_price(), set_price(), care_instructions(), to_dict()
│   dunder     : __str__, __repr__, __eq__, __lt__
│
│   care_instructions() — overridden in every child (polymorphism)
│   Same theme: how to care for the flower
│   Different behavior: driven by each class's own data
│
├── Rose(Flower)
│       data used : has_thorns (bool)
│       care      : thorny → gloves + specific pruning technique
│                   thornless → safe handling + standard pruning
│
├── Sunflower(Flower)
│       data used : height_cm (int)
│       care      : >200cm → strong stake + water every 2 days
│                   ≤200cm → light stake + water every 3 days
│
├── Tulip(Flower)
│       data used : season (str)
│       care      : Spring → 8 weeks cold storage before planting
│                   Summer → plant in warm soil, no cold needed
│                   Autumn → plant in mid-summer, protect from frost
│                   Winter → mulch heavily, no extra watering
│
└── Lavender(Flower)
        data used : scent_level (str)
        care      : Strong → very dry soil, prune 1/3 after flowering
                    Mild   → moderate watering, light pruning
                    Light  → most adaptable, regular pruning

Cart         (Composition — contains Flower objects)  __len__()
FlowerShop   (Composition — contains Flower catalog)  @classmethod  @staticmethod
    """, language="text")

    st.info("🎓 Project by Ndacyayisenga Parfait — University of Lodz 🇵🇱 | From Rwanda 🇷🇼")

