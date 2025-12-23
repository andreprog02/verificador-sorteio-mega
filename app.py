import streamlit as st
import re
import requests
import urllib3

# Desabilitar avisos de segurança para a API da Caixa
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# 🎨 CONFIGURAÇÃO VISUAL (MODERNO & CLEAN)
# ==============================================================================
st.set_page_config(
    page_title="Conferidor Mega da Virada 2025",
    page_icon="🍀",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# ... (logo abaixo de st.set_page_config)

# 🔒 REMOVER MENU E RODAPÉ PADRÃO
st.markdown("""
    <style>
        /* Esconde o menu de 3 pontinhos no canto superior direito */
        #MainMenu {visibility: hidden;}
        
        /* Esconde o rodapé padrão "Made with Streamlit" */
        footer {visibility: hidden;}
        
        /* Esconde o cabeçalho colorido */
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# CSS Personalizado para Cartões Bonitos
st.markdown("""
    <style>
    /* Estilo Geral */
    .main {
        background-color: #FFFFFF;
    }
    h1 {
        color: #1E3A8A; /* Azul Escuro Profissional */
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: 800;
    }
    
    /* Cartões de Resultado */
    .ticket-card {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Verdana', sans-serif;
        color: #333;
    }
    
    /* Cores Específicas para Prêmios */
    .sena-card {
        background: linear-gradient(135deg, #fff9c4 0%, #fff176 100%);
        border-left: 8px solid #FFD700;
    }
    .quina-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 8px solid #1976D2;
    }
    .quadra-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 8px solid #388E3C;
    }
    
    /* Tags e Textos */
    .local-tag {
        font-size: 0.85em;
        text-transform: uppercase;
        color: #555;
        font-weight: bold;
        margin-bottom: 5px;
        display: block;
    }
    .win-title {
        font-size: 1.2em;
        font-weight: bold;
        margin: 5px 0;
    }
    .numbers {
        background-color: rgba(255,255,255,0.6);
        padding: 5px 10px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    /* Rodapé */
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9em;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 📝 SEUS JOGOS (DADOS)
# ==============================================================================
MEUS_JOGOS = """
### 📄 IMAGEM 1: Aposta Combinada (10 Números)
A: 05 - 07 - 08 - 13 - 24 - 26 - 31 - 33 - 42 - 54
B: 02 - 09 - 10 - 12 - 17 - 19 - 27 - 51 - 57 - 60

### 📄 IMAGEM 2: Aposta Combinada (8 Números) - 5 Jogos
A: 18 - 21 - 27 - 29 - 37 - 50 - 54 - 60
B: 11 - 14 - 15 - 20 - 31 - 38 - 48 - 56
C: 13 - 14 - 22 - 25 - 47 - 50 - 57 - 59
D: 03 - 06 - 20 - 23 - 27 - 51 - 52 - 55
E: 04 - 12 - 15 - 22 - 28 - 31 - 34 - 52

### 📄 IMAGEM 3: Aposta Combinada (8 Números) - 10 Jogos
A: 08 - 10 - 26 - 35 - 41 - 44 - 50 - 51
B: 10 - 22 - 23 - 24 - 29 - 41 - 53 - 54
C: 04 - 16 - 25 - 31 - 36 - 37 - 40 - 57
D: 15 - 24 - 25 - 32 - 41 - 53 - 55 - 58
E: 06 - 09 - 16 - 23 - 30 - 36 - 50 - 55
F: 09 - 37 - 41 - 43 - 51 - 56 - 58 - 60
G: 05 - 16 - 18 - 20 - 26 - 35 - 52 - 53
H: 19 - 23 - 29 - 31 - 44 - 46 - 49 - 50
I: 02 - 15 - 16 - 22 - 35 - 36 - 38 - 49
J: 01 - 20 - 23 - 34 - 42 - 48 - 57 - 60

### 📄 IMAGEM 4: Aposta Combinada (8 Números) - 10 Jogos
A: 11 - 12 - 18 - 43 - 47 - 50 - 55 - 57
B: 03 - 28 - 36 - 44 - 48 - 54 - 55 - 58
C: 02 - 04 - 07 - 13 - 20 - 26 - 34 - 35
D: 10 - 19 - 26 - 28 - 30 - 32 - 39 - 40
E: 01 - 07 - 11 - 19 - 42 - 47 - 49 - 58
F: 06 - 09 - 16 - 25 - 26 - 31 - 53 - 58
G: 05 - 16 - 25 - 30 - 36 - 44 - 45 - 58
H: 07 - 19 - 34 - 41 - 43 - 47 - 51 - 56
I: 01 - 17 - 18 - 28 - 29 - 44 - 49 - 54
J: 07 - 23 - 24 - 27 - 29 - 45 - 49 - 57

### 📄 IMAGEM 5: Aposta Combinada (8 Números) - 10 Jogos
A: 02 - 06 - 07 - 17 - 33 - 47 - 54 - 60
B: 03 - 07 - 08 - 20 - 39 - 44 - 55 - 60
C: 30 - 43 - 46 - 48 - 52 - 54 - 56 - 59
D: 11 - 17 - 20 - 24 - 31 - 41 - 45 - 54
E: 09 - 37 - 41 - 47 - 50 - 56 - 57 - 60
F: 06 - 08 - 10 - 13 - 29 - 44 - 49 - 50
G: 07 - 23 - 32 - 34 - 35 - 46 - 49 - 57
H: 32 - 35 - 42 - 44 - 47 - 50 - 54 - 58
I: 06 - 12 - 21 - 22 - 24 - 39 - 44 - 52
J: 08 - 10 - 18 - 19 - 24 - 38 - 46 - 57

### 📄 IMAGEM 6: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
13 - 24 - 38 - 43 - 46 - 54
07 - 11 - 13 - 36 - 45 - 47
05 - 11 - 14 - 22 - 31 - 36
14 - 16 - 34 - 43 - 49 - 51
01 - 23 - 37 - 40 - 49 - 52
16 - 25 - 37 - 40 - 49 - 57
11 - 12 - 22 - 34 - 46 - 55
04 - 05 - 35 - 53 - 54 - 56
08 - 20 - 21 - 42 - 50 - 53
05 - 20 - 29 - 32 - 56 - 60

**Cupom 2 (Superior Meio):**
18 - 20 - 26 - 41 - 47 - 48
11 - 18 - 22 - 25 - 53 - 59
01 - 04 - 31 - 41 - 50 - 58
05 - 11 - 29 - 39 - 40 - 45
03 - 19 - 20 - 24 - 34 - 37
03 - 13 - 17 - 22 - 30 - 52
09 - 22 - 32 - 47 - 49 - 54
01 - 10 - 13 - 20 - 27 - 33
01 - 02 - 09 - 21 - 34 - 55
03 - 12 - 15 - 19 - 36 - 39

**Cupom 3 (Superior Dir):**
15 - 20 - 28 - 29 - 51 - 52
23 - 34 - 40 - 41 - 48 - 51
01 - 03 - 19 - 20 - 22 - 41
01 - 03 - 04 - 22 - 47 - 48
29 - 32 - 33 - 44 - 50 - 51
09 - 21 - 30 - 31 - 39 - 54
06 - 42 - 45 - 46 - 52 - 60
09 - 11 - 34 - 35 - 42 - 46
02 - 05 - 13 - 35 - 40 - 59
01 - 19 - 20 - 25 - 39 - 59

**Cupom 4 (Inferior Esq):**
19 - 25 - 36 - 39 - 51 - 59
10 - 13 - 25 - 50 - 51 - 60
02 - 04 - 06 - 15 - 47 - 52
01 - 13 - 17 - 19 - 40 - 49
03 - 12 - 39 - 43 - 48 - 56
04 - 19 - 23 - 35 - 49 - 58
18 - 26 - 32 - 38 - 46 - 59
04 - 16 - 47 - 51 - 54 - 60
04 - 06 - 08 - 13 - 21 - 37
12 - 18 - 25 - 26 - 33 - 39

**Cupom 5 (Inferior Meio):**
05 - 18 - 19 - 24 - 47 - 58
15 - 25 - 31 - 37 - 42 - 55
11 - 16 - 26 - 34 - 44 - 60
25 - 40 - 42 - 49 - 50 - 55
01 - 05 - 20 - 30 - 40 - 46
02 - 04 - 07 - 21 - 28 - 31
04 - 17 - 22 - 39 - 43 - 54
11 - 13 - 26 - 28 - 41 - 48
10 - 12 - 22 - 25 - 26 - 42
01 - 06 - 16 - 26 - 30 - 46

**Cupom 6 (Inferior Dir):**
03 - 10 - 21 - 30 - 49 - 56
02 - 08 - 09 - 13 - 15 - 26
13 - 17 - 31 - 43 - 50 - 58
01 - 02 - 18 - 23 - 54 - 58
14 - 16 - 17 - 30 - 35 - 36
05 - 07 - 15 - 21 - 42 - 48
08 - 18 - 22 - 24 - 36 - 55
10 - 12 - 30 - 47 - 49 - 53
10 - 14 - 23 - 41 - 50 - 51
11 - 26 - 33 - 37 - 38 - 50

### 📄 IMAGEM 7: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
02 - 21 - 23 - 38 - 41 - 55
10 - 13 - 25 - 31 - 39 - 54
06 - 15 - 17 - 25 - 28 - 49
12 - 16 - 20 - 21 - 32 - 41
08 - 13 - 18 - 36 - 37 - 44
10 - 12 - 30 - 44 - 55 - 60
05 - 16 - 21 - 49 - 55 - 59
02 - 12 - 21 - 39 - 43 - 57
04 - 18 - 25 - 31 - 34 - 44
04 - 09 - 20 - 29 - 46 - 50

**Cupom 2 (Superior Meio):**
22 - 24 - 25 - 34 - 36 - 59
03 - 09 - 44 - 47 - 50 - 53
11 - 18 - 20 - 24 - 26 - 57
06 - 22 - 25 - 31 - 41 - 53
11 - 19 - 24 - 38 - 43 - 58
02 - 05 - 11 - 20 - 28 - 46
05 - 07 - 09 - 23 - 46 - 55
13 - 15 - 16 - 18 - 32 - 42
26 - 43 - 47 - 49 - 55 - 56
03 - 11 - 21 - 34 - 40 - 53

**Cupom 3 (Superior Dir):**
18 - 26 - 27 - 42 - 49 - 57
10 - 23 - 25 - 49 - 52 - 55
01 - 07 - 22 - 29 - 38 - 47
17 - 32 - 46 - 49 - 54 - 55
09 - 15 - 16 - 38 - 44 - 53
02 - 14 - 19 - 31 - 44 - 49
09 - 10 - 25 - 36 - 44 - 57
03 - 04 - 05 - 11 - 28 - 29
17 - 27 - 30 - 38 - 42 - 44
05 - 10 - 24 - 31 - 34 - 54

**Cupom 4 (Inferior Esq):**
12 - 20 - 35 - 40 - 47 - 56
19 - 23 - 24 - 43 - 45 - 51
03 - 09 - 31 - 42 - 50 - 54
14 - 22 - 24 - 32 - 36 - 58
02 - 04 - 21 - 27 - 30 - 56
11 - 34 - 38 - 43 - 48 - 52
12 - 25 - 29 - 33 - 53 - 59
01 - 05 - 15 - 34 - 52 - 56
14 - 15 - 22 - 35 - 43 - 48
02 - 05 - 19 - 21 - 31 - 48

**Cupom 5 (Inferior Meio):**
07 - 22 - 38 - 40 - 50 - 53
11 - 30 - 32 - 42 - 44 - 56
05 - 10 - 33 - 42 - 50 - 58
04 - 08 - 17 - 45 - 46 - 49
05 - 08 - 09 - 21 - 27 - 52
14 - 17 - 26 - 44 - 50 - 57
06 - 12 - 26 - 37 - 39 - 42
08 - 25 - 32 - 36 - 55 - 56
02 - 09 - 30 - 40 - 53 - 55
06 - 08 - 10 - 34 - 37 - 42

**Cupom 6 (Inferior Dir):**
02 - 09 - 11 - 30 - 34 - 35
02 - 12 - 13 - 17 - 45 - 57
04 - 08 - 28 - 31 - 48 - 54
09 - 14 - 25 - 42 - 46 - 60
28 - 52 - 55 - 58 - 59 - 60
02 - 15 - 17 - 23 - 50 - 54
07 - 17 - 19 - 24 - 36 - 41
12 - 20 - 31 - 36 - 38 - 51
14 - 16 - 33 - 35 - 44 - 51
01 - 12 - 22 - 33 - 40 - 54

### 📄 IMAGEM 8: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
03 - 09 - 18 - 34 - 46 - 50
07 - 15 - 35 - 40 - 51 - 57
03 - 26 - 34 - 35 - 40 - 43
08 - 12 - 33 - 34 - 43 - 55
10 - 26 - 27 - 32 - 42 - 50
10 - 23 - 24 - 28 - 39 - 56
08 - 27 - 28 - 30 - 40 - 41
05 - 09 - 11 - 20 - 38 - 55
04 - 07 - 28 - 35 - 41 - 52
10 - 24 - 45 - 48 - 54 - 57

**Cupom 2 (Superior Meio):**
16 - 19 - 21 - 25 - 26 - 60
04 - 14 - 19 - 33 - 39 - 48
06 - 30 - 39 - 47 - 48 - 55
01 - 21 - 23 - 36 - 41 - 56
03 - 15 - 27 - 31 - 36 - 58
03 - 05 - 24 - 33 - 34 - 51
03 - 07 - 20 - 22 - 39 - 47
15 - 20 - 26 - 36 - 37 - 54
08 - 12 - 20 - 25 - 46 - 56
05 - 17 - 24 - 32 - 41 - 55

**Cupom 3 (Superior Dir):**
18 - 21 - 28 - 33 - 42 - 59
02 - 17 - 35 - 36 - 41 - 49
03 - 17 - 22 - 30 - 33 - 59
02 - 13 - 17 - 30 - 40 - 42
02 - 13 - 21 - 46 - 51 - 57
15 - 25 - 37 - 45 - 46 - 47
06 - 10 - 21 - 43 - 48 - 49
02 - 18 - 27 - 50 - 53 - 54
15 - 21 - 26 - 44 - 46 - 49
01 - 06 - 14 - 27 - 34 - 58

**Cupom 4 (Inferior Esq):**
04 - 17 - 32 - 36 - 51 - 53
23 - 29 - 30 - 39 - 51 - 53
14 - 29 - 40 - 52 - 59 - 60
01 - 05 - 29 - 33 - 49 - 60
14 - 19 - 20 - 41 - 42 - 50
03 - 06 - 10 - 20 - 21 - 25
06 - 08 - 15 - 33 - 55 - 58
06 - 17 - 28 - 31 - 42 - 50
06 - 07 - 09 - 18 - 23 - 24
11 - 27 - 37 - 42 - 45 - 58

**Cupom 5 (Inferior Meio):**
01 - 10 - 22 - 36 - 40 - 58
10 - 20 - 27 - 30 - 43 - 51
02 - 18 - 26 - 33 - 52 - 58
06 - 16 - 39 - 43 - 51 - 54
09 - 11 - 16 - 20 - 45 - 56
02 - 15 - 31 - 35 - 40 - 51
36 - 40 - 45 - 46 - 47 - 54
22 - 26 - 43 - 47 - 48 - 56
04 - 10 - 18 - 22 - 49 - 56
14 - 42 - 44 - 46 - 48 - 56

**Cupom 6 (Inferior Dir):**
03 - 26 - 32 - 35 - 43 - 49
05 - 26 - 27 - 31 - 32 - 57
14 - 33 - 41 - 48 - 49 - 50
01 - 06 - 08 - 33 - 49 - 50
01 - 22 - 28 - 33 - 38 - 45
02 - 05 - 20 - 31 - 45 - 52
08 - 29 - 41 - 42 - 46 - 50
10 - 12 - 21 - 42 - 50 - 52
03 - 10 - 13 - 34 - 47 - 49
09 - 11 - 13 - 14 - 24 - 44

### 📄 IMAGEM 9: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
02 - 26 - 28 - 31 - 34 - 60
12 - 20 - 26 - 37 - 41 - 53
42 - 45 - 47 - 50 - 55 - 60
23 - 27 - 37 - 49 - 51 - 55
19 - 31 - 36 - 48 - 54 - 55
22 - 27 - 33 - 43 - 46 - 51
01 - 03 - 05 - 07 - 08 - 60
04 - 15 - 24 - 35 - 40 - 49
01 - 26 - 35 - 41 - 42 - 51
06 - 10 - 15 - 23 - 26 - 31

**Cupom 2 (Superior Meio):**
02 - 14 - 20 - 30 - 33 - 59
16 - 22 - 31 - 37 - 44 - 53
09 - 11 - 38 - 41 - 47 - 48
08 - 09 - 18 - 25 - 46 - 52
02 - 05 - 27 - 28 - 45 - 48
11 - 12 - 14 - 21 - 29 - 31
01 - 02 - 16 - 21 - 24 - 55
32 - 43 - 50 - 56 - 58 - 60
09 - 10 - 16 - 26 - 27 - 52
10 - 11 - 17 - 33 - 39 - 57

**Cupom 3 (Superior Dir):**
10 - 24 - 34 - 36 - 37 - 39
26 - 41 - 45 - 50 - 56 - 58
11 - 24 - 28 - 30 - 37 - 56
08 - 29 - 40 - 47 - 54 - 58
20 - 26 - 32 - 34 - 42 - 51
04 - 10 - 16 - 27 - 35 - 54
07 - 10 - 20 - 42 - 49 - 59
02 - 11 - 14 - 20 - 23 - 35
02 - 13 - 22 - 34 - 40 - 50
13 - 24 - 29 - 30 - 41 - 48

**Cupom 4 (Inferior Esq):**
11 - 12 - 21 - 24 - 43 - 47
03 - 10 - 15 - 19 - 31 - 40
12 - 24 - 32 - 38 - 41 - 43
08 - 10 - 12 - 16 - 20 - 53
02 - 03 - 10 - 22 - 28 - 36
01 - 19 - 22 - 27 - 42 - 53
17 - 18 - 19 - 24 - 36 - 52
12 - 18 - 21 - 38 - 47 - 60
02 - 15 - 29 - 35 - 41 - 49
01 - 02 - 10 - 26 - 32 - 44

**Cupom 5 (Inferior Meio):**
01 - 28 - 38 - 42 - 43 - 45
05 - 08 - 22 - 25 - 37 - 41
07 - 08 - 44 - 49 - 55 - 56
15 - 17 - 23 - 38 - 39 - 47
08 - 17 - 28 - 34 - 40 - 58
02 - 18 - 20 - 22 - 32 - 40
22 - 27 - 30 - 35 - 50 - 52
04 - 36 - 40 - 41 - 42 - 46
21 - 25 - 26 - 34 - 37 - 38
18 - 19 - 34 - 35 - 40 - 47

**Cupom 6 (Inferior Dir):**
25 - 36 - 43 - 45 - 52 - 57
14 - 21 - 26 - 27 - 28 - 37
30 - 35 - 43 - 48 - 52 - 54
11 - 27 - 32 - 38 - 42 - 45
09 - 18 - 20 - 27 - 30 - 33
07 - 13 - 27 - 51 - 52 - 59
04 - 30 - 31 - 40 - 45 - 46
09 - 46 - 49 - 50 - 53 - 58
05 - 15 - 18 - 37 - 55 - 60
17 - 23 - 26 - 37 - 45 - 47

### 📄 IMAGEM 10: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
23 - 29 - 43 - 49 - 53 - 55
06 - 13 - 24 - 30 - 42 - 59
02 - 13 - 21 - 29 - 34 - 59
06 - 08 - 12 - 15 - 16 - 29
09 - 18 - 21 - 25 - 34 - 41
07 - 11 - 13 - 29 - 39 - 57
05 - 11 - 26 - 40 - 43 - 54
03 - 08 - 25 - 33 - 43 - 50
01 - 16 - 26 - 28 - 35 - 49
23 - 38 - 42 - 43 - 44 - 51

**Cupom 2 (Superior Meio):**
06 - 21 - 29 - 30 - 33 - 44
04 - 09 - 22 - 23 - 48 - 49
05 - 09 - 24 - 28 - 32 - 33
14 - 32 - 42 - 52 - 54 - 57
15 - 26 - 30 - 31 - 32 - 52
17 - 22 - 25 - 31 - 32 - 58
07 - 20 - 25 - 39 - 42 - 51
03 - 13 - 21 - 44 - 46 - 59
01 - 28 - 31 - 44 - 49 - 53
11 - 13 - 14 - 24 - 33 - 38

**Cupom 3 (Superior Dir):**
21 - 32 - 33 - 36 - 39 - 51
04 - 17 - 18 - 27 - 33 - 45
01 - 03 - 21 - 38 - 56 - 58
13 - 16 - 18 - 23 - 29 - 53
17 - 26 - 28 - 43 - 50 - 55
07 - 13 - 15 - 39 - 41 - 48
03 - 05 - 10 - 13 - 15 - 60
02 - 07 - 22 - 34 - 37 - 43
15 - 19 - 20 - 40 - 48 - 60
04 - 05 - 14 - 23 - 36 - 43

**Cupom 4 (Inferior Esq):**
22 - 24 - 30 - 52 - 56 - 60
09 - 10 - 19 - 26 - 53 - 55
10 - 14 - 16 - 41 - 57 - 59
13 - 31 - 41 - 53 - 55 - 60
05 - 11 - 27 - 32 - 33 - 56
22 - 27 - 30 - 39 - 53 - 55
09 - 11 - 26 - 35 - 36 - 57
02 - 10 - 19 - 35 - 51 - 55
24 - 29 - 30 - 33 - 40 - 50
19 - 31 - 43 - 50 - 52 - 53

**Cupom 5 (Inferior Meio):**
04 - 25 - 30 - 38 - 43 - 47
06 - 09 - 14 - 26 - 57 - 60
10 - 11 - 17 - 23 - 28 - 60
03 - 04 - 17 - 27 - 34 - 42
01 - 18 - 21 - 38 - 56 - 60
04 - 08 - 22 - 24 - 35 - 47
12 - 30 - 31 - 37 - 43 - 44
07 - 14 - 15 - 19 - 20 - 42
03 - 07 - 20 - 34 - 40 - 54
10 - 18 - 23 - 26 - 35 - 43

**Cupom 6 (Inferior Dir):**
06 - 27 - 34 - 40 - 48 - 53
14 - 24 - 39 - 41 - 44 - 49
02 - 20 - 25 - 32 - 43 - 52
04 - 17 - 34 - 35 - 54 - 60
14 - 16 - 35 - 37 - 40 - 52
01 - 09 - 29 - 32 - 37 - 44
06 - 11 - 20 - 24 - 31 - 53
11 - 17 - 35 - 39 - 48 - 57
05 - 07 - 16 - 20 - 21 - 53
03 - 18 - 23 - 53 - 54 - 59

### 📄 IMAGEM 11: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
02 - 03 - 10 - 26 - 38 - 44
04 - 11 - 30 - 40 - 55 - 58
10 - 11 - 17 - 19 - 30 - 32
19 - 37 - 38 - 40 - 53 - 55
27 - 28 - 36 - 46 - 50 - 58
02 - 03 - 11 - 18 - 24 - 29
04 - 28 - 29 - 45 - 57 - 59
03 - 12 - 16 - 23 - 25 - 57
09 - 24 - 27 - 28 - 39 - 48
04 - 12 - 31 - 35 - 43 - 58

**Cupom 2 (Superior Meio):**
06 - 13 - 14 - 39 - 49 - 56
17 - 25 - 38 - 50 - 53 - 55
12 - 15 - 19 - 32 - 34 - 56
04 - 08 - 09 - 39 - 41 - 52
01 - 07 - 31 - 35 - 37 - 47
06 - 10 - 37 - 49 - 54 - 58
01 - 11 - 16 - 49 - 53 - 56
11 - 22 - 41 - 42 - 46 - 53
24 - 36 - 39 - 51 - 58 - 59
12 - 33 - 39 - 46 - 47 - 52

**Cupom 3 (Superior Dir):**
03 - 10 - 11 - 26 - 31 - 47
16 - 20 - 21 - 24 - 27 - 37
19 - 32 - 44 - 55 - 57 - 60
01 - 02 - 18 - 22 - 43 - 46
05 - 12 - 19 - 21 - 25 - 43
31 - 39 - 40 - 51 - 52 - 58
01 - 11 - 24 - 33 - 52 - 59
06 - 09 - 13 - 35 - 37 - 46
18 - 30 - 39 - 43 - 50 - 51
06 - 09 - 16 - 21 - 32 - 56

**Cupom 4 (Inferior Esq):**
06 - 12 - 18 - 26 - 28 - 34
12 - 14 - 27 - 32 - 43 - 54
07 - 16 - 21 - 28 - 41 - 47
09 - 14 - 18 - 29 - 36 - 54
13 - 25 - 35 - 43 - 46 - 48
27 - 33 - 46 - 50 - 54 - 55
07 - 15 - 17 - 18 - 42 - 47
30 - 34 - 35 - 37 - 39 - 42
03 - 14 - 32 - 34 - 45 - 48
02 - 09 - 17 - 26 - 48 - 54

**Cupom 5 (Inferior Meio):**
29 - 37 - 39 - 50 - 51 - 58
05 - 07 - 08 - 13 - 18 - 19
34 - 35 - 37 - 45 - 49 - 50
11 - 13 - 19 - 38 - 40 - 55
06 - 11 - 17 - 35 - 46 - 48
01 - 04 - 11 - 24 - 37 - 44
13 - 33 - 36 - 46 - 54 - 56
01 - 05 - 08 - 28 - 39 - 41
06 - 14 - 22 - 30 - 35 - 37
03 - 18 - 31 - 34 - 42 - 45

**Cupom 6 (Inferior Dir):**
09 - 19 - 39 - 40 - 43 - 53
06 - 13 - 37 - 48 - 50 - 55
02 - 12 - 28 - 37 - 51 - 56
08 - 13 - 31 - 41 - 49 - 54
05 - 26 - 27 - 33 - 34 - 36
08 - 17 - 31 - 45 - 55 - 57
04 - 24 - 43 - 44 - 56 - 59
02 - 08 - 11 - 14 - 46 - 54
10 - 14 - 34 - 37 - 39 - 40
13 - 15 - 31 - 39 - 43 - 44

### 📄 IMAGEM 12: 6 Cupons de Apostas Simples
**Cupom 1 (Superior Esq):**
04 - 24 - 35 - 41 - 52 - 59
06 - 29 - 32 - 48 - 55 - 59
05 - 06 - 14 - 24 - 29 - 42
03 - 24 - 29 - 30 - 46 - 50
15 - 24 - 41 - 56 - 58 - 60
02 - 18 - 21 - 31 - 37 - 58
05 - 26 - 35 - 37 - 58 - 60
05 - 06 - 23 - 28 - 41 - 47
06 - 14 - 29 - 41 - 50 - 53
11 - 24 - 30 - 33 - 36 - 57

**Cupom 2 (Superior Meio):**
05 - 20 - 22 - 31 - 32 - 60
06 - 09 - 16 - 22 - 37 - 56
08 - 15 - 17 - 32 - 39 - 42
02 - 04 - 07 - 13 - 25 - 35
05 - 10 - 21 - 22 - 27 - 50
12 - 13 - 20 - 28 - 42 - 59
04 - 10 - 15 - 18 - 33 - 60
14 - 24 - 25 - 30 - 41 - 56
04 - 10 - 24 - 31 - 50 - 56
05 - 08 - 34 - 38 - 43 - 51

**Cupom 3 (Superior Dir):**
03 - 09 - 23 - 30 - 38 - 56
24 - 31 - 38 - 39 - 49 - 57
07 - 26 - 29 - 33 - 41 - 48
05 - 13 - 29 - 39 - 55 - 57
06 - 07 - 11 - 15 - 23 - 51
06 - 07 - 21 - 36 - 37 - 56
05 - 11 - 24 - 37 - 54 - 56
01 - 13 - 17 - 37 - 53 - 55
27 - 37 - 46 - 47 - 49 - 60
06 - 11 - 28 - 40 - 50 - 59

**Cupom 4 (Inferior Esq):**
13 - 19 - 20 - 21 - 44 - 50
11 - 24 - 25 - 34 - 50 - 59
04 - 10 - 12 - 23 - 37 - 50
15 - 30 - 35 - 36 - 40 - 53
14 - 15 - 32 - 34 - 39 - 48
07 - 28 - 29 - 33 - 45 - 56
06 - 15 - 27 - 30 - 54 - 55
08 - 12 - 28 - 42 - 48 - 55
06 - 17 - 19 - 29 - 45 - 50
04 - 07 - 23 - 32 - 45 - 46

**Cupom 5 (Inferior Meio):**
03 - 13 - 16 - 27 - 36 - 57
11 - 16 - 21 - 28 - 42 - 50
09 - 13 - 26 - 34 - 35 - 45
10 - 12 - 27 - 33 - 42 - 60
01 - 11 - 13 - 26 - 29 - 50
03 - 19 - 24 - 30 - 39 - 51
10 - 13 - 25 - 28 - 42 - 51
19 - 43 - 50 - 53 - 55 - 56
14 - 15 - 24 - 26 - 28 - 36
09 - 18 - 19 - 24 - 31 - 48

**Cupom 6 (Inferior Dir):**
01 - 13 - 25 - 29 - 30 - 54
09 - 24 - 48 - 54 - 55 - 56
10 - 34 - 43 - 50 - 53 - 58
17 - 21 - 25 - 44 - 47 - 55
02 - 11 - 15 - 25 - 27 - 54
30 - 31 - 34 - 47 - 49 - 55
12 - 19 - 24 - 27 - 52 - 58
06 - 25 - 32 - 33 - 51 - 53
01 - 15 - 22 - 40 - 49 - 55
11 - 20 - 24 - 31 - 45 - 53

### 📄 IMAGEM 13: 5 Jogos Simples (6 Números)
A: 06 - 31 - 51 - 56 - 59 - 60
B: 14 - 17 - 24 - 28 - 54 - 57
C: 04 - 21 - 23 - 38 - 39 - 43
D: 05 - 14 - 21 - 33 - 36 - 55
E: 04 - 20 - 31 - 41 - 51 - 52
"""

# ==============================================================================
# ⚙️ FUNÇÕES DO BACKEND (LÓGICA)
# ==============================================================================

def buscar_resultado_api(concurso):
    url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/{concurso}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            lista_dezenas = dados.get('listaDezenas')
            if not lista_dezenas: return None
            return set(map(int, lista_dezenas))
        return None
    except:
        return None

def processar_jogos(texto_jogos):
    padrao_aposta = re.compile(r"([A-J0-9]+)?[:\s]*((?:\d{2}\s*-\s*)+\d{2})")
    apostas_processadas = []
    imagem_atual = "Geral"
    contador_simples = 1

    for linha in texto_jogos.split('\n'):
        linha = linha.strip()
        if not linha: continue
        
        # Identifica cabeçalhos de imagem
        if "IMAGEM" in linha or "Cupom" in linha:
            imagem_atual = linha.replace('#', '').replace('*', '').strip()
            contador_simples = 1
            continue

        match = padrao_aposta.search(linha)
        if match:
            # Captura ID (Letra) ou gera um número
            identificador = match.group(1)
            if not identificador:
                identificador = f"Jogo {contador_simples}"
                contador_simples += 1
            else:
                identificador = identificador.replace(':', '')

            numeros_str = match.group(2).replace('-', ' ').split()
            numeros_int = set(map(int, numeros_str))
            
            apostas_processadas.append({
                'id': identificador,
                'nums': numeros_int,
                'local': imagem_atual
            })
            
    return apostas_processadas

# ==============================================================================
# 🚀 FRONTEND (STREAMLIT)
# ==============================================================================

st.title("🍀 Conferidor Mega da Virada")
st.markdown("---")

# Input do Concurso
col1, col2 = st.columns([3, 1])
with col1:
    concurso_input = st.text_input("Número do Concurso", value="2955")
with col2:
    st.write("") # Espaçamento
    btn_conferir = st.button("CONFERIR AGORA", type="primary")

if btn_conferir:
    with st.spinner(f"Buscando resultado do concurso {concurso_input}..."):
        # 1. Busca Resultado
        resultado = buscar_resultado_api(concurso_input)
        
        # Se falhar na API, permite teste manual (mock) ou avisa erro
        if not resultado:
            st.error("Não foi possível obter o resultado oficial ainda (ou erro de conexão).")
            st.info("DICA: Se for um teste, digite o concurso 2700 para ver funcionando.")
        else:
            # Mostra as bolas sorteadas
            st.balloons()
            st.success(f"🔢 DEZENAS SORTEADAS: {', '.join(map(str, sorted(resultado)))}")
            
            # 2. Processa Apostas
            apostas = processar_jogos(MEUS_JOGOS)
            premios = {'Sena': [], 'Quina': [], 'Quadra': []}
            
            # 3. Confere
            for aposta in apostas:
                acertos = aposta['nums'].intersection(resultado)
                qtd = len(acertos)
                
                detalhe = {
                    'local': aposta['local'],
                    'id': aposta['id'],
                    'acertos': sorted(acertos),
                    'numeros_full': sorted(aposta['nums'])
                }
                
                if qtd == 4: premios['Quadra'].append(detalhe)
                elif qtd == 5: premios['Quina'].append(detalhe)
                elif qtd >= 6: premios['Sena'].append(detalhe)

            # 4. Exibe Resultados
            total_premios = len(premios['Sena']) + len(premios['Quina']) + len(premios['Quadra'])
            
            if total_premios == 0:
                st.warning("😢 Nenhum prêmio encontrado nestes bilhetes.")
            else:
                # Sena
                if premios['Sena']:
                    st.markdown("### 🏆 SENA (6 Acertos)")
                    for p in premios['Sena']:
                        st.markdown(f"""
                        <div class="ticket-card sena-card">
                            <span class="local-tag">📍 {p['local']}</span>
                            <div class="win-title">BILHETE {p['id']} - GANHADOR DA SENA!</div>
                            <div>Seus Números: <span class="numbers">{', '.join(map(str, p['numeros_full']))}</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Quina
                if premios['Quina']:
                    st.markdown("### 💰 QUINA (5 Acertos)")
                    for p in premios['Quina']:
                        st.markdown(f"""
                        <div class="ticket-card quina-card">
                            <span class="local-tag">📍 {p['local']}</span>
                            <div class="win-title">Bilhete {p['id']}</div>
                            <div>Acertou: <span class="numbers">{', '.join(map(str, p['acertos']))}</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                # Quadra
                if premios['Quadra']:
                    st.markdown("### 👍 QUADRA (4 Acertos)")
                    for p in premios['Quadra']:
                        st.markdown(f"""
                        <div class="ticket-card quadra-card">
                            <span class="local-tag">📍 {p['local']}</span>
                            <div class="win-title">Bilhete {p['id']}</div>
                            <div>Acertou: <span class="numbers">{', '.join(map(str, p['acertos']))}</span></div>
                        </div>
                        """, unsafe_allow_html=True)

# Rodapé com Créditos

st.markdown("<div class='footer'>Desenvolvido por <b>André Santos</b> © 2025</div>", unsafe_allow_html=True)
