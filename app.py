import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Pose et Install",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin: 0.2rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-height: 110px;
        max-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }
    
    .kpi-card h4 {
        margin: 0;
        padding: 0;
        color: white !important;
        font-size: 0.8rem !important;
        font-weight: 600;
        letter-spacing: 0.5px;
        line-height: 1.2;
        text-align: center;
        text-transform: uppercase;
        opacity: 0.95;
        flex-shrink: 0;
    }
    
    .kpi-card h1 {
        margin: 0;
        padding: 0;
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: bold;
        line-height: 1;
        text-align: center;
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .kpi-card p {
        margin: 0;
        padding: 0;
        color: white !important;
        font-size: 0.7rem;
        opacity: 0.9;
        line-height: 1;
        text-align: center;
        flex-shrink: 0;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #2196F3, #1976D2);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
    }
    
    .install-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196F3;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .devis-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%);
        border-left: 4px solid #FF9800;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px dashed #6c757d;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #007bff;
        background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%);
    }
    
    .continue-button {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        border: none;
        padding: 1.2rem 4rem;
        border-radius: 30px;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 3rem auto;
        display: block;
        box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
        width: 350px;
        text-align: center;
        text-decoration: none;
    }
    
    .continue-button:hover {
        background: linear-gradient(135deg, #c82333, #bd2130);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.5);
    }
    
    h1 {
        font-size: 1.8rem !important;
        color: #1565C0;
        margin-bottom: 0.5rem !important;
        text-align: center;
    }
    
    h2 {
        font-size: 1.3rem !important;
        color: #424242;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        color: #666;
        margin: 0.5rem 0 0.3rem 0 !important;
    }
    
    .stDataFrame {
        font-size: 0.85rem;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .stSelectbox label, .stRadio label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #424242 !important;
    }
    
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    hr {
        margin: 0.8rem 0 !important;
    }
    
    .euro-amount {
        color: #2E7D32 !important;
        font-weight: bold !important;
    }
    
    @media (max-width: 768px) {
        .kpi-card h1 {
            font-size: 1.2rem !important;
        }
        .kpi-card h4 {
            font-size: 0.6rem !important;
        }
        .kpi-card {
            min-height: 80px;
            max-height: 80px;
            padding: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def clean_dataframe_for_arrow(df):
    """
    Nettoie un DataFrame pour éviter les erreurs de sérialisation Arrow
    """
    df_clean = df.copy()
    
    # Colonnes qui doivent rester en string (identifiants complexes)
    string_columns = ['N° Commande', 'DEVIS', 'COMMANDE', 'NUMERO DEVIS', 'NUMERO COMMANDE', 
                     'Temps de travail', 'CLIENT', 'Nom client', 'Prestataire', 'POSEUR RETENU', 'COMMERCIAL']
    
    # Colonnes de montants (à garder en float)
    amount_columns = ['Montant facturé', 'POSE VENDUE PAR SIGNALS (HT)']
    
    # Colonnes de dates (à garder en datetime)
    date_columns = ['Date planifiée1', 'Date planifiée2', 'Date DEVIS', 'Date_Fictive_A_Planifier']
    
    # Colonnes entières
    int_columns = ['Année Fiscale', 'ANNEE FISCALE', 'Année']
    
    for col in df_clean.columns:
        if col in string_columns:
            df_clean[col] = df_clean[col].astype(str)
        elif col in amount_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0.0)
        elif col in date_columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce', dayfirst=True)
        elif col in int_columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype('Int64')
    
    return df_clean

def format_date(date_val):
    """Formate une date pour afficher seulement la date sans l'heure"""
    if pd.isna(date_val) or date_val is None:
        return "N/A"
    if isinstance(date_val, str):
        return date_val
    try:
        return date_val.strftime("%d/%m/%Y")
    except:
        return str(date_val)

def format_euro(amount):
    """Formate un montant en euros"""
    if pd.isna(amount) or amount is None:
        return "0 €"
    try:
        return f"{float(amount):,.0f} €".replace(",", " ")
    except:
        return f"{amount} €"

def get_fiscal_year_range(fiscal_year):
    """Retourne les dates de début et fin d'année fiscale"""
    try:
        year = int(fiscal_year)
        start_date = datetime(year-1, 8, 1)  # 1er août année N-1
        end_date = datetime(year, 7, 31)     # 31 juillet année N
        return start_date, end_date
    except:
        return None, None

def is_in_fiscal_year(date_val, fiscal_year):
    """Vérifie si une date est dans l'année fiscale"""
    if pd.isna(date_val) or fiscal_year is None:
        return False
    
    start_date, end_date = get_fiscal_year_range(fiscal_year)
    if start_date is None:
        return False
    
    try:
        if isinstance(date_val, str):
            date_val = pd.to_datetime(date_val, dayfirst=True)
        return start_date <= date_val <= end_date
    except:
        return False

def load_data():
    """Charge les données depuis les fichiers Excel uploadés"""
    data = {}
    if 'df_installations' in st.session_state:
        data['installations'] = st.session_state.df_installations
    if 'df_dossiers' in st.session_state:
        data['dossiers'] = st.session_state.df_dossiers
    if 'df_veolia' in st.session_state:
        data['veolia'] = st.session_state.df_veolia
    return data

def process_installations_data(df):
    """Traite et filtre les données d'installation"""
    # Supprimer d'abord les doublons complets
    df = df.drop_duplicates()
    
    df_filtered = df.dropna(subset=['Etat', 'Année Fiscale'])
    df_filtered = df_filtered.copy()
    
    # Convertir l'année fiscale en int
    df_filtered['Année Fiscale'] = pd.to_numeric(df_filtered['Année Fiscale'], errors='coerce').astype('Int64')
    
    # S'assurer que N° Commande est en string
    if 'N° Commande' in df_filtered.columns:
        df_filtered['N° Commande'] = df_filtered['N° Commande'].astype(str)
    
    # Convertir les dates en datetime
    date_cols = ['Date planifiée1', 'Date planifiée2']
    for col in date_cols:
        if col in df_filtered.columns:
            df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce', dayfirst=True, format='mixed')
    
    # CORRECTION TEMPS DE TRAVAIL : Nettoyer la colonne pour éviter les erreurs Arrow
    if 'Temps de travail' in df_filtered.columns:
        df_filtered['Temps de travail'] = df_filtered['Temps de travail'].astype(str)
    
    # Pour les installations "A planifier", créer une date fictive basée sur Mois installation + Année Fiscale
    if 'Mois installation' in df_filtered.columns:
        df_filtered['Date_Fictive_A_Planifier'] = None
        
        # Mapping des mois français vers les numéros
        mois_mapping = {
            'Janvier': 1, 'Février': 2, 'Mars': 3, 'Avril': 4, 'Mai': 5, 'Juin': 6,
            'Juillet': 7, 'Août': 8, 'Septembre': 9, 'Octobre': 10, 'Novembre': 11, 'Décembre': 12
        }
        
        for idx, row in df_filtered.iterrows():
            if row['Etat'] == 'A planifier':
                mois_str = row.get('Mois installation', '')
                annee_fiscale = row.get('Année Fiscale')
                
                if mois_str and pd.notna(annee_fiscale):
                    try:
                        mois_num = mois_mapping.get(mois_str.capitalize(), None)
                        annee_fiscale_int = int(annee_fiscale)
                        
                        if mois_num:
                            # Déterminer l'année réelle selon l'année fiscale
                            if mois_num >= 8:  # Août à Décembre = année N-1
                                annee_reelle = annee_fiscale_int - 1
                            else:  # Janvier à Juillet = année N
                                annee_reelle = annee_fiscale_int
                            
                            # Créer une date fictive au 15 du mois
                            date_fictive = datetime(annee_reelle, mois_num, 15)
                            df_filtered.at[idx, 'Date_Fictive_A_Planifier'] = date_fictive
                    except:
                        continue
    
    return df_filtered
def process_dossiers_data(df):
    """Traite les données des dossiers en cours"""
    df = df.copy()
    
    # CORRECTION COLONNES PROBLÉMATIQUES : Convertir en string pour éviter erreurs Arrow
    if 'DEVIS' in df.columns:
        df['DEVIS'] = df['DEVIS'].astype(str)
    
    if 'COMMANDE' in df.columns:
        df['COMMANDE'] = df['COMMANDE'].astype(str)
    
    if 'ANNEE FISCALE' in df.columns:
        df['ANNEE FISCALE'] = pd.to_numeric(df['ANNEE FISCALE'], errors='coerce').astype('Int64')
    
    # Nettoyer et convertir la colonne des montants en euros
    if 'POSE VENDUE PAR SIGNALS (HT)' in df.columns:
        def clean_euro_amount(value):
            if pd.isna(value):
                return 0.0
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                # Supprimer le symbole €, les espaces, et convertir les virgules en points
                cleaned = str(value).replace('€', '').replace(' ', '').replace(',', '.')
                # Supprimer tout caractère non numérique sauf le point
                cleaned = ''.join(c for c in cleaned if c.isdigit() or c == '.')
                try:
                    return float(cleaned) if cleaned else 0.0
                except:
                    return 0.0
            return 0.0
        
        df['POSE VENDUE PAR SIGNALS (HT)'] = df['POSE VENDUE PAR SIGNALS (HT)'].apply(clean_euro_amount)
    
    return df

def process_veolia_data(df):
    """Traite les données Veolia"""
    df = df.copy()
     # CORRECTION COLONNES NUMÉRIQUES PROBLÉMATIQUES : Convertir en string
    if 'NUMERO DEVIS' in df.columns:
        df['NUMERO DEVIS'] = df['NUMERO DEVIS'].astype(str)
    
    if 'NUMERO COMMANDE' in df.columns:
        df['NUMERO COMMANDE'] = df['NUMERO COMMANDE'].astype(str)
    
    # Mapping des mois en français
    mois_francais = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }
    
    if 'Date DEVIS' in df.columns:
        df['Date DEVIS'] = pd.to_datetime(df['Date DEVIS'], errors='coerce', dayfirst=True)
        df['Mois'] = df['Date DEVIS'].dt.month.map(mois_francais)
        df['Année'] = df['Date DEVIS'].dt.year.astype('Int64')
    
    # Nettoyer et convertir la colonne des montants en euros
    if 'POSE VENDUE PAR SIGNALS (HT)' in df.columns:
        def clean_euro_amount(value):
            if pd.isna(value):
                return 0.0
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                # Supprimer le symbole €, les espaces, et convertir les virgules en points
                cleaned = str(value).replace('€', '').replace(' ', '').replace(',', '.')
                # Supprimer tout caractère non numérique sauf le point
                cleaned = ''.join(c for c in cleaned if c.isdigit() or c == '.')
                try:
                    return float(cleaned) if cleaned else 0.0
                except:
                    return 0.0
            return 0.0
        
        df['POSE VENDUE PAR SIGNALS (HT)'] = df['POSE VENDUE PAR SIGNALS (HT)'].apply(clean_euro_amount)
    
    return df

def filter_by_fiscal_year(df, selected_fiscal_year):
    """Filtre le dataframe par année fiscale selon la logique métier"""
    if selected_fiscal_year == "Toutes":
        return df
    
    try:
        fiscal_year_int = int(selected_fiscal_year)
        start_date = datetime(fiscal_year_int - 1, 8, 1)  # 1er août N-1
        end_date = datetime(fiscal_year_int, 7, 31)       # 31 juillet N
    except:
        return df
    
    filtered_rows = []
    
    for idx, row in df.iterrows():
        etat = row.get('Etat', '')
        
        if etat == 'A planifier':
            # Pour "A planifier", utiliser la date fictive créée
            date_fictive = row.get('Date_Fictive_A_Planifier')
            if pd.notna(date_fictive) and start_date <= date_fictive <= end_date:
                filtered_rows.append(idx)
        else:
            # Pour les autres états, utiliser Date planifiée1
            date_planifiee = row.get('Date planifiée1')
            if pd.notna(date_planifiee) and start_date <= date_planifiee <= end_date:
                filtered_rows.append(idx)
    
    return df.loc[filtered_rows] if filtered_rows else df.iloc[0:0]

def get_installations_alerts(df, days_ahead=10, selected_fiscal_year=None):
    """Récupère les installations planifiées dans les prochains jours"""
    today = datetime.now()
    future_date = today + timedelta(days=days_ahead)
    
    planified = df[df['Etat'] == 'planifié'].copy()
    
    alerts = []
    for _, row in planified.iterrows():
        date1 = row.get('Date planifiée1')
        date2 = row.get('Date planifiée2')
        
        # Si une année fiscale est sélectionnée, filtrer par celle-ci
        if selected_fiscal_year and selected_fiscal_year != "Toutes":
            if not (is_in_fiscal_year(date1, selected_fiscal_year) or is_in_fiscal_year(date2, selected_fiscal_year)):
                continue
        
        is_alert = False
        
        if pd.notna(date1):
            if today <= date1 <= future_date:
                is_alert = True
        
        if pd.notna(date2) and not is_alert:
            if today <= date2 <= future_date:
                is_alert = True
        
        if pd.notna(date1) and pd.notna(date2) and not is_alert:
            if date1 <= future_date and date2 >= today:
                is_alert = True
        
        if is_alert:
            alerts.append(row)
    
    return pd.DataFrame(alerts) if alerts else pd.DataFrame()

def create_kpi_grid(etat_amounts, etat_counts, total_amount, total_count, title="TOTAL GÉNÉRAL"):
    """Crée une grille de KPIs où tous les KPIs sont sur la même ligne"""
    
    etats = etat_amounts.index.tolist()
    nb_etats = len(etats)
    
    if nb_etats == 0:
        # Afficher seulement le total si aucun état
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f'''
            <div class="kpi-card" style="background: linear-gradient(135deg, #4CAF50, #45a049); margin-bottom: 1rem; padding: 1rem;">
                <h4>{title}</h4>
                <h1 style="font-size: 1.6rem !important;">{format_euro(total_amount)}</h1>
                <p>{total_count} éléments</p>
            </div>
            ''', unsafe_allow_html=True)
        return
    
    # Tous les KPIs sur une seule ligne
    # Total + états = nb_etats + 1
    total_kpis = nb_etats + 1
    cols = st.columns(total_kpis)
    
    # Définir les couleurs pour chaque état
    colors = [
        '#FF9800', '#2196F3', '#9C27B0', '#4CAF50', '#F44336', '#795548',
        '#607D8B', '#E91E63', '#00BCD4', '#8BC34A', '#FFC107', '#3F51B5'
    ]
    
    # Première colonne : Total
    with cols[0]:
        st.markdown(f'''
        <div class="kpi-card" style="background: linear-gradient(135deg, #4CAF50, #45a049);">
            <h4>{title}</h4>
            <h1>{format_euro(total_amount)}</h1>
            <p>{total_count} éléments</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Colonnes suivantes : États
    for i, etat in enumerate(etats):
        color = colors[i % len(colors)]
        amount = etat_amounts[etat]
        count = etat_counts[etat]
        
        with cols[i + 1]:
            st.markdown(f'''
            <div class="kpi-card" style="background: linear-gradient(135deg, {color}, {color}CC);">
                <h4>{etat.upper()}</h4>
                <h1>{format_euro(amount)}</h1>
                <p>{count} éléments</p>
            </div>
            ''', unsafe_allow_html=True)

def format_dataframe_with_colors(df, amount_columns=None):
    """Formate un DataFrame avec des colonnes colorées ET nettoie pour Arrow"""

    if amount_columns is None:
        amount_columns = ['Montant facturé', 'POSE VENDUE PAR SIGNALS (HT)']
    
    # NETTOYER AVANT LE FORMATAGE pour éviter les erreurs Arrow
    df_display = clean_dataframe_for_arrow(df)
    # Formater les colonnes de montants
    for col in amount_columns:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(format_euro)
    
    # Formater les colonnes de dates
    date_columns = ['Date planifiée1', 'Date planifiée2', 'Date DEVIS']
    for col in date_columns:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(format_date)
    
    return df_display

def upload_files_page():
    """Page d'upload des fichiers avec présentation améliorée"""
    st.markdown('<h1>🔧 Pose et Install</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #6c757d; margin-bottom: 2rem;">📁 Import des fichiers Excel</h2>', unsafe_allow_html=True)
    
    # Sections horizontales pour les imports
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Titre coloré pour Installations
        st.markdown('<h3 style="color: #007bff; text-align: center; margin-bottom: 1rem;">📋 Fichier Installations</h3>', 
                   unsafe_allow_html=True)
        
        installations_file = st.file_uploader(
            "Sélectionnez le fichier Excel des installations",
            type=['xlsx', 'xls'],
            key="installations",
            help="Fichier contenant les données d'installations"
        )
        
        if installations_file:
            try:
                df_installations = pd.read_excel(installations_file)
                st.markdown(f'<div class="alert-success" style="margin-top: 1rem;">✅ Fichier chargé avec succès: {len(df_installations)} lignes</div>', 
                           unsafe_allow_html=True)
                st.session_state.df_installations = df_installations
            except Exception as e:
                st.markdown(f'<div class="alert-danger" style="margin-top: 1rem;">❌ Erreur lors du chargement: {str(e)}</div>', 
                           unsafe_allow_html=True)
    
    with col2:
        # Titre coloré pour Dossiers
        st.markdown('<h3 style="color: #28a745; text-align: center; margin-bottom: 1rem;">📊 Fichier Dossiers en cours</h3>', 
                   unsafe_allow_html=True)
        
        dossiers_file = st.file_uploader(
            "Sélectionnez le fichier Excel des dossiers",
            type=['xlsx', 'xls'],
            key="dossiers",
            help="Fichier contenant les dossiers en cours"
        )
        
        if dossiers_file:
            try:
                df_dossiers = pd.read_excel(dossiers_file)
                st.markdown(f'<div class="alert-success" style="margin-top: 1rem;">✅ Fichier chargé avec succès: {len(df_dossiers)} lignes</div>', 
                           unsafe_allow_html=True)
                st.session_state.df_dossiers = df_dossiers
            except Exception as e:
                st.markdown(f'<div class="alert-danger" style="margin-top: 1rem;">❌ Erreur lors du chargement: {str(e)}</div>', 
                           unsafe_allow_html=True)
    
    with col3:
        # Titre coloré pour Veolia
        st.markdown('<h3 style="color: #ffc107; text-align: center; margin-bottom: 1rem;">🏢 Fichier Veolia</h3>', 
                   unsafe_allow_html=True)
        
        veolia_file = st.file_uploader(
            "Sélectionnez le fichier Excel Veolia",
            type=['xlsx', 'xls'],
            key="veolia",
            help="Fichier contenant les données Veolia"
        )
        
        if veolia_file:
            try:
                df_veolia = pd.read_excel(veolia_file)
                st.markdown(f'<div class="alert-success" style="margin-top: 1rem;">✅ Fichier chargé avec succès: {len(df_veolia)} lignes</div>', 
                           unsafe_allow_html=True)
                st.session_state.df_veolia = df_veolia
            except Exception as e:
                st.markdown(f'<div class="alert-danger" style="margin-top: 1rem;">❌ Erreur lors du chargement: {str(e)}</div>', 
                           unsafe_allow_html=True)
    
    # Bouton centré et stylé - affiché seulement si tous les fichiers sont chargés
    if ('df_installations' in st.session_state and 
        'df_dossiers' in st.session_state and 
        'df_veolia' in st.session_state):
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Centrer le bouton sur toute la largeur de la page
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col3:
            st.markdown('''
            <div style="text-align: center;">
                <p style="color: #28a745; font-weight: bold; margin-bottom: 1rem;">
                    ✅ Tous les fichiers sont chargés avec succès !
                </p>
            </div>
            ''', unsafe_allow_html=True)
            
            if st.button("🚀 Continuer vers l'analyse", key="continue_btn", 
                        help="Commencer l'analyse des données",
                        type="primary"):
                st.session_state.page = "installations"
                st.rerun()
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('''
        <div style="text-align: center; padding: 2rem;">
            <p style="color: #6c757d; font-size: 1.1rem;">
                📋 Veuillez charger les 3 fichiers Excel pour continuer
            </p>
            <p style="color: #6c757d; font-size: 0.9rem;">
                Installations • Dossiers en cours • Veolia
            </p>
        </div>
        ''', unsafe_allow_html=True)

def get_filtered_options(df, filter_col, selected_values, dependent_cols):
    """Retourne les options filtrées pour les colonnes dépendantes"""
    if not selected_values or selected_values == "Toutes" or selected_values == "Tous":
        return {col: sorted(df[col].dropna().unique()) for col in dependent_cols if col in df.columns}
    
    # Filtrer le dataframe selon les valeurs sélectionnées
    if isinstance(selected_values, list):
        filtered_df = df[df[filter_col].isin(selected_values)]
    else:
        filtered_df = df[df[filter_col] == selected_values]
    
    return {col: sorted(filtered_df[col].dropna().unique()) for col in dependent_cols if col in df.columns}

def installations_page():
    """Page principale des installations avec filtrage simplifié"""
    data = load_data()
    
    if 'installations' not in data:
        st.markdown('<div class="alert-danger">❌ Fichier installations non chargé</div>', unsafe_allow_html=True)
        return
    
    df_processed = process_installations_data(data['installations'])
    
    st.markdown('<h1>🔧 Installations</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar pour les filtres avec cascade
    with st.sidebar:
        st.markdown('<h3>🎛️ Filtres</h3>', unsafe_allow_html=True)
        
        # Première sélection : Année fiscale
        annees = sorted([int(x) for x in df_processed['Année Fiscale'].dropna().unique()])
        selected_annee = st.selectbox(
            "Année fiscale:",
            ["Toutes"] + annees
        )
        
        # Filtrer d'abord par année fiscale
        if selected_annee != "Toutes":
            df_temp = filter_by_fiscal_year(df_processed, selected_annee)
        else:
            df_temp = df_processed
        
        # Deuxième sélection : Mois (basé sur l'année fiscale sélectionnée)
        if 'Mois installation' in df_temp.columns:
            mois_ordre = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                         'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
            mois_disponibles = [m for m in mois_ordre if m in df_temp['Mois installation'].values]
            selected_mois = st.selectbox(
                "Mois:",
                ["Tous"] + mois_disponibles,
                key="installations_mois"
            )
        else:
            selected_mois = "Tous"
        
        # Filtrer par mois
        if selected_mois != "Tous":
            df_temp2 = df_temp[df_temp['Mois installation'] == selected_mois]
        else:
            df_temp2 = df_temp
        
        # Troisième sélection : Prestataire (basé sur les filtres précédents)
        prestataires_disponibles = sorted(df_temp2['Prestataire'].dropna().unique())
        selected_prestataire = st.selectbox(
            "Prestataire:",
            ["Tous"] + prestataires_disponibles,
            key="prestataire_cascade"
        )
        
        # Appliquer le filtre final
        if selected_prestataire != "Tous":
            df_filtered = df_temp2[df_temp2['Prestataire'] == selected_prestataire]
        else:
            df_filtered = df_temp2
    
    # Alertes d'installations planifiées
    st.markdown('<h2>🚨 Alertes (10 prochains jours)</h2>', unsafe_allow_html=True)
    
    alerts_df = get_installations_alerts(df_processed, selected_fiscal_year=selected_annee)
    
    if not alerts_df.empty:
        st.markdown(f'<div class="alert-warning">⚠️ {len(alerts_df)} installation(s) à venir</div>', 
                   unsafe_allow_html=True)
        
        for _, alert in alerts_df.iterrows():
            st.markdown(f'''
            <div class="install-card">
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem;">
                    <div><strong>Commande:</strong> {alert.get('N° Commande', 'N/A')}</div>
                    <div><strong>Client:</strong> {alert.get('Nom client', 'N/A')}</div>
                    <div><strong>Prestataire:</strong> {alert.get('Prestataire', 'N/A')}</div>
                    <div><strong>Date:</strong> {format_date(alert.get('Date planifiée1'))}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Table détaillée des alertes
        st.markdown('<h3>📋 Détails des installations à venir</h3>', unsafe_allow_html=True)
        alert_cols = ['Nom client', 'N° Commande', 'Etat', 'Temps de travail', 
                     'Prestataire', 'Montant facturé', 'Mois installation', 'Date planifiée1']
        available_alert_cols = [col for col in alert_cols if col in alerts_df.columns]
        
        # Utiliser la fonction de formatage avec couleurs
        alerts_display = format_dataframe_with_colors(alerts_df[available_alert_cols], ['Montant facturé'])
        
        st.dataframe(alerts_display, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="alert-success">✅ Aucune installation à venir</div>', unsafe_allow_html=True)
    
    # Afficher les informations de filtrage
    filtres_actifs = []
    if selected_annee != "Toutes":
        try:
            annee_int = int(selected_annee)
            filtres_actifs.append(f"Année fiscale: {selected_annee} (Août {annee_int-1} → Juillet {annee_int})")
        except:
            filtres_actifs.append(f"Année fiscale: {selected_annee}")
    if selected_mois != "Tous":
        filtres_actifs.append(f"Mois: {selected_mois}")
    if selected_prestataire != "Tous":
        filtres_actifs.append(f"Prestataire: {selected_prestataire}")
    
    if filtres_actifs:
        st.info(f"📊 Filtres actifs: {' | '.join(filtres_actifs)}")
    
    # KPIs avec montants par état
    st.markdown('<h2>💰 KPIs - Montants par État</h2>', unsafe_allow_html=True)
    
    # Calculer les montants par état
    etat_counts = df_filtered['Etat'].value_counts()
    etat_amounts = df_filtered.groupby('Etat')['Montant facturé'].sum() if 'Montant facturé' in df_filtered.columns else pd.Series()
    total_amount = df_filtered['Montant facturé'].sum() if 'Montant facturé' in df_filtered.columns else 0
    
    # Utiliser la nouvelle fonction pour créer les KPIs
    create_kpi_grid(etat_amounts, etat_counts, total_amount, len(df_filtered), "TOTAL INSTALLATIONS")
    
    st.markdown("---")
    
    # Tables détaillées par état
    st.markdown('<h2>📋 Détails par État</h2>', unsafe_allow_html=True)
    
    for etat in ['A planifier', 'planifié', 'installé']:
        if etat in df_filtered['Etat'].values:
            count = etat_counts.get(etat, 0)
            amount = etat_amounts.get(etat, 0)
            
            with st.expander(f"📊 {etat.upper()} - {count} installations - {format_euro(amount)}", expanded=False):
                etat_df = df_filtered[df_filtered['Etat'] == etat]
                
                display_cols = ['Nom client', 'N° Commande', 'Temps de travail', 
                              'Prestataire', 'Montant facturé']
                
                # Pour "A planifier", afficher le mois d'installation au lieu des dates
                if etat == 'A planifier':
                    display_cols.append('Mois installation')
                else:
                    display_cols.extend(['Date planifiée1', 'Date planifiée2'])
                
                available_cols = [col for col in display_cols if col in etat_df.columns]
                
                # Utiliser la fonction de formatage avec couleurs
                etat_display = format_dataframe_with_colors(etat_df[available_cols], ['Montant facturé'])
                
                st.dataframe(etat_display, use_container_width=True, hide_index=True)

def dossiers_page():
    """Page des dossiers en cours avec filtrage en cascade"""
    data = load_data()
    
    if 'dossiers' not in data:
        st.markdown('<div class="alert-danger">❌ Fichier dossiers non chargé</div>', unsafe_allow_html=True)
        return
    
    df_processed = process_dossiers_data(data['dossiers'])
    
    st.markdown('<h1>📂 Dossiers en cours</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar pour les filtres avec cascade
    with st.sidebar:
        st.markdown('<h3>🎛️ Filtres</h3>', unsafe_allow_html=True)
        
        # Première sélection : Année fiscale
        if 'ANNEE FISCALE' in df_processed.columns:
            annees = sorted([int(x) for x in df_processed['ANNEE FISCALE'].dropna().unique()])
            selected_annee = st.selectbox(
                "Année fiscale:",
                ["Toutes"] + annees,
                key="dossiers_annee"
            )
        else:
            selected_annee = "Toutes"
        
        # Filtrer d'abord par année fiscale
        if selected_annee != "Toutes":
            df_temp = df_processed[df_processed['ANNEE FISCALE'] == selected_annee]
        else:
            df_temp = df_processed
        
        # Deuxième sélection : Mois (basé sur l'année fiscale sélectionnée)
        if 'Mois DEVIS' in df_temp.columns:
            mois_ordre = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                         'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
            mois_disponibles = [m for m in mois_ordre if m in df_temp['Mois DEVIS'].values]
            selected_mois = st.selectbox(
                "Mois:",
                ["Tous"] + mois_disponibles,
                key="dossiers_mois"
            )
        else:
            selected_mois = "Tous"
        
        # Filtrer par mois
        if selected_mois != "Tous":
            df_temp2 = df_temp[df_temp['Mois DEVIS'] == selected_mois]
        else:
            df_temp2 = df_temp
        
        # Troisième sélection : Commercial (basé sur les filtres précédents)
        if 'COMMERCIAL' in df_temp2.columns:
            commerciaux_disponibles = sorted(df_temp2['COMMERCIAL'].dropna().unique())
            selected_commercial = st.selectbox(
                "Commercial:",
                ["Tous"] + commerciaux_disponibles,
                key="dossiers_commercial"
            )
        else:
            selected_commercial = "Tous"
        
        # Filtrer par commercial
        if selected_commercial != "Tous":
            df_temp3 = df_temp2[df_temp2['COMMERCIAL'] == selected_commercial]
        else:
            df_temp3 = df_temp2
        
        # Quatrième sélection : Prestataire (basé sur les filtres précédents)
        if 'POSEUR RETENU' in df_temp3.columns:
            prestataires_disponibles = sorted(df_temp3['POSEUR RETENU'].dropna().unique())
            selected_prestataire = st.selectbox(
                "Prestataire:",
                ["Tous"] + prestataires_disponibles,
                key="dossiers_prestataire"
            )
        else:
            selected_prestataire = "Tous"
    
    # Appliquer le filtre final
    df_filtered = df_temp3.copy()
    if selected_prestataire != "Tous":
        df_filtered = df_filtered[df_filtered['POSEUR RETENU'] == selected_prestataire]
    
    # Afficher les informations de filtrage
    filtres_actifs = []
    if selected_annee != "Toutes":
        filtres_actifs.append(f"Année: {selected_annee}")
    if selected_mois != "Tous":
        filtres_actifs.append(f"Mois: {selected_mois}")
    if selected_commercial != "Tous":
        filtres_actifs.append(f"Commercial: {selected_commercial}")
    if selected_prestataire != "Tous":
        filtres_actifs.append(f"Prestataire: {selected_prestataire}")
    
    if filtres_actifs:
        st.info(f"📊 Filtres actifs: {' | '.join(filtres_actifs)}")
    
    # KPIs par état de devis
    st.markdown('<h2>💰 KPIs - Montants par État de Devis</h2>', unsafe_allow_html=True)
    
    if 'ETAT DE DEVIS' in df_filtered.columns and 'POSE VENDUE PAR SIGNALS (HT)' in df_filtered.columns:
        try:
            # S'assurer que les montants sont numériques
            df_filtered['POSE VENDUE PAR SIGNALS (HT)'] = pd.to_numeric(df_filtered['POSE VENDUE PAR SIGNALS (HT)'], errors='coerce').fillna(0)
            
            etat_amounts = df_filtered.groupby('ETAT DE DEVIS')['POSE VENDUE PAR SIGNALS (HT)'].sum()
            etat_counts = df_filtered['ETAT DE DEVIS'].value_counts()
            total_amount = df_filtered['POSE VENDUE PAR SIGNALS (HT)'].sum()
            
            # Utiliser la nouvelle fonction pour créer les KPIs
            create_kpi_grid(etat_amounts, etat_counts, total_amount, len(df_filtered), "TOTAL DOSSIERS")
            
            st.markdown("---")
            
            # Tables détaillées par état
            st.markdown('<h2>📋 Détails par État de Devis</h2>', unsafe_allow_html=True)
            
            etats = etat_amounts.index.tolist()
            for etat in etats:
                count = etat_counts[etat]
                amount = etat_amounts[etat]
                
                with st.expander(f"📊 {etat} - {count} dossiers - {format_euro(amount)}", expanded=False):
                    etat_df = df_filtered[df_filtered['ETAT DE DEVIS'] == etat]
                    
                    display_cols = ['CLIENT', 'DEVIS', 'Mois DEVIS', 'ANNEE FISCALE', 
                                  'COMMANDE', 'COMMERCIAL', 'POSEUR RETENU', 'POSE VENDUE PAR SIGNALS (HT)']
                    
                    available_cols = [col for col in display_cols if col in etat_df.columns]
                    
                    # Utiliser la fonction de formatage avec couleurs
                    etat_display = format_dataframe_with_colors(etat_df[available_cols], ['POSE VENDUE PAR SIGNALS (HT)'])
                    
                    st.dataframe(etat_display, use_container_width=True, hide_index=True)
                    
        except Exception as e:
            st.error(f"Erreur lors du calcul des montants: {str(e)}")
            st.info("Vérifiez que la colonne 'POSE VENDUE PAR SIGNALS (HT)' contient des valeurs numériques.")
    else:
        st.warning("Colonnes requises manquantes pour les KPIs")

def veolia_page():
    """Page Veolia avec filtrage en cascade"""
    data = load_data()
    
    if 'veolia' not in data:
        st.markdown('<div class="alert-danger">❌ Fichier Veolia non chargé</div>', unsafe_allow_html=True)
        return
    
    df_processed = process_veolia_data(data['veolia'])
    
    st.markdown('<h1>🏢 Veolia</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar pour les filtres avec cascade
    with st.sidebar:
        st.markdown('<h3>🎛️ Filtres</h3>', unsafe_allow_html=True)
        
        # Première sélection : Année
        if 'Année' in df_processed.columns:
            annees = sorted([int(x) for x in df_processed['Année'].dropna().unique()])
            selected_annee = st.selectbox(
                "Année:",
                ["Toutes"] + annees,
                key="veolia_annee"
            )
        else:
            selected_annee = "Toutes"
        
        # Filtrer d'abord par année
        if selected_annee != "Toutes":
            df_temp = df_processed[df_processed['Année'] == selected_annee]
        else:
            df_temp = df_processed
        
        # Deuxième sélection : Mois (basé sur l'année sélectionnée)
        if 'Mois' in df_temp.columns:
            mois_ordre = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                         'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
            mois_disponibles = [m for m in mois_ordre if m in df_temp['Mois'].values]
            selected_mois = st.selectbox(
                "Mois:",
                ["Tous"] + mois_disponibles,
                key="veolia_mois"
            )
        else:
            selected_mois = "Tous"
    
    # Appliquer le filtre final
    df_filtered = df_temp.copy()
    if selected_mois != "Tous":
        df_filtered = df_filtered[df_filtered['Mois'] == selected_mois]
    
    # Afficher les informations de filtrage
    filtres_actifs = []
    if selected_annee != "Toutes":
        filtres_actifs.append(f"Année: {selected_annee}")
    if selected_mois != "Tous":
        filtres_actifs.append(f"Mois: {selected_mois}")
    
    if filtres_actifs:
        st.info(f"📊 Filtres actifs: {' | '.join(filtres_actifs)}")
    
    # KPIs par état de devis
    st.markdown('<h2>💰 KPIs - Montants par État de Devis</h2>', unsafe_allow_html=True)
    
    if 'ETAT DE DEVIS' in df_filtered.columns and 'POSE VENDUE PAR SIGNALS (HT)' in df_filtered.columns:
        try:
            # S'assurer que les montants sont numériques
            df_filtered['POSE VENDUE PAR SIGNALS (HT)'] = pd.to_numeric(df_filtered['POSE VENDUE PAR SIGNALS (HT)'], errors='coerce').fillna(0)
            
            etat_amounts = df_filtered.groupby('ETAT DE DEVIS')['POSE VENDUE PAR SIGNALS (HT)'].sum()
            etat_counts = df_filtered['ETAT DE DEVIS'].value_counts()
            total_amount = df_filtered['POSE VENDUE PAR SIGNALS (HT)'].sum()
            
            # Utiliser la nouvelle fonction pour créer les KPIs
            create_kpi_grid(etat_amounts, etat_counts, total_amount, len(df_filtered), "TOTAL VEOLIA")
            
            st.markdown("---")
            
            # Tables détaillées par état
            st.markdown('<h2>📋 Détails par État de Devis Veolia</h2>', unsafe_allow_html=True)
            
            etats = etat_amounts.index.tolist()
            for etat in etats:
                count = etat_counts[etat]
                amount = etat_amounts[etat]
                
                with st.expander(f"📊 {etat} - {count} dossiers - {format_euro(amount)}", expanded=False):
                    etat_df = df_filtered[df_filtered['ETAT DE DEVIS'] == etat]
                    
                    display_cols = ['CLIENT', 'NUMERO DEVIS', 'NUMERO COMMANDE', 'Date DEVIS', 
                                  'POSEUR RETENU', 'POSE VENDUE PAR SIGNALS (HT)', 'Mois', 'Année']
                    
                    available_cols = [col for col in display_cols if col in etat_df.columns]
                    
                    # Utiliser la fonction de formatage avec couleurs
                    etat_display = format_dataframe_with_colors(etat_df[available_cols], ['POSE VENDUE PAR SIGNALS (HT)'])
                    
                    st.dataframe(etat_display, use_container_width=True, hide_index=True)
                    
        except Exception as e:
            st.error(f"Erreur lors du calcul des montants: {str(e)}")
            st.info("Vérifiez que la colonne 'POSE VENDUE PAR SIGNALS (HT)' contient des valeurs numériques.")
    else:
        st.warning("Colonnes requises manquantes pour les KPIs")

def main():
    """Fonction principale"""
    
    # Initialiser la session state
    if 'page' not in st.session_state:
        st.session_state.page = "upload"
    
    # Navigation
    if st.session_state.page != "upload":
        st.sidebar.markdown('<h3>📱 Navigation</h3>', unsafe_allow_html=True)
        
        # Bouton Import en premier
        if st.sidebar.button("📁 Import", use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()
        
        st.sidebar.markdown("---")  # Un seul séparateur après Import
        
        if st.sidebar.button("🔧 Installations", use_container_width=True):
            st.session_state.page = "installations"
            st.rerun()
        
        if st.sidebar.button("📂 Dossiers", use_container_width=True):
            st.session_state.page = "dossiers"
            st.rerun()
        
        if st.sidebar.button("🏢 Veolia", use_container_width=True):
            st.session_state.page = "veolia"
            st.rerun()
    
    # Affichage des pages
    if st.session_state.page == "upload":
        upload_files_page()
    elif st.session_state.page == "installations":
        installations_page()
    elif st.session_state.page == "dossiers":
        dossiers_page()
    elif st.session_state.page == "veolia":
        veolia_page()

if __name__ == "__main__":
    main()