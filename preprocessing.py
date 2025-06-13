import streamlit as st
import pandas as pd
import ollama
import base64
import re

st.set_page_config(page_title="🔐 Veri Mahremiyet Analizi", layout="wide")

# Özelleştirilmiş başlık ve stil
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #e0f7fa, #f0f4ff);
            background-attachment: fixed;
        }
        header[data-testid="stHeader"] {
            background: linear-gradient(to right, #e0f7fa, #f0f4ff);
            border-bottom: 2px solid #1f77b4;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        }        
        .main {background-color: #f5f7fa;}
        .title-style {
            font-size: 36px;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 0.5em;
        }
        .subtitle-style {
            font-size: 20px;
            color: #333333;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 0.6em 1.2em;
        }
        .stButton>button:hover {
            background-color: #105a8d;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-style">LLM ile Sağlık & Kişisel Veri Gizlilik Analizi</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Lütfen bir CSV dosyası yükleyin", type="csv")

def extract_columns_from_summary(text):
    """
    LLM çıktısından kaldırılan sütunları dinamik olarak ayıklar.
    Hem satır içi virgüllü liste hem de madde işaretli (•, -, vb.) liste formatlarını destekler.
    """
    # 1. "The following columns were removed: ID Number, Email, Phone Number" tarzı satırları yakala
    inline_pattern = r"The following columns were removed:\s*([A-Za-z0-9_.,\- ()]+)"
    inline_match = re.search(inline_pattern, text, flags=re.IGNORECASE)

    if inline_match:
        inline_raw = inline_match.group(1)
        return [col.strip() for col in inline_raw.split(',') if col.strip()]

    # 2. Alternatif olarak, madde işaretli listeleri yakala ("Removed columns:" altında olabilir)
    block_pattern = r"Removed columns:.*?(?:\n[-•*]\s*([A-Za-z0-9_.,\- ()]+))+"
    block_matches = re.findall(r"[-•*]\s*([A-Za-z0-9_.,\- ()]+)", text)

    if block_matches:
        return [col.strip() for col in block_matches if col.strip()]

    return []


try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown('<div class="subtitle-style">Yüklenen Veri Seti</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

    if st.button("🔍 LLM ile Analizi Başlat"):
        with st.spinner("LLM analiz gerçekleştiriyor, lütfen bekleyin..."):
            sample_data = df.head(3).to_dict(orient="records")

            prompt = f"""
            
Below are sample records from a healthcare dataset.

Please perform the following steps on this dataset:

1. Identify which columns violate PII, HIPAA, GDPR, KVKK, and PCI DSS regulations. Evaluate and explain the reasons.

2. For columns that violate regulations:
   - For example, if Medical Condition is only considered risky due to its link with ID Number, then removing the ID Number makes it safe to keep the Medical Condition.

3. For each column removed, explain in detail which regulation(s) compliance has been achieved by its removal.

4. Finally, list the removed columns in the following format exactly as shown below (on a single line, comma-separated):

The following columns were removed: Column1, Column2, Column3

Our goal is to retain as much useful data as possible while ensuring full compliance with all relevant regulations.

Data will not be returned. Only mention which columns must be removed or masked.
Data:
{sample_data}
"""

            try:
                response = ollama.chat(model="llama3", messages=[
                    {"role": "user", "content": prompt}
                ])

                content = response['message']['content']
                st.success("✅ Analiz başarıyla tamamlandı")
                st.markdown("### 🧠 LLM Yanıtı")
                st.markdown(content)

                retained_cols = extract_columns_from_summary(content)
                if retained_cols:
                    st.markdown("### ❌ Kaldırılacak Sütunlar")
                    st.write(retained_cols)

                    # Tüm sütunları küçük harfle eşleyerek eşleştirme yap
                    df_cols_lower = {col.lower(): col for col in df.columns}
                    cols_to_remove = [df_cols_lower[c.lower()] for c in retained_cols if c.lower() in df_cols_lower]

                    # Bu sütunlar hariç tüm sütunları al
                    cols_to_keep = [col for col in df.columns if col not in cols_to_remove]
                    cleaned_df = df[cols_to_keep]

                    st.markdown("### 🚀 Temizlenmiş Veri Seti (Kaldırılanlar Hariç)")
                    st.dataframe(cleaned_df, use_container_width=True)

                    csv = cleaned_df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Temizlenmiş CSV'yi İndir", data=csv, file_name="temizlenmis_veri.csv", mime="text/csv")

                else:
                    st.info("📎 LLM çıktısında tutulacak sütunlar bulunamadı.")

            except Exception as e:
                st.error(f"Hata oluştu: {e}")

except FileNotFoundError:
    st.error(f"❌ 'dosya bulunamadı.")
