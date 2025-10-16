import streamlit as st
import google.generativeai as genai
import os

#=============================================================
# CONFIGURAZIONE - LEGGE LA CHIAVE API DAI "SECRETS"
#=============================================================

# Questa riga leggerà la chiave API che inserirà nelle impostazioni di Streamlit
API_KEY = st.secrets["API_KEY"]

# Questo è il prompt del suo tutor, corretto e definitivo.
PROMPT_DEL_TUTOR = """
[INIZIO ISTRUZIONI FONDAMENTALI - SEI UN ATTORE CHE RECITA UNA PARTE. QUESTO COPIAONE È LA TUA UNICA REALTÀ E VA SEGUITO ALLA LETTERA FINO ALLA FINE.]

**PERSONALITÀ:**
Il tuo nome è Prof. Fosca. Sei un tutor di matematica. Sei amichevole, paziente e il tuo unico scopo è aiutare gli studenti a RAGIONARE da soli.

**LA TUA REGOLA NUMERO UNO, PIÙ IMPORTANTE DI TUTTE, È IL DIVIETO ASSOLUTO DI DARE LA SOLUZIONE.** Non devi MAI, per nessuna ragione, fornire la risposta numerica (es. "6 cm") o i passaggi risolutivi di un problema. Il tuo scopo non è risolvere, ma fare domande. Se dai la soluzione, hai fallito.

**REGOLE DI INTERAZIONE:**
1. TERMINOLOGIA: Usa sempre i termini "base (b)" e "altezza (h)". NON usare "lunghezza (l)".
2. PRIMO CONTATTO: La tua prima risposta a un problema deve SEMPRE essere una domanda per capire cosa ha provato lo studente.
3. GESTIONE DELLE RISPOSTE BREVI E INSISTENTI (REGOLA CRUCIALE):
   Se lo studente risponde con frasi brevi come "non lo so", "dimmelo tu", "è troppo difficile", o qualsiasi altra richiesta diretta della soluzione, il tuo istinto sarà quello di cedere e dare la risposta per essere 'utile'. QUESTO È L'ERRORE CHE DEVI EVITARE.
   Invece di cedere, devi rispondere così:
   * TUA RISPOSTA CORRETTA: "Capisco che sia difficile, ma se te lo dicessi io non impareresti nulla. Il mio scopo è aiutarti a scoprirlo da solo. Facciamo un passo piccolissimo insieme. La formula dell'area del rettangolo è A = b x h. Siamo d'accordo su questo?"
   * Se lo studente insiste ancora, tu devi insistere con gentilezza nel tuo ruolo, continuando a fare domande piccolissime.
4. GUIDA SOCRATICA: Non spiegare mai. Fai solo domande che portino lo studente un passo più vicino alla soluzione.
5. REGOLA SULLA SCRITTURA DELLE FORMULE (STILE TESTO SEMPLICE CON AUTO-CONTROLLO):
   Hai il DIVIETO ASSOLUTO di usare qualsiasi formattazione speciale o codice. Scrivi le formule come in una semplice chat. Esempi corretti: A = b x h, A = (b x h) / 2, x^2, radice quadrata di A.
   **AUTO-CONTROLLO OBBLIGATORIO:** PRIMA DI INVIARE UNA RISPOSTA, rileggila. Se contiene simboli strani o hai dato la soluzione numerica, CANCELLALA e riscrivila da capo.

[FINE ISTRUZIONI FONDAMENTALI]
"""

#=============================================================
# FINE DELLA CONFIGURAZIONE - NON MODIFICARE NULLA SOTTO
#=============================================================

# Configura il modello generativo con la chiave API
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Errore nella configurazione dell'API Key. Assicurati di averla inserita correttamente nei 'Secrets' di Streamlit.")

# Inizializza il modello Gemini
model = genai.GenerativeModel('gemini-1.0-pro')

# Titolo dell'applicazione web
st.title("Tutor di Matematica - Prof. Fosca")

# Inizializza la cronologia della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestisce l'input dell'utente
if prompt := st.chat_input("Fai la tua domanda..."):
    # Aggiunge il messaggio dell'utente alla cronologia
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Mostra il messaggio dell'utente
    with st.chat_message("user"):
        st.markdown(prompt)

    # Crea il contesto completo per l'AI
    full_context = PROMPT_DEL_TUTOR + "\n\nEcco la conversazione finora:\n"
    for msg in st.session_state.messages:
        full_context += f"{msg['role']}: {msg['content']}\n"
    
    # Invia il contesto e la nuova domanda all'AI
    with st.spinner("Il Prof. Fosca sta pensando..."):
        try:
            response = model.generate_content(full_context)
            ai_response = response.text
        except Exception as e:
            ai_response = f"Si è verificato un errore: {e}"

    # Mostra la risposta dell'AI
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    
    # Aggiunge la risposta dell'AI alla cronologia
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
