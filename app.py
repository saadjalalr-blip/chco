from flask import Flask, render_template, request, redirect, flash, session
from datetime import timedelta

# 📌 قاعدة البيانات
from database import init_db, ajouter_commande

app = Flask(__name__)
app.secret_key = "CHOCOKING123"
app.permanent_session_lifetime = timedelta(days=365)

# ---- Produits ----
produits = [
    {
        "id": 1,
        "nom": "CHOCOFIT – Dattes",
        "img": "prod1.png",
        "prix": 177,
        "promo": "-20 DH livraison (1ère commande)",
        "description": "Pâte à tartiner naturelle à base de dattes, cacao pur, noisettes et huile de coco."
    },
    {
        "id": 2,
        "nom": "CHOCOFIT – Kaki",
        "img": "prod2.png",
        "prix": 188,
        "promo": "-20 DH livraison (1ère commande)",
        "description": "Pâte à tartiner naturelle au kaki, cacao pur et fruits secs marocains."
    },
    {
        "id": 3,
        "nom": "Pack Duo (Dattes + Kaki)",
        "img": "packduo.png",
        "prix": 345,
        "promo": "Pack duo spécial CHOCOFIT",
        "description": "Combo parfait : CHOCOFIT dattes + CHOCOFIT kaki."
    },
    {
        "id": 4,
        "nom": "Black Friday – CHOCOFIT Dattes",
        "img": "prod1_black.png",
        "prix": 147,
        "promo": "OFFRE BLACK FRIDAY",
        "description": "Prix spécial Black Friday – quantité limitée."
    },
    {
        "id": 5,
        "nom": "Black Friday – CHOCOFIT Kaki",
        "img": "prod2_black.png",
        "prix": 158,
        "promo": "OFFRE BLACK FRIDAY",
        "description": "Prix spécial Black Friday – quantité limitée."
    }
]


@app.route('/')
def home():
    return render_template("index.html", produits=produits)


@app.route('/commande/<int:pid>')
def commande(pid):
    produit = next((p for p in produits if p["id"] == pid), None)
    return render_template("commande.html", produit=produit)


@app.route('/confirmation', methods=['POST'])
def confirmation():

    champs = ["nom", "prenom", "email", "telephone", "adresse"]
    for c in champs:
        if request.form.get(c) == "":
            flash("⚠️ Vous devez remplir tous les champs !")
            return redirect(request.referrer)

    nom = request.form["nom"]
    prenom = request.form["prenom"]
    email = request.form["email"]
    telephone = request.form["telephone"]
    adresse = request.form["adresse"]
    produit_nom = request.form["produit"]
    prix_base = int(request.form["prix"])

    # ⭐ تقييم
    rating = request.form.get("rating", None)

    # Remise 1ère commande
    if "a_commande" not in session:
        remise = -20
        session["a_commande"] = True
    else:
        remise = 0

    total = prix_base + remise

    # حفظ البيانات
    ajouter_commande(nom, prenom, email, telephone, adresse, produit_nom, prix_base, remise, total, rating)

    return render_template(
        "confirmation.html",
        nom=nom,
        produit=produit_nom,
        prix=prix_base,
        remise=remise,
        total=total,
        rating=rating
    )


# 🔥 إنشاء قاعدة البيانات
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)







