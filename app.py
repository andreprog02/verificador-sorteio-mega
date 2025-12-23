import streamlit as st
import re
import requests
import urllib3

# Desabilitar avisos de segurança
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# 🎨 CONFIGURAÇÃO VISUAL
# ==============================================================================
st.set_page_config(
    page_title="Verificador Mega da Virada 2025",
    page_icon="🍀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS: Remove Menus, Limpa Inputs e Estiliza Cartões
st.markdown("""
    <style>
    /* 1. Esconde menus do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. Estilo dos Inputs Manuais (Visual Limpo) */
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E3A8A;
    }

    /* 3. Estilo dos Cartões de Resultado */
    .ticket-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-family: sans-serif;
        background-color: white;
        color: #333;
    }
    .sena-card { border-left: 8px solid #FFD700; background-color: #FFFDE7; }
    .quina-card { border-left: 8px solid #1976D2; background-color: #E3F2FD; }
    .quadra-card { border-left: 8px solid #388E3C; background-color: #E8F5E9; }
    
    .local-tag { font-size: 0.8em; font-weight: bold; color: #666; display: block; margin-bottom: 5px; }
    .win-title { font-size: 1.1em; font-weight: bold; }
    .numbers { font-family: monospace; font-weight: bold; background: #eee; padding: 2px 6px; border-radius: 4px; }
    
    .footer { margin-top: 50px; text-align: center; font-size: 0.8em; color: #888; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 📝 SEUS JOGOS (DADOS)
# ==============================================================================
MEUS_JOGOS = """
1. Cupom: A2D1-8F0063033192AA80B8-2

A: 13 24 38 43 46 54

B: 07 11 13 36 45 47

C: 05 11 14 22 31 36

D: 14 16 34 43 49 51

E: 01 23 37 40 49 52

F: 16 25 37 40 49 57

G: 11 12 22 34 46 55

H: 04 05 35 53 54 56

I: 08 20 21 42 50 53

J: 05 20 29 32 56 60

2. Cupom: A2D1-5A886E0218EA37ABA3-8

A: 18 20 26 41 47 48

B: 11 18 22 25 53 59

C: 01 04 31 41 50 58

D: 05 11 29 39 40 45

E: 03 19 20 24 34 37

F: 03 13 17 22 30 52

G: 09 22 32 47 49 54

H: 01 10 13 20 27 33

I: 01 02 09 21 34 55

J: 03 12 15 19 36 39

3. Cupom: A2D1-16106CDC5D5F5C16EC-4

A: 15 20 28 29 51 52

B: 23 34 40 41 48 51

C: 01 03 19 20 22 41

D: 01 03 04 22 47 48

E: 29 32 33 44 50 51

F: 09 21 30 31 39 54

G: 06 42 45 46 52 60

H: 09 11 34 35 42 46

I: 02 05 13 35 40 59

J: 01 19 20 25 39 59

4. Cupom: A2D1-C2303688E52E36FAD5-4

A: 19 25 36 39 51 59

B: 10 13 25 50 51 60

C: 02 04 06 15 47 52

D: 01 13 17 19 40 49

E: 03 12 39 43 48 56

F: 04 19 23 35 49 58

G: 18 26 32 38 46 59

H: 04 16 47 51 54 60

I: 04 06 08 13 21 37

J: 12 18 25 26 33 39

5. Cupom: A2D1-38506E03C4836D6E54-8

A: 05 18 19 24 47 58

B: 15 25 31 37 42 55

C: 11 16 26 34 44 60

D: 25 40 42 49 50 55

E: 01 05 20 30 40 46

F: 02 04 07 21 28 31

G: 04 17 22 39 43 54

H: 11 13 26 28 41 48

I: 10 12 22 25 26 42

J: 01 06 16 26 30 46

6. Cupom: A2D1-38E0600D2FD25857CF-6

A: 03 10 21 30 49 56

B: 02 08 09 13 15 26

C: 13 17 31 43 50 58

D: 01 02 18 23 54 58

E: 14 16 17 30 35 36

F: 05 07 15 21 42 48

G: 08 18 22 24 36 55

H: 10 12 30 47 49 53

I: 10 14 23 41 50 51

J: 11 26 33 37 38 50

7. Cupom: A2D1-CCF065FC9A38AF13EE-8

A: 11 12 18 43 47 50 55 57

B: 03 28 36 44 48 54 55 58

C: 02 04 07 13 20 26 34 35

D: 10 19 26 28 30 32 39 40

E: 01 07 11 19 42 47 49 58

F: 06 09 16 25 26 31 53 58

G: 05 16 25 30 36 44 45 58

H: 07 19 34 41 43 47 51 56

I: 01 17 18 28 29 44 49 54

J: 07 23 24 27 29 45 49 57


8. Cupom: A2D1-35AB64634DEEE48ECE-7

A: 02 26 28 31 34 60

B: 12 20 26 37 41 53

C: 42 45 47 50 55 60

D: 23 27 37 49 51 55

E: 19 31 36 48 54 55

F: 22 27 33 43 46 51

G: 01 03 05 07 08 50

H: 04 15 24 35 40 49

I: 01 26 35 41 42 51

J: 06 10 15 23 26 31

9. Cupom: A2D1-ACF089D1F63DC57776-8

A: 02 14 20 30 33 59

B: 16 22 31 37 44 53

C: 09 11 38 41 47 48

D: 08 09 18 25 46 52

E: 02 05 27 28 45 48

F: 11 12 14 21 29 31

G: 01 02 16 21 24 55

H: 32 43 50 56 58 60

I: 09 10 16 26 27 52

J: 10 11 17 33 39 57

10. Cupom: A2D1-38F0652E6E3E28DF28-4

A: 10 24 34 36 37 39

B: 26 41 45 50 56 58

C: 11 24 28 30 37 56

D: 08 29 40 47 54 58

E: 20 26 32 34 42 51

F: 04 10 16 27 35 54

G: 07 10 20 42 49 59

H: 02 11 14 20 23 35

I: 02 13 22 34 40 50

J: 13 24 29 30 41 48

11. Cupom: A2D1-F89865C0972FAE93CD-0

A: 11 12 21 24 43 47

B: 03 10 15 19 31 40

C: 12 24 32 38 41 43

D: 08 10 12 16 20 53

E: 02 03 10 22 28 36

F: 01 19 22 27 42 53

G: 17 18 19 24 36 52

H: 12 18 21 38 47 50

I: 02 15 29 35 41 49

J: 01 02 10 26 32 44

12. Cupom: A2D1-B7F86F015FE99AADA7-6

A: 01 28 38 42 43 45

B: 05 08 22 25 37 41

C: 07 08 44 49 55 56

D: 15 17 23 38 39 47

E: 08 17 28 34 40 58

F: 02 18 20 22 32 40

G: 22 27 30 35 50 52

H: 04 36 40 41 42 46

I: 21 25 26 34 37 38

J: 18 19 34 35 40 47

13. Cupom: A2D1-34906AE8933E38DD79-2

A: 25 36 43 45 52 57

B: 14 21 26 27 28 37

C: 30 35 43 48 52 54

D: 11 27 32 38 42 45

E: 09 18 20 27 30 33

F: 07 13 27 51 52 59

G: 04 30 31 40 45 46

H: 09 46 49 50 53 58

I: 05 15 18 37 55 60

J: 17 23 26 37 45 47


14. Cupom: A2D1-1EE06462062430B5C0-9

A: 02 03 10 26 38 44

B: 04 11 30 40 55 58

C: 10 11 17 19 30 32

D: 19 37 38 40 53 55

E: 27 28 36 46 50 58

F: 03 11 18 24 29

G: 04 28 29 45 57 59

H: 03 12 16 23 25 57

I: 09 24 27 28 39 48

J: 04 12 31 35 43 58

15. Cupom: A2D1-E99063E7202BF0CD45-5

A: 06 13 14 39 49 56

B: 17 25 38 50 53 55

C: 12 15 19 32 34 56

D: 04 08 09 39 41 52

E: 01 07 31 35 37 47

F: 06 10 37 49 54 58

G: 01 11 16 49 53 56

H: 11 22 41 42 46 53

I: 24 36 39 51 58 59

J: 12 33 39 46 47 52

16. Cupom: A2D1-53A88F2EC01F1C856C-1

A: 03 10 11 26 31 47

B: 16 20 21 24 27 37

C: 19 32 44 55 57 60

D: 01 02 18 22 43 46

E: 05 12 19 21 25 43

F: 31 39 40 51 52 58

G: 01 11 24 33 52 59

H: 06 09 13 35 37 46

I: 18 30 39 43 50 51

J: 06 09 16 21 32 56

17. Cupom: A2D1-6F806F122FC4FC5BE9-7

A: 06 12 18 26 28 34

B: 12 14 27 32 43 54

C: 07 16 21 28 41 47

D: 09 14 18 29 36 54

E: 13 25 35 43 46 48

F: 27 33 46 50 54 55

G: 07 15 17 18 42 47

H: 30 34 35 37 39 42

I: 03 14 32 34 45 48

J: 02 09 17 26 48 54

18. Cupom: A2D1-85E067F8E80B02AF30-3

A: 29 37 39 50 51 58

B: 05 07 08 13 18 19

C: 34 35 37 45 49 50

D: 11 13 19 38 40 55

E: 06 11 17 35 46 48

F: 01 04 11 24 37 44

G: 13 33 36 46 54 56

H: 01 05 08 28 39 41

I: 06 14 22 30 35 37

J: 03 18 31 34 42 45

19. Cupom: A2D1-889064478D87B25231-9

A: 09 19 39 40 43 53

B: 06 13 37 48 50 55

C: 02 12 28 37 51 56

D: 08 13 31 41 49 54

E: 05 26 27 33 34 36

F: 08 17 31 45 55 57

G: 04 24 43 44 56 59

H: 02 08 11 14 46 54

I: 10 14 34 37 39 40

J: 13 15 31 39 43 44


20. Cupom: A2D1-3C20581A4447778331-8

A: 23 29 43 49 53 55

B: 06 13 24 30 42 59

C: 02 13 21 29 34 59

D: 06 08 12 15 16 29

E: 09 18 21 25 34 41

F: 07 11 13 29 39 57

G: 05 11 26 40 43 54

H: 03 08 25 33 43 58

I: 01 16 26 28 35 49

J: 23 38 42 43 44 51

21. Cupom: A2D1-84A062D0E153FBC10E-4

A: 06 21 29 30 33 44

B: 04 09 22 23 48 49

C: 05 09 24 28 32 33

D: 14 32 42 52 54 57

E: 15 26 30 31 32 52

F: 17 22 25 31 32 58

G: 07 20 25 39 42 51

H: 03 13 21 44 46 59

I: 01 28 31 44 49 53

J: 11 13 14 24 33 38

22. Cupom: A2D1-573065DCBF85DC4420-8

A: 21 32 33 36 39 51

B: 04 17 18 27 33 45

C: 01 03 21 38 56 58

D: 13 16 18 23 29 53

E: 17 26 28 43 50 55

F: 07 13 15 39 41 48

G: 03 06 10 13 15 60

H: 02 07 22 34 37 43

I: 15 19 20 40 48 60

J: 04 05 14 23 36 43

23. Cupom: A2D1-02A0666E3243BDAC80-6

A: 22 24 30 52 56 60

B: 09 10 19 26 53 55

C: 10 14 16 41 57 59

D: 13 31 41 53 55 60

E: 05 11 27 32 33 56

F: 22 27 30 39 53 55

G: 09 11 26 35 36 57

H: 02 10 19 35 51 55

I: 24 29 30 33 40 50

J: 19 31 43 50 52 53

24. Cupom: A2D1-3070808013676DD0809-3

A: 04 25 30 38 43 47

B: 06 09 14 26 57 60

C: 10 11 17 23 28 60

D: 03 04 17 27 34 42

E: 01 18 21 38 56 60

F: 04 08 22 24 35 47

G: 12 30 31 37 43 44

H: 07 14 15 19 20 42

I: 03 07 20 34 40 54

J: 10 18 23 26 35 43

25. Cupom: A2D1-9F2064BFC74AA2F427-2

A: 06 27 34 40 48 53

B: 14 24 39 41 44 49

C: 02 20 25 32 43 52

D: 04 17 34 35 54 60

E: 14 16 35 37 40 52

F: 01 09 29 32 37 44

G: 06 11 20 24 31 53

H: 11 17 35 39 48 57

I: 05 07 16 20 21 53

J: 03 18 23 53 54 59


26. Cupom: A2D1-B99067C4E829F66D18-8

A: 06 31 51 56 59 60

B: 14 17 24 28 54 57

C: 04 21 23 38 39 43

D: 05 14 21 33 36 55

E: 04 20 31 41 51 52


27. Cupom: A2D1-14D06F296A13BBEF-5

A: 04 24 35 41 52 59

B: 06 29 32 48 55 59

C: 05 06 14 24 29 42

D: 03 24 29 30 46 50

E: 15 24 41 56 58 60

F: 02 18 21 31 37 58

G: 05 26 35 37 58 60

H: 05 06 23 28 41 47

I: 06 14 29 41 50 53

J: 11 24 30 33 36 57

28. Cupom: A2D1-C8A066BD4817885FCA-1

A: 05 20 22 31 32 60

B: 06 09 16 22 37 56

C: 08 15 17 32 39 42

D: 02 04 07 13 25 35

E: 05 10 21 22 27 50

F: 12 13 20 28 42 59

G: 04 10 15 18 33 60

H: 14 24 25 30 41 56

I: 04 10 24 31 50 56

J: 05 08 34 38 43 51

29. Cupom: A2D1-6F306323593ABEB62E-7

A: 03 09 23 30 38 56

B: 24 31 38 39 49 57

C: 07 26 29 33 41 48

D: 05 13 29 39 55 57

E: 06 07 11 15 23 51

F: 06 07 21 36 37 56

G: 05 11 24 37 54 56

H: 01 13 17 37 53 55

I: 27 37 46 47 49 60

J: 06 11 28 40 50 59

30. Cupom: A2D1-1C106BF038F400E7BC-0

A: 13 19 20 21 44 50

B: 11 24 25 34 50 59

C: 04 10 12 23 37 50

D: 15 30 35 36 40 53

E: 14 15 32 34 39 48

F: 07 28 29 33 45 56

G: 06 15 27 30 54 55

H: 08 12 28 42 48 55

I: 06 17 19 29 45 50

J: 04 07 23 32 45 46

31. Cupom: A2D1-FEE06F1D598F4FE011-4

A: 03 13 16 27 36 57

B: 11 16 21 28 42 50

C: 09 13 26 34 35 45

D: 10 12 27 33 42 60

E: 01 11 13 26 29 50

F: 03 19 24 30 39 51

G: 10 13 25 28 42 51

H: 19 43 50 53 55 56

I: 14 15 24 26 28 36

J: 09 18 19 24 31 48

32. Cupom: A2D1-01806F16D50B5CF409-8

A: 01 13 25 29 30 54

B: 09 24 48 54 55 56

C: 10 34 43 50 53 58

D: 17 21 25 44 47 55

E: 02 11 15 25 27 54

F: 30 31 34 47 49 55

G: 12 19 24 27 52 58

H: 06 25 32 33 51 53

I: 01 15 22 40 49 55

J: 11 20 24 31 45 53


33. Cupom: A2D1-7DE06418D6FF6235DC-0

A: 02 21 23 38 41 55

B: 10 13 25 31 39 54

C: 06 15 17 25 28 49

D: 12 16 20 21 32 41

E: 08 13 18 36 37 44

F: 10 12 30 44 55 60

G: 05 16 21 49 55 59

H: 02 12 21 39 43 57

I: 04 18 25 31 34 44

J: 04 09 20 29 46 50

34. Cupom: A2D1-1AF06F79D15BF3D260-6

A: 22 24 25 34 36 59

B: 03 09 44 47 50 53

C: 11 18 20 24 26 57

D: 06 22 25 31 41 53

E: 11 19 24 38 43 58

F: 02 05 11 20 28 46

G: 05 07 09 23 46 55

H: 13 15 16 18 32 42

I: 26 43 47 49 55 56

J: 03 11 21 34 40 53

35. Cupom: A2D1-A060620D8350BCF445-2

A: 18 26 27 42 49 57

B: 10 23 25 49 52 55

C: 01 07 22 29 38 47

D: 17 32 46 49 54 55

E: 09 15 16 38 44 53

F: 02 14 19 31 44 49

G: 09 10 25 36 44 57

H: 03 04 05 11 28 29

I: 17 27 30 38 42 44

J: 05 10 24 31 34 54

36. Cupom: A2D1-24B0652F084F01799C-3

A: 12 20 35 40 47 56

B: 19 23 24 43 45 51

C: 03 09 31 42 50 54

D: 14 22 24 32 36 58

E: 02 04 21 27 30 56

F: 11 34 38 43 48 52

G: 12 25 29 33 53 59

H: 01 05 15 34 52 56

I: 14 15 22 35 43 48

J: 02 05 19 21 31 48

37. Cupom: A2D1-41F06598C2D501871A-9

A: 07 22 38 40 50 53

B: 11 30 32 42 44 56

C: 05 10 33 42 50 58

D: 04 08 17 45 46 49

E: 05 08 09 21 27 52

F: 14 17 26 44 50 57

G: 06 12 26 37 39 42

H: 08 25 32 36 55 56

I: 02 09 30 40 53 55

J: 06 08 10 34 37 42

38. Cupom: A2D1-66C061C2D338187D56-5

A: 02 09 11 30 34 35

B: 02 12 13 17 45 57

C: 04 08 28 31 48 54

D: 09 14 25 42 46 60

E: 28 52 55 58 59 60

F: 02 15 17 23 50 54

G: 07 17 19 24 36 41

H: 12 20 31 36 38 51

I: 14 16 33 35 44 51

J: 01 12 22 33 40 54


39. Cupom: A2D1-F2D06A446AA0262428-9

A: 03 09 18 34 46 50

B: 07 15 35 40 51 57

C: 03 26 34 35 40 43

D: 08 12 33 34 43 55

E: 10 26 27 32 42 50

F: 10 23 24 28 39 56

G: 08 27 28 30 40 41

H: 05 09 11 20 38 55

I: 04 07 28 35 41 52

J: 10 24 45 48 54 57

40. Cupom: A2D1-44D0671FF78594E776-7

A: 16 19 21 25 26 60

B: 04 14 19 33 39 48

C: 06 30 39 47 48 55

D: 01 21 29 36 41 56

E: 03 15 27 31 36 58

F: 03 05 24 33 34 51

G: 03 07 20 22 39 47

H: 15 20 26 36 37 54

I: 08 12 20 25 46 56

J: 05 17 24 32 41 55

41. Cupom: A2D1-54B06443E5A3DD1230-3

A: 18 21 28 33 42 59

B: 02 17 35 36 41 49

C: 03 17 22 30 33 59

D: 02 13 17 30 40 42

E: 02 13 21 46 51 57

F: 15 25 37 45 46 47

G: 06 10 21 43 48 49

H: 02 18 27 50 53 54

I: 15 21 26 44 46 49

J: 01 06 14 27 34 58

42. Cupom: A2D1-F2D06A446AB262428-9

A: 04 17 32 36 51 53

B: 23 29 30 39 51 53

C: 14 29 40 52 59 60

D: 01 05 29 33 49 60

E: 14 19 20 41 42 50

F: 03 06 10 20 21 25

G: 06 08 15 33 55 58

H: 06 17 28 31 42 50

I: 06 07 09 18 23 24

J: 11 27 37 42 45 58

43. Cupom: A2D1-8E806B5F9D55A6C5465-5

A: 01 10 22 36 40 58

B: 10 20 27 30 43 51

C: 02 18 26 33 52 58

D: 06 16 39 43 51 54

E: 09 11 16 20 45 56

F: 03 15 31 35 40 51

G: 36 40 45 46 47 54

H: 22 26 43 47 48 56

I: 04 10 18 22 49 56

J: 14 42 44 46 48 56

44. Cupom: A2D1-63506B883892838FA4-1

A: 03 26 32 35 43 49

B: 05 26 27 31 32 57

C: 14 33 41 48 49 50

D: 01 06 08 33 49 50

E: 01 22 28 33 38 45

F: 02 05 20 31 45 52

G: 08 29 41 42 46 50

H: 10 12 21 42 50 52

I: 03 10 13 34 47 49

J: 09 11 13 14 24 44


45. Cupom: A2D1-08F0692387E2E71FAA-4

A: 02 06 07 17 33 47 54 60

B: 03 07 08 20 39 44 55 60

C: 30 43 46 48 52 54 56 59

D: 11 17 20 24 31 41 45 54

E: 09 37 41 47 50 56 57 60

F: 06 08 10 13 29 44 49 50

G: 07 23 32 34 35 46 49 57

H: 32 35 42 44 47 50 54 58

I: 06 12 21 22 24 39 44 52

J: 08 10 18 19 24 38 46 57
"""

# ==============================================================================
# ⚙️ FUNÇÕES
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
        if "IMAGEM" in linha or "Cupom" in linha:
            imagem_atual = linha.replace('#', '').replace('*', '').strip()
            contador_simples = 1
            continue
        match = padrao_aposta.search(linha)
        if match:
            identificador = match.group(1)
            if not identificador:
                identificador = f"Jogo {contador_simples}"
                contador_simples += 1
            else:
                identificador = identificador.replace(':', '')
            numeros_str = match.group(2).replace('-', ' ').split()
            apostas_processadas.append({
                'id': identificador,
                'nums': set(map(int, numeros_str)),
                'local': imagem_atual
            })
    return apostas_processadas

def exibir_resultados(resultado, apostas):
    premios = {'Sena': [], 'Quina': [], 'Quadra': []}
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

    total_premios = len(premios['Sena']) + len(premios['Quina']) + len(premios['Quadra'])
    if total_premios == 0:
        st.warning("😢 Nenhum prêmio encontrado nestes bilhetes.")
    else:
        if premios['Sena']:
            st.markdown("### 🏆 SENA (6 Acertos)")
            for p in premios['Sena']:
                st.markdown(f"<div class='ticket-card sena-card'><span class='local-tag'>📍 {p['local']}</span><div class='win-title'>BILHETE {p['id']} - GANHADOR!</div><div>Seus Números: <span class='numbers'>{', '.join(map(str, p['numeros_full']))}</span></div></div>", unsafe_allow_html=True)
        if premios['Quina']:
            st.markdown("### 💰 QUINA (5 Acertos)")
            for p in premios['Quina']:
                st.markdown(f"<div class='ticket-card quina-card'><span class='local-tag'>📍 {p['local']}</span><div class='win-title'>Bilhete {p['id']}</div><div>Acertou: <span class='numbers'>{', '.join(map(str, p['acertos']))}</span></div></div>", unsafe_allow_html=True)
        if premios['Quadra']:
            st.markdown("### 👍 QUADRA (4 Acertos)")
            for p in premios['Quadra']:
                st.markdown(f"<div class='ticket-card quadra-card'><span class='local-tag'>📍 {p['local']}</span><div class='win-title'>Bilhete {p['id']}</div><div>Acertou: <span class='numbers'>{', '.join(map(str, p['acertos']))}</span></div></div>", unsafe_allow_html=True)

# ==============================================================================
# 🚀 INTERFACE DO USUÁRIO
# ==============================================================================

st.title("🍀 Verificador Mega da Virada")
st.markdown("<div style='text-align: center; color: #666; margin-bottom: 20px;'>Boa sorte! Que seus números sejam os sorteados!</div>", unsafe_allow_html=True)

# Abas para Alternar entre Modos
tab1, tab2 = st.tabs(["📡 Buscar Concurso", "✍️ Digitar Números"])

# --- MODO 1: AUTOMÁTICO ---
with tab1:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        concurso_input = st.text_input("Número do Concurso", value="2955")
    with col_b:
        st.write("") 
        st.write("")
        btn_auto = st.button("BUSCAR NA CAIXA", type="primary", key="auto")
    
    if btn_auto:
        with st.spinner("Buscando dados oficiais..."):
            resultado = buscar_resultado_api(concurso_input)
            if not resultado:
                st.error("Erro ao buscar dados. Tente o modo manual.")
            else:
                st.success(f"Dezenas Sorteadas: {', '.join(map(str, sorted(resultado)))}")
                apostas = processar_jogos(MEUS_JOGOS)
                exibir_resultados(resultado, apostas)

# --- MODO 2: MANUAL (6 INPUTS DE TEXTO LIMPOS) ---
with tab2:
    st.info("Insira as 6 dezenas sorteadas:")
    cols = st.columns(6)
    
    # Cria 6 campos de TEXTO (sem setas, sem X)
    n1 = cols[0].text_input("Bola 1", max_chars=2, placeholder="01")
    n2 = cols[1].text_input("Bola 2", max_chars=2, placeholder="02")
    n3 = cols[2].text_input("Bola 3", max_chars=2, placeholder="03")
    n4 = cols[3].text_input("Bola 4", max_chars=2, placeholder="04")
    n5 = cols[4].text_input("Bola 5", max_chars=2, placeholder="05")
    n6 = cols[5].text_input("Bola 6", max_chars=2, placeholder="06")
    
    if st.button("CONFERIR MANUALMENTE", type="primary", key="manual"):
        inputs = [n1, n2, n3, n4, n5, n6]
        
        # Validação
        if any(v == "" for v in inputs):
            st.warning("⚠️ Preencha todas as 6 dezenas.")
        else:
            try:
                # Converte para inteiro e valida intervalo
                numeros_int = []
                for val in inputs:
                    num = int(val)
                    if num < 1 or num > 60:
                        raise ValueError
                    numeros_int.append(num)
                
                numeros_set = set(numeros_int)
                
                if len(numeros_set) < 6:
                    st.warning("⚠️ Números repetidos detectados. Insira 6 números diferentes.")
                else:
                    st.balloons()
                    st.success(f"Conferindo: {', '.join(map(str, sorted(numeros_set)))}")
                    apostas = processar_jogos(MEUS_JOGOS)
                    exibir_resultados(numeros_set, apostas)
                    
            except ValueError:
                st.error("⚠️ Erro: Certifique-se de digitar apenas números entre 01 e 60.")

# Rodapé
st.markdown("<div class='footer'>Desenvolvido por <b>André Santos</b> © 2025</div>", unsafe_allow_html=True)



