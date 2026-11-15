import os, hashlib
from datetime import date, datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BOUTIQUE ABDEL PRO — Biz-Pilot", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 100%); }
.kpi-card { background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.25); }
.kpi-title { color: #94a3b8; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px; }
.kpi-value { font-size: 1.6rem; font-weight: 800; color: #f8fafc; }
.kpi-sub { font-size: 0.8rem; margin-top: 5px; }
.receipt-box { background: #ffffff; color: #0f172a; padding: 25px; border-radius: 14px; border-top: 8px solid #2563eb; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: sans-serif; max-width: 460px; margin: auto; }
</style>
""", unsafe_allow_html=True)

FICHIER = "donnees_abdel.csv"
MDP_HASH = hashlib.sha256("abdel2026".encode()).hexdigest()

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("<br><br><h1 style='text-align:center;'>🚀 BOUTIQUE ABDEL PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8;'>Espace de Gestion Sécurisé — Biz-Pilot Pro</p>", unsafe_allow_html=True)
        with st.form("login"):
            mdp = st.text_input("Mot de passe d'accès", type="password", placeholder="Entrez votre mot de passe privé")
            if st.form_submit_button("🔓 Se connecter", width="stretch"):
                if hashlib.sha256(mdp.encode()).hexdigest() == MDP_HASH:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect.")
        st.caption("🔒 Licence Pro activée • Support : +235 66 02 15 37")
    st.stop()
def charger():
    cols = ["ID", "Date", "Caisse", "Type", "Produit", "Client", "Quantite", "Prix_Vente", "Cout_Achat"]
    if os.path.exists(FICHIER):
        return pd.read_csv(FICHIER)[cols]
    return pd.DataFrame(columns=cols)

def ajouter(v_date, caisse, op_type, prod, client, qty, prix, cout):
    df = charger()
    tid = f"TRX-{datetime.now().strftime('%H%M%S')}"
    row = pd.DataFrame([{"ID": tid, "Date": str(v_date), "Caisse": caisse, "Type": op_type, "Produit": prod.strip(), "Client": client.strip() or "Client Comptoir", "Quantite": int(qty), "Prix_Vente": float(prix), "Cout_Achat": float(cout)}])
    pd.concat([df, row], ignore_index=True).to_csv(FICHIER, index=False)
    return tid

h1, h2 = st.columns([3, 1])
with h1:
    st.title("🚀 BOUTIQUE ABDEL PRO")
    st.caption("Biz-Pilot Pro — Gestion Multi-Caisses, Bénéfices & Reçus Certifiés")
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔒 Verrouiller", width="stretch"):
        st.session_state.auth = False
        st.rerun()

df = charger()
if not df.empty:
    df["Total"] = df.apply(lambda r: (r["Quantite"] * r["Prix_Vente"]) if r["Type"] == "Entrée (+)" else -(r["Quantite"] * r["Prix_Vente"]), axis=1)
    df["Benefice"] = df.apply(lambda r: ((r["Quantite"] * r["Prix_Vente"]) - (r["Quantite"] * r["Cout_Achat"])) if (r["Caisse"] == "Boutique" and r["Type"] == "Entrée (+)") else (r["Total"] if r["Type"] == "Sortie (-)" and r["Caisse"] == "Boutique" else 0), axis=1)

t1, t2, t3, t4 = st.tabs(["📊 Tableau de Bord", "➕ Nouvelle Opération", "🧾 Reçu Client QR", "⚙️ Sauvegarde"])

with t1:
    if df.empty:
        st.info("👋 Bienvenue Abdel ! Cliquez sur l'onglet **➕ Nouvelle Opération** pour enregistrer votre première vente.")
    else:
        sb = df[df["Caisse"] == "Boutique"]["Total"].sum()
        bb = df[df["Caisse"] == "Boutique"]["Benefice"].sum()
        sp = df[df["Caisse"] == "Argent Personnel"]["Total"].sum()
        sc = df[df["Caisse"] == "Dépôt Client"]["Total"].sum()
        ca = df[(df["Caisse"] == "Boutique") & (df["Type"] == "Entrée (+)")]["Total"].sum()
        marge = (bb / ca * 100) if ca > 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='kpi-card' style='border-left:4px solid #3b82f6;'><div class='kpi-title'>🏪 Caisse Boutique</div><div class='kpi-value'>{sb:,.0f} FCFA</div><div class='kpi-sub' style='color:#60a5fa;'>Trésorerie commerciale</div></div>".replace(",", " "), unsafe_allow_html=True)
        c2.markdown(f"<div class='kpi-card' style='border-left:4px solid #10b981;'><div class='kpi-title'>💰 Bénéfice Net</div><div class='kpi-value'>{bb:,.0f} FCFA</div><div class='kpi-sub' style='color:#34d399;'>Marge : {marge:.1f}%</div></div>".replace(",", " "), unsafe_allow_html=True)
        c3.markdown(f"<div class='kpi-card' style='border-left:4px solid #8b5cf6;'><div class='kpi-title'>👤 Argent Personnel</div><div class='kpi-value'>{sp:,.0f} FCFA</div><div class='kpi-sub' style='color:#a78bfa;'>Fonds privés isolés</div></div>".replace(",", " "), unsafe_allow_html=True)
        c4.markdown(f"<div class='kpi-card' style='border-left:4px solid #f59e0b;'><div class='kpi-title'>🤝 Dépôts Clients</div><div class='kpi-value'>{sc:,.0f} FCFA</div><div class='kpi-sub' style='color:#fbbf24;'>Fonds gardés pour tiers</div></div>".replace(",", " "), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        filtre = f1.selectbox("Filtrer par caisse :", ["Toutes les caisses", "Boutique", "Argent Personnel", "Dépôt Client"])
        rech = f2.text_input("🔍 Rechercher produit, client ou ID :", placeholder="Ex: Téléphone, Client...")
        dfa = df if filtre == "Toutes les caisses" else df[df["Caisse"] == filtre]
        if rech.strip():
            dfa = dfa[dfa.apply(lambda r: rech.lower() in str(r["Produit"]).lower() or rech.lower() in str(r["Client"]).lower() or rech.lower() in str(r["ID"]).lower(), axis=1)]

        g1, g2 = st.columns(2)
        with g1:
            st.subheader("🏆 Top Produits & Services")
            vp = dfa[dfa["Type"] == "Entrée (+)"]
            if not vp.empty:
                st.bar_chart(vp.groupby("Produit")["Total"].sum(), color="#3b82f6")
        with g2:
            st.subheader("📈 Courbe de Trésorerie")
            if not dfa.empty:
                st.area_chart(dfa.groupby("Date")["Total"].sum(), color="#10b981")

        st.subheader("📋 Journal des Opérations")
        st.dataframe(dfa.iloc[::-1], width="stretch", hide_index=True)
with t2:
    st.subheader("➕ Enregistrer un mouvement")
    with st.form("f_op", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        od = c1.date_input("Date", value=date.today())
        oc = c1.selectbox("Caisse", ["Boutique", "Argent Personnel", "Dépôt Client"])
        ot = c2.selectbox("Type", ["Entrée (+)", "Sortie (-)"])
        op = c2.text_input("Désignation", placeholder="Ex: Vente article / Prestation")
        ocl = c3.text_input("Client", placeholder="Ex: Nom du client")
        oq = c3.number_input("Quantité", min_value=1, value=1)
        p1, p2 = st.columns(2)
        opx = p1.number_input("Prix unitaire / Montant (FCFA)", min_value=0, value=5000, step=500)
        oct = p2.number_input("Coût d'achat unitaire", min_value=0, value=0, step=500)
        if st.form_submit_button("✅ Enregistrer", width="stretch"):
            if not op.strip():
                st.error("Saisissez une désignation.")
            else:
                nid = ajouter(od, oc, ot, op, ocl, oq, opx, oct)
                st.success(f"Opération **{nid}** enregistrée !")

with t3:
    st.subheader("🧾 Reçu Certifié par QR Code")
    if df.empty:
        st.info("Enregistrez d'abord une transaction.")
    else:
        cc, cp = st.columns([1, 1.3])
        with cc:
            nb = st.text_input("Nom boutique", value="BOUTIQUE ABDEL PRO")
            tb = st.text_input("Téléphone", value="+235 00 00 00 00")
            ltrx = df["ID"] + " • " + df["Produit"] + " (" + df["Client"] + ")"
            ch = st.selectbox("Transaction :", ltrx.iloc[::-1])
            lg = df[df["ID"] == ch.split(" • ")[0]].iloc[0]
            tot = lg["Quantite"] * lg["Prix_Vente"]
            qrd = f"RECU:{lg['ID']}|DATE:{lg['Date']}|CLIENT:{lg['Client']}|TOTAL:{tot:.0f}FCFA"
            qru = f"https://qrserver.com{qrd}"
        with cp:
            st.markdown(f"<div class='receipt-box'><h3 style='text-align:center;margin:0;color:#1e3a8a;'>{nb}</h3><p style='text-align:center;margin:4px 0 12px 0;color:#475569;'>Tél : {tb}</p><hr><p><strong>Reçu N° :</strong> {lg['ID']}</p><p><strong>Date :</strong> {lg['Date']}</p><p><strong>Client :</strong> {lg['Client']}</p><hr><p><strong>Article :</strong> {lg['Produit']} (x{lg['Quantite']})</p><p><strong>Prix Unitaire :</strong> {lg['Prix_Vente']:,.0f} FCFA</p><h2 style='text-align:right;color:#0f172a;'>TOTAL : {tot:,.0f} FCFA</h2><div style='text-align:center;margin-top:15px;'><img src='{qru}'><p style='font-size:0.75rem;color:#64748b;'>Code QR d'authenticité • Biz-Pilot Pro</p></div></div>".replace(",", " "), unsafe_allow_html=True)

with t4:
    st.subheader("⚙️ Sauvegarde et Maintenance")
    if not df.empty:
        csv_e = df.drop(columns=["Total", "Benefice"], errors="ignore").to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Télécharger ma sauvegarde (CSV)", data=csv_e, file_name=f"Sauvegarde_{date.today()}.csv", mime="text/csv")
        if st.button("🗑️ Annuler la dernière opération"):
            df.drop(columns=["Total", "Benefice"], errors="ignore").iloc[:-1].to_csv(FICHIER, index=False)
            st.rerun()
