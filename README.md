# 🌸 AI Flower Shop
### Object-Oriented Programming Project + AI Integration
**Author:** Ndacyayisenga Parfait  
**University:** University of Lodz  
**Course:** Object-Oriented Programming

---

## 🌍 Live Demo
👉 **[Open the Live App](https://flower-shop-oop-cblq6e9upgbfmuxtmy2rgp.streamlit.app/)**  


---

## 📌 Project Description

A fully functional **AI-powered Flower Shop** built entirely with Python OOP principles and deployed as a web application using Streamlit. Customers can browse flowers, add them to a cart, and get personalized bouquet suggestions from an AI assistant named **Flora**.

---

## 🧠 OOP Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **Classes & Objects** | `Flower`, `Rose`, `Sunflower`, `Tulip`, `Lavender`, `Cart`, `FlowerShop` |
| **Encapsulation** | `__price` private attribute with `get_price()` / `set_price()` |
| **Inheritance** | Rose, Sunflower, Tulip, Lavender all inherit from Flower |
| **Polymorphism** | `special_feature()` overridden in every child class |
| **`super()`** | Every child calls `super().__init__()` |
| **Magic Methods** | `__str__`, `__len__` |
| **Composition** | Cart and FlowerShop contain Flower objects |
| **Class Methods** | `FlowerShop.create_default_shop()` |
| **Static Methods** | `FlowerShop.care_tip()` |
| **AI Integration** | OpenRouter API powers the Flora AI assistant |

---

## 🗂️ Class Hierarchy

```
Flower  (Base Class)
├── Rose        → adds: has_thorns
├── Sunflower   → adds: height_cm  
├── Tulip       → adds: season
└── Lavender    → adds: scent_level

Cart            (Composition — manages Flower objects)
FlowerShop      (Composition — manages catalog of Flowers)
```

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/Aime-coder/flower-shop-oop.git
cd flower-shop-oop

pip install -r requirements.txt

# Create .env file with your API key
echo "OPENROUTER_API_KEY=your-key-here" > .env

streamlit run app.py
```

---

## 👨‍💻 Author

**Ndacyayisenga Parfait**  
Student — University of Lodz, Poland 🇵🇱  
From Rwanda 🇷🇼