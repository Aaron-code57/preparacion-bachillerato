import random

import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

# ============================================================
# CONFIGURACIÓ
# ============================================================

st.set_page_config(
    page_title="Preparació Batxillerat",
    page_icon="🎓",
    layout="wide",
)

# ============================================================
# TEMARI
# ============================================================

TEMARI = {
    "1r Batxillerat": {
        "📐 Matemàtiques I": [
            "Nombres reals, intervals i errors",
            "Polinomis, fraccions algebraiques i mètode de Gauss",
            "Equacions exponencials, logarítmiques i inequacions",
            "Nombres complexos",
            "Raons trigonomètriques, identitats i resolució de triangles",
            "Vectors en el pla",
            "Geometria analítica plana",
            "Llocs geomètrics i còniques",
            "Funcions elementals i dominis",
            "Límits de funcions i continuïtat",
            "Derivades",
            "Probabilitat i estadística bidimensional",
        ],
        "⚛️ Física I": [
            "Cinemàtica",
            "Dinàmica",
            "Treball i Energia",
            "Moviment Harmònic Simple (MAS)",
            "Estàtica i Fluids",
        ],
        "⚗️ Química I": [
            "Conceptes bàsics i lleis",
            "Estructura atòmica",
            "Enllaç químic i formulació",
            "Aspectes quantitatius",
            "Reaccions químiques",
            "Química del carboni",
        ],
    },
    "2n Batxillerat": {
        "📐 Matemàtiques II": [
            "Matrius i determinants",
            "Sistemes d'equacions lineals avançats",
            "Vectors en l'espai",
            "Rectes i plans en l'espai",
            "Problemes mètrics",
            "Límits avançats i indeterminacions",
            "Continuïtat i teoremes fonamentals",
            "Derivabilitat i representació gràfica de funcions",
            "Optimització de problemes reals",
            "Càlcul d'integrals indefinides i definides",
            "Probabilitat condicionada, Bayes i probabilitat total",
            "Variables aleatòries, Binomial i Normal",
        ],
        "⚛️ Física II": [
            "Camp Gravitatori",
            "Camp Elèctric",
            "Camp Magnètic",
            "Ones",
            "Òptica",
            "Física Moderna",
        ],
        "⚗️ Química II": [
            "Estructura de la matèria i enllaç avançat",
            "Termoquímica",
            "Cinètica química",
            "Equilibri químic",
            "Reaccions en dissolució",
            "Química orgànica",
        ],
    },
}

# ============================================================
# ESTAT DE L'APLICACIÓ
# ============================================================

DEFAULT_STATE = {
    "curs": None,
    "assignatura": None,
    "tema": None,
    "dificultat": None,
    "exercici": None,
    "mostrar_resposta": False,
    "mostrar_passos": False,
    "historial_exercicis": [],
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "historial_exercicis" not in st.session_state:
    st.session_state.historial_exercicis = []


# ============================================================
# GENERADORS D'EXERCICIS
# ============================================================

def resposta_unica(valor):
    return {"resposta": [str(sp.simplify(valor))]}


def exercici_det_2x2():
    while True:
        a, b, c, d = [random.randint(-9, 9) for _ in range(4)]
        A = sp.Matrix([[a, b], [c, d]])
        det = sp.expand(A.det())
        if det != 0:
            break

    passos = f"""
Per a una matriu $2\\times2$:

$$
\\det(A)=ad-bc
$$

Substituïm:

$$
\\det(A)=({a})\\cdot({d})-({b})\\cdot({c})
$$

$$
={sp.latex(a*d)}-{sp.latex(b*c)}
$$

$$
\\boxed{{{sp.latex(det)}}}
$$
"""

    return {
        "enunciat": f"""
Calcula el determinant de:

$$
A={sp.latex(A)}
$$
""",
        "resposta": [str(det)],
        "passos": passos,
    }


def exercici_det_3x3():
    while True:
        vals = [random.randint(-5, 5) for _ in range(9)]
        A = sp.Matrix(3, 3, vals)
        det = sp.expand(A.det())
        if det != 0:
            break

    a, b, c = A[0, 0], A[0, 1], A[0, 2]
    d, e, f = A[1, 0], A[1, 1], A[1, 2]
    g, h, i = A[2, 0], A[2, 1], A[2, 2]

    m1 = sp.expand(e*i - f*h)
    m2 = sp.expand(d*i - f*g)
    m3 = sp.expand(d*h - e*g)

    steps = f"""
Desenvolupem per la primera fila:

$$
\\det(A)=
a\\begin{{vmatrix}}e&f\\\\h&i\\end{{vmatrix}}
-b\\begin{{vmatrix}}d&f\\\\g&i\\end{{vmatrix}}
+c\\begin{{vmatrix}}d&e\\\\g&h\\end{{vmatrix}}
$$

Els menors són:

$$
M_1={sp.latex(m1)},\\qquad
M_2={sp.latex(m2)},\\qquad
M_3={sp.latex(m3)}
$$

Per tant:

$$
\\det(A)=({a})({sp.latex(m1)})
-({b})({sp.latex(m2)})
+({c})({sp.latex(m3)})
$$

$$
\\boxed{{{sp.latex(det)}}}
$$
"""

    return {
        "enunciat": f"""
Calcula el determinant de:

$$
A={sp.latex(A)}
$$
""",
        "resposta": [str(det)],
        "passos": steps,
    }

def exercici_parametre():
    k = sp.Symbol("k")
    m = random.randint(2, 9)
    A = sp.Matrix([[k, m], [3, k]])
    det = sp.expand(A.det())
    sol = sp.solve(sp.Eq(det, 0), k)

    passos = f"""
Calculem el determinant:

$$
\\det(A)=k^2-3\\cdot({m})
$$

$$
\\det(A)=k^2-{3*m}
$$

Perquè el determinant sigui zero:

$$
k^2-{3*m}=0
$$

$$
k^2={3*m}
$$

Per tant:

$$
\\boxed{{k={sp.latex(sol[0])}\\quad\\text{o}\\quad k={sp.latex(sol[1])}}}
$$
"""

    return {
        "enunciat": f"""
Calcula els valors de $k$ perquè el determinant sigui zero:

$$
A=
\\begin{{pmatrix}}
k & {m}\\\
3 & k
\\end{{pmatrix}}
$$
""",
        "resposta": [str(s) for s in sol],
        "passos": passos,
    }


def exercici_element_determinant():
    a, b, c = [random.randint(-6, 6) for _ in range(3)]
    while a == 0:
        a = random.randint(-6, 6)

    # a*x - b*c = D
    x = sp.Symbol("x")
    A = sp.Matrix([[a, b], [c, x]])
    det = sp.expand(A.det())
    objectiu = random.randint(-20, 20)
    sol = sp.solve(sp.Eq(det, objectiu), x)[0]

    passos = f"""
Per a una matriu $2\\times2$:

$$
\\det(A)=ad-bc
$$

En aquest cas:

$$
\\det(A)=({a})x-({b})({c})
$$

Ens diuen que el determinant ha de ser:

$$
{objectiu}
$$

Així:

$$
({a})x-{b*c}={objectiu}
$$

$$
({a})x={objectiu + b*c}
$$

$$
\\boxed{{x={sp.latex(sol)}}}
$$
"""

    return {
        "enunciat": f"""
Troba el valor de $x$ perquè el determinant sigui ${objectiu}$:

$$
A=
\\begin{{pmatrix}}
{a} & {b}\\\
{c} & x
\\end{{pmatrix}}
$$
""",
        "resposta": [str(sol)],
        "passos": passos,
    }


def exercici_matriu_triangular():
    # Diagonal non-zero so determinant is non-zero.
    diagonal = [random.randint(-7, 7) or 1 for _ in range(3)]
    A = sp.Matrix([
        [diagonal[0], random.randint(-5, 5), random.randint(-5, 5)],
        [0, diagonal[1], random.randint(-5, 5)],
        [0, 0, diagonal[2]],
    ])
    det = sp.prod(diagonal)

    passos = f"""
La matriu és triangular superior. En una matriu triangular,
el determinant és el producte dels elements de la diagonal principal:

$$
\\det(A)=a_{11}\\cdot a_{22}\\cdot a_{33}
$$

Per tant:

$$
\\det(A)=({diagonal[0]})\\cdot({diagonal[1]})\\cdot({diagonal[2]})
$$

$$
\\boxed{{{det}}}
$$
"""

    return {
        "enunciat": f"""
Calcula el determinant de la matriu triangular:

$$
A={sp.latex(A)}
$$
""",
        "resposta": [str(det)],
        "passos": passos,
    }


def exercici_propietat_escalar():
    n = random.randint(2, 5)
    det_a = random.choice([d for d in range(-8, 9) if d != 0])
    escalar = random.choice([2, 3, -2, -3])

    # det(lambda A) = lambda^n det(A)
    resultat = sp.Integer(escalar) ** n * det_a

    passos = f"""
Si $A$ és una matriu $n\\times n$, tenim:

$$
\\det(\\lambda A)=\\lambda^n\\det(A)
$$

En aquest cas:

$$
\\det({escalar}A)
=({escalar})^{n}\\cdot({det_a})
$$

$$
={sp.latex(resultat)}
$$

$$
\\boxed{{{sp.latex(resultat)}}}
$$
"""

    return {
        "enunciat": f"""
Sabent que $A$ és una matriu ${n}\\times{n}$ i que
$\\det(A)={det_a}$, calcula:

$$
\\det({escalar}A)
$$
""",
        "resposta": [str(resultat)],
        "passos": passos,
    }


def exercici_producte_determinants():
    da = random.choice([d for d in range(-8, 9) if d != 0])
    db = random.choice([d for d in range(-8, 9) if d != 0])
    resultat = da * db

    passos = f"""
Utilitzem la propietat:

$$
\\det(AB)=\\det(A)\\det(B)
$$

Per tant:

$$
\\det(AB)=({da})({db})
$$

$$
\\boxed{{{resultat}}}
$$
"""

    return {
        "enunciat": f"""
Sabent que:

$$
\\det(A)={da}
\\qquad\\text{{i}}\\qquad
\\det(B)={db}
$$

calcula:

$$
\\det(AB)
$$
""",
        "resposta": [str(resultat)],
        "passos": passos,
    }


def exercici_invertible():
    while True:
        A, det = generar_matriu_2x2()
        if det not in (1, -1):
            break

    resultat = "sí" if det != 0 else "no"

    passos = f"""
Una matriu és invertible si i només si el seu determinant és diferent de zero:

$$
\\det(A)\\neq0
$$

En aquest cas:

$$
\\det(A)={sp.latex(det)}
$$

Com que és diferent de zero, la matriu:

$$
\\boxed{{\\text{{sí és invertible}}}}
$$
"""

    # Keep this as a numeric question so the same checker can be used.
    return {
        "enunciat": f"""
Calcula el determinant de:

$$
A={sp.latex(A)}
$$

i indica el valor del determinant.
""",
        "resposta": [str(det)],
        "passos": passos,
    }


def exercici_parametre_3x3():
    k = sp.Symbol("k")

    # Matriu dissenyada perquè el determinant sigui una quadràtica
    # no trivial en k i doni arrels exactes.
    q = random.choice([2, 3, 4, 5])
    A = sp.Matrix([
        [k, 1, 0],
        [1, k, 2],
        [0, 3, q],
    ])
    det = sp.factor(A.det())
    sol = sp.solve(sp.Eq(det, 0), k)

    steps = f"""
Calculem el determinant:

$$
\\det(A)={sp.latex(det)}
$$

Com que volem que el determinant sigui zero:

$$
{sp.latex(det)}=0
$$

Resolem l'equació:

$$
\\boxed{{k={sp.latex(sol[0])}\\quad\\text{{o}}\\quad k={sp.latex(sol[1])}}}
$$
"""

    return {
        "enunciat": f"""
Calcula els valors de $k$ perquè el determinant sigui zero:

$$
A={sp.latex(A)}
$$
""",
        "resposta": [str(s) for s in sol],
        "passos": steps,
    }


def exercici_element_determinant_3x3():
    x = sp.Symbol("x")

    while True:
        vals = [random.randint(-4, 4) for _ in range(8)]
        a, b, c, d, e, f, g, h = vals
        A = sp.Matrix([
            [a, b, c],
            [d, e, f],
            [g, x, h],
        ])
        det_expr = sp.expand(A.det())
        coeff = det_expr.coeff(x)

        if coeff != 0:
            target = random.randint(-12, 12)
            sol = sp.solve(sp.Eq(det_expr, target), x)
            if sol and sol[0].is_rational:
                break

    solution = sp.simplify(sol[0])

    steps = f"""
Desenvolupem el determinant en funció de $x$:

$$
\\det(A)={sp.latex(det_expr)}
$$

Com que el determinant ha de ser ${target}$:

$$
{sp.latex(det_expr)}={target}
$$

Aïllem $x$:

$$
\\boxed{{x={sp.latex(solution)}}}
$$
"""

    return {
        "enunciat": f"""
Troba el valor de $x$ perquè el determinant sigui ${target}$:

$$
A={sp.latex(A)}
$$
""",
        "resposta": [str(solution)],
        "passos": steps,
    }


def exercici_determinant_potencia():
    det_a = random.choice([d for d in range(-6, 7) if d not in (0, 1, -1)])
    exponent = random.choice([2, 3, 4])
    resultat = sp.Integer(det_a) ** exponent

    steps = f"""
Utilitzem:

$$
\\det(A^n)=\\det(A)^n
$$

Per tant:

$$
\\det(A^{{{exponent}}})=({det_a})^{{{exponent}}}
={sp.latex(resultat)}
$$

$$
\\boxed{{{sp.latex(resultat)}}}
$$
"""

    return {
        "enunciat": f"""
Sabent que $\\det(A)={det_a}$, calcula:

$$
\\det(A^{{{exponent}}})
$$
""",
        "resposta": [str(resultat)],
        "passos": steps,
    }


def exercici_determinant_inversa():
    det_a = random.choice([d for d in range(-6, 7) if d not in (0, 1, -1)])
    resultat = sp.Rational(1, det_a)

    steps = f"""
Com que $\\det(A)\\neq0$, $A$ és invertible.

Utilitzem:

$$
\\det(A^{{-1}})=\\frac{{1}}{{\\det(A)}}
$$

Així:

$$
\\det(A^{{-1}})=\\frac{{1}}{{{det_a}}}
={sp.latex(resultat)}
$$

$$
\\boxed{{{sp.latex(resultat)}}}
$$
"""

    return {
        "enunciat": f"""
Sabent que $\\det(A)={det_a}$, calcula:

$$
\\det(A^{{-1}})
$$
""",
        "resposta": [str(resultat)],
        "passos": steps,
    }



def matriu_text(A):
    """Representació LaTeX compacta d'una matriu."""
    return sp.latex(A)


def exercici_suma_matrius():
    a = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
    b = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
    c = a + b

    passos = f"""
Sumem els elements que ocupen la mateixa posició:

$$
A+B={matriu_text(a)}+{matriu_text(b)}
$$

$$
A+B={matriu_text(c)}
$$

Per tant:

$$
\\boxed{{A+B={matriu_text(c)}}}
$$
"""
    return {
        "enunciat": f"""
Calcula $A+B$:

$$
A={matriu_text(a)}
\\qquad
B={matriu_text(b)}
$$
""",
        "resposta": [c],
        "tipus_resposta": "matriu",
        "passos": passos,
    }


def exercici_resta_matrius():
    a = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
    b = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
    c = a - b

    passos = f"""
Restem els elements de les mateixes posicions:

$$
A-B={matriu_text(a)}-{matriu_text(b)}
$$

$$
A-B={matriu_text(c)}
$$

Per tant:

$$
\\boxed{{A-B={matriu_text(c)}}}
$$
"""
    return {
        "enunciat": f"""
Calcula $A-B$:

$$
A={matriu_text(a)}
\\qquad
B={matriu_text(b)}
$$
""",
        "resposta": [c],
        "tipus_resposta": "matriu",
        "passos": passos,
    }


def exercici_transposada():
    a = sp.Matrix([[random.randint(-7, 7) for _ in range(2)] for _ in range(3)])
    at = a.T

    passos = f"""
La transposada s'obté intercanviant files i columnes:

$$
A={matriu_text(a)}
$$

Per tant:

$$
A^T={matriu_text(at)}
$$

És a dir, la primera fila passa a ser la primera columna.

$$
\\boxed{{A^T={matriu_text(at)}}}
$$
"""
    return {
        "enunciat": f"""
Calcula la matriu transposada $A^T$:

$$
A={matriu_text(a)}
$$
""",
        "resposta": [at],
        "tipus_resposta": "matriu",
        "passos": passos,
    }


def exercici_producte_matrius():
    # Evitem resultats massa grans.
    a = sp.Matrix([[random.randint(-3, 4) for _ in range(2)] for _ in range(2)])
    b = sp.Matrix([[random.randint(-3, 4) for _ in range(2)] for _ in range(2)])
    c = a * b

    passos = f"""
Per multiplicar matrius, cada element és el producte escalar
d'una fila de $A$ amb una columna de $B$:

$$
AB={matriu_text(a)}{matriu_text(b)}
$$

Per exemple, l'element de la primera fila i primera columna és:

$$
({a[0,0]})({b[0,0]})+({a[0,1]})({b[1,0]})
={sp.expand(c[0,0])}
$$

Fent el mateix amb totes les posicions:

$$
AB={matriu_text(c)}
$$

$$
\\boxed{{AB={matriu_text(c)}}}
$$
"""
    return {
        "enunciat": f"""
Calcula el producte $AB$:

$$
A={matriu_text(a)}
\\qquad
B={matriu_text(b)}
$$
""",
        "resposta": [c],
        "tipus_resposta": "matriu",
        "passos": passos,
    }


def exercici_inversa_2x2():
    # Determinant no nul i senzill, però no trivial.
    while True:
        a, b, c, d = [random.randint(-5, 5) for _ in range(4)]
        A = sp.Matrix([[a, b], [c, d]])
        det = sp.expand(A.det())
        if det in (-3, -2, 2, 3, 4, -4):
            break

    inv = A.inv()

    passos = f"""
Per a una matriu

$$
A=\\begin{{pmatrix}}a&b\\\\c&d\\end{{pmatrix}}
$$

tenim:

$$
A^{{-1}}=\\frac{{1}}{{\\det(A)}}
\\begin{{pmatrix}}d&-b\\\\-c&a\\end{{pmatrix}}
$$

Primer:

$$
\\det(A)=({a})({d})-({b})({c})={det}
$$

Per tant:

$$
A^{{-1}}
=\\frac{{1}}{{{det}}}
\\begin{{pmatrix}}{d}&{-b}\\{-c}&{a}\\end{{pmatrix}}
={matriu_text(inv)}
$$

$$
\\boxed{{A^{{-1}}={matriu_text(inv)}}}
$$
"""
    return {
        "enunciat": f"""
Calcula la matriu inversa $A^{{-1}}$:

$$
A={matriu_text(A)}
$$
""",
        "resposta": [inv],
        "tipus_resposta": "matriu",
        "passos": passos,
    }


def exercici_rang_2x2():
    # Generem una matriu 2x2 amb rang clarament 1 o 2.
    if random.choice([True, False]):
        a = random.randint(-6, 6) or 1
        b = random.randint(-6, 6)
        factor = random.randint(-4, 4)
        if factor == 0:
            factor = 2
        A = sp.Matrix([[a, b], [factor*a, factor*b]])
        rang = 1
    else:
        while True:
            A = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
            if A.det() != 0:
                break
        rang = 2

    passos = f"""
Per una matriu $2\\times2$:

- si $\\det(A)\\neq0$, el rang és $2$;
- si $\\det(A)=0$ i la matriu no és nul·la, el rang és $1$.

En aquest cas:

$$
\\det(A)={sp.expand(A.det())}
$$

Per tant:

$$
\\boxed{{\\operatorname{{rang}}(A)={rang}}}
$$
"""
    return {
        "enunciat": f"""
Calcula el rang de la matriu:

$$
A={matriu_text(A)}
$$
""",
        "resposta": [str(rang)],
        "tipus_resposta": "escalar",
        "passos": passos,
    }


def exercici_inversa_triangular_3x3():
    # Matriu triangular amb diagonal 1: inversa exacta i manejable.
    p, q, r = [random.randint(-3, 3) for _ in range(3)]
    A = sp.Matrix([
        [1, p, q],
        [0, 1, r],
        [0, 0, 1],
    ])
    inv = A.inv()

    passos = f"""
Com que la diagonal principal és 1, $\\det(A)=1$ i la matriu és invertible.

Busquem $A^{{-1}}$ mitjançant Gauss-Jordan:

$$
[A\\mid I]\\longrightarrow[I\\mid A^{{-1}}]
$$

En aquest cas, el resultat és:

$$
A^{{-1}}={matriu_text(inv)}
$$

Podem comprovar-ho perquè:

$$
A\\,A^{{-1}}=I
$$

$$
\\boxed{{A^{{-1}}={matriu_text(inv)}}}
$$
"""
    return {
        "enunciat": f"""
Calcula $A^{{-1}}$ mitjançant Gauss-Jordan:

$$
A={matriu_text(A)}
$$
""",
        "resposta": [inv],
        "tipus_resposta": "matriu",
        "passos": passos,
    }


def exercici_rang_3x3():
    # Construïm directament dues files independents i una tercera
    # que és combinació lineal de les dues primeres. Així el rang és 2.
    p, q, r = [random.randint(-3, 3) for _ in range(3)]
    u = random.randint(-3, 3) or 2
    v = random.randint(-3, 3) or -1

    row1 = sp.Matrix([[1, p, q]])
    row2 = sp.Matrix([[0, 1, r]])
    row3 = u * row1 + v * row2
    A = sp.Matrix.vstack(row1, row2, row3)

    passos = f"""
Observem que la tercera fila és combinació lineal de les dues primeres:

$$
F_3={u}F_1+({v})F_2
$$

Per tant, $F_3$ no aporta una nova fila independent.

Les dues primeres files són independents, perquè no són proporcionals.
Així:

$$
\\boxed{{\\operatorname{{rang}}(A)=2}}
$$
"""
    return {
        "enunciat": f"""
Calcula el rang de la matriu:

$$
A={matriu_text(A)}
$$
""",
        "resposta": [str(2)],
        "tipus_resposta": "escalar",
        "passos": passos,
    }


def exercici_matriu_equacio_escalar():
    # Exercici de combinació lineal de matrius: X + A = B -> X = B-A.
    A = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
    X = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
    B = X + A

    passos = f"""
Partim de:

$$
X+A=B
$$

Restem $A$ als dos costats:

$$
X=B-A
$$

Substituïm:

$$
X={matriu_text(B)}-{matriu_text(A)}
$$

$$
X={matriu_text(X)}
$$

$$
\\boxed{{X={matriu_text(X)}}}
$$
"""
    return {
        "enunciat": f"""
Troba la matriu $X$ sabent que:

$$
X+A=B
$$

on

$$
A={matriu_text(A)}
\\qquad
B={matriu_text(B)}
$$
""",
        "resposta": [X],
        "tipus_resposta": "matriu",
        "passos": passos,
    }





# ============================================================
# VECTORS EN L'ESPAI
# ============================================================

def _vector_latex(v):
    return sp.latex(sp.Matrix(v).reshape(3, 1))


def _vector_solution_text(v):
    vals = [sp.latex(sp.simplify(x)) for x in list(v)]
    return "(" + ", ".join(vals) + ")"


def exercici_vector_suma():
    u = sp.Matrix([random.randint(-6, 6) for _ in range(3)])
    v = sp.Matrix([random.randint(-6, 6) for _ in range(3)])
    r = u + v
    passos = f"""
Tenim:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$

Sumem component a component:

$$
\\vec u+\\vec v={_vector_latex(r)}
$$

**Resposta:** $${_vector_solution_text(r)}$$
"""
    return {
        "enunciat": f"""
Calcula el vector $\\vec u+\\vec v$ si:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$
""",
        "resposta": [r],
        "tipus_resposta": "vector",
        "passos": passos,
    }


def exercici_vector_resta():
    u = sp.Matrix([random.randint(-6, 6) for _ in range(3)])
    v = sp.Matrix([random.randint(-6, 6) for _ in range(3)])
    r = u - v
    passos = f"""
Restem component a component:

$$
\\vec u-\\vec v={_vector_latex(r)}
$$

**Resposta:** $${_vector_solution_text(r)}$$
"""
    return {
        "enunciat": f"""
Calcula el vector $\\vec u-\\vec v$ si:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$
""",
        "resposta": [r],
        "tipus_resposta": "vector",
        "passos": passos,
    }


def exercici_vector_norma():
    v = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    while v == sp.zeros(3, 1):
        v = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    norma = sp.sqrt(sum(x**2 for x in v))
    passos = f"""
La norma d'un vector és:

$$
|\\vec v|=\\sqrt{{v_x^2+v_y^2+v_z^2}}
$$

En aquest cas:

$$
|\\vec v|=\\sqrt{{{sp.latex(sum(x**2 for x in v))}}}={sp.latex(norma)}
$$

**Resposta:** $${sp.latex(norma)}$$
"""
    return {
        "enunciat": f"""
Calcula la norma del vector:

$$
\\vec v={_vector_latex(v)}
$$
""",
        "resposta": [norma],
        "tipus_resposta": "escalar",
        "passos": passos,
    }


def exercici_vector_punts():
    A = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    B = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    r = B - A
    passos = f"""
El vector que va de $A$ a $B$ és:

$$
\\overrightarrow{{AB}}=B-A
$$

Per tant:

$$
\\overrightarrow{{AB}}={_vector_latex(B)}-{_vector_latex(A)}={_vector_latex(r)}
$$

**Resposta:** $${_vector_solution_text(r)}$$
"""
    return {
        "enunciat": f"""
Calcula el vector $\\overrightarrow{{AB}}$ a partir dels punts:

$$
A={_vector_latex(A)},\\qquad B={_vector_latex(B)}
$$
""",
        "resposta": [r],
        "tipus_resposta": "vector",
        "passos": passos,
    }


def exercici_vector_producte_escalar():
    v = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    k = random.choice([-4, -3, -2, 2, 3, 4])
    r = k * v
    passos = f"""
Multipliquem cada component per $k={k}$:

$$
{k}\\vec v={_vector_latex(r)}
$$

**Resposta:** $${_vector_solution_text(r)}$$
"""
    return {
        "enunciat": f"""
Calcula el vector $ {k}\\vec v $ si:

$$
\\vec v={_vector_latex(v)}
$$
""",
        "resposta": [r],
        "tipus_resposta": "vector",
        "passos": passos,
    }


def exercici_producte_escalar():
    u = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    v = sp.Matrix([random.randint(-5, 5) for _ in range(3)])
    r = sp.expand(u.dot(v))
    passos = f"""
El producte escalar és:

$$
\\vec u\\cdot\\vec v=u_xv_x+u_yv_y+u_zv_z
$$

Per tant:

$$
\\vec u\\cdot\\vec v={sp.latex(r)}
$$

**Resposta:** $${sp.latex(r)}$$
"""
    return {
        "enunciat": f"""
Calcula el producte escalar $\\vec u\\cdot\\vec v$:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$
""",
        "resposta": [r],
        "tipus_resposta": "escalar",
        "passos": passos,
    }


def exercici_vectors_ortogonals_parametre():
    k = sp.Symbol("k")
    u = sp.Matrix([k, random.randint(1, 4), random.randint(1, 4)])
    v = sp.Matrix([random.choice([-3, -2, 2, 3]), random.randint(-4, 4), random.randint(-4, 4)])
    # Force an integer solution for k by constructing v_x and constants.
    vx = random.choice([-3, -2, 2, 3])
    vy = random.choice([-3, -2, 2, 3])
    vz = random.choice([-3, -2, 2, 3])
    y = random.choice([1, 2, 3])
    z = random.choice([1, 2, 3])
    u = sp.Matrix([k, y, z])
    v = sp.Matrix([vx, vy, vz])
    sol = sp.solve(sp.Eq(u.dot(v), 0), k)[0]
    passos = f"""
Dos vectors són perpendiculars quan:

$$
\\vec u\\cdot\\vec v=0
$$

Calculem:

$$
{sp.latex(u.dot(v))}=0
$$

D'aquí obtenim:

$$
 k={sp.latex(sol)}
$$

**Resposta:** $${sp.latex(sol)}$$
"""
    return {
        "enunciat": f"""
Troba el valor de $k$ perquè els vectors siguin perpendiculars:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$
""",
        "resposta": [sol],
        "tipus_resposta": "escalar",
        "passos": passos,
    }


def exercici_producte_vectorial():
    u = sp.Matrix([random.randint(-4, 4) for _ in range(3)])
    v = sp.Matrix([random.randint(-4, 4) for _ in range(3)])
    r = u.cross(v)
    if r == sp.zeros(3, 1):
        return exercici_producte_vectorial()
    passos = f"""
El producte vectorial es pot calcular amb el determinant:

$$
\\vec u\\times\\vec v=
\\begin{{vmatrix}}
\\vec i&\\vec j&\\vec k\\\
{u[0]}&{u[1]}&{u[2]}\\\
{v[0]}&{v[1]}&{v[2]}
\\end{{vmatrix}}
$$

El resultat és:

$$
\\vec u\\times\\vec v={_vector_latex(r)}
$$

**Resposta:** $${_vector_solution_text(r)}$$
"""
    return {
        "enunciat": f"""
Calcula el producte vectorial $\\vec u\\times\\vec v$:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$
""",
        "resposta": [r],
        "tipus_resposta": "vector",
        "passos": passos,
    }


def exercici_area_parallelogram():
    u = sp.Matrix([random.randint(-3, 3) for _ in range(3)])
    v = sp.Matrix([random.randint(-3, 3) for _ in range(3)])
    cross = u.cross(v)
    if cross == sp.zeros(3, 1):
        return exercici_area_parallelogram()
    area = sp.sqrt(sum(x**2 for x in cross))
    passos = f"""
L'àrea del paral·lelogram definit per dos vectors és:

$$
A=|\\vec u\\times\\vec v|
$$

Primer calculem:

$$
\\vec u\\times\\vec v={_vector_latex(cross)}
$$

I després la seva norma:

$$
A={sp.latex(area)}
$$

**Resposta:** $${sp.latex(area)}$$
"""
    return {
        "enunciat": f"""
Calcula l'àrea del paral·lelogram definit pels vectors:

$$
\\vec u={_vector_latex(u)},\\qquad \\vec v={_vector_latex(v)}
$$
""",
        "resposta": [area],
        "tipus_resposta": "escalar",
        "passos": passos,
    }


def exercici_tres_vectors_coplanars():
    u = sp.Matrix([random.randint(-3, 3) for _ in range(3)])
    v = sp.Matrix([random.randint(-3, 3) for _ in range(3)])
    while u.cross(v) == sp.zeros(3, 1):
        v = sp.Matrix([random.randint(-3, 3) for _ in range(3)])
    a = random.randint(-3, 3)
    b = random.randint(-3, 3)
    w = a*u + b*v
    triple = sp.Matrix.hstack(u, v, w).det()
    passos = f"""
Tres vectors són coplanaris si el seu producte mixt és zero:

$$
[\\vec u,\\vec v,\\vec w]=0
$$

Com que $\\vec w={a}\\vec u+{b}\\vec v$, els tres vectors són dependents linealment i:

$$
\\det({matriu_text(sp.Matrix.hstack(u,v,w))})={sp.latex(triple)}
$$

Per tant, són **coplanaris**.
"""
    return {
        "enunciat": f"""
Indica si els tres vectors són coplanaris:

$$
\\vec u={_vector_latex(u)},\\quad
\\vec v={_vector_latex(v)},\\quad
\\vec w={_vector_latex(w)}
$$
""",
        "resposta": ["SI"],
        "tipus_resposta": "classificacio_vector",
        "passos": passos,
    }


def generar_exercici_vectors(dificultat):
    if dificultat == "Fàcil":
        generadors = [
            exercici_vector_suma,
            exercici_vector_resta,
            exercici_vector_norma,
            exercici_vector_punts,
            exercici_vector_producte_escalar,
        ]
    elif dificultat == "Mitjà":
        generadors = [
            exercici_producte_escalar,
            exercici_vectors_ortogonals_parametre,
            exercici_vector_punts,
            exercici_vector_norma,
            exercici_vector_producte_escalar,
        ]
    else:
        generadors = [
            exercici_producte_vectorial,
            exercici_area_parallelogram,
            exercici_tres_vectors_coplanars,
            exercici_vectors_ortogonals_parametre,
        ]
    return random.choice(generadors)()


# ============================================================
# SISTEMES D'EQUACIONS LINEALS AVANÇATS
# ============================================================

def _latex_system(A, b):
    """Construeix un sistema amb LaTeX simple i compatible amb Streamlit/KaTeX."""
    n = A.rows
    vars_ = [sp.Symbol(chr(ord("x") + i)) for i in range(n)]
    eqs = []
    for i in range(n):
        lhs = sp.Add(*[A[i, j] * vars_[j] for j in range(n)]).doit()
        eqs.append(f"{sp.latex(lhs)}={sp.latex(b[i])}")
    return r"\\begin{aligned}" + r"\\".join(eqs) + r"\\end{aligned}"


def _solution_list(A, b):
    """Solució única com llista ordenada de SymPy."""
    sol = A.LUsolve(b)
    return [sp.simplify(v) for v in sol]


def _solution_text(solution):
    names = ['x', 'y', 'z', 'w'][:len(solution)]
    return ", ".join(f"{name}={sp.latex(value)}" for name, value in zip(names, solution))


def _gauss_jordan_steps(A, b):
    """Retorna una seqüència de transformacions Gauss-Jordan exactes."""
    M = A.row_join(b)
    rows, cols = M.rows, M.cols
    steps = ["Matriu ampliada inicial:", f"$$ {sp.latex(M)} $$"]
    pivot_row = 0

    for col in range(cols - 1):
        pivot = None
        for r in range(pivot_row, rows):
            if sp.simplify(M[r, col]) != 0:
                pivot = r
                break
        if pivot is None:
            continue

        if pivot != pivot_row:
            M.row_swap(pivot, pivot_row)
            steps.append(f"Intercanviem $F_{pivot+1}$ i $F_{pivot_row+1}$:")
            steps.append(f"$$ {sp.latex(M)} $$")

        pivot_value = sp.simplify(M[pivot_row, col])
        if pivot_value != 1:
            M.row_op(pivot_row, lambda v, _: sp.simplify(v / pivot_value))
            steps.append(f"Dividim $F_{pivot_row+1}$ per ${sp.latex(pivot_value)}$:")
            steps.append(f"$$ {sp.latex(M)} $$")

        for r in range(rows):
            if r == pivot_row:
                continue
            factor = sp.simplify(M[r, col])
            if factor != 0:
                M.row_op(r, lambda v, j: sp.simplify(v - factor * M[pivot_row, j]))
                sign = "-" if factor > 0 else "+"
                absf = sp.latex(abs(factor))
                steps.append(f"$F_{r+1} \\leftarrow F_{r+1} {sign} {absf}F_{pivot_row+1}$:")
                steps.append(f"$$ {sp.latex(M)} $$")

        pivot_row += 1
        if pivot_row == rows:
            break

    return "\n\n".join(steps), M


def exercici_sistema_2x2_scd():
    while True:
        A = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
        if A.det() != 0:
            break
    sol = _solution_list(A, sp.Matrix([random.randint(-8, 8) for _ in range(2)]))
    b = A * sp.Matrix(sol)
    passos = f"""
El determinant de la matriu de coeficients és:

$$
\\Delta=\\det(A)={sp.latex(A.det())}\\neq0
$$

Per tant, pel teorema de Rouché-Frobenius, el sistema és **compatible determinat (SCD)** i té una única solució.

Resolent el sistema, obtenim:

**Solució:** $${_solution_text(sol)}$$
"""
    return {
        "enunciat": f"""
Resol el sistema:

$$
{_latex_system(A,b)}
$$

Escriu la resposta com `x=..., y=...`.
""",
        "resposta": [sol],
        "tipus_resposta": "sistema",
        "passos": passos,
    }


def exercici_sistema_2x2_gauss():
    while True:
        A = sp.Matrix([[random.randint(-5, 5) for _ in range(2)] for _ in range(2)])
        if A.det() != 0:
            break
    x, y = [random.randint(-6, 6) for _ in range(2)]
    sol = [sp.Integer(x), sp.Integer(y)]
    b = A * sp.Matrix(sol)
    steps, _ = _gauss_jordan_steps(A, b)
    return {
        "enunciat": f"""
Resol el sistema mitjançant **Gauss-Jordan**:

$$
{_latex_system(A,b)}
$$

Escriu la resposta com `x=..., y=...`.
""",
        "resposta": [sol],
        "tipus_resposta": "sistema",
        "passos": f"""
A partir de la matriu ampliada $[A|b]$, apliquem Gauss-Jordan:

{steps}

Per tant:

**Solució:** $${_solution_text(sol)}$$
""",
    }


def exercici_sistema_3x3_cramer():
    while True:
        A = sp.Matrix([[random.randint(-4, 4) for _ in range(3)] for _ in range(3)])
        if A.det() != 0:
            break
    sol = [sp.Integer(random.randint(-5, 5)) for _ in range(3)]
    b = A * sp.Matrix(sol)
    det_a = sp.expand(A.det())
    determinants = []
    for j in range(3):
        Aj = A.copy()
        Aj[:, j] = b
        determinants.append(sp.expand(Aj.det()))

    passos = f"""
Pel mètode de Cramer, primer calculem:

$$
\\Delta=\\det(A)={sp.latex(det_a)}\\neq0
$$

Substituint successivament la columna de $x$, $y$ i $z$ pel terme independent:

$$
\\Delta_x={sp.latex(determinants[0])},\\qquad
\\Delta_y={sp.latex(determinants[1])},\\qquad
\\Delta_z={sp.latex(determinants[2])}
$$

Així:

$$
x=\\frac{{\\Delta_x}}{{\\Delta}}={sp.latex(sol[0])},\\quad
 y=\\frac{{\\Delta_y}}{{\\Delta}}={sp.latex(sol[1])},\\quad
 z=\\frac{{\\Delta_z}}{{\\Delta}}={sp.latex(sol[2])}
$$

**Solució:** $${_solution_text(sol)}$$
"""
    return {
        "enunciat": f"""
Resol el sistema **mitjançant la regla de Cramer**:

$$
{_latex_system(A,b)}
$$

Escriu la resposta com `x=..., y=..., z=...`.
""",
        "resposta": [sol],
        "tipus_resposta": "sistema",
        "passos": passos,
    }


def exercici_sistema_3x3_gauss_jordan():
    while True:
        A = sp.Matrix([[random.randint(-3, 3) for _ in range(3)] for _ in range(3)])
        if A.det() != 0:
            break
    sol = [sp.Integer(random.randint(-4, 4)) for _ in range(3)]
    b = A * sp.Matrix(sol)
    steps, rref = _gauss_jordan_steps(A, b)
    return {
        "enunciat": f"""
Resol el sistema mitjançant **Gauss-Jordan**:

$$
{_latex_system(A,b)}
$$

Escriu la resposta com `x=..., y=..., z=...`.
""",
        "resposta": [sol],
        "tipus_resposta": "sistema",
        "passos": f"""
Escrivim la matriu ampliada:

$$
[A|b]
$$

Apliquem operacions elementals de fila fins arribar a la forma reduïda:

{steps}

La matriu reduïda final és:

$$
{sp.latex(rref)}
$$

Per tant:

**Solució:** $${_solution_text(sol)}$$
""",
    }


def exercici_rouche_2x2():
    # Construïm un cas SCI o SI de manera controlada.
    tipus = random.choice(["SCI", "SI"])
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    k = random.randint(-6, 6)
    A = sp.Matrix([[a, b], [2*a, 2*b]])
    if tipus == "SCI":
        c = random.randint(-6, 6)
        rhs = sp.Matrix([c, 2*c])
    else:
        c = random.randint(-6, 6)
        rhs = sp.Matrix([c, 2*c + random.choice([-2, 2])])

    aug = A.row_join(rhs)
    rank_a = A.rank()
    rank_aug = aug.rank()
    if rank_a == rank_aug and rank_a < 2:
        classificacio = "SCI"
        text = "sistema compatible indeterminat"
    else:
        classificacio = "SI"
        text = "sistema incompatible"

    passos = f"""
Calculem els rangs:

$$
\\operatorname{{rang}}(A)={rank_a},\\qquad
\\operatorname{{rang}}(A^*)={rank_aug}
$$

Segons Rouché-Frobenius:

- si $\\operatorname{{rang}}(A)=\\operatorname{{rang}}(A^*)=n$, és SCD;
- si $\\operatorname{{rang}}(A)=\\operatorname{{rang}}(A^*)<n$, és SCI;
- si $\\operatorname{{rang}}(A)\\neq\\operatorname{{rang}}(A^*)$, és SI.

Per tant, aquest sistema és:

**Per tant:** **{text} ({classificacio}).**
"""
    return {
        "enunciat": f"""
**Discuteix i classifica** el sistema segons Rouché-Frobenius.

$$
{_latex_system(A,rhs)}
$$

Escriu `SCD`, `SCI` o `SI`.
""",
        "resposta": [classificacio],
        "tipus_resposta": "classificacio",
        "passos": passos,
    }


def exercici_rouche_parametre():
    # Casos 2x2 amb paràmetre on la classificació canvia.
    k = sp.Symbol("k")
    # x + y = 2
    # 2x + 2y = k
    # k=4 -> SCI; qualsevol altre -> SI. Per a SCD, el generador mitjà ja cobreix casos.
    A = sp.Matrix([[1, 1], [2, 2]])
    b = sp.Matrix([2, k])
    passos = f"""
La matriu de coeficients és:

$$
A={matriu_text(A)},\\qquad
A^*={matriu_text(A.row_join(b))}
$$

Sempre tenim:

$$
\\operatorname{{rang}}(A)=1
$$

Si $k=4$, la segona equació és el doble de la primera i:

$$
\\operatorname{{rang}}(A)=\\operatorname{{rang}}(A^*)=1<2
$$

Per tant, hi ha **infinites solucions (SCI)**.

Si $k\\neq4$, els rangs són diferents i el sistema és **incompatible (SI)**.

**Resultat:** $k=4 \\Rightarrow SCI$ i $k\\neq4 \\Rightarrow SI$.
"""
    return {
        "enunciat": """
Discuteix segons Rouché-Frobenius el sistema amb paràmetre $k$:

$$
x+y=2\\
2x+2y=k
$$

Indica per a quin valor de $k$ hi ha infinites solucions i què passa per als altres valors.
""",
        "resposta": ["4"],
        "tipus_resposta": "parametre_rouche",
        "passos": passos,
    }


def exercici_rouche_3x3_scd():
    while True:
        A = sp.Matrix([[random.randint(-3, 3) for _ in range(3)] for _ in range(3)])
        if A.det() != 0:
            break
    sol = [sp.Integer(random.randint(-4, 4)) for _ in range(3)]
    b = A * sp.Matrix(sol)
    aug = A.row_join(b)
    passos = f"""
Calculem els rangs:

$$
\\operatorname{{rang}}(A)={A.rank()},\\qquad
\\operatorname{{rang}}(A^*)={aug.rank()}
$$

Com que tots dos rangs són 3:

$$
\\operatorname{{rang}}(A)=\\operatorname{{rang}}(A^*)=3=n
$$

El sistema és **compatible determinat (SCD)** i té una única solució.

**Solució:** $${_solution_text(sol)}$$
"""
    return {
        "enunciat": f"""
Discuteix i resol el sistema aplicant Rouché-Frobenius:

$$
{_latex_system(A,b)}
$$

Indica el tipus de sistema i la solució.
""",
        "resposta": [sol],
        "tipus_resposta": "sistema",
        "passos": passos,
    }


def exercici_rouche_3x3_parametre():
    # Sistema amb una discussió real: per k != 4 és SCD;
    # per k = 4 es transforma en SI.
    k = sp.Symbol("k")
    A = sp.Matrix([
        [1, 1, 1],
        [1, 2, 3],
        [2, 3, k],
    ])
    b = sp.Matrix([3, 6, 9])

    det_expr = sp.factor(A.det())
    # Per k=4, la tercera fila dels coeficients és F1+F2,
    # però el terme independent és 8 en lloc de 9, de manera que és SI.
    b = sp.Matrix([3, 6, 8])
    aug = A.row_join(b)

    # det(A) = k - 4. Per k != 4, SCD.
    passos = f"""
Calculem el determinant de la matriu de coeficients:

$$
\\det(A)={sp.latex(det_expr)}=k-4
$$

### Cas 1: $k\\neq4$

Si $k\\neq4$:

$$
\\det(A)\\neq0\\Rightarrow\\operatorname{{rang}}(A)=3
$$

Per tant, el sistema és **SCD** i té una única solució.

### Cas 2: $k=4$

Si $k=4$, tenim:

$$
A={matriu_text(A.subs(k,4))}
$$

En aquest cas:

$$
\\operatorname{{rang}}(A)=2,
\\qquad
\\operatorname{{rang}}(A^*)=3
$$

Com que els rangs són diferents, el sistema és **SI**.

Per tant:

**Resultat:** $k=4 \\Rightarrow SI$ i $k\\neq4 \\Rightarrow SCD$.
"""
    return {
        "enunciat": """
Discuteix segons Rouché-Frobenius el sistema en funció de $k$:

$$
\\left\\{\\begin{aligned}
x+y+z=3\\\\
x+2y+3z=6\\\\
2x+3y+kz=8
\\end{aligned}\\right.
$$

Indica per a quin valor de $k$ el sistema és incompatible i què passa per a la resta de valors.
""",
        "resposta": ["4"],
        "tipus_resposta": "parametre_rouche",
        "passos": passos,
    }


def generar_exercici_sistemes(dificultat):
    if dificultat == "Fàcil":
        generadors = [
            exercici_sistema_2x2_scd,
            exercici_sistema_2x2_gauss,
            exercici_rouche_2x2,
        ]
    elif dificultat == "Mitjà":
        generadors = [
            exercici_sistema_3x3_cramer,
            exercici_sistema_3x3_gauss_jordan,
            exercici_rouche_3x3_scd,
            exercici_rouche_parametre,
        ]
    else:
        generadors = [
            exercici_rouche_3x3_parametre,
            exercici_sistema_3x3_cramer,
            exercici_sistema_3x3_gauss_jordan,
            exercici_rouche_parametre,
        ]
    return random.choice(generadors)()

def generar_exercici_matrius(dificultat):
    if dificultat == "Fàcil":
        generadors = [
            exercici_det_2x2,
            exercici_matriu_triangular,
            exercici_suma_matrius,
            exercici_resta_matrius,
            exercici_transposada,
        ]
    elif dificultat == "Mitjà":
        generadors = [
            exercici_det_3x3,
            exercici_element_determinant,
            exercici_propietat_escalar,
            exercici_producte_determinants,
            exercici_producte_matrius,
            exercici_inversa_2x2,
            exercici_rang_2x2,
            exercici_matriu_equacio_escalar,
        ]
    else:
        # En difícil només entren problemes que requereixen
        # paràmetres, 3x3, rang, inversa o propietats avançades.
        generadors = [
            exercici_parametre_3x3,
            exercici_element_determinant_3x3,
            exercici_determinant_potencia,
            exercici_determinant_inversa,
            exercici_inversa_triangular_3x3,
            exercici_rang_3x3,
        ]

    return random.choice(generadors)()


# ============================================================
# 2n MATEMÀTIQUES II — RESTA DE TEMES
# ============================================================


def _safe_limit(expr, x, value):
    return sp.simplify(sp.limit(expr, x, value))


def exercici_recta_punt_parametre():
    P = sp.Matrix([random.randint(-5,5) for _ in range(3)])
    v = sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    t = random.randint(-3,3)
    Q = P + t*v
    passos=f"""
Una recta en forma paramètrica és:

$$
(x,y,z)=P+t\\vec v
$$

Per al punt $Q$, imposem $P+t\\vec v=Q$. En aquest cas:

$$
t={t}
$$

Per tant, $Q$ pertany a la recta i el paràmetre és $t={t}$.
"""
    return {"enunciat":f"""
Sigui la recta que passa per
$$P={sp.latex(P)}$$
amb vector director
$$\\vec v={_vector_latex(v)}.$$
Troba el valor de $t$ perquè el punt $Q$ pertanyi a la recta:
$$Q={sp.latex(Q)}$$
""", "resposta":[t], "tipus_resposta":"escalar", "passos":passos}


def exercici_rectes_posicio():
    # Two lines are either parallel or secant; ask classification.
    P=sp.Matrix([random.randint(-4,4) for _ in range(3)])
    v=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    if random.choice([True,False]):
        Q=P+random.randint(-3,3)*v+sp.Matrix([0,0,random.choice([-1,1])])
        w=v
        # parallel distinct (choose Q not on line by forcing a perturbation perpendicular-ish)
        while Q==P:
            Q=P+sp.Matrix([1,0,0])
        clas="PARAL·LELES"
        text="paral·leles"
    else:
        Q=sp.Matrix([random.randint(-4,4) for _ in range(3)])
        w=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
        # construct a guaranteed intersection point R
        R=P+random.randint(-2,2)*v
        Q=R-random.randint(-2,2)*w
        clas="SECANTS"
        text="secants"
    passos=f"""
Comparem els vectors directors i busquem si les rectes comparteixen algun punt.

En aquest cas, la posició relativa és **{text}**.

Per tant, la classificació és:
$$\\boxed{{{clas}}}$$
"""
    return {"enunciat":f"""
Determina la posició relativa de les rectes $r$ i $s$.

$$r:\\ (x,y,z)={sp.latex(P)}+t{_vector_latex(v)}$$

$$s:\\ (x,y,z)={sp.latex(Q)}+u{_vector_latex(w)}$$

Escriu `PARAL·LELES` o `SECANTS`.
""", "resposta":[clas], "tipus_resposta":"classificacio", "passos":passos}


def exercici_plano_normal():
    P=sp.Matrix([random.randint(-4,4) for _ in range(3)])
    n=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    # ask d in ax+by+cz+d=0
    d=-(n.dot(P))
    passos=f"""
Un pla amb vector normal $\\vec n=(a,b,c)$ té equació:

$$
ax+by+cz+d=0.
$$

Com que $P$ pertany al pla:

$$
{sp.latex(n.dot(P))}+d=0.
$$

Per tant:
$$d={sp.latex(d)}.$$
"""
    return {"enunciat":f"""
Un pla passa pel punt $P={sp.latex(P)}$ i té vector normal
$$\\vec n={_vector_latex(n)}.$$
Troba el terme independent $d$ de l'equació $ax+by+cz+d=0$.
""", "resposta":[d], "passos":passos}


def exercici_recta_plano_interseccio():
    P=sp.Matrix([random.randint(-3,3) for _ in range(3)])
    v=sp.Matrix([random.choice([-2,-1,1,2]) for _ in range(3)])
    n=sp.Matrix([random.choice([-2,-1,1,2]) for _ in range(3)])
    # choose plane through a known intersection Q=P+t*v
    t=random.randint(-2,2)
    Q=P+t*v
    d=-(n.dot(Q))
    # ask parameter t of intersection, but it is unique only if n.v != 0
    while n.dot(v)==0:
        n=sp.Matrix([random.choice([-2,-1,1,2]) for _ in range(3)])
        d=-(n.dot(Q))
    sol=sp.solve(sp.Eq(n.dot(P)+sp.Symbol('u')*n.dot(v)+d,0), sp.Symbol('u'))[0]
    passos=f"""
Substituïm la recta al pla:

$$
\\vec n\\cdot(P+u\\vec v)+d=0.
$$

Això dona una equació lineal en $u$ i resulta:
$$u={sp.latex(sol)}.$$
"""
    return {"enunciat":f"""
Troba el paràmetre $u$ del punt d'intersecció entre:

$$r:(x,y,z)={sp.latex(P)}+u{_vector_latex(v)}$$

$$\\pi: {sp.latex(n[0])}x+{sp.latex(n[1])}y+{sp.latex(n[2])}z+{sp.latex(d)}=0$$
""", "resposta":[sol], "passos":passos}


def exercici_rectes_plans_avancat():
    # Ask whether a line is parallel to a plane.
    v=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    n=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    if random.choice([True,False]):
        # construct perpendicular? n dot v = 0 => line parallel plane
        n=sp.Matrix([v[1],-v[0],0])
        if n==sp.zeros(3,1): n=sp.Matrix([0,v[2],-v[1]])
        clas="PARAL·LELA"
    else:
        clas="SECANT"
        while n.dot(v)==0:
            n=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    passos=f"""
Una recta és paral·lela a un pla quan el vector director és perpendicular al vector normal:
$$\\vec v\\cdot\\vec n=0.$$

En aquest cas, la classificació és **{clas.lower()}**.
"""
    return {"enunciat":f"""
Sigui una recta amb vector director
$$\\vec v={_vector_latex(v)}$$
i un pla amb vector normal
$$\\vec n={_vector_latex(n)}.$$
Indica si la recta és `PARAL·LELA` o `SECANT` al pla.
""", "resposta":[clas], "tipus_resposta":"classificacio", "passos":passos}


def generar_exercici_rectes_plans(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_recta_punt_parametre, exercici_plano_normal, exercici_rectes_posicio])()
    if dificultat=="Mitjà": return random.choice([exercici_recta_plano_interseccio, exercici_rectes_posicio, exercici_rectes_plans_avancat, exercici_plano_normal])()
    return random.choice([exercici_recta_plano_interseccio, exercici_rectes_plans_avancat, exercici_rectes_posicio])()


def exercici_angle_vectors():
    u=sp.Matrix([1,0,0])
    angle=random.choice([30,45,60,90])
    # construct v with simple exact cosine via angle, but answer angle itself
    # use u=(1,0,0), v=(cos theta, sin theta,0), then ask angle
    passos=f"""
Fem servir:
$$\\cos\\theta=\\frac{{\\vec u\\cdot\\vec v}}{{|\\vec u||\\vec v|}}.$$

En aquest cas el valor del cosinus correspon a $\\theta={angle}^\\circ$.
"""
    c=sp.cos(sp.pi*angle/180)
    v=sp.Matrix([c, sp.sin(sp.pi*angle/180), 0])
    return {"enunciat":f"""
Calcula l'angle entre:
$$\\vec u=(1,0,0),\\qquad \\vec v={_vector_latex(v)}.$$
Dona la resposta en graus.
""", "resposta":[angle], "passos":passos}


def exercici_distancia_punt_plano():
    P=sp.Matrix([random.randint(-5,5) for _ in range(3)])
    n=sp.Matrix([random.choice([-3,-2,-1,1,2,3]) for _ in range(3)])
    d=random.randint(-5,5)
    num=sp.Abs(n.dot(P)+d)
    den=sp.sqrt(n.dot(n))
    dist=sp.simplify(num/den)
    passos=f"""
La distància d'un punt al pla és:
$$d(P,\\pi)=\\frac{{|ax_0+by_0+cz_0+d|}}{{\\sqrt{{a^2+b^2+c^2}}}}.$$

Substituïm i obtenim:
$$d={sp.latex(dist)}.$$
"""
    return {"enunciat":f"""
Calcula la distància del punt $P={sp.latex(P)}$ al pla
$$ {sp.latex(n[0])}x+{sp.latex(n[1])}y+{sp.latex(n[2])}z+{d}=0.$$
""", "resposta":[dist], "passos":passos}


def exercici_distancia_dos_punts():
    A=sp.Matrix([random.randint(-5,5) for _ in range(3)])
    B=sp.Matrix([random.randint(-5,5) for _ in range(3)])
    dist=sp.sqrt(sum((B[i]-A[i])**2 for i in range(3)))
    return {"enunciat":f"Calcula la distància entre $A={sp.latex(A)}$ i $B={sp.latex(B)}$.", "resposta":[sp.simplify(dist)], "passos":f"La fórmula és $d(A,B)=\\sqrt{{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}}$.\n\n$$d={sp.latex(dist)}.$$"}


def exercici_area_triangle_espai():
    u=sp.Matrix([random.randint(-3,3) for _ in range(3)])
    v=sp.Matrix([random.randint(-3,3) for _ in range(3)])
    while u.cross(v)==sp.zeros(3,1): v=sp.Matrix([random.randint(-3,3) for _ in range(3)])
    area=sp.simplify(sp.sqrt(u.cross(v).dot(u.cross(v)))/2)
    return {"enunciat":f"Calcula l'àrea del triangle definit pels vectors $\\vec u={_vector_latex(u)}$ i $\\vec v={_vector_latex(v)}$.", "resposta":[area], "passos":f"L'àrea és la meitat de la del paral·lelogram:\n\n$$A=\\frac12|\\vec u\\times\\vec v|={sp.latex(area)}.$$"}


def exercici_angle_planes():
    n1=sp.Matrix([1,0,0]); n2=sp.Matrix([random.choice([1,-1]),1,0])
    # angle between normals: 45 or 135; use acute angle
    angle=45
    return {"enunciat":f"Calcula l'angle agut entre els plans amb normals $\\vec n_1={_vector_latex(n1)}$ i $\\vec n_2={_vector_latex(n2)}$.", "resposta":[angle], "passos":"L'angle entre plans és l'angle agut entre els seus vectors normals. En aquest cas és $45^\\circ$."}


def generar_exercici_metics(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_distancia_dos_punts, exercici_angle_vectors])()
    if dificultat=="Mitjà": return random.choice([exercici_distancia_punt_plano, exercici_area_triangle_espai, exercici_angle_vectors])()
    return random.choice([exercici_distancia_punt_plano, exercici_area_triangle_espai, exercici_angle_planes, exercici_angle_vectors])()


def exercici_limit_directe():
    x=sp.Symbol('x'); a=random.randint(-4,4); n=random.randint(1,5)
    expr=(x**2 + n*x + a)
    val=sp.simplify(expr.subs(x,a))
    return {"enunciat":f"Calcula $\\lim_{{x\\to {a}}}({sp.latex(expr)})$.", "resposta":[val], "passos":f"Com que el polinomi és continu, substituïm directament:\n\n$$L={sp.latex(val)}.$$"}


def exercici_limit_factor():
    x=sp.Symbol('x'); a=random.randint(-4,4); m=random.choice([2,3,4]); b=random.randint(-5,5)
    expr=((x-a)*(x+b))/(x-a)
    val=sp.simplify((x+b).subs(x,a))
    return {"enunciat":f"Calcula $\\lim_{{x\\to {a}}} {sp.latex(expr)}$.", "resposta":[val], "passos":f"Per $x\\neq{a}$ simplifiquem el factor $x-{a}$:\n\n$$\\frac{{(x-{a})(x+{b})}}{{x-{a}}}=x+{b}.$$\n\nAleshores $L={sp.latex(val)}$."}


def exercici_limit_infinf():
    x=sp.Symbol('x'); a=random.randint(1,5); b=random.randint(1,5)
    expr=(a*x**2+b)/(2*x**2+1)
    val=sp.Rational(a,2)
    return {"enunciat":f"Calcula $\\lim_{{x\\to\\infty}} {sp.latex(expr)}$.", "resposta":[val], "passos":f"Dividim numerador i denominador per $x^2$. El límit és el quocient dels coeficients principals:\n\n$$L=\\frac{{{a}}}{{2}}={sp.latex(val)}.$$"}


def exercici_limit_lhopital():
    x=sp.Symbol('x'); a=random.randint(1,4)
    expr=(sp.exp(x-a)-1)/(x-a)
    val=1
    return {"enunciat":f"Calcula $\\lim_{{x\\to {a}}}\\frac{{e^{{x-{a}}}-1}}{{x-{a}}}$.", "resposta":[val], "passos":"És una indeterminació $0/0$. Aplicant L'Hôpital:\n\n$$L=\\lim\\frac{e^{x-a}}{1}=1.$$"}


def exercici_limit_arrel():
    x=sp.Symbol('x'); a=random.randint(1,5); b=random.randint(1,5)
    expr=(sp.sqrt(x+b)-sp.sqrt(a+b))/(x-a)
    val=sp.Rational(1,2)/sp.sqrt(a+b)
    return {"enunciat":f"Calcula $\\lim_{{x\\to {a}}} {sp.latex(expr)}$.", "resposta":[val], "passos":f"Racionalitzem el quocient i simplifiquem. El resultat és:\n\n$$L={sp.latex(val)}.$$"}


def generar_exercici_limits(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_limit_directe, exercici_limit_factor])()
    if dificultat=="Mitjà": return random.choice([exercici_limit_factor, exercici_limit_infinf, exercici_limit_arrel])()
    return random.choice([exercici_limit_lhopital, exercici_limit_arrel, exercici_limit_infinf])()


def exercici_continu_parametre():
    a=random.randint(-3,3); b=random.randint(-4,4)
    if a==0: a=2
    k=sp.Integer(a)
    return {"enunciat":f"Troba $k$ perquè la funció sigui contínua a $x={a}$:\n\nPer $x<{a}$: $$f(x)=x^2+{b}$$\n\nPer $x\\ge {a}$: $$f(x)=kx+{b}$$", "resposta":[k], "passos":f"Igualem els límits laterals i el valor de la funció:\n\n$$a^2+b=ka+b.$$\n\nCom que $a={a}$, obtenim $k={k}$."}


def exercici_bolzano():
    # Ask existence yes, construct f=x^3-2 on [1,2]
    f=lambda t:t**3-2
    exists=f(1)*f(2)<0
    return {"enunciat":"Segons el teorema de Bolzano, existeix almenys un zero de $f(x)=x^3-2$ a l'interval $[1,2]$? Escriu `SI` o `NO`.", "resposta":["SI" if exists else "NO"], "tipus_resposta":"classificacio_vector", "passos":"$f(1)=-1$ i $f(2)=6$. Com que canvia de signe i la funció és contínua, Bolzano garanteix almenys un zero dins de l'interval. **Resposta: SI.**"}


def exercici_rolle():
    a=random.randint(-3,0); b=random.randint(1,4)
    # f=x^2 -(a+b)x + ab has equal endpoint values and derivative zero at midpoint
    c=a+b
    x=sp.Symbol('x'); f=x**2-c*x+a*b; sol=sp.Rational(c,2)
    return {"enunciat":f"Aplica Rolle a $f(x)=x^2-{c}x+{a*b}$ en $[{a},{b}]$ i troba el valor de $c$ on $f'(c)=0$.", "resposta":[sol], "passos":f"Derivem: $$f'(x)=2x-{c}.$$\n\nImposem $f'(c_0)=0$: $$2c_0-{c}=0\\Rightarrow c_0={sp.latex(sol)}.$$"}


def exercici_valor_mitja():
    a=0; b=random.randint(2,6); x=sp.Symbol('x'); f=x**2
    c=sp.Rational(b,2)
    return {"enunciat":f"Pel teorema del valor mitjà, troba $c\\in(0,{b})$ per a $f(x)=x^2$.", "resposta":[c], "passos":f"La pendent mitjana és $({b}^2-0)/{b}={b}$. Com que $f'(x)=2x$, imposem $2c={b}$.\n\n$$c={sp.latex(c)}.$$"}


def exercici_weierstrass():
    return {"enunciat":"La funció $f(x)=x^2$ té un màxim i un mínim absoluts en $[-2,1]$? Escriu `SI` o `NO`.", "resposta":["SI"], "tipus_resposta":"classificacio_vector", "passos":"És contínua i està definida en un interval tancat i acotat. Pel teorema de Weierstrass, assoleix màxim i mínim absoluts. **Resposta: SI.**"}


def generar_exercici_continuïtat(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_bolzano, exercici_weierstrass])()
    if dificultat=="Mitjà": return random.choice([exercici_continu_parametre, exercici_rolle, exercici_valor_mitja])()
    return random.choice([exercici_continu_parametre, exercici_rolle, exercici_valor_mitja, exercici_bolzano])()


def exercici_derivada_punt():
    x=sp.Symbol('x'); a=random.randint(-3,3); p=random.randint(2,4); q=random.randint(-3,3)
    f=x**p+q*x
    val=sp.diff(f,x).subs(x,a)
    return {"enunciat":f"Calcula $f'({a})$ per a $f(x)={sp.latex(f)}$.", "resposta":[val], "passos":f"$$f'(x)={sp.latex(sp.diff(f,x))}.$$\n\nSubstituïm $x={a}$:\n$$f'({a})={sp.latex(val)}.$$"}


def exercici_tangent_slope():
    x=sp.Symbol('x'); a=random.randint(-3,3); m=random.randint(1,5)
    f=x**2+m*x
    slope=sp.diff(f,x).subs(x,a)
    return {"enunciat":f"Troba el pendent de la tangent a $f(x)={sp.latex(f)}$ en $x={a}$.", "resposta":[slope], "passos":f"Derivem: $$f'(x)={sp.latex(sp.diff(f,x))}.$$\n\nEl pendent és $f'({a})={sp.latex(slope)}$."}


def exercici_critical_points_count():
    x=sp.Symbol('x'); a=random.choice([1,2,3]); f=x**3-3*a*x
    crit=sp.solve(sp.Eq(sp.diff(f,x),0),x)
    return {"enunciat":f"Quants punts crítics té $f(x)={sp.latex(f)}$?", "resposta":[len(crit)], "passos":f"$$f'(x)={sp.latex(sp.diff(f,x))}.$$\n\nEls punts crítics compleixen $f'(x)=0$ i són $x={sp.latex(crit[0])}$ i $x={sp.latex(crit[1])}$. Per tant, n'hi ha **{len(crit)}**."}


def exercici_monotonia_sign():
    x=sp.Symbol('x'); a=random.randint(1,4); f=x**2-a*x
    # ask derivative zero point
    c=sp.Rational(a,2)
    return {"enunciat":f"Per a $f(x)={sp.latex(f)}$, troba el valor de $x$ on pot canviar el sentit de creixement/decreixement.", "resposta":[c], "passos":f"$$f'(x)=2x-{a}.$$\n\nIgualem a zero: $$2x-{a}=0\\Rightarrow x={sp.latex(c)}.$$"}


def generar_exercici_derivabilitat(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_derivada_punt, exercici_tangent_slope])()
    if dificultat=="Mitjà": return random.choice([exercici_tangent_slope, exercici_critical_points_count, exercici_monotonia_sign])()
    return random.choice([exercici_critical_points_count, exercici_monotonia_sign, exercici_derivada_punt])()


def exercici_opt_rectangle():
    P=random.choice([20,24,30,40]); x=sp.symbols('x', positive=True)
    y=sp.Rational(P,2)-x; area=sp.expand(x*y); xm=sp.Rational(P,4); maxa=sp.simplify(area.subs(x,xm))
    return {"enunciat":f"Un rectangle té perímetre {P}. Quina és la seva àrea màxima?", "resposta":[maxa], "passos":f"Si un costat és $x$, l'altre és ${P}/2-x$.\n\n$$A(x)=x({P}/2-x).$$\n\nIgualem $A'(x)=0$ i obtenim $x={sp.latex(xm)}$.\n\n$$A_{{max}}={sp.latex(maxa)}.$$"}


def exercici_opt_caixa():
    # Simple open-top box from square sheet; choose dimensions so derivative has clean root.
    L=random.choice([20,24,30]); x=sp.symbols('x', positive=True); V=x*(L-2*x)**2
    crit=sp.solve(sp.diff(V,x),x); xm=[c for c in crit if c.is_real and c>0 and c<L/2][0]
    vmax=sp.simplify(V.subs(x,xm))
    return {"enunciat":f"D'una cartolina quadrada de costat {L} cm es retallen quadrats de costat $x$ a les cantonades per formar una caixa oberta. Quina és la capacitat màxima?", "resposta":[vmax], "passos":f"$$V(x)=x({L}-2x)^2.$$\n\nDerivem i igualem a zero. El punt interior vàlid és $x={sp.latex(xm)}$.\n\n$$V_{{max}}={sp.latex(vmax)}\\,cm^3.$$"}


def exercici_opt_cost():
    a=random.choice([2,3,4]); b=random.choice([1,2,3]); x=sp.symbols('x', positive=True); f=a*x**2+b
    xmin=sp.Integer(0)
    return {"enunciat":f"Una funció de cost simplificada és $C(x)={sp.latex(f)}$ per $x\\ge0$. Quin és el valor de $x$ que minimitza el cost?", "resposta":[xmin], "passos":f"$$C'(x)={sp.latex(sp.diff(f,x))}.$$\n\nCom que $C'(x)>0$ per a $x>0$, el mínim en el domini és $x=0$."}


def generar_exercici_optimitzacio(dificultat):
    if dificultat=="Fàcil": return exercici_opt_rectangle()
    if dificultat=="Mitjà": return random.choice([exercici_opt_rectangle, exercici_opt_caixa])()
    return random.choice([exercici_opt_caixa, exercici_opt_rectangle, exercici_opt_cost])()


def exercici_integral_polinomi():
    x=sp.Symbol('x'); a=random.randint(1,5); b=random.randint(-4,4); f=a*x**2+b*x
    F=sp.integrate(f,x)
    return {"enunciat":f"Calcula una primitiva de $f(x)={sp.latex(f)}$ (sense escriure la constant $C$).", "resposta":[F], "passos":f"Integram terme a terme:\n\n$$\\int {sp.latex(f)}dx={sp.latex(F)}+C.$$"}


def exercici_integral_definida():
    x=sp.Symbol('x'); a=random.randint(1,4); b=random.randint(a+1,6); f=x**2
    val=sp.integrate(f,(x,a,b))
    return {"enunciat":f"Calcula $\\int_{{{a}}}^{{{b}}}x^2\\,dx$.", "resposta":[val], "passos":f"Una primitiva és $F(x)=x^3/3$.\n\n$$\\int_{{{a}}}^{{{b}}}x^2dx=F({b})-F({a})={sp.latex(val)}.$$"}


def exercici_area_sota():
    x=sp.Symbol('x'); b=random.randint(1,5); f=x+1
    val=sp.integrate(f,(x,0,b))
    return {"enunciat":f"Calcula l'àrea limitada per $f(x)=x+1$, l'eix $x$ i les rectes $x=0$ i $x={b}$.", "resposta":[val], "passos":f"Com que $f(x)>0$ en l'interval, l'àrea és:\n\n$$A=\\int_0^{b}(x+1)dx={sp.latex(val)}.$$"}


def exercici_area_entre_funcions():
    x=sp.Symbol('x'); b=random.choice([1,2,3]); f=x**2; g=x
    val=sp.integrate(g-f,(x,0,b))
    return {"enunciat":f"Calcula l'àrea entre $y=x$ i $y=x^2$ en $[0,{b}]$.", "resposta":[val], "passos":f"En l'interval, $x\\ge x^2$.\n\n$$A=\\int_0^{b}(x-x^2)dx={sp.latex(val)}.$$"}


def generar_exercici_integrals(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_integral_polinomi, exercici_integral_definida])()
    if dificultat=="Mitjà": return random.choice([exercici_integral_definida, exercici_area_sota, exercici_area_entre_funcions])()
    return random.choice([exercici_integral_polinomi, exercici_area_entre_funcions, exercici_integral_definida])()


def exercici_prob_cond():
    A=random.randint(3,7); B=random.randint(3,7); both=random.randint(1,min(A,B)-1)
    # universe 20, P(A)=A/10, P(B)=B/10, intersection=both/20 is coherent enough if <= mins.
    den=20; pa=sp.Rational(A,10); pab=sp.Rational(both,20)
    pc=sp.simplify(pab/pa)
    return {"enunciat":f"En una mostra, $P(A)={sp.latex(pa)}$ i $P(A\\cap B)={sp.latex(pab)}$. Calcula $P(B|A)$.", "resposta":[pc], "passos":f"Per probabilitat condicionada:\n\n$$P(B|A)=\\frac{{P(A\\cap B)}}{{P(A)}}={sp.latex(pc)}.$$"}


def exercici_bayes():
    # two machines, defect probability
    p1=sp.Rational(3,5); p2=sp.Rational(2,5); d1=sp.Rational(1,20); d2=sp.Rational(1,10)
    total=sp.simplify(p1*d1+p2*d2); ans=sp.simplify(p1*d1/total)
    return {"enunciat":"Una peça prové de la màquina 1 amb probabilitat $3/5$ i de la màquina 2 amb $2/5$. Les taxes de defecte són $1/20$ i $1/10$. Si una peça és defectuosa, calcula la probabilitat que provingui de la màquina 1.", "resposta":[ans], "passos":f"Primer, probabilitat total de defecte:\n\n$$P(D)=\\frac35\\frac1{{20}}+\\frac25\\frac1{{10}}={sp.latex(total)}.$$\n\nPer Bayes:\n$$P(M_1|D)=\\frac{{P(M_1)P(D|M_1)}}{{P(D)}}={sp.latex(ans)}.$$"}


def exercici_prob_total():
    p1=sp.Rational(2,5); p2=sp.Rational(3,5); a1=sp.Rational(1,4); a2=sp.Rational(1,2)
    ans=sp.simplify(p1*a1+p2*a2)
    return {"enunciat":"Dos grups tenen probabilitats $2/5$ i $3/5$. La probabilitat d'un esdeveniment $A$ és $1/4$ en el primer grup i $1/2$ en el segon. Calcula $P(A)$.", "resposta":[ans], "passos":f"Per probabilitat total:\n\n$$P(A)=\\frac25\\frac14+\\frac35\\frac12={sp.latex(ans)}.$$"}


def exercici_independencia():
    pa=sp.Rational(1,2); pb=sp.Rational(2,5); pab=sp.Rational(1,5)
    ans="SI" if sp.simplify(pab-pa*pb)==0 else "NO"
    return {"enunciat":"Són independents $A$ i $B$ si $P(A)=1/2$, $P(B)=2/5$ i $P(A\\cap B)=1/5$? Escriu `SI` o `NO`.", "resposta":[ans], "tipus_resposta":"classificacio_vector", "passos":f"Dos esdeveniments són independents si $P(A\\cap B)=P(A)P(B)$.\n\nAquí $P(A)P(B)=1/5$, per tant la resposta és **{ans}**."}


def generar_exercici_prob_condicionada(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_prob_cond, exercici_prob_total])()
    if dificultat=="Mitjà": return random.choice([exercici_prob_cond, exercici_prob_total, exercici_independencia])()
    return random.choice([exercici_bayes, exercici_prob_cond, exercici_independencia])()


def exercici_binomial_prob():
    n=random.choice([5,6,8,10]); p=sp.Rational(1,2); k=random.randint(1,n-1)
    ans=sp.binomial(n,k)*p**k*(1-p)**(n-k)
    return {"enunciat":f"Sigui $X\\sim B({n},1/2)$. Calcula $P(X={k})$.", "resposta":[ans], "passos":f"$$P(X=k)=\\binom nk p^k(1-p)^{{n-k}}.$$\n\nSubstituïm:\n$$P(X={k})={sp.latex(ans)}.$$"}


def exercici_binomial_esperanca():
    n=random.choice([10,12,20]); p=sp.Rational(1,4); ans=n*p
    return {"enunciat":f"Si $X\\sim B({n},1/4)$, calcula l'esperança $E(X)$.", "resposta":[ans], "passos":f"Per una binomial, $E(X)=np$.\n\n$$E(X)={n}\\cdot\\frac14={sp.latex(ans)}.$$"}


def exercici_normal_z():
    mu=random.choice([50,60,70]); sigma=random.choice([5,10]); x=mu+sigma*random.choice([-2,-1,1,2])
    z=sp.Rational(x-mu,sigma)
    return {"enunciat":f"Una variable $X$ segueix una normal $N({mu},{sigma}^2)$. Calcula la puntuació tipificada $z$ per a $x={x}$.", "resposta":[z], "passos":f"Estandarditzem:\n\n$$z=\\frac{{x-\\mu}}{{\\sigma}}=\\frac{{{x}-{mu}}}{{{sigma}}}={sp.latex(z)}.$$"}


def exercici_normal_interval_sigma():
    # ask interval containing about 68%: [mu-sigma, mu+sigma]
    mu=random.choice([100,120,150]); sigma=random.choice([10,20])
    a=mu-sigma; b=mu+sigma
    return {"enunciat":f"Per a $X\\sim N({mu},{sigma}^2)$, quin interval centrat en la mitjana conté aproximadament el 68% de les dades? Dona els dos extrems com `a,b`.", "resposta":[[a,b]], "tipus_resposta":"interval", "passos":f"Per la regla 68-95-99,7, aproximadament el 68% està entre $\\mu-\\sigma$ i $\\mu+\\sigma$.\n\n$$[{a},{b}].$$"}


def interpretar_interval(text):
    parts=[p.strip() for p in text.replace(';',',').split(',') if p.strip()]
    if len(parts)!=2: raise ValueError('interval')
    return [interpretar_resposta(parts[0]), interpretar_resposta(parts[1])]


def resposta_interval_correcta(alumne, correctes):
    return any(len(alumne)==2 and all(sp.simplify(a-b)==0 for a,b in zip(alumne,r)) for r in correctes)


def generar_exercici_variables(dificultat):
    if dificultat=="Fàcil": return random.choice([exercici_binomial_prob, exercici_binomial_esperanca])()
    if dificultat=="Mitjà": return random.choice([exercici_binomial_prob, exercici_binomial_esperanca, exercici_normal_z])()
    return random.choice([exercici_binomial_prob, exercici_normal_z, exercici_normal_interval_sigma])()


def generar_exercici_mates2(dificultat, tema):
    dispatch={
        "Matrius i determinants": generar_exercici_matrius,
        "Sistemes d'equacions lineals avançats": generar_exercici_sistemes,
        "Vectors en l'espai": generar_exercici_vectors,
        "Rectes i plans en l'espai": generar_exercici_rectes_plans,
        "Problemes mètrics": generar_exercici_metics,
        "Límits avançats i indeterminacions": generar_exercici_limits,
        "Continuïtat i teoremes fonamentals": generar_exercici_continuïtat,
        "Derivabilitat i representació gràfica de funcions": generar_exercici_derivabilitat,
        "Optimització de problemes reals": generar_exercici_optimitzacio,
        "Càlcul d'integrals indefinides i definides": generar_exercici_integrals,
        "Probabilitat condicionada, Bayes i probabilitat total": generar_exercici_prob_condicionada,
        "Variables aleatòries, Binomial i Normal": generar_exercici_variables,
    }
    if tema in dispatch:
        return dispatch[tema](dificultat)
    return None


# ============================================================
# 2n FÍSICA II
# ============================================================

G = sp.Float('6.67e-11')
K_E = sp.Float('9e9')
MU0 = 4*sp.pi*sp.Float('1e-7')
H_PLANCK = sp.Float('6.626e-34')
C_LIGHT = sp.Integer(300000000)
E_CHARGE = sp.Float('1.602e-19')


def _num(v):
    return sp.N(v, 8)


def fis_gravitatori_fuerza():
    m1 = random.choice([2, 4, 5, 8]) * 1e20
    m2 = random.choice([2, 3, 6]) * 1e22
    r = random.choice([2, 3, 4, 5]) * 1e6
    F = G * m1 * m2 / r**2
    return {
        'enunciat': f"Calcula la força gravitatòria entre dues masses $m_1={m1:.0e}$ kg i $m_2={m2:.0e}$ kg separades $r={r:.0e}$ m. Dona el resultat en N.",
        'resposta': [F], 'passos': f"\n$$F=G\\frac{{m_1m_2}}{{r^2}}$$\n\n$$F=6,67\\cdot10^{{-11}}\\frac{{({m1:.0e})({m2:.0e})}}{{({r:.0e})^2}}={sp.latex(F)}\\,N.$$"
    }


def fis_gravitatori_camp():
    M = random.choice([5, 6, 8]) * 1e24
    r = random.choice([6, 8, 10]) * 1e6
    g = G * M / r**2
    return {
        'enunciat': f"Calcula la intensitat del camp gravitatori creat per una massa $M={M:.0e}$ kg a una distància $r={r:.0e}$ m. Dona el resultat en N/kg.",
        'resposta': [g], 'passos': f"$$g=G\\frac{{M}}{{r^2}}$$\n\n$$g={sp.latex(g)}\\,N/kg.$$"
    }


def fis_gravitatori_potencial():
    M = random.choice([4, 6, 8]) * 1e24
    m = random.choice([2, 3, 5]) * 1e3
    r = random.choice([2, 4, 6]) * 1e7
    U = -G * M * m / r
    return {
        'enunciat': f"Calcula l'energia potencial gravitatòria d'una massa $m={m:.0e}$ kg situada a $r={r:.0e}$ m d'una massa $M={M:.0e}$ kg. Pren $U=0$ a l'infinit.",
        'resposta': [U], 'passos': f"$$U=-G\\frac{{Mm}}{{r}}$$\n\n$$U={sp.latex(U)}\\,J.$$"
    }


def fis_gravitatori_orbita():
    M = random.choice([5, 6, 8]) * 1e24
    r = random.choice([7, 9, 12]) * 1e6
    v = sp.sqrt(G * M / r)
    return {
        'enunciat': f"Calcula la velocitat orbital d'un satèl·lit en una òrbita circular de radi $r={r:.0e}$ m al voltant d'una massa $M={M:.0e}$ kg. Dona el resultat en m/s.",
        'resposta': [v], 'passos': f"En una òrbita circular, $\\frac{{GMm}}{{r^2}}=\\frac{{mv^2}}{{r}}$.\n\nPer tant:\n$$v=\\sqrt{{\\frac{{GM}}{{r}}}}={sp.latex(v)}\\,m/s.$$"
    }


def generar_exercici_fis_gravitatori(d):
    if d == 'Fàcil': return random.choice([fis_gravitatori_fuerza, fis_gravitatori_camp])()
    if d == 'Mitjà': return random.choice([fis_gravitatori_camp, fis_gravitatori_potencial])()
    return random.choice([fis_gravitatori_potencial, fis_gravitatori_orbita])()


def fis_electric_coulomb():
    q1 = random.choice([2, 3, 4]) * 1e-6
    q2 = random.choice([2, 5, 6]) * 1e-6
    r = random.choice([0.2, 0.3, 0.5])
    F = K_E * q1 * q2 / r**2
    return {'enunciat': f"Calcula el mòdul de la força elèctrica entre dues càrregues $q_1={q1:.0e}$ C i $q_2={q2:.0e}$ C separades {r} m.", 'resposta':[F], 'passos':f"$$F=k\\frac{{|q_1q_2|}}{{r^2}}$$\n\n$$F={sp.latex(F)}\\,N.$$"}


def fis_electric_camp():
    q = random.choice([2, 4, 6]) * 1e-6
    r = random.choice([0.2, 0.4, 0.5])
    E = K_E * q / r**2
    return {'enunciat': f"Calcula el camp elèctric creat per una càrrega puntual $q={q:.0e}$ C a una distància $r={r}$ m.", 'resposta':[E], 'passos':f"$$E=k\\frac{{|q|}}{{r^2}}={sp.latex(E)}\\,N/C.$$"}


def fis_electric_potencial():
    q = random.choice([2, 3, 5]) * 1e-6
    r = random.choice([0.2, 0.5, 1.0])
    V = K_E * q / r
    return {'enunciat': f"Calcula el potencial elèctric creat per una càrrega $q={q:.0e}$ C a una distància $r={r}$ m.", 'resposta':[V], 'passos':f"$$V=k\\frac{{q}}{{r}}={sp.latex(V)}\\,V.$$"}


def fis_electric_energia():
    q1 = random.choice([2, 3]) * 1e-6; q2 = random.choice([4, 5]) * 1e-6; r = random.choice([0.2,0.5])
    U = K_E*q1*q2/r
    return {'enunciat': f"Calcula l'energia potencial electrostàtica de dues càrregues $q_1={q1:.0e}$ C i $q_2={q2:.0e}$ C separades {r} m.", 'resposta':[U], 'passos':f"$$U=k\\frac{{q_1q_2}}{{r}}={sp.latex(U)}\\,J.$$"}


def generar_exercici_fis_electric(d):
    if d=='Fàcil': return random.choice([fis_electric_coulomb, fis_electric_camp])()
    if d=='Mitjà': return random.choice([fis_electric_camp, fis_electric_potencial, fis_electric_energia])()
    return random.choice([fis_electric_energia, fis_electric_potencial, fis_electric_coulomb])()


def fis_magnetic_lorentz():
    q = random.choice([2,3,4])*1e-6; v = random.choice([2,3,5])*1e4; B=random.choice([0.2,0.4,0.5])
    F=q*v*B
    return {'enunciat': f"Una càrrega $q={q:.0e}$ C es mou perpendicularment a un camp magnètic $B={B}$ T amb velocitat $v={v:.0e}$ m/s. Calcula el mòdul de la força magnètica.", 'resposta':[F], 'passos':f"Com que $v$ i $B$ són perpendiculars, $F=|q|vB$.\n\n$$F={sp.latex(F)}\\,N.$$"}


def fis_magnetic_wire():
    I=random.choice([2,4,5]); r=random.choice([0.02,0.05,0.1]); B=MU0*I/(2*sp.pi*r)
    return {'enunciat': f"Calcula el camp magnètic a una distància $r={r}$ m d'un fil rectilini infinit pel qual circula un corrent $I={I}$ A.", 'resposta':[B], 'passos':f"$$B=\\frac{{\\mu_0 I}}{{2\\pi r}}={sp.latex(B)}\\,T.$$"}


def fis_magnetic_induccion():
    dphi=random.choice([0.02,0.04,0.06]); dt=random.choice([0.1,0.2,0.3]); emf=dphi/dt
    return {'enunciat': f"El flux magnètic a través d'una espira canvia en {dphi} Wb en {dt} s. Calcula el mòdul de la força electromotriu induïda.", 'resposta':[emf], 'passos':f"Per Faraday: $$|\\varepsilon|=\\left|\\frac{{\\Delta\\Phi}}{{\\Delta t}}\\right|={sp.latex(emf)}\\,V.$$"}


def generar_exercici_fis_magnetic(d):
    if d=='Fàcil': return random.choice([fis_magnetic_lorentz, fis_magnetic_wire])()
    if d=='Mitjà': return random.choice([fis_magnetic_wire, fis_magnetic_induccion])()
    return random.choice([fis_magnetic_lorentz, fis_magnetic_induccion, fis_magnetic_wire])()


def fis_ones_freq():
    f=random.choice([2,5,10]); lam=random.choice([0.2,0.5,1.5]); v=f*lam
    return {'enunciat': f"Una ona té freqüència $f={f}$ Hz i longitud d'ona $\\lambda={lam}$ m. Calcula la velocitat de propagació.", 'resposta':[v], 'passos':f"$$v=\\lambda f={lam}\\cdot{f}={sp.latex(v)}\\,m/s.$$"}


def fis_ones_wavelength():
    v=random.choice([300,340,500]); f=random.choice([2,4,5,10]); lam=sp.Rational(v,f)
    return {'enunciat': f"Una ona es propaga a $v={v}$ m/s amb freqüència $f={f}$ Hz. Calcula $\\lambda$.", 'resposta':[lam], 'passos':f"$$\\lambda=\\frac{{v}}{{f}}={sp.latex(lam)}\\,m.$$"}


def fis_ones_energia_foton():
    f=random.choice([4,5,6])*1e14; E=H_PLANCK*f
    return {'enunciat': f"Calcula l'energia d'un fotó de freqüència $f={f:.0e}$ Hz.", 'resposta':[E], 'passos':f"$$E=hf={sp.latex(E)}\\,J.$$"}


def generar_exercici_fis_ones(d):
    if d=='Fàcil': return fis_ones_freq()
    if d=='Mitjà': return random.choice([fis_ones_freq,fis_ones_wavelength])()
    return random.choice([fis_ones_wavelength,fis_ones_energia_foton])()


def fis_optica_snell():
    n1=random.choice([1.0,1.33]); n2=random.choice([1.5,1.6,2.0]); angle=random.choice([30,45,60])
    s=sp.sin(sp.pi*angle/180)*n1/n2
    if abs(float(s))>1: return fis_optica_snell()
    theta2=sp.asin(s)*180/sp.pi
    return {'enunciat': f"Un raig passa d'un medi de $n_1={n1}$ a un altre de $n_2={n2}$ amb angle d'incidència $\\theta_1={angle}^\\circ$. Calcula l'angle de refracció.", 'resposta':[theta2], 'passos':f"Llei de Snell: $$n_1\\sin\\theta_1=n_2\\sin\\theta_2.$$\n\n$$\\theta_2={sp.latex(theta2)}^\\circ.$$"}


def fis_optica_lent():
    f=random.choice([10,20,25]); do=random.choice([20,30,40]);
    while do == f:
        do=random.choice([20,30,40])
    di=sp.simplify(f*do/(do-f))
    return {'enunciat': f"Una lent convergent té distància focal $f={f}$ cm. Un objecte es troba a $d_o={do}$ cm. Calcula la distància de la imatge $d_i$.", 'resposta':[di], 'passos':f"$$\\frac1f=\\frac1{{d_o}}+\\frac1{{d_i}}$$\n\n$$d_i=\\frac{{fd_o}}{{d_o-f}}={sp.latex(di)}\\,cm.$$"}


def fis_optica_aug():
    f=random.choice([10,20]); do=random.choice([30,40]); di=sp.simplify(f*do/(do-f)); m=-di/do
    return {'enunciat': f"Una lent convergent té $f={f}$ cm i un objecte a $d_o={do}$ cm. Calcula l'augment lineal $m=-d_i/d_o$.", 'resposta':[m], 'passos':f"Primer, $$d_i=\\frac{{fd_o}}{{d_o-f}}={sp.latex(di)}\\,cm.$$\n\nDesprés, $$m=-\\frac{{d_i}}{{d_o}}={sp.latex(m)}.$$"}


def generar_exercici_fis_optica(d):
    if d=='Fàcil': return fis_optica_snell()
    if d=='Mitjà': return random.choice([fis_optica_snell,fis_optica_lent])()
    return random.choice([fis_optica_lent,fis_optica_aug])()


def fis_moderna_photoelectric():
    f=random.choice([8,10,12])*1e14; phi=random.choice([2,3])*1.6e-19; E=H_PLANCK*f; K=E-phi
    return {'enunciat': f"En l'efecte fotoelèctric, la radiació té $f={f:.0e}$ Hz i la funció de treball del metall és $\\phi={float(phi/E_CHARGE):.1f}$ eV. Calcula l'energia cinètica màxima dels electrons en J.", 'resposta':[K], 'passos':f"$$K_{{max}}=hf-\\phi$$\n\n$$K_{{max}}={sp.latex(K)}\\,J.$$"}


def fis_moderna_relativitat():
    v=random.choice([0.6,0.8])*float(C_LIGHT); gamma=1/sp.sqrt(1-(sp.Rational(str(v/float(C_LIGHT)))**2)); t0=random.choice([1,2,5]); t=gamma*t0
    return {'enunciat': f"Un rellotge propi mesura $\\Delta t_0={t0}$ s en un objecte que es mou a $v={v/float(C_LIGHT):.1f}c$. Calcula el temps mesurat per un observador extern.", 'resposta':[t], 'passos':f"Dilatació temporal: $$\\Delta t=\\gamma\\Delta t_0,\\qquad \\gamma=\\frac1{{\\sqrt{{1-v^2/c^2}}}}.$$\n\n$$\\Delta t={sp.latex(t)}\\,s.$$"}


def fis_moderna_massa():
    dm=random.choice([1,2,5])*1e-30; E=dm*C_LIGHT**2
    return {'enunciat': f"Calcula l'energia equivalent a un defecte de massa $\\Delta m={dm:.0e}$ kg.", 'resposta':[E], 'passos':f"$$E=\\Delta mc^2={sp.latex(E)}\\,J.$$"}


def generar_exercici_fis_moderna(d):
    if d=='Fàcil': return fis_moderna_massa()
    if d=='Mitjà': return random.choice([fis_moderna_massa,fis_moderna_photoelectric])()
    return random.choice([fis_moderna_photoelectric,fis_moderna_relativitat,fis_moderna_massa])()


def generar_exercici_fisica2(dificultat, tema):
    dispatch={
        'Camp Gravitatori': generar_exercici_fis_gravitatori,
        'Camp Elèctric': generar_exercici_fis_electric,
        'Camp Magnètic': generar_exercici_fis_magnetic,
        'Ones': generar_exercici_fis_ones,
        'Òptica': generar_exercici_fis_optica,
        'Física Moderna': generar_exercici_fis_moderna,
    }
    return dispatch[tema](dificultat)


# ============================================================
# 2n QUÍMICA II
# ============================================================

def qui_estructura_config():
    elements=[('Na',11),('Cl',17),('Ca',20),('O',8),('Al',13),('K',19)]
    sym,Z=random.choice(elements)
    if Z<=20:
        levels=[]; rem=Z
        for cap in [2,8,8,2]:
            take=min(rem,cap); levels.append(take); rem-=take
            if rem==0: break
        conf=' '.join(map(str,levels))
    else: conf=str(Z)
    return {'enunciat':f"Indica la distribució electrònica per capes de l'àtom neutre de ${sym}$ ($Z={Z}$).", 'resposta':[conf], 'tipus_resposta':'text', 'passos':f"Omplim les capes començant per les de menor energia. Per $Z={Z}$, la distribució per capes és **{conf}**."}


def qui_estructura_periodica():
    pairs=[('Na','K','K té un radi atòmic més gran que Na'),('F','Cl','F té un radi atòmic més petit que Cl'),('Mg','Al','Al té una energia de ionització menor que Mg')]
    a,b,ans=random.choice(pairs)
    return {'enunciat':f"Compara ${a}$ i ${b}$. Indica quina de les dues afirmacions següents és correcta segons les propietats periòdiques: {ans}.", 'resposta':[ans], 'tipus_resposta':'text', 'passos':f"Consultem la tendència periòdica corresponent. Per a aquest parell: **{ans}**."}


def qui_enllac_polaritat():
    pairs=[('HCl','covalent polar'),('Cl2','covalent apolar'),('NaCl','iònic'),('Cu','metàl·lic')]
    mol,ans=random.choice(pairs)
    return {'enunciat':f"Indica el tipus d'enllaç predominant en ${mol}$.", 'resposta':[ans], 'tipus_resposta':'text', 'passos':f"La diferència d'electronegativitat i la naturalesa dels elements permet classificar ${mol}$ com a **{ans}**."}


def qui_forces_intermoleculars():
    pairs=[('H2O','ponts d’hidrogen'),('CH4','forces de London'),('HCl','dipol-dipol')]
    mol,ans=random.choice(pairs)
    return {'enunciat':f"Quina és la força intermolecular més característica entre molècules de ${mol}$?", 'resposta':[ans], 'tipus_resposta':'text', 'passos':f"En ${mol}$, la interacció predominant és **{ans}**."}


def generar_exercici_qui_estructura(d):
    if d=='Fàcil': return random.choice([qui_estructura_config,qui_enllac_polaritat])()
    if d=='Mitjà': return random.choice([qui_estructura_periodica,qui_forces_intermoleculars])()
    return random.choice([qui_estructura_periodica,qui_enllac_polaritat,qui_forces_intermoleculars])()


def qui_termo_q():
    m=random.choice([100,200,250]); c=random.choice([4.18,4.2,1.0]); dt=random.choice([10,20,25]); q=m*c*dt
    return {'enunciat':f"Calcula la calor absorbida per una mostra de massa $m={m}$ g, calor específica $c={c}$ J/(g·K) i increment de temperatura $\\Delta T={dt}$ K.", 'resposta':[q], 'passos':f"$$q=mc\\Delta T={m}\\cdot{c}\\cdot{dt}={sp.latex(q)}\\,J.$$"}


def qui_termo_hess():
    a=random.choice([-100,-150,-200]); b=random.choice([-50,-80,-120]); c=random.choice([-30,-40,-60]); total=a+b-c
    return {'enunciat':f"Aplicant la llei de Hess, una reacció es pot obtenir combinant tres etapes amb $\\Delta H_1={a}$ kJ, $\\Delta H_2={b}$ kJ i una etapa que s'inverteix amb $\\Delta H_3={c}$ kJ. Calcula $\\Delta H$ total.", 'resposta':[total], 'passos':f"Invertir la tercera etapa canvia el signe: $$\\Delta H={a}+({b})-({c})={sp.latex(total)}\\,kJ.$$"}


def qui_termo_gibbs():
    H=random.choice([-80,-100,-120]); T=random.choice([298,300,350]); S=random.choice([-0.1,0.2,0.3]); G=H-T*S
    return {'enunciat':f"Calcula $\\Delta G$ a $T={T}$ K si $\\Delta H={H}$ kJ/mol i $\\Delta S={S}$ kJ/(mol·K).", 'resposta':[G], 'passos':f"$$\\Delta G=\\Delta H-T\\Delta S={H}-{T}({S})={sp.latex(G)}\\,kJ/mol.$$"}


def generar_exercici_qui_termo(d):
    if d=='Fàcil': return qui_termo_q()
    if d=='Mitjà': return random.choice([qui_termo_q,qui_termo_hess])()
    return random.choice([qui_termo_hess,qui_termo_gibbs])()


def qui_cinetica_velocitat():
    dc=random.choice([0.1,0.2,0.5]); dt=random.choice([2,5,10]); v=dc/dt
    return {'enunciat':f"La concentració d'un reactiu disminueix en {dc} mol/L durant {dt} s. Calcula la velocitat mitjana de desaparició en mol·L⁻¹·s⁻¹.", 'resposta':[v], 'passos':f"$$v=-\\frac{{\\Delta[A]}}{{\\Delta t}}={sp.latex(v)}\\,mol\\,L^{{-1}}s^{{-1}}.$$"}


def qui_cinetica_factor():
    return {'enunciat':'Indica l’efecte habitual d’augmentar la temperatura sobre la velocitat d’una reacció.', 'resposta':['augmenta'], 'tipus_resposta':'text', 'passos':'En augmentar la temperatura, augmenta la fracció de xocs amb energia suficient i, en general, **augmenta la velocitat de reacció**.'}


def qui_cinetica_arrhenius():
    Ea=random.choice([40000,50000,60000]); R=8.314; T=random.choice([300,320]); k0=1e7
    k=k0*sp.exp(-Ea/(R*T))
    return {'enunciat':f"Segons Arrhenius $k=Ae^{{-E_a/(RT)}}$, calcula $k$ per $A={k0:.0e}$, $E_a={Ea}$ J/mol i $T={T}$ K.", 'resposta':[k], 'passos':f"$$k=Ae^{{-E_a/(RT)}}={sp.latex(k)}.$$"}


def generar_exercici_qui_cinetica(d):
    if d=='Fàcil': return qui_cinetica_velocitat()
    if d=='Mitjà': return random.choice([qui_cinetica_velocitat,qui_cinetica_factor])()
    return random.choice([qui_cinetica_arrhenius,qui_cinetica_velocitat])()


def qui_equilibri_kc():
    a=random.choice([2,3,4]); b=random.choice([2,5]); c=random.choice([4,6]); K=sp.Rational(c,a*b)
    return {'enunciat':f"Per a un equilibri $A+B\\rightleftharpoons C$, en equilibri $[A]={a}$ M, $[B]={b}$ M i $[C]={c}$ M. Calcula $K_c$.", 'resposta':[K], 'passos':f"$$K_c=\\frac{{[C]}}{{[A][B]}}=\\frac{{{c}}}{{{a}\\cdot{b}}}={sp.latex(K)}.$$"}


def qui_equilibri_dissociacio():
    # A <-> B + C, Kc = x^2/(1-x), use a simple x.
    x=sp.Rational(1,5); K=sp.simplify(x*x/(1-x))
    return {'enunciat':'Per a $A\\rightleftharpoons B+C$, partint de $[A]_0=1$ M, a l’equilibri s’han format $0,2$ M de B. Calcula $K_c$.', 'resposta':[K], 'passos':f"$[B]=[C]=0,2$ M i $[A]=0,8$ M.\n\n$$K_c=\\frac{{[B][C]}}{{[A]}}={sp.latex(K)}.$$"}


def qui_equilibri_lechatelier():
    return {'enunciat':'En l’equilibri $N_2+3H_2\\rightleftharpoons2NH_3+calor$, què passa amb l’equilibri si augmentem la temperatura?', 'resposta':['es desplaça cap als reactius'], 'tipus_resposta':'text', 'passos':'La reacció directa és exotèrmica. En augmentar la temperatura, el sistema afavoreix el sentit endotèrmic: **es desplaça cap als reactius**.'}


def generar_exercici_qui_equilibri(d):
    if d=='Fàcil': return qui_equilibri_kc()
    if d=='Mitjà': return random.choice([qui_equilibri_kc,qui_equilibri_dissociacio])()
    return random.choice([qui_equilibri_dissociacio,qui_equilibri_lechatelier])()


def qui_dissolucions_ph():
    c=random.choice([0.001,0.01,0.1]); pH=-sp.log(c,10)
    return {'enunciat':f"Calcula el pH d'una dissolució d'un àcid fort monoprotònic de concentració ${c}$ M.", 'resposta':[pH], 'passos':f"Per a un àcid fort, $[H^+]={c}$ M.\n\n$$pH=-\\log[H^+]={sp.latex(pH)}.$$"}


def qui_dissolucions_coul():
    c=random.choice([0.01,0.05,0.1]); V=random.choice([100,250,500]); n=c*V/1000
    return {'enunciat':f"Quants mols de solut hi ha en {V} mL d'una dissolució de concentració {c} M?", 'resposta':[n], 'passos':f"$$n=cV={c}\\cdot{V/1000}={sp.latex(n)}\\,mol.$$"}


def qui_redox_pila():
    Ecat=random.choice([0.34,0.80,1.10]); Ean=random.choice([-0.44,-0.76,-0.28]); E=Ecat-Ean
    return {'enunciat':f"Una pila té $E^\\circ_{{càtode}}={Ecat}$ V i $E^\\circ_{{ànode}}={Ean}$ V. Calcula $E^\\circ_{{pila}}$.", 'resposta':[E], 'passos':f"$$E^\\circ_{{pila}}=E^\\circ_{{càtode}}-E^\\circ_{{ànode}}={Ecat}-({Ean})={sp.latex(E)}\\,V.$$"}


def qui_electrolisi():
    I=random.choice([2,5,10]); t=random.choice([60,120,300]); z=random.choice([0.00033,0.0005]); m=z*I*t
    return {'enunciat':f"En una electròlisi, circulen $I={I}$ A durant $t={t}$ s i el rendiment electroquímic és $z={z}$ g/C. Calcula la massa dipositada.", 'resposta':[m], 'passos':f"$$m=zIt={z}\\cdot{I}\\cdot{t}={sp.latex(m)}\\,g.$$"}


def generar_exercici_qui_dissolucions(d):
    if d=='Fàcil': return random.choice([qui_dissolucions_ph,qui_dissolucions_coul])()
    if d=='Mitjà': return random.choice([qui_dissolucions_ph,qui_redox_pila,qui_dissolucions_coul])()
    return random.choice([qui_redox_pila,qui_electrolisi,qui_dissolucions_ph])()


def qui_organica_formula():
    n=random.choice([2,3,4,5,6]); H=2*n+2
    return {'enunciat':f"Un alcà acíclic té $n={n}$ àtoms de carboni. Quants àtoms d'hidrogen té i quina és la seva fórmula molecular? Respon amb el nombre d'H.", 'resposta':[H], 'passos':f"Els alcans compleixen $C_nH_{{2n+2}}$.\n\nPer $n={n}$: $$H=2({n})+2={H}.$$"}


def qui_organica_ish():
    n=random.choice([3,4,5,6]); uns=random.choice([1,2]); H=2*n+2-2*uns
    return {'enunciat':f"Un hidrocarbur acíclic té $n={n}$ carbonis i {uns} graus d'insaturació. Quants hidrògens té?", 'resposta':[H], 'passos':f"Cada grau d'insaturació redueix 2 H respecte de l'alcà: $$H=2n+2-2I={H}.$$"}


def qui_organica_funcio():
    pairs=[('CH3COOH','àcid carboxílic'),('CH3CH2OH','alcohol'),('CH3CHO','aldehid'),('CH3COCH3','cetona')]
    formula,ans=random.choice(pairs)
    return {'enunciat':f"Identifica el grup funcional principal de ${formula}$.", 'resposta':[ans], 'tipus_resposta':'text', 'passos':f"La fórmula conté el grup característic corresponent a un **{ans}**."}


def generar_exercici_qui_organica(d):
    if d=='Fàcil': return random.choice([qui_organica_formula,qui_organica_funcio])()
    if d=='Mitjà': return random.choice([qui_organica_formula,qui_organica_ish,qui_organica_funcio])()
    return random.choice([qui_organica_ish,qui_organica_funcio,qui_organica_formula])()


def generar_exercici_quimica2(dificultat, tema):
    dispatch={
        'Estructura de la matèria i enllaç avançat': generar_exercici_qui_estructura,
        'Termoquímica': generar_exercici_qui_termo,
        'Cinètica química': generar_exercici_qui_cinetica,
        'Equilibri químic': generar_exercici_qui_equilibri,
        'Reaccions en dissolució': generar_exercici_qui_dissolucions,
        'Química orgànica': generar_exercici_qui_organica,
    }
    return dispatch[tema](dificultat)



# ============================================================
X = sp.Symbol("x", real=True)


# ============================================================
# 1r BATXILLERAT — GENERADORS COMPLETS I VARIATS
# ============================================================


def _sf4(v):
    """Arrodoniment numèric a 4 xifres significatives, preservant exactes simbòlics."""
    try:
        z = sp.sympify(v)
        if z.free_symbols:
            return z
        if z.is_number and z.is_real:
            import math
            x = float(z)
            if x == 0:
                return sp.Integer(0)
            dec = 4 - int(math.floor(math.log10(abs(x)))) - 1
            return sp.Float(round(x, dec))
    except Exception:
        pass
    return v


def _ans(v, tipus=None):
    d = {"resposta": [_sf4(v)]}
    if tipus:
        d["tipus_resposta"] = tipus
    return d


def _merge(base, enunciat, passos, tipus=None):
    base["enunciat"] = enunciat
    base["passos"] = passos
    if tipus:
        base["tipus_resposta"] = tipus
    return base

# --------------------------
# MATEMÀTIQUES I
# --------------------------

def m1_reals_f(d):
    x = random.choice([8.3, 12.7, 5.46, 0.873, 14.28])
    a = round(x, random.choice([0, 1, 2]))
    e = abs(sp.Float(str(x)) - sp.Float(str(a)))
    return _merge(_ans(e), f"Un valor exacte és $x={x}$. S'aproxima per $x_a={a}$. Calcula l'error absolut.", f"$$E_a=|x-x_a|=|{x}-{a}|={sp.latex(e)}.$$\n\nAmb 4 xifres significatives: $$E_a={sp.latex(_sf4(e))}.$$" )


def m1_reals_m(d):
    x,a=random.choice([(2.4,2.3),(7.35,7.4),(12.48,12.5),(0.846,0.85),(5.46,5.5)])
    e=abs(sp.Float(str(x))-sp.Float(str(a)))
    er=sp.simplify(e/sp.Float(str(x)))
    percent=100*er
    return _merge(_ans(percent), f"Un valor exacte és $x={x}$. S'aproxima per $x_a={a}$. Calcula l'error relatiu i dona'l en tant per cent.", f"$$E_r=\\frac{{|x-x_a|}}{{|x|}}={sp.latex(er)}.$$\n\n$$E_r(\\%)=100E_r={sp.latex(percent)}\\%.$$\n\nArrodonint a 4 xifres significatives: **{_sf4(percent)} %**.")


def m1_reals_d(d):
    x = random.choice([12.4, 7.8, 3.6])
    inc = random.choice([0.05, 0.1, 0.2])
    # error màxim i interval compatible
    lower, upper = x - inc, x + inc
    return _merge(_ans(inc), f"Una mesura s'expressa com $x={x}\\pm {inc}$. Calcula l'error absolut màxim i escriu l'interval de valors compatibles.", f"L'error absolut màxim és directament $E_a={inc}$.\n\nL'interval és $[{lower},{upper}]$.\n\nPer tant, la resposta numèrica és **{_sf4(inc)}**.")


def generar_m1_reals(d):
    return {"Fàcil": m1_reals_f, "Mitjà": m1_reals_m, "Difícil": m1_reals_d}[d](d)


def m1_poly_f(d):
    a = random.choice([1, 2, 3]); b = random.randint(-5, 5); c = random.randint(-5, 5); x0 = random.randint(-3, 3)
    P = a*X**2 + b*X + c; val = P.subs(X, x0)
    return _merge(_ans(val), f"Sigui $P(x)={sp.latex(P)}$. Calcula $P({x0})$.", f"Substituïm $x={x0}$:\n\n$$P({x0})={sp.latex(P.subs(X,x0))}={sp.latex(val)}.$$" )


def m1_poly_m(d):
    r1, r2 = random.sample([-3, -2, -1, 1, 2, 3], 2)
    P = sp.expand((X-r1)*(X-r2))
    return _merge(_ans(sp.Integer(r1+r2)), f"Factoritza $P(x)={sp.latex(P)}$ i calcula la suma de les seves arrels.", f"$$P(x)=({sp.latex(r1)})({sp.latex(r2)})$$ en forma de factors.\n\nLes arrels són ${r1}$ i ${r2}$, així que la suma és $r_1+r_2={r1+r2}$.")


def m1_poly_d(d):
    # Sistema 3x3 amb coeficients variables i solució garantida.
    sol = sp.Matrix([random.randint(-3, 4) for _ in range(3)])
    A = sp.Matrix([[2, 1, -1], [1, -2, 2], [3, 1, 1]])
    b = A*sol
    return _merge({"resposta": [[sol[0], sol[1], sol[2]]], "tipus_resposta": "sistema"},
                  f"Resol per eliminació de Gauss el sistema:\n\n$$\\begin{{cases}}2x+y-z={b[0]}\\\\x-2y+2z={b[1]}\\\3x+y+z={b[2]}\\end{{cases}}$$",
                  f"Formem la matriu ampliada i fem eliminació de Gauss fins a obtenir una matriu triangular.\n\nEl resultat és:\n\n$$\\boxed{{x={sol[0]},\\quad y={sol[1]},\\quad z={sol[2]}}}$$")


def generar_m1_poly(d):
    return {"Fàcil": m1_poly_f, "Mitjà": m1_poly_m, "Difícil": m1_poly_d}[d](d)


def m1_exp_f(d):
    base = random.choice([2, 3, 5]); e = random.randint(2, 5); target = base**e
    return _merge(_ans(e), f"Resol l'equació ${base}^x={target}$.", f"Com que ${target}={base}^{{{e}}}$, igualem exponents i obtenim $x={e}$.")


def m1_exp_m(d):
    base = random.choice([2, 3, 5]); e = random.randint(2, 4); target = base**e
    return _merge(_ans(target), f"Resol $\\log_{{{base}}}(x)+\\log_{{{base}}}({base})={e+1}$.", f"$$\\log_{{{base}}}({base}x)={e+1}.$$\n\nPer tant $ {base}x={base**(e+1)}$ i $x={target}$.")


def m1_exp_d(d):
    base = random.choice([2, 3]); r = random.choice([2, 3, 4])
    # (a^x)^2 -(r+1)a^x+r = 0 -> a^x=1 o r
    return _merge({"resposta": [sp.Integer(0), sp.log(r, base)]}, f"Resol $({base}^x)^2-({r+1}){base}^x+{r}=0$.", f"Fem $t={base}^x$, de manera que $t^2-{r+1}t+{r}=0$.\n\nFactoritzem: $$(t-1)(t-{r})=0.$$\n\nAixí $t=1$ o $t={r}$. Per tant $x=0$ o $x=\\log_{{{base}}}({r})$.")


def generar_m1_exp(d):
    return {"Fàcil": m1_exp_f, "Mitjà": m1_exp_m, "Difícil": m1_exp_d}[d](d)


def m1_complex_f(d):
    z1 = random.choice([1,2,3,-1,-2])+sp.I*random.choice([1,2,-1,-2]); z2 = random.choice([1,2,3,-1,-2])+sp.I*random.choice([1,2,-1,-2]); z=sp.expand(z1+z2)
    return _merge(_ans(z), f"Calcula $z_1+z_2$ si $z_1={sp.latex(z1)}$ i $z_2={sp.latex(z2)}$.", f"Sumem les parts reals i les parts imaginàries:\n\n$$z_1+z_2={sp.latex(z)}.$$" )


def m1_complex_m(d):
    z = random.choice([1,2,-1,-2])+sp.I*random.choice([1,2,-1,-2]); prod=sp.expand(z*sp.conjugate(z))
    return _merge(_ans(prod), f"Calcula $|z|^2$ per a $z={sp.latex(z)}$.", f"$$|z|^2=z\\bar z=({sp.latex(z)})({sp.latex(sp.conjugate(z))})={sp.latex(prod)}.$$" )


def m1_complex_d(d):
    z = random.choice([1,2,3])+sp.I*random.choice([1,2,3]); n=random.choice([3,4,5]); w=sp.expand(z**n)
    return _merge(_ans(w), f"Calcula $z^{{{n}}}$ per a $z={sp.latex(z)}$ i dona el resultat en forma binòmica.", f"Podem aplicar De Moivre o multiplicar successivament. Després de simplificar:\n\n$$z^{{{n}}}={sp.latex(w)}.$$" )


def generar_m1_complex(d):
    return {"Fàcil": m1_complex_f, "Mitjà": m1_complex_m, "Difícil": m1_complex_d}[d](d)


def m1_trig_f(d):
    triples=[(3,4,5),(5,12,13),(8,15,17)]; opp,adj,h=random.choice(triples)
    return _merge(_ans(sp.Rational(opp,h)), f"En un triangle rectangle, l'angle $\\alpha$ té catet oposat {opp} i hipotenusa {h}. Calcula $\\sin\\alpha$.", f"$$\\sin\\alpha=\\frac{{catet\\ oposat}}{{hipotenusa}}=\\frac{{{opp}}}{{{h}}}={sp.latex(sp.Rational(opp,h))}.$$" )


def m1_trig_m(d):
    ang=random.choice([30,45,60])
    mode=random.choice(["sum","square"])
    if mode == "sum":
        expr=sp.sin(sp.pi*ang/180)+sp.cos(sp.pi*ang/180)
        en=f"Calcula exactament $\\sin({ang}^\\circ)+\\cos({ang}^\\circ)$."
        pasos=f"Fem servir els valors trigonomètrics notables de ${ang}^\\circ$.\n\n$$\\sin({ang}^\\circ)+\\cos({ang}^\\circ)={sp.latex(sp.simplify(expr))}.$$"
    else:
        expr=sp.sin(sp.pi*ang/180)**2
        en=f"Calcula exactament $\\sin^2({ang}^\\circ)$."
        pasos=f"Fem servir el valor notable de $\\sin({ang}^\\circ)$.\n\n$$\\sin^2({ang}^\\circ)={sp.latex(sp.simplify(expr))}.$$"
    return _merge(_ans(sp.simplify(expr)), en, pasos)


def m1_trig_d(d):
    a=random.choice([5,6,7,8]); b=random.choice([4,5,9]); C=random.choice([60,120]); c=sp.sqrt(a*a+b*b-2*a*b*sp.cos(sp.pi*C/180))
    return _merge(_ans(c), f"En un triangle, $a={a}$, $b={b}$ i l'angle comprès és $C={C}^\\circ$. Calcula el costat oposat $c$ amb el teorema del cosinus.", f"$$c^2=a^2+b^2-2ab\\cos C.$$\n\n$$c=\\sqrt{{{a}^2+{b}^2-2({a})({b})\\cos({C}^\\circ)}}={sp.latex(c)}.$$" )


def generar_m1_trig(d):
    return {"Fàcil": m1_trig_f, "Mitjà": m1_trig_m, "Difícil": m1_trig_d}[d](d)


def m1_vec_f(d):
    u=sp.Matrix([random.randint(-5,5),random.randint(-5,5)]); v=sp.Matrix([random.randint(-5,5),random.randint(-5,5)]); r=u+v
    return _merge(_ans(sp.sqrt(r.dot(r))), f"Calcula la norma de $\\vec u+\\vec v$ si $\\vec u=({u[0]},{u[1]})$ i $\\vec v=({v[0]},{v[1]})$.", f"$$\\vec u+\\vec v=({r[0]},{r[1]}).$$\n\n$$|\\vec u+\\vec v|=\\sqrt{{{r[0]}^2+{r[1]}^2}}={sp.latex(sp.sqrt(r.dot(r)))}.$$" )


def m1_vec_m(d):
    u=sp.Matrix([random.randint(-4,4),random.randint(-4,4)]); v=sp.Matrix([random.randint(-4,4),random.randint(-4,4)]); dot=u.dot(v)
    return _merge(_ans(dot), f"Calcula el producte escalar de $\\vec u=({u[0]},{u[1]})$ i $\\vec v=({v[0]},{v[1]})$ i indica si són perpendiculars.", f"$$\\vec u\\cdot\\vec v={u[0]}({v[0]})+{u[1]}({v[1]})={dot}.$$\n\nSón perpendiculars només si el resultat és 0.")


def m1_vec_d(d):
    u=sp.Matrix([random.choice([2,3]),random.choice([1,2,3])]); a=random.choice([-4,-3,-2,1,2,3]); k=sp.solve(sp.Eq(u.dot(sp.Matrix([a,sp.Symbol('k')])),0),sp.Symbol('k'))[0]
    return _merge(_ans(k), f"Troba $k$ perquè $\\vec u=({u[0]},{u[1]})$ i $\\vec v=({a},k)$ siguin perpendiculars.", f"Perpendicularitat: $$\\vec u\\cdot\\vec v={u[0]}({a})+{u[1]}k=0.$$\n\nResolent: $$k={sp.latex(k)}.$$" )


def generar_m1_vectors(d): return {"Fàcil":m1_vec_f,"Mitjà":m1_vec_m,"Difícil":m1_vec_d}[d](d)


def m1_geo_f(d):
    A=(random.randint(-4,4),random.randint(-4,4)); B=(A[0]+random.choice([-3,-2,2,3]),A[1]+random.choice([-3,-1,1,3])); m=sp.Rational(B[1]-A[1],B[0]-A[0])
    return _merge(_ans(m), f"Calcula el pendent de la recta que passa per $A{A}$ i $B{B}$.", f"$$m=\\frac{{y_B-y_A}}{{x_B-x_A}}=\\frac{{{B[1]}-{A[1]}}}{{{B[0]}-{A[0]}}}={sp.latex(m)}.$$" )


def m1_geo_m(d):
    A=(random.randint(-3,3),random.randint(-3,3)); B=(random.randint(-3,3),random.randint(-3,3))
    while B==A or B[0]==A[0]: B=(random.randint(-3,3),random.randint(-3,3))
    m=sp.Rational(B[1]-A[1],B[0]-A[0]); b=A[1]-m*A[0]
    return _merge(_ans(b), f"Troba l'equació de la recta que passa per $A{A}$ i $B{B}$. Dona el terme independent $b$ en $y=mx+b$.", f"$$m=\\frac{{{B[1]}-{A[1]}}}{{{B[0]}-{A[0]}}}={sp.latex(m)}.$$\n\n$$b=y_A-mx_A={A[1]}-({sp.latex(m)})({A[0]})={sp.latex(b)}.$$" )


def m1_geo_d(d):
    A=(random.randint(-3,3),random.randint(-3,3)); B=(random.randint(-3,3),random.randint(-3,3)); C=(random.randint(-3,3),random.randint(-3,3))
    while B==A: B=(random.randint(-3,3),random.randint(-3,3))
    # distància de C a AB
    den=sp.sqrt((B[0]-A[0])**2+(B[1]-A[1])**2); num=abs((B[1]-A[1])*C[0]-(B[0]-A[0])*C[1]+B[0]*A[1]-B[1]*A[0]); dist=sp.simplify(sp.Rational(num,1)/den)
    return _merge(_ans(dist), f"Calcula la distància del punt $C{C}$ a la recta que passa per $A{A}$ i $B{B}$.", f"La distància punt-recta és $$d=\\frac{{|ax_C+by_C+c|}}{{\\sqrt{{a^2+b^2}}}}.$$\n\nSubstituint les coordenades s'obté $$d={sp.latex(dist)}.$$" )


def generar_m1_geo(d): return {"Fàcil":m1_geo_f,"Mitjà":m1_geo_m,"Difícil":m1_geo_d}[d](d)


def m1_conic_f(d):
    r=random.choice([2,3,4,5]); return _merge(_ans(r), f"Calcula el radi de la circumferència $x^2+y^2={r*r}$.", f"Com que $x^2+y^2=r^2$, tenim $r=\\sqrt{{{r*r}}}={r}$.")


def m1_conic_m(d):
    a,b=random.choice([(5,3),(5,4),(6,4)]); e=sp.sqrt(a*a-b*b)/a
    return _merge(_ans(e), f"Per a l'el·lipse $\\frac{{x^2}}{{{a*a}}}+\\frac{{y^2}}{{{b*b}}}=1$, calcula l'excentricitat.", f"$$e=\\sqrt{{1-\\frac{{b^2}}{{a^2}}}}={sp.latex(e)}.$$" )


def m1_conic_d(d):
    p=random.choice([1,2,3,4]); return _merge(_ans(p), f"La paràbola és $y^2={4*p}x$. Calcula la distància del vèrtex al focus.", f"La forma canònica és $y^2=4px$.\n\nPer tant, $p={p}$ i la distància del vèrtex al focus és **{p}**.")


def generar_m1_conics(d): return {"Fàcil":m1_conic_f,"Mitjà":m1_conic_m,"Difícil":m1_conic_d}[d](d)


def m1_func_f(d):
    a=random.randint(1,5); return _merge(_ans(a*a+2*a), f"Calcula $f({a})$ per a $f(x)=x^2+2x$.", f"$$f({a})={a}^2+2({a})={a*a+2*a}.$$" )


def m1_func_m(d):
    k=random.choice([1,2,3])
    return _merge(_ans(0), f"Per a $f(x)=\\sqrt{{x+{k}}}$, indica el domini i calcula $f(-{k})$.", f"Perquè existeixi l'arrel cal $x+{k}\\ge0$, així que $D_f=[-{k},\\infty)$.\n\n$$f(-{k})=0.$$" )


def m1_func_d(d):
    a=random.choice([1,2,3]); b=random.choice([1,2]); c=random.choice([1,2]); x0=random.choice([-2,-1,1,2])
    val=(b*x0+c)**2+a
    passos=f"""Primer calculem $g({x0})={b}({x0})+{c}={b*x0+c}$.

Després apliquem $f$:
$$f(g({x0}))=({b*x0+c})^2+{a}={val}.$$"""
    return _merge(_ans(val), f"Siguin $f(x)=x^2+{a}$ i $g(x)={b}x+{c}$. Calcula $(f\\circ g)({x0})$.", passos)


def generar_m1_functions(d): return {"Fàcil":m1_func_f,"Mitjà":m1_func_m,"Difícil":m1_func_d}[d](d)


def m1_limit_f(d):
    a=random.choice([-2,-1,0,1,2]); b=random.choice([1,2,3]); expr=(X**2+b*X+1); val=expr.subs(X,a)
    return _merge(_ans(val), f"Calcula $\\lim_{{x\\to {a}}}(x^2+{b}x+1)$.", f"És una funció polinòmica i, per tant, podem substituir directament:\n\n$$L={a}^2+{b}({a})+1={val}.$$" )


def m1_limit_m(d):
    a=random.choice([1,2,3]); expr=(X**2-a**2)/(X-a); val=2*a
    return _merge(_ans(val), f"Calcula $\\lim_{{x\\to {a}}}\\frac{{x^2-{a*a}}}{{x-{a}}}$.", f"És una indeterminació $0/0$. Factoritzem:\n\n$$\\frac{{(x-{a})(x+{a})}}{{x-{a}}}=x+{a}.$$\n\nPer tant el límit és **{val}**.")


def m1_limit_d(d):
    a=random.choice([1,2,3]); expr=(X**2+3*X+2)/(X+1) if a==1 else (X**2-a**2)/(X-a)
    val=sp.limit(expr,X,a)
    return _merge(_ans(val), f"Calcula un límit que presenta una indeterminació $0/0$: $\\lim_{{x\\to {a}}}\\frac{{x^2-{a*a}}}{{x-{a}}}$.", f"Factoritzem el numerador i simplifiquem el factor que provoca la indeterminació:\n\n$$\\frac{{(x-{a})(x+{a})}}{{x-{a}}}=x+{a}.$$\n\nAixí $L={val}$.")


def generar_m1_limits(d): return {"Fàcil":m1_limit_f,"Mitjà":m1_limit_m,"Difícil":m1_limit_d}[d](d)


def m1_deriv_f(d):
    n=random.choice([2,3,4]); a=random.choice([2,3,4]); val=n*a**(n-1)
    return _merge(_ans(val), f"Calcula $f'({a})$ si $f(x)=x^{n}$.", f"$$f'(x)={n}x^{{{n-1}}}.$$\n\n$$f'({a})={n}({a})^{{{n-1}}}={val}.$$" )


def m1_deriv_m(d):
    a=random.choice([1,2,3]); b=random.choice([1,2,3]); x0=random.choice([1,2]);
    # f=(x^2+a)*e^(bx), derivative at x0
    f=(X**2+a)*sp.exp(b*X); val=sp.diff(f,X).subs(X,x0)
    return _merge(_ans(val), f"Calcula $f'({x0})$ si $f(x)=({sp.latex(X**2+a)})e^{{{b}x}}$.", f"Regla del producte:\n\n$$f'(x)=2x e^{{{b}x}}+({sp.latex(X**2+a)}){b}e^{{{b}x}}.$$\n\nSubstituint $x={x0}$:\n$$f'({x0})={sp.latex(val)}.$$" )


def m1_deriv_d(d):
    a=random.choice([1,2]); b=random.choice([1,2]); x0=random.choice([1,2]);
    f=sp.sin(X**2+a)/(X+b); val=sp.diff(f,X).subs(X,x0)
    return _merge(_ans(val), f"Calcula $f'({x0})$ per a $f(x)=\\frac{{\\sin(x^2+{a})}}{{x+{b}}}$.", f"Cal aplicar simultàniament la regla del quocient i la regla de la cadena.\n\n$$f'(x)=\\frac{{(x+{b})\\cos(x^2+{a})2x-\\sin(x^2+{a})}}{{(x+{b})^2}}.$$\n\nPer $x={x0}$:\n$$f'({x0})={sp.latex(val)}.$$" )


def generar_m1_derivatives(d): return {"Fàcil":m1_deriv_f,"Mitjà":m1_deriv_m,"Difícil":m1_deriv_d}[d](d)


def m1_prob_f(d):
    red,blue=5,3; total=red+blue; p=sp.Rational(red,total)
    return _merge(_ans(p), f"En una urna hi ha {red} boles vermelles i {blue} blaves. Calcula la probabilitat d'extreure una vermella.", f"$$P(V)=\\frac{{{red}}}{{{total}}}={sp.latex(p)}.$$" )


def m1_prob_m(d):
    n=random.choice([5,6,8]); k=random.choice([2,3]); p=sp.Rational(1,2); val=sp.binomial(n,k)*p**k*(1-p)**(n-k)
    return _merge(_ans(val), f"Es llança una moneda equilibrada {n} vegades. Calcula la probabilitat d'obtenir exactament {k} cares.", f"És una binomial $X\\sim B({n},0,5)$.\n\n$$P(X={k})=\\binom{{{n}}}{{{k}}}(0,5)^{{{k}}}(0,5)^{{{n-k}}}={sp.latex(val)}.$$" )


def m1_prob_d(d):
    # Bayes simple but with different data.
    pA=sp.Rational(2,5); pB_given_A=sp.Rational(3,4); pB_given_notA=sp.Rational(1,5); pB=pA*pB_given_A+(1-pA)*pB_given_notA; ans=sp.simplify(pA*pB_given_A/pB)
    return _merge(_ans(ans), "En una població, $P(A)=0,4$, $P(B|A)=0,75$ i $P(B|\\overline A)=0,2$. Calcula $P(A|B)$.", f"Primer, probabilitat total:\n\n$$P(B)=0,4(0,75)+0,6(0,2)=0,42.$$\n\nPer Bayes:\n$$P(A|B)=\\frac{{P(B|A)P(A)}}{{P(B)}}={sp.latex(ans)}.$$" )


def generar_m1_probability(d): return {"Fàcil":m1_prob_f,"Mitjà":m1_prob_m,"Difícil":m1_prob_d}[d](d)

def generar_exercici_mates1(d, tema):
    dispatch={
        "Nombres reals, intervals i errors": generar_m1_reals,
        "Polinomis, fraccions algebraiques i mètode de Gauss": generar_m1_poly,
        "Equacions exponencials, logarítmiques i inequacions": generar_m1_exp,
        "Nombres complexos": generar_m1_complex,
        "Raons trigonomètriques, identitats i resolució de triangles": generar_m1_trig,
        "Vectors en el pla": generar_m1_vectors,
        "Geometria analítica plana": generar_m1_geo,
        "Llocs geomètrics i còniques": generar_m1_conics,
        "Funcions elementals i dominis": generar_m1_functions,
        "Límits de funcions i continuïtat": generar_m1_limits,
        "Derivades": generar_m1_derivatives,
        "Probabilitat i estadística bidimensional": generar_m1_probability,
    }
    return dispatch[tema](d)


# --------------------------
# FÍSICA I
# --------------------------

def f1_cin_f(d):
    mode=random.choice(["mru", "mrua", "conversion"])
    if mode == "mru":
        v=random.choice([5,8,12]); t=random.choice([4,6,10]); val=v*t
        return _merge(_ans(val), f"Un mòbil es mou amb MRU a $v={v}$ m/s durant $t={t}$ s. Quina distància recorre?", f"$$s=vt={v}({t})={val}\\,m.$$" )
    if mode == "mrua":
        v0=random.choice([0,2,4]); a=random.choice([1,2,3]); t=random.choice([3,5]); val=v0*t+sp.Rational(a,2)*t**2
        return _merge(_ans(val), f"Un mòbil parteix amb $v_0={v0}$ m/s i accelera a $a={a}$ m/s² durant {t} s. Calcula l'espai recorregut.", f"$$s=v_0t+\\frac12at^2={v0}({t})+\\frac12({a})({t})^2={val}\\,m.$$" )
    km=random.choice([36,54,72,90]); val=sp.Rational(km,3.6)
    return _merge(_ans(val), f"Converteix una velocitat de {km} km/h a m/s.", f"$$v={km}\\frac{{1000}}{{3600}}={sp.latex(val)}\\,m/s.$$" )


def f1_cin_m(d):
    mode=random.choice(["meeting", "braking", "vertical"])
    if mode == "meeting":
        v1=random.choice([8,10,12]); v2=random.choice([5,6,7]); D=random.choice([100,150,200]); t=sp.Rational(D,v1+v2)
        return _merge(_ans(t), f"Dos ciclistes es troben separats {D} m i es dirigeixen l'un cap a l'altre a {v1} m/s i {v2} m/s. Quant triguen a trobar-se?", f"La velocitat relativa és $v_r={v1}+{v2}={v1+v2}$ m/s.\n\n$$t=\\frac{{D}}{{v_r}}=\\frac{{{D}}}{{{v1+v2}}}={sp.latex(t)}\\,s.$$" )
    if mode == "braking":
        v0=random.choice([12,15,18]); a=random.choice([-2,-3,-4]); val=sp.sqrt(v0**2/(2*abs(a)))
        return _merge(_ans(val), f"Un vehicle circula a {v0} m/s i frena amb acceleració constant $a={a}$ m/s² fins aturar-se. Calcula la distància de frenada.", f"$$v^2=v_0^2+2a\\Delta x.$$\n\nAmb $v=0$:\n$$\\Delta x=-\\frac{{v_0^2}}{{2a}}={sp.latex(val)}\\,m.$$" )
    v0=random.choice([8,10,12]); h=random.choice([5,10,15]); g=9.81; val=sp.sqrt(v0**2+2*g*h)
    return _merge(_ans(val), f"Es deixa caure un objecte des d'una altura de {h} m amb velocitat inicial vertical de {v0} m/s cap avall. Calcula la velocitat abans d'arribar a terra. Pren $g=9,81$ m/s².", f"$$v^2=v_0^2+2gh.$$\n\n$$v={sp.latex(val)}\\,m/s.$$" )


def f1_cin_d(d):
    mode=random.choice(["projectile", "circular", "two_stage"])
    if mode == "projectile":
        v0=random.choice([12,15,18]); angle=random.choice([30,45,60]); g=9.81; R=v0**2*sp.sin(2*sp.pi*angle/180)/g
        return _merge(_ans(R), f"Es llança un projectil amb $v_0={v0}$ m/s i angle $\\theta={angle}^\\circ$. Negligint l'aire, calcula l'abast horitzontal.", f"$$R=\\frac{{v_0^2\\sin(2\\theta)}}{{g}}={sp.latex(R)}\\,m.$$" )
    if mode == "circular":
        r=random.choice([2,3,4]); v=random.choice([4,6,8]); a=v**2/r
        return _merge(_ans(a), f"Un mòbil descriu una circumferència de radi {r} m amb velocitat constant {v} m/s. Calcula l'acceleració centrípeta.", f"$$a_c=\\frac{{v^2}}{{r}}=\\frac{{{v}^2}}{{{r}}}={a}\\,m/s^2.$$" )
    v1=random.choice([5,8,10]); a=random.choice([2,3]); t1=random.choice([2,3]); t2=random.choice([2,4]); v2=v1+a*t1; s1=v1*t1+sp.Rational(a,2)*t1**2; s2=v2*t2; total=s1+s2
    return _merge(_ans(total), f"Un mòbil recorre una primera etapa de {t1} s amb $v_0={v1}$ m/s i acceleració {a} m/s². Després manté la velocitat assolida durant {t2} s. Calcula la distància total.", f"Primera etapa: $v_1={v1}+{a}({t1})={v2}$ m/s i $s_1={s1}$ m.\n\nSegona etapa: $s_2=v_1t_2={v2}({t2})={s2}$ m.\n\n$$s_T={s1}+{s2}={total}\\,m.$$" )


def generar_f1_cinematica(d): return {"Fàcil":f1_cin_f,"Mitjà":f1_cin_m,"Difícil":f1_cin_d}[d](d)


def f1_dyn_f(d):
    mode=random.choice(["net", "two_forces", "weight"])
    if mode == "net":
        m=random.choice([2,4,5]); F=random.choice([10,15,20]); a=sp.Rational(F,m)
        return _merge(_ans(a), f"Un bloc de massa {m} kg rep una força horitzontal neta de {F} N. Calcula l'acceleració.", f"$$F=ma\\Rightarrow a=\\frac{{{F}}}{{{m}}}={sp.latex(a)}\\,m/s^2.$$" )
    if mode == "two_forces":
        m=random.choice([3,5,8]); F1=random.choice([20,30,40]); F2=random.choice([5,10,15]); a=sp.Rational(F1-F2,m)
        return _merge(_ans(a), f"Sobre un cos de {m} kg actuen dues forces horitzontals oposades de {F1} N i {F2} N. Calcula l'acceleració.", f"La força neta és $F_R={F1}-{F2}={F1-F2}$ N.\n\n$$a=\\frac{{F_R}}{{m}}={sp.latex(a)}\\,m/s^2.$$" )
    m=random.choice([2,4,6]); g=9.81; P=m*g
    return _merge(_ans(P), f"Calcula el pes d'una massa de {m} kg. Pren $g=9,81$ m/s².", f"$$P=mg={m}(9,81)={sp.latex(P)}\\,N.$$" )


def f1_dyn_m(d):
    mode=random.choice(["incline", "friction_horizontal", "tension"])
    if mode == "incline":
        angle=random.choice([25,30,35]); mu=random.choice([0.10,0.20]); g=9.81; a=g*(sp.sin(sp.pi*angle/180)-mu*sp.cos(sp.pi*angle/180))
        return _merge(_ans(a), f"Un bloc baixa per un pla inclinat de {angle}° amb coeficient de fregament $\\mu={mu}$. Calcula l'acceleració. Pren $g=9,81$ m/s².", f"$$ma=mg\\sin\\theta-\\mu mg\\cos\\theta.$$\n\n$$a=g(\\sin\\theta-\\mu\\cos\\theta)={sp.latex(a)}\\,m/s^2.$$" )
    if mode == "friction_horizontal":
        m=random.choice([4,6,8]); F=random.choice([20,30,40]); mu=random.choice([0.10,0.20]); g=9.81; a=(F-mu*m*g)/m
        return _merge(_ans(a), f"Un bloc de {m} kg és estirat horitzontalment amb {F} N sobre una superfície amb $\\mu={mu}$. Calcula l'acceleració. Pren $g=9,81$ m/s².", f"El fregament és $f=\\mu mg$.\n\n$$ma=F-\\mu mg\\Rightarrow a=\\frac{{F-\\mu mg}}{{m}}={sp.latex(a)}\\,m/s^2.$$" )
    m=random.choice([2,3,4]); F=random.choice([12,18,24]); a=sp.Rational(F,m); T=F
    return _merge(_ans(T), f"Un cos de {m} kg és arrossegat horitzontalment per una corda ideal i adquireix una acceleració de {sp.latex(a)} m/s². Calcula la tensió de la corda si no hi ha fregament.", f"$$T=ma={m}({sp.latex(a)})={T}\\,N.$$" )


def f1_dyn_d(d):
    mode=random.choice(["pulley", "incline_pulley", "lift"])
    g=9.81
    if mode == "pulley":
        m1=random.choice([2,3,4]); m2=random.choice([4,5,6]); a=(m2-m1)*g/(m1+m2)
        return _merge(_ans(a), f"Una màquina d'Atwood ideal té masses $m_1={m1}$ kg i $m_2={m2}$ kg. Calcula l'acceleració del sistema.", f"$$m_2g-T=m_2a,\\qquad T-m_1g=m_1a.$$\n\nSumant:\n$$a=\\frac{{(m_2-m_1)g}}{{m_1+m_2}}={sp.latex(a)}\\,m/s^2.$$" )
    if mode == "incline_pulley":
        m1=random.choice([2,3,4]); m2=random.choice([1,2]); mu=random.choice([0.10,0.15]); angle=random.choice([25,30,35]); a=(m1*g*sp.sin(sp.pi*angle/180)-mu*m1*g*sp.cos(sp.pi*angle/180)-m2*g)/(m1+m2)
        return _merge(_ans(a), f"$m_1={m1}$ kg és sobre un pla inclinat de {angle}° amb $\\mu={mu}$ i està unit a $m_2={m2}$ kg penjant. Suposa que $m_1$ baixa pel pla. Calcula $a$.", f"Per a $m_1$: $m_1a=m_1g\\sin\\theta-\\mu m_1g\\cos\\theta-T$.\n\nPer a $m_2$: $m_2a=T-m_2g$.\n\nEliminant $T$:\n$$a=\\frac{{m_1g(\\sin\\theta-\\mu\\cos\\theta)-m_2g}}{{m_1+m_2}}={sp.latex(a)}\\,m/s^2.$$" )
    m=random.choice([500,800,1000]); F=random.choice([6000,8000,10000]); a=sp.Rational(F,m)-g
    return _merge(_ans(a), f"Un ascensor de massa {m} kg puja amb una força de tracció constant de {F} N. Calcula la seva acceleració vertical. Pren $g=9,81$ m/s².", f"Prenem cap amunt com a positiu:\n$$F-mg=ma.$$\n\n$$a=\\frac{{F}}{{m}}-g={sp.latex(a)}\\,m/s^2.$$" )


def generar_f1_dinamica(d): return {"Fàcil":f1_dyn_f,"Mitjà":f1_dyn_m,"Difícil":f1_dyn_d}[d](d)


def f1_energy_f(d):
    mode=random.choice(["potential", "kinetic", "work"])
    if mode == "potential":
        m=random.choice([2,4,5]); h=random.choice([3,5,8]); E=m*9.81*h
        return _merge(_ans(E), f"Calcula l'energia potencial gravitatòria d'una massa de {m} kg a {h} m. Pren $g=9,81$ m/s².", f"$$E_p=mgh={m}(9,81)({h})={sp.latex(E)}\\,J.$$" )
    if mode == "kinetic":
        m=random.choice([2,3,5]); v=random.choice([4,6,8]); E=sp.Rational(m,2)*v**2
        return _merge(_ans(E), f"Calcula l'energia cinètica d'un cos de {m} kg que es mou a {v} m/s.", f"$$E_c=\\frac12mv^2=\\frac12({m})({v})^2={sp.latex(E)}\\,J.$$" )
    F=random.choice([10,15,20]); d=random.choice([3,5,8]); W=F*d
    return _merge(_ans(W), f"Una força constant de {F} N actua en la mateixa direcció del moviment durant {d} m. Calcula el treball.", f"$$W=Fd={F}({d})={W}\\,J.$$" )


def f1_energy_m(d):
    mode=random.choice(["drop", "spring", "friction"])
    g=9.81
    if mode == "drop":
        v0=random.choice([4,6,8]); h=random.choice([2,4,6]); vf=sp.sqrt(v0**2+2*g*h)
        return _merge(_ans(vf), f"Un cos es mou a {v0} m/s i baixa sense fregament {h} m. Calcula la velocitat final.", f"$$\\frac12mv_0^2+mgh=\\frac12mv_f^2.$$\n\n$$v_f=\\sqrt{{v_0^2+2gh}}={sp.latex(vf)}\\,m/s.$$" )
    if mode == "spring":
        m=random.choice([1,2,3]); k=random.choice([80,120,160]); A=random.choice([0.05,0.08,0.10]); v=A*sp.sqrt(k/m)
        return _merge(_ans(v), f"Una massa de {m} kg unida a una molla de $k={k}$ N/m s'allibera des de $A={A}$ m. Calcula la velocitat en l'equilibri.", f"$$\\frac12kA^2=\\frac12mv^2\\Rightarrow v=A\\sqrt{{k/m}}={sp.latex(v)}\\,m/s.$$" )
    m=random.choice([2,4,5]); v0=random.choice([8,10,12]); mu=random.choice([0.10,0.15]); d=random.choice([4,5,6]); vf=sp.sqrt(v0**2-2*mu*g*d)
    return _merge(_ans(vf), f"Un cos de {m} kg entra en una superfície rugosa a {v0} m/s amb $\\mu={mu}$ i recorre {d} m. Calcula la velocitat final. Pren $g=9,81$ m/s².", f"El fregament fa treball $W_f=-\\mu mgd$.\n\n$$\\frac12mv_f^2=\\frac12mv_0^2-\\mu mgd.$$\n\n$$v_f={sp.latex(vf)}\\,m/s.$$" )


def f1_energy_d(d):
    mode=random.choice(["spring_position", "incline_friction", "pendulum"])
    g=9.81
    if mode == "spring_position":
        m=random.choice([1,2,3]); k=random.choice([100,150,200]); A=random.choice([0.08,0.10,0.12]); x=random.choice([0.02,0.04,0.06]); v=sp.sqrt(k/m*(A**2-x**2))
        return _merge(_ans(v), f"En un MAS de molla, $m={m}$ kg, $k={k}$ N/m i $A={A}$ m. Calcula la velocitat quan $|x|={x}$ m.", f"$$\\frac12kA^2=\\frac12kx^2+\\frac12mv^2.$$\n\n$$v=\\sqrt{{\\frac{{k}}{{m}}(A^2-x^2)}}={sp.latex(v)}\\,m/s.$$" )
    if mode == "incline_friction":
        m=random.choice([2,3,4]); angle=random.choice([20,30,35]); mu=random.choice([0.10,0.15]); d=random.choice([4,6,8]); v=sp.sqrt(2*g*d*(sp.sin(sp.pi*angle/180)-mu*sp.cos(sp.pi*angle/180)))
        return _merge(_ans(v), f"Un bloc parteix del repòs i llisca {d} m per un pla de {angle}° amb $\\mu={mu}$. Calcula la velocitat final. Pren $g=9,81$ m/s².", f"L'energia potencial perduda menys el treball del fregament és energia cinètica:\n$$mgd\\sin\\theta-\\mu mgd\\cos\\theta=\\frac12mv^2.$$\n\n$$v={sp.latex(v)}\\,m/s.$$" )
    L=random.choice([0.8,1.0,1.2]); h=random.choice([0.1,0.2,0.3]); v=sp.sqrt(2*g*h)
    return _merge(_ans(v), f"Un pèndol ideal baixa des d'una posició situada {h} m per sobre del punt més baix. Calcula la velocitat en el punt més baix. Pren $g=9,81$ m/s².", f"Conservació de l'energia: $mgh=\\frac12mv^2$.\n\n$$v=\\sqrt{{2gh}}={sp.latex(v)}\\,m/s.$$" )


def generar_f1_energy(d): return {"Fàcil":f1_energy_f,"Mitjà":f1_energy_m,"Difícil":f1_energy_d}[d](d)


def f1_mas_f(d):
    mode=random.choice(["omega", "frequency", "period"])
    if mode == "omega":
        T=random.choice([1,2,4]); val=2*sp.pi/T
        return _merge(_ans(val), f"Un oscil·lador té període $T={T}$ s. Calcula la freqüència angular.", f"$$\\omega=\\frac{{2\\pi}}{{T}}={sp.latex(val)}\\,rad/s.$$" )
    if mode == "frequency":
        T=random.choice([1,2,4,5]); val=sp.Rational(1,T)
        return _merge(_ans(val), f"Un MAS té període $T={T}$ s. Calcula la freqüència.", f"$$f=\\frac1T={sp.latex(val)}\\,Hz.$$" )
    f=random.choice([0.5,1,2,4]); val=2*sp.pi*f
    return _merge(_ans(val), f"Un oscil·lador té freqüència $f={f}$ Hz. Calcula $\\omega$.", f"$$\\omega=2\\pi f={sp.latex(val)}\\,rad/s.$$" )


def f1_mas_m(d):
    mode=random.choice(["spring_omega", "position", "energy"])
    if mode == "spring_omega":
        k=random.choice([50,80,120]); m=random.choice([1,2,3]); omega=sp.sqrt(sp.Rational(k,m))
        return _merge(_ans(omega), f"Una massa $m={m}$ kg oscil·la amb una molla de constant $k={k}$ N/m. Calcula $\\omega$.", f"$$\\omega=\\sqrt{{\\frac{{k}}{{m}}}}={sp.latex(omega)}\\,rad/s.$$" )
    A=random.choice([0.08,0.10,0.12]); T=random.choice([1,2]); t=T/4; x=0
    return _merge(_ans(x), f"Un MAS té amplitud $A={A}$ m i període $T={T}$ s. Si comença en $x=A$, quina és la posició al cap de $T/4$?", f"Amb $x=A\\cos(\\omega t)$ i $\\omega T=2\\pi$, per $t=T/4$ tenim $\\cos(\\pi/2)=0$.\n\nPer tant $x=0$ m.")


def f1_mas_d(d):
    mode=random.choice(["speed_position", "period_from_data", "max_accel"])
    if mode == "speed_position":
        m=random.choice([1,2,3]); k=random.choice([50,80,120]); A=random.choice([0.06,0.08,0.10]); x=random.choice([0.02,0.03,0.04]); v=sp.sqrt(k/m*(A**2-x**2))
        return _merge(_ans(v), f"En un MAS de molla, $m={m}$ kg, $k={k}$ N/m i $A={A}$ m. Calcula $v$ quan $|x|={x}$ m.", f"$$v=\\sqrt{{\\frac{k}{m}(A^2-x^2)}}={sp.latex(v)}\\,m/s.$$" )
    m=random.choice([1,2,3]); k=random.choice([50,80,120]); omega=sp.sqrt(sp.Rational(k,m)); T=2*sp.pi/omega
    return _merge(_ans(T), f"Una massa de {m} kg està unida a una molla de $k={k}$ N/m. Calcula el període del MAS.", f"$$\\omega=\\sqrt{{k/m}},\\qquad T=\\frac{{2\\pi}}{{\\omega}}={sp.latex(T)}\\,s.$$" )


def generar_f1_mas(d): return {"Fàcil":f1_mas_f,"Mitjà":f1_mas_m,"Difícil":f1_mas_d}[d](d)


def f1_static_f(d):
    mode=random.choice(["moment", "equilibrium", "pressure"])
    if mode == "moment":
        F=random.choice([20,30,40]); braç=random.choice([0.5,0.8,1.2]); M=F*braç
        return _merge(_ans(M), f"Una força perpendicular $F={F}$ N actua a {braç} m del punt de gir. Calcula el moment.", f"$$M=Fd={F}({braç})={M}\\,N\\cdot m.$$" )
    if mode == "equilibrium":
        F=random.choice([20,30,40]); d1=random.choice([0.5,0.8]); d2=random.choice([1,1.2]); F2=F*d1/d2
        return _merge(_ans(F2), f"Una palanca en equilibri té una força de {F} N aplicada a {d1} m. Quina força cal aplicar a {d2} m per equilibrar-la?", f"Equilibri de moments:\n$$Fd_1=F_2d_2.$$\n\n$$F_2=\\frac{{Fd_1}}{{d_2}}={sp.latex(F2)}\\,N.$$" )
    rho=random.choice([800,1000,1200]); h=random.choice([1,2,4]); p=rho*9.81*h
    return _merge(_ans(p), f"Calcula la pressió hidrostàtica a {h} m en un líquid de densitat $\\rho={rho}$ kg/m³. Pren $g=9,81$ m/s².", f"$$p=\\rho gh={sp.latex(p)}\\,Pa.$$" )


def f1_static_m(d):
    mode=random.choice(["pressure", "buoyancy", "hydraulic"])
    if mode == "pressure":
        rho=random.choice([800,1000,1200]); h=random.choice([2,4,6]); p=rho*9.81*h
        return _merge(_ans(p), f"Calcula la pressió hidrostàtica a {h} m en un líquid de densitat $\\rho={rho}$ kg/m³. Pren $g=9,81$ m/s².", f"$$p=\\rho gh={sp.latex(p)}\\,Pa.$$" )
    rho=random.choice([500,700,800]); V=random.choice([0.002,0.003]); rhoa=1000; Fb=rhoa*9.81*V; W=rho*9.81*V; net=Fb-W
    return _merge(_ans(net), f"Un bloc de densitat {rho} kg/m³ i volum {V} m³ està submergit en aigua. Calcula la força resultant vertical (empenta menys pes).", f"$$E=\\rho_a gV,\\qquad P=\\rho gV.$$\n\n$$F_R=E-P={sp.latex(net)}\\,N.$$" )


def f1_static_d(d):
    mode=random.choice(["accel_buoyancy", "hydrostatic_force", "lever"])
    if mode == "accel_buoyancy":
        rho=random.choice([600,700,800]); g=9.81; a=(1000-rho)*g/rho
        return _merge(_ans(a), f"Un bloc de densitat {rho} kg/m³ es deixa anar completament submergit en aigua. Calcula l'acceleració inicial. Pren $g=9,81$ m/s².", f"$$ma=(\\rho_a-\\rho)gV,\\quad m=\\rho V.$$\n\n$$a=\\frac{{(\\rho_a-\\rho)g}}{{\\rho}}={sp.latex(a)}\\,m/s^2.$$" )
    rho=random.choice([900,1000,1100]); A=random.choice([0.2,0.4]); h=random.choice([2,4]); F=rho*9.81*h*A
    return _merge(_ans(F), f"Una superfície plana horitzontal de {A} m² està a {h} m de profunditat en un líquid de densitat {rho} kg/m³. Calcula la força deguda a la pressió hidrostàtica (pressió manomètrica).", f"$$p=\\rho gh.$$\n\n$$F=pA=\\rho ghA={sp.latex(F)}\\,N.$$" )


def generar_f1_static(d): return {"Fàcil":f1_static_f,"Mitjà":f1_static_m,"Difícil":f1_static_d}[d](d)


def generar_exercici_fisica1(d, tema):
    dispatch={'Cinemàtica':generar_f1_cinematica,'Dinàmica':generar_f1_dinamica,'Treball i Energia':generar_f1_energy,'Moviment Harmònic Simple (MAS)':generar_f1_mas,'Estàtica i Fluids':generar_f1_static}
    return dispatch[tema](d)

# --------------------------
# QUÍMICA I
# --------------------------

def q1_basic_f(d):
    mode=random.choice(["density", "mass", "volume"])
    if mode == "density":
        m=random.choice([20,50,80]); V=random.choice([10,20,40]); val=sp.Rational(m,V)
        return _merge(_ans(val), f"Una mostra té massa {m} g i volum {V} cm³. Calcula la densitat.", f"$$\\rho=\\frac{{m}}{{V}}={sp.latex(val)}\\,g/cm^3.$$" )
    if mode == "mass":
        rho=random.choice([0.8,1.2,2.5]); V=random.choice([10,20,50]); val=rho*V
        return _merge(_ans(val), f"Una substància té densitat {rho} g/cm³ i volum {V} cm³. Calcula la massa.", f"$$m=\\rho V={rho}({V})={val}\\,g.$$" )
    rho=random.choice([0.8,1.0,2.0]); m=random.choice([8,10,20]); val=m/rho
    return _merge(_ans(val), f"Una mostra té massa {m} g i densitat {rho} g/cm³. Calcula el volum.", f"$$V=\\frac{{m}}{{\\rho}}=\\frac{{{m}}}{{{rho}}}={val}\\,cm^3.$$" )


def q1_basic_m(d):
    mode=random.choice(["ideal", "moles_from_mass", "molarity"])
    if mode == "ideal":
        P=random.choice([1.2,2.0,3.0]); V=random.choice([2,4,5]); T=random.choice([300,350,400]); R=0.082057; n=P*V/(R*T)
        return _merge(_ans(n), f"Un gas ocupa {V} L a {P} atm i {T} K. Calcula els mols amb $PV=nRT$.", f"$$n=\\frac{{PV}}{{RT}}={sp.latex(n)}\\,mol.$$" )
    m=random.choice([18,36,44,88]); M=random.choice([18,44]); n=sp.Rational(m,M)
    return _merge(_ans(n), f"Calcula els mols de {m} g d'una substància de massa molar {M} g/mol.", f"$$n=\\frac{{m}}{{M}}={sp.latex(n)}\\,mol.$$" )


def q1_basic_d(d):
    mode=random.choice(["empirical", "molecular", "gas_mixture"])
    if mode == "empirical":
        return _merge({"resposta":["CH2O"],"tipus_resposta":"text"}, "Una substància conté 40,0% de C, 6,67% d'H i 53,33% d'O. Determina la fórmula empírica.", "Prenem 100 g, convertim a mols i dividim totes les quantitats pel menor valor.\n\nLa proporció és 1:2:1, per tant **CH₂O**.")
    if mode == "molecular":
        return _merge({"resposta":["C2H4O2"],"tipus_resposta":"text"}, "La fórmula empírica d'un compost és CH₂O i la seva massa molar és 60 g/mol. Determina la fórmula molecular.", "La massa de CH₂O és 30 g/mol.\n\n$$n=\\frac{60}{30}=2.$$\n\nMultipliquem tots els subíndexs per 2: **C₂H₄O₂**.")
    P,V,T=1.0,2.0,300; R=0.082057; n=P*V/(R*T)
    return _merge(_ans(n), "Una mescla gasosa ocupa 2,00 L a 1,00 atm i 300 K. Calcula els mols totals amb la llei dels gasos ideals.", f"$$n=\\frac{{PV}}{{RT}}={sp.latex(n)}\\,mol.$$\n\nCal controlar unitats i xifres significatives.")


def generar_q1_basic(d): return {"Fàcil":q1_basic_f,"Mitjà":q1_basic_m,"Difícil":q1_basic_d}[d](d)


def q1_atomic_f(d):
    mode=random.choice(["electrons", "protons", "mass_number"])
    if mode == "electrons":
        Z=random.choice([6,8,11,17,20]); return _merge(_ans(Z), f"Un àtom neutre té $Z={Z}$. Quants electrons té?", f"En un àtom neutre $e^-=Z={Z}$.")
    if mode == "protons":
        Z=random.choice([6,8,12,17,20]); return _merge(_ans(Z), f"Un element té nombre atòmic $Z={Z}$. Quants protons té?", f"El nombre atòmic és el nombre de protons: $p^+={Z}$.")
    Z=random.choice([6,8,11,17]); N=random.choice([6,8,10,18]); return _merge(_ans(Z+N), f"Un nucli té $Z={Z}$ protons i {N} neutrons. Calcula el nombre màssic $A$.", f"$$A=Z+N={Z}+{N}={Z+N}.$$" )


def q1_atomic_m(d):
    mode=random.choice(["ion", "isotope", "average"])
    if mode == "ion":
        Z,N,charge=random.choice([(17,18,-1),(11,12,1),(8,8,-2),(20,20,2)]); e=Z-charge
        return _merge(_ans(e), f"Un ió té $Z={Z}$, {N} neutrons i càrrega {charge:+d}. Calcula els electrons.", f"$$q=Z-e^-\\Rightarrow e^-={Z}-({charge})={e}.$$" )
    if mode == "isotope":
        A=random.choice([23,35,37,40]); Z=random.choice([11,17,20]); N=A-Z
        return _merge(_ans(N), f"Un isòtop té nombre màssic $A={A}$ i nombre atòmic $Z={Z}$. Calcula els neutrons.", f"$$N=A-Z={A}-{Z}={N}.$$" )
    return _merge(_ans(2), "Un element té dos isòtops amb abundàncies 75% i 25%. Els nombres màssics són 1 i 5. Quin és el nombre màssic mitjà?", "$$A_{mitjà}=0,75(1)+0,25(5)=2.$$" )


def q1_atomic_d(d):
    mode=random.choice(["configuration", "orbital_capacity", "periodic_position"])
    if mode == "configuration":
        choices=[("Cl",17,"1s2 2s2 2p6 3s2 3p5",7),("Ca",20,"1s2 2s2 2p6 3s2 3p6 4s2",2),("O",8,"1s2 2s2 2p4",6),("Na",11,"1s2 2s2 2p6 3s1",1)]
        sym,Z,conf,val=random.choice(choices)
        return _merge({"resposta":[conf],"tipus_resposta":"text"}, f"Escriu la configuració electrònica de {sym} ($Z={Z}$) i indica els electrons de valència.", f"La configuració és **{conf}** i té **{val}** electrons de valència.")
    if mode == "orbital_capacity":
        n=random.choice([2,3,4]); val=2*n*n
        return _merge(_ans(val), f"Quants electrons com a màxim pot contenir la capa principal $n={n}$?", f"La capacitat màxima és $2n^2$.\n\n$$2({n})^2={val}.$$" )
    return _merge({"resposta":["halogen"],"tipus_resposta":"text"}, "Un element del grup 17 pertany a quina família de la taula periòdica?", "El grup 17 correspon als **halògens**.")


def generar_q1_atomic(d): return {"Fàcil":q1_atomic_f,"Mitjà":q1_atomic_m,"Difícil":q1_atomic_d}[d](d)


def q1_bond_f(d):
    pairs=[("NaCl","iònic"),("H2O","covalent polar"),("Cl2","covalent apolar"),("Cu","metàl·lic"),("MgO","iònic"),("O2","covalent apolar")]
    f,a=random.choice(pairs); return _merge({"resposta":[a],"tipus_resposta":"text"}, f"Indica el tipus d'enllaç predominant en {f}.", f"Segons els elements i l'electronegativitat, predomina l'enllaç **{a}**.")


def q1_bond_m(d):
    mode=random.choice(["polarity", "geometry", "lewis"])
    if mode == "polarity":
        pairs=[("H2O","polar"),("CO2","apolar"),("NH3","polar"),("CH4","apolar"),("SO2","polar")]; mol,ans=random.choice(pairs)
        return _merge({"resposta":[ans],"tipus_resposta":"text"}, f"Indica si la molècula {mol} és polar o apolar.", f"Cal combinar polaritat dels enllaços i geometria. Per a {mol}, el resultat és **{ans}**.")
    if mode == "geometry":
        pairs=[("CO2","lineal"),("H2O","angular"),("NH3","piramidal trigonal"),("CH4","tetraèdrica")]; mol,ans=random.choice(pairs)
        return _merge({"resposta":[ans],"tipus_resposta":"text"}, f"Indica la geometria molecular aproximada de {mol}.", f"Segons VSEPR, {mol} presenta geometria **{ans}**.")
    return _merge({"resposta":["2H2O"],"tipus_resposta":"text"}, "Quants parells d'electrons no enllaçants té l'àtom d'oxigen en H₂O?", "L'oxigen té 6 electrons de valència, en comparteix dos en els enllaços i conserva 4 electrons com a dos parells lliures.\n\nResposta: **2 parells**.")


def q1_bond_d(d):
    mode=random.choice(["formula", "oxidation", "stoich"])
    if mode == "formula":
        pairs=[("sulfat d'alumini","Al2(SO4)3"),("hidròxid de calci","Ca(OH)2"),("clorur de ferro(III)","FeCl3"),("carbonat de sodi","Na2CO3"),("nitrat de magnesi","Mg(NO3)2")]; name,formula=random.choice(pairs)
        return _merge({"resposta":[formula],"tipus_resposta":"text"}, f"Escriu la fórmula de **{name}**.", f"Neutralitzem les càrregues dels ions i simplifiquem la proporció.\n\nLa fórmula és **{formula}**.")
    if mode == "oxidation":
        return _merge(_ans(6), "Quin és el nombre d'oxidació del sofre en SO₄²⁻?", "L'oxigen aporta $4(-2)=-8$. La càrrega total és -2:\n\n$$x-8=-2\\Rightarrow x=+6.$$" )
    return _merge(_ans(2), "Quina és la proporció mínima d'ions Al³⁺ i O²⁻ en un compost neutre?", "El mínim comú múltiple de 3 i 2 és 6: calen 2 Al³⁺ i 3 O²⁻.\n\nLa proporció és **2:3**.")


def generar_q1_bond(d): return {"Fàcil":q1_bond_f,"Mitjà":q1_bond_m,"Difícil":q1_bond_d}[d](d)


def q1_quant_f(d):
    M=random.choice([18,44,58.5]); m=random.choice([18,44,117]); n=sp.Rational(str(m))/sp.Rational(str(M))
    return _merge(_ans(n), f"Calcula els mols de {m} g d'una substància de massa molar $M={M}$ g/mol.", f"$$n=\\frac{{m}}{{M}}=\\frac{{{m}}}{{{M}}}={sp.latex(n)}\\,mol.$$" )


def q1_quant_m(d):
    C=random.choice([0.20,0.50,1.00]); V=random.choice([0.25,0.50,1.00]); n=C*V
    return _merge(_ans(n), f"Quants mols de solut hi ha en {V} L d'una dissolució de concentració {C} mol/L?", f"$$n=cV={C}({V})={sp.latex(n)}\\,mol.$$" )


def q1_quant_d(d):
    molH2=random.choice([2.5,3.0,5.0,7.0]); molO2=random.choice([1.0,1.5,2.0,3.0]); product=min(molH2,2*molO2)
    return _merge(_ans(product), f"En $2H_2+O_2\\rightarrow2H_2O$, reaccionen {molH2} mol d'H₂ i {molO2} mol d'O₂. Determina els mols màxims d'H₂O que es poden formar.", f"La proporció és $2:1:2$.\n\nEl producte màxim és el menor entre $n(H_2)$ i $2n(O_2)$:\n$$n(H_2O)={sp.latex(product)}\\,mol.$$" )


def generar_q1_quant(d): return {"Fàcil":q1_quant_f,"Mitjà":q1_quant_m,"Difícil":q1_quant_d}[d](d)


def q1_rxn_f(d):
    mode=random.choice(["stoich", "balance", "mass"])
    if mode == "stoich":
        n=random.choice([1,2,3,4]); return _merge(_ans(n), f"En $2H_2+O_2\\rightarrow2H_2O$, si reaccionen {n} mol d'H₂ amb O₂ en excés, quants mols d'H₂O es formen?", f"La relació H₂:H₂O és 1:1, per tant es formen **{n} mol**.")
    if mode == "balance":
        return _merge({"resposta":["2H2+O2->2H2O"],"tipus_resposta":"text"}, "Ajusta la reacció $H_2+O_2\\rightarrow H_2O$.", "Per conservar H i O:\n\n$$2H_2+O_2\\rightarrow2H_2O.$$" )
    m=random.choice([12,24,36]); n=sp.Rational(m,12)
    return _merge(_ans(n), f"En $C+O_2\\rightarrow CO_2$, quants mols de CO₂ es formen a partir de {m} g de C? Usa $M(C)=12$ g/mol.", f"$$n(C)=\\frac{{{m}}}{{12}}={sp.latex(n)}\\,mol.$$\n\nLa proporció és 1:1.")


def q1_rxn_m(d):
    mode=random.choice(["moles", "solution", "concentration"])
    if mode == "moles":
        m=random.choice([10,20,25,36]); n=sp.Rational(m,12)
        return _merge(_ans(n), f"En $C+O_2\\rightarrow CO_2$, calcula els mols de CO₂ obtinguts a partir de {m} g de C. Usa $M(C)=12$ g/mol.", f"$$n(C)=\\frac{{m}}{{M}}={sp.latex(n)}\\,mol.$$\n\nLa proporció és 1:1.")
    C=random.choice([0.20,0.50,1.00]); V=random.choice([0.25,0.50,1.00]); n=C*V
    return _merge(_ans(n), f"Quants mols de solut hi ha en {V} L d'una dissolució {C} M?", f"$$n=CV={C}({V})={n}\\,mol.$$" )


def q1_rxn_d(d):
    mode=random.choice(["limiting", "yield", "combustion"])
    if mode == "limiting":
        H2=random.choice([3,5,7]); O2=random.choice([1,2,3]); product=min(H2,2*O2)
        return _merge(_ans(product), f"En $2H_2+O_2\\rightarrow2H_2O$, reaccionen {H2} mol d'H₂ i {O2} mol d'O₂. Determina el màxim d'H₂O.", f"Per la proporció 2:1:2,\n$$n(H_2O)=\\min({H2},2\\cdot{O2})={product}\\,mol.$$" )
    if mode == "yield":
        real,teor=random.choice([(10.0,12.5),(15.0,20.0),(18.0,24.0),(32.0,40.0)]); eta=100*real/teor
        return _merge(_ans(eta), f"S'obtenen {real} g de producte quan teòricament se n'haurien d'obtenir {teor} g. Calcula el rendiment.", f"$$\\eta=\\frac{{{real}}}{{{teor}}}100={eta}\\%.$$" )
    return _merge({"resposta":["C3H8+5O2->3CO2+4H2O"],"tipus_resposta":"text"}, "Ajusta la combustió completa del propà, C₃H₈.", "Ajustem C, H i finalment O:\n\n$$C_3H_8+5O_2\\rightarrow3CO_2+4H_2O.$$" )


def generar_q1_rxn(d): return {"Fàcil":q1_rxn_f,"Mitjà":q1_rxn_m,"Difícil":q1_rxn_d}[d](d)


def q1_carbon_f(d):
    mode=random.choice(["family", "formula", "functional"])
    if mode == "family":
        pairs=[("CH4","alcà"),("C2H4","alquè"),("C2H2","alquí"),("CH3CH2OH","alcohol"),("CH3COOH","àcid carboxílic")]; f,a=random.choice(pairs)
        return _merge({"resposta":[a],"tipus_resposta":"text"}, f"Identifica la família principal de {f}.", f"La fórmula correspon a un **{a}**.")
    pairs=[("CH3CH2OH","alcohol"),("CH3CHO","aldehid"),("CH3COCH3","cetona"),("CH3COOH","àcid carboxílic")]; f,a=random.choice(pairs)
    return _merge({"resposta":[a],"tipus_resposta":"text"}, f"Identifica el grup funcional predominant en {f}.", f"El grup funcional correspon a un **{a}**.")


def q1_carbon_m(d):
    mode=random.choice(["naming", "formula", "isomer"])
    if mode == "naming":
        pairs=[("CH3CH2OH","etanol"),("CH3COOH","àcid etanoic"),("CH3CHO","etanal"),("CH3COCH3","propanona"),("CH3CH2CH2OH","propan-1-ol")]; f,n=random.choice(pairs)
        return _merge({"resposta":[n],"tipus_resposta":"text"}, f"Dona el nom del compost **{f}**.", f"Identifiquem la cadena principal i el grup funcional. El nom és **{n}**.")
    pairs=[("etanol","CH3CH2OH"),("etè","C2H4"),("etí","C2H2"),("àcid etanoic","CH3COOH")]; n,f=random.choice(pairs)
    return _merge({"resposta":[f],"tipus_resposta":"text"}, f"Escriu la fórmula molecular o semidesenvolupada de **{n}**.", f"La fórmula correcta és **{f}**.")


def q1_carbon_d(d):
    mode=random.choice(["combustion", "formula_from_combustion", "reaction"])
    if mode == "combustion":
        choices=[("C3H8",5,3,4),("C2H6",7,4,6),("C4H10",13,8,10)]; formula,o2,co2,h2o=random.choice(choices); reaction=f"{formula}+{o2}O2->{co2}CO2+{h2o}H2O"
        return _merge({"resposta":[reaction],"tipus_resposta":"text"}, f"Ajusta la combustió completa de **{formula}**.", f"Conservem C, H i finalment O:\n\n$$\\boxed{{{formula}+{o2}O_2\\rightarrow{co2}CO_2+{h2o}H_2O}}.$$" )
    return _merge({"resposta":["C2H4"],"tipus_resposta":"text"}, "Un hidrocarbur té 2 àtoms de carboni i un doble enllaç. Escriu la fórmula molecular.", "Un alquè acíclic segueix $C_nH_{2n}$. Per $n=2$:\n\n**C₂H₄**.")


def generar_q1_carbon(d): return {"Fàcil":q1_carbon_f,"Mitjà":q1_carbon_m,"Difícil":q1_carbon_d}[d](d)


def generar_exercici_quimica1(d, tema):
    dispatch={'Conceptes bàsics i lleis':generar_q1_basic,'Estructura atòmica':generar_q1_atomic,'Enllaç químic i formulació':generar_q1_bond,'Aspectes quantitatius':generar_q1_quant,'Reaccions químiques':generar_q1_rxn,'Química del carboni':generar_q1_carbon}
    return dispatch[tema](d)


# ============================================================
# NORMALITZACIÓ DE RESULTATS — 4 XIFRES SIGNIFICATIVES
# ============================================================

def quatre_xifres(v):
    """Arrodoneix un nombre real a 4 xifres significatives."""
    try:
        z = sp.sympify(v)
        if z.free_symbols or not z.is_number or not z.is_real:
            return v
        import math
        x = float(z)
        if x == 0:
            return sp.Integer(0)
        exponent = int(math.floor(math.log10(abs(x))))
        decimals = 3 - exponent
        return sp.Float(round(x, decimals))
    except Exception:
        return v


def normalitza_exercici_ciencia(exercici):
    """Física/Química: guarda els resultats numèrics arrodonits a 4 xifres significatives."""
    if exercici.get('tipus_resposta', 'escalar') in {'text','vector','vector2','matriu','sistema','classificacio','classificacio_vector','interval'}:
        return exercici
    exercici['resposta'] = [quatre_xifres(r) if isinstance(r, (int,float,sp.Number,sp.Expr)) else r for r in exercici.get('resposta', [])]
    return exercici


def normalitza_exercici_mates(exercici):
    """Matemàtiques: els resultats numèrics decimals tenen com a màxim 4 xifres significatives."""
    tipus = exercici.get('tipus_resposta', 'escalar')
    if tipus in {'text','classificacio','parametre_rouche','matriu','sistema','vector','classificacio_vector','interval'}:
        # Els resultats exactes (fraccions, radicals, matrius...) es mantenen exactes.
        return exercici
    out=[]
    for r in exercici.get('resposta', []):
        try:
            expr=sp.sympify(r)
            if not expr.free_symbols and expr.is_number and expr.is_real and isinstance(expr, (sp.Float, float)):
                out.append(quatre_xifres(expr))
            else:
                out.append(r)
        except Exception:
            out.append(r)
    exercici['resposta']=out
    return exercici


def format_ciencia_4sf(v):
    """Mostra exactament 4 xifres significatives per als resultats de Física i Química."""
    try:
        x=float(sp.N(v))
        if x == 0:
            return "0.000"
        import math
        exponent=int(math.floor(math.log10(abs(x))))
        decimals=3-exponent
        if decimals >= 0 and decimals <= 12:
            return f"{x:.{decimals}f}"
        return f"{x:.3e}"
    except Exception:
        return str(v)


def resposta_ciencia_correcta(alumne, correctes):
    """Accepta el valor exacte o el valor correctament arrodonit a 4 xifres significatives."""
    try:
        x=float(sp.N(alumne))
    except Exception:
        return resposta_correcta(alumne, correctes)
    import math
    for r in correctes:
        try:
            y=float(sp.N(r))
            if y == 0:
                if abs(x) <= 5e-12:
                    return True
                continue
            exponent=int(math.floor(math.log10(abs(y))))
            decimals=3-exponent
            tol=0.5*(10**(-decimals)) + 1e-12
            if abs(x-y) <= tol:
                return True
        except Exception:
            try:
                if sp.simplify(alumne-r)==0:
                    return True
            except Exception:
                pass
    return False

# ============================================================
# FUNCIONS DE NAVEGACIÓ
# ============================================================

def tornar_inici():
    st.session_state.curs = None
    st.session_state.assignatura = None
    st.session_state.tema = None
    st.session_state.dificultat = None
    st.session_state.exercici = None
    st.session_state.mostrar_resposta = False
    st.session_state.mostrar_passos = False
    st.session_state.historial_exercicis = []


def tornar_assignatures():
    st.session_state.assignatura = None
    st.session_state.tema = None
    st.session_state.dificultat = None
    st.session_state.exercici = None
    st.session_state.mostrar_resposta = False
    st.session_state.mostrar_passos = False
    st.session_state.historial_exercicis = []


def tornar_temes():
    st.session_state.tema = None
    st.session_state.dificultat = None
    st.session_state.exercici = None
    st.session_state.mostrar_resposta = False
    st.session_state.mostrar_passos = False
    st.session_state.historial_exercicis = []


def tornar_dificultat():
    st.session_state.dificultat = None
    st.session_state.exercici = None
    st.session_state.mostrar_resposta = False
    st.session_state.mostrar_passos = False
    st.session_state.historial_exercicis = []


def _firma_exercici(exercici):
    """Crea una firma simple per detectar exercicis idèntics."""
    respostes = exercici.get("resposta", [])
    signatures = []
    for r in respostes:
        if isinstance(r, sp.MatrixBase):
            signatures.append(tuple(map(str, list(r))))
        else:
            signatures.append(str(r))
    return (
        exercici.get("enunciat", ""),
        tuple(signatures),
    )


def nou_exercici():
    if st.session_state.assignatura == "📐 Matemàtiques I":
        generador = lambda d: generar_exercici_mates1(d, st.session_state.tema)
    elif st.session_state.assignatura == "⚛️ Física I":
        generador = lambda d: generar_exercici_fisica1(d, st.session_state.tema)
    elif st.session_state.assignatura == "⚗️ Química I":
        generador = lambda d: generar_exercici_quimica1(d, st.session_state.tema)
    elif st.session_state.assignatura == "📐 Matemàtiques II":
        generador = lambda d: generar_exercici_mates2(d, st.session_state.tema)
    elif st.session_state.assignatura == "⚛️ Física II":
        generador = lambda d: generar_exercici_fisica2(d, st.session_state.tema)
    elif st.session_state.assignatura == "⚗️ Química II":
        generador = lambda d: generar_exercici_quimica2(d, st.session_state.tema)
    else:
        st.session_state.exercici = None
        st.session_state.mostrar_resposta = False
        st.session_state.mostrar_passos = False
        return

    exercici = None
    firma = None

    for _ in range(30):
        try:
            candidat = generador(st.session_state.dificultat)
            if st.session_state.assignatura in ["⚛️ Física I", "⚛️ Física II", "⚗️ Química I", "⚗️ Química II"]:
                candidat = normalitza_exercici_ciencia(candidat)
            elif st.session_state.assignatura in ["📐 Matemàtiques I", "📐 Matemàtiques II"]:
                candidat = normalitza_exercici_mates(candidat)
            candidata_firma = _firma_exercici(candidat)

            if candidata_firma not in st.session_state.historial_exercicis:
                exercici = candidat
                firma = candidata_firma
                break

            if exercici is None:
                exercici = candidat
                firma = candidata_firma

        except Exception:
            continue

    if exercici is None:
        st.error(
            "No s'ha pogut generar un exercici nou. "
            "Torna a seleccionar la dificultat."
        )
        return

    st.session_state.exercici = exercici
    st.session_state.historial_exercicis.append(firma)
    st.session_state.historial_exercicis = st.session_state.historial_exercicis[-30:]
    st.session_state.mostrar_resposta = False
    st.session_state.mostrar_passos = False


# ============================================================
# COMPROVADOR DE RESPOSTES
# ============================================================

TRANSFORMATIONS = (
    standard_transformations
    + (implicit_multiplication_application, convert_xor)
)


def interpretar_resposta(text):
    """
    Interpreta una resposta escalar.

    Exemples:
    5
    -2
    3/4
    sqrt(6)
    2^3
    """
    text = text.strip().replace(",", ".")

    if not text:
        raise ValueError("Resposta buida")

    return parse_expr(
        text,
        transformations=TRANSFORMATIONS,
        evaluate=True,
    )



def interpretar_vector(text):
    """Interpreta un vector de 3 components: 1,2,3; (1,2,3); [1 2 3]."""
    text = text.strip()
    if not text:
        raise ValueError("Vector buit")
    text = text.replace("(", "").replace(")", "")
    text = text.replace("[", "").replace("]", "")
    parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
    if len(parts) == 1:
        parts = text.split()
    if len(parts) != 3:
        raise ValueError("Un vector de l'espai ha de tenir 3 components")
    return sp.Matrix([interpretar_resposta(p) for p in parts])


def resposta_vector_correcta(resposta_alumne, respostes_correctes):
    for correcta in respostes_correctes:
        correcta = sp.Matrix(correcta)
        if resposta_alumne.shape != correcta.shape:
            continue
        if all(sp.simplify(a - b) == 0 for a, b in zip(resposta_alumne, correcta)):
            return True
    return False


def resposta_classificacio_vector_correcta(resposta_alumne, respostes_correctes):
    text = resposta_alumne.strip().upper()
    aliases = {"SI": "SI", "SÍ": "SI", "NO": "NO", "COPLANARS": "SI", "NO COPLANARS": "NO"}
    normalized = aliases.get(text, text)
    return any(normalized == str(r).upper() for r in respostes_correctes)

def interpretar_matriu(text):
    """
    Interpreta matrius escrites com:
      1 2; 3 4
      [1 2; 3 4]
      [[1,2],[3,4]]
    """
    text = text.strip()

    # Format Python/llista: [[1,2],[3,4]]
    if text.startswith("[[") and text.endswith("]]"):
        text = text[2:-2]
        text = text.replace("],[", ";")
        text = text.replace("], [", ";")
        text = text.replace("],  [", ";")
        text = text.replace("[", "").replace("]", "")
    else:
        text = text.replace("[", "").replace("]", "")
        text = text.replace(",", " ")

    files = [f.strip() for f in text.split(";") if f.strip()]
    if not files:
        raise ValueError("Matriu buida")

    files_parsed = []
    for fila in files:
        parts = fila.replace(",", " ").split()
        if not parts:
            raise ValueError("Fila buida")
        files_parsed.append([
            interpretar_resposta(part) for part in parts
        ])

    ncols = len(files_parsed[0])
    if any(len(fila) != ncols for fila in files_parsed):
        raise ValueError(
            "Totes les files han de tenir el mateix nombre d'elements"
        )

    return sp.Matrix(files_parsed)



def interpretar_sistema(text, n):
    """Interpreta respostes com x=1, y=-2, z=3 o simplement 1, -2, 3."""
    text = text.strip()
    if not text:
        raise ValueError("Resposta buida")

    # Accepta x=..., y=..., z=...
    if "=" in text:
        parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
        values = []
        for part in parts:
            if "=" not in part:
                raise ValueError("Format incorrecte")
            _, value = part.split("=", 1)
            values.append(interpretar_resposta(value))
    else:
        parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
        values = [interpretar_resposta(p) for p in parts]

    if len(values) != n:
        raise ValueError("Nombre de variables incorrecte")
    return [sp.simplify(v) for v in values]


def resposta_sistema_correcta(resposta_alumne, respostes_correctes):
    for correcta in respostes_correctes:
        if len(resposta_alumne) != len(correcta):
            continue
        if all(sp.simplify(a - b) == 0 for a, b in zip(resposta_alumne, correcta)):
            return True
    return False


def resposta_classificacio_correcta(resposta_alumne, respostes_correctes):
    text = resposta_alumne.strip().upper()
    aliases = {
        "SCD": "SCD",
        "COMPATIBLE DETERMINAT": "SCD",
        "COMPATIBLE DETERMINADO": "SCD",
        "SCI": "SCI",
        "COMPATIBLE INDETERMINAT": "SCI",
        "COMPATIBLE INDETERMINADO": "SCI",
        "SI": "SI",
        "INCOMPATIBLE": "SI",
    }
    normalized = aliases.get(text, text)
    return any(normalized == str(r).upper() for r in respostes_correctes)

def resposta_text_correcta(resposta_alumne, respostes_correctes):
    text = " ".join(resposta_alumne.strip().lower().split())
    for correcta in respostes_correctes:
        if text == " ".join(str(correcta).strip().lower().split()):
            return True
    return False


def format_mates_4sf(v):
    """Mostra resultats numèrics de Matemàtiques amb un màxim de 4 xifres significatives."""
    if isinstance(v, sp.MatrixBase):
        return sp.latex(v)
    if isinstance(v, (sp.Integer, int)):
        return str(v)
    if isinstance(v, sp.Rational) and not v.is_Integer:
        return sp.latex(v)
    try:
        expr=sp.sympify(v)
        if expr.free_symbols:
            return sp.latex(expr)
        if expr.is_Rational and not expr.is_Integer:
            return sp.latex(expr)
        x=float(sp.N(expr))
        if x == 0:
            return "0"
        return format(x, ".4g")
    except Exception:
        return sp.latex(v) if isinstance(v, sp.Basic) else str(v)


def resposta_mates_correcta_4sf(alumne, correctes):
    """Comprova Matemàtiques permetent l'arrodoniment a un màxim de 4 xifres significatives."""
    for correcta in correctes:
        try:
            y=float(sp.N(correcta))
            x=float(sp.N(alumne))
            if y == 0:
                if abs(x) < 0.00005:
                    return True
                continue
            import math
            exponent=int(math.floor(math.log10(abs(y))))
            decimals=3-exponent
            unit=10**(-decimals)
            tol=0.5*abs(unit)+1e-12
            if abs(x-y) <= tol:
                return True
        except Exception:
            pass
        try:
            if sp.simplify(alumne-correcta)==0:
                return True
        except Exception:
            pass
    return False


def resposta_correcta(resposta_alumne, respostes_correctes):
    """Comprova una resposta escalar contra les respostes correctes."""
    for resposta in respostes_correctes:
        correcta = interpretar_resposta(str(resposta))

        try:
            if sp.simplify(resposta_alumne - correcta) == 0:
                return True
        except Exception:
            pass

        try:
            if sp.N(resposta_alumne - correcta) == 0:
                return True
        except Exception:
            pass

    return False


def resposta_matriu_correcta(resposta_alumne, respostes_correctes):
    """Comprova una resposta matricial element per element."""
    for correcta in respostes_correctes:
        if not isinstance(correcta, sp.MatrixBase):
            correcta = sp.Matrix(correcta)

        if resposta_alumne.shape != correcta.shape:
            continue

        diferencia = resposta_alumne - correcta
        if all(sp.simplify(x) == 0 for x in diferencia):
            return True

    return False


# ============================================================
# PANTALLA 1 — CURS
# ============================================================

if st.session_state.curs is None:

    st.title("🎓 Preparació Batxillerat")
    st.write("### Selecciona el curs que vols preparar")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🟢 1r Batxillerat", use_container_width=True):
            st.session_state.curs = "1r Batxillerat"
            st.rerun()

    with col2:
        if st.button("🔵 2n Batxillerat", use_container_width=True):
            st.session_state.curs = "2n Batxillerat"
            st.rerun()


# ============================================================
# PANTALLA 2 — ASSIGNATURA
# ============================================================

elif st.session_state.assignatura is None:

    st.title(f"📚 {st.session_state.curs}")
    st.write("### Selecciona l'assignatura")

    assignatures = list(TEMARI[st.session_state.curs].keys())
    columnes = st.columns(len(assignatures))

    for columna, assignatura in zip(columnes, assignatures):
        with columna:
            if st.button(assignatura, use_container_width=True):
                st.session_state.assignatura = assignatura
                st.rerun()

    st.divider()

    if st.button("← Tornar a l'inici"):
        tornar_inici()
        st.rerun()


# ============================================================
# PANTALLA 3 — TEMA
# ============================================================

elif st.session_state.tema is None:

    st.title(st.session_state.assignatura)
    st.caption(st.session_state.curs)
    st.write("### Selecciona el tema")

    temes = TEMARI[
        st.session_state.curs
    ][
        st.session_state.assignatura
    ]

    for inici in range(0, len(temes), 3):
        fila = temes[inici:inici + 3]
        columnes = st.columns(3)

        for columna, tema in zip(columnes, fila):
            with columna:
                if st.button(tema, use_container_width=True):
                    st.session_state.tema = tema
                    st.rerun()

    st.divider()

    if st.button("← Tornar a les assignatures"):
        tornar_assignatures()
        st.rerun()

    if st.button("🏠 Tornar a l'inici"):
        tornar_inici()
        st.rerun()


# ============================================================
# PANTALLA 4 — DIFICULTAT
# ============================================================

elif st.session_state.dificultat is None:

    st.title(st.session_state.tema)

    st.caption(
        f"{st.session_state.curs} · "
        f"{st.session_state.assignatura}"
    )

    st.write("### Selecciona la dificultat")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🟢 Fàcil", use_container_width=True):
            st.session_state.dificultat = "Fàcil"
            nou_exercici()
            st.rerun()

    with col2:
        if st.button("🟡 Mitjà", use_container_width=True):
            st.session_state.dificultat = "Mitjà"
            nou_exercici()
            st.rerun()

    with col3:
        if st.button("🔴 Difícil", use_container_width=True):
            st.session_state.dificultat = "Difícil"
            nou_exercici()
            st.rerun()

    if st.session_state.assignatura in ["📐 Matemàtiques I", "⚛️ Física I", "⚗️ Química I", "📐 Matemàtiques II", "⚛️ Física II", "⚗️ Química II"]:
        st.success("✅ Aquest tema té generadors per als tres nivells de dificultat.")

    st.divider()

    if st.button("← Tornar als temes"):
        tornar_temes()
        st.rerun()

    if st.button("🏠 Tornar a l'inici"):
        tornar_inici()
        st.rerun()


# ============================================================
# PANTALLA 5 — EXERCICI
# ============================================================

else:

    if st.session_state.exercici is None:
        st.info("Aquest tema encara no té exercicis disponibles.")

        if st.button("← Tornar als temes"):
            tornar_temes()
            st.rerun()

    else:

        exercici = st.session_state.exercici

        st.title(
            f"✏️ Exercici · {st.session_state.dificultat}"
        )

        st.caption(
            f"{st.session_state.curs} · "
            f"{st.session_state.assignatura} · "
            f"{st.session_state.tema}"
        )

        st.divider()

        # ENUNCIAT
        st.markdown(exercici["enunciat"])

        st.divider()

        # AJUDA D'ESCRIPTURA
        st.markdown(
            "**✏️ Introduceix la teva resposta**"
        )

        tipus_resposta = exercici.get("tipus_resposta", "escalar")

        if tipus_resposta == "matriu":
            st.caption(
                "💡 Escriu la matriu separant les files amb `;` i els elements "
                "amb espais. Exemple: `1 2; 3 4`. També pots usar `[[1,2],[3,4]]`."
            )
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: 1 2; 3 4", label_visibility="collapsed"
            )
        elif tipus_resposta == "sistema":
            st.caption(
                "💡 Escriu les solucions com `x=2, y=-1, z=3`. També pots escriure només `2, -1, 3`. "
                "Usa `sqrt(6)` per a arrels i `/` per a fraccions."
            )
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: x=2, y=-1, z=3", label_visibility="collapsed"
            )
        elif tipus_resposta == "classificacio":
            st.caption("💡 Escriu `SCD` (una solució), `SCI` (infinites) o `SI` (cap solució).")
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: SCD", label_visibility="collapsed"
            )
        elif tipus_resposta == "parametre_rouche":
            st.caption("💡 Escriu el valor del paràmetre amb la mateixa sintaxi matemàtica: `4`, `-2`, `sqrt(6)`, etc.")
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: 4", label_visibility="collapsed"
            )
        elif tipus_resposta == "vector":
            st.caption("💡 Escriu el vector com `1, 2, 3`. També pots usar `(1, 2, 3)` o `1 2 3`. Usa `sqrt(6)` per a arrels.")
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: 2, -1, 3", label_visibility="collapsed"
            )
        elif tipus_resposta == "classificacio_vector":
            st.caption("💡 Escriu `SI` si són coplanaris o `NO` si no ho són.")
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: SI", label_visibility="collapsed"
            )
        elif tipus_resposta == "interval":
            st.caption("💡 Escriu els dos extrems separats per una coma. Exemple: `90,110`.")
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: 90, 110", label_visibility="collapsed"
            )
        elif tipus_resposta == "text":
            st.caption("💡 Escriu la resposta amb paraules. No cal que coincideixi exactament en majúscules/minúscules.")
            resposta = st.text_input(
                "Resposta:", placeholder="Escriu la resposta...", label_visibility="collapsed"
            )
        else:
            if st.session_state.assignatura in ["⚛️ Física I", "⚛️ Física II", "⚗️ Química I", "⚗️ Química II"]:
                st.caption(
                    "💡 Dona el resultat amb **4 xifres significatives**. Si cal, arrodoneix. Usa `sqrt(6)` per a √6, `^` per a potències i `/` per a fraccions. Exemple: `3.142`."
                )
            else:
                st.caption(
                    "💡 En resultats numèrics, dona com a màxim **4 xifres significatives**. Usa `sqrt(6)` per a √6, `^` per a potències i `/` per a fraccions. Exemple: `3/4`."
                )
            resposta = st.text_input(
                "Resposta:", placeholder="Exemple: 5, -2, sqrt(6), 3/4...", label_visibility="collapsed"
            )

        # COMPROVAR
        if st.button("✅ Comprovar resposta"):

            if not resposta.strip():
                st.warning(
                    "⚠️ Escriu una resposta abans de comprovar-la."
                )

            else:
                try:
                    tipus = exercici.get("tipus_resposta", "escalar")

                    if tipus == "matriu":
                        alumne = interpretar_matriu(resposta)
                        correcte = resposta_matriu_correcta(
                            alumne, exercici["resposta"]
                        )
                    elif tipus == "sistema":
                        # El nombre de variables se dedueix de la resposta correcta.
                        n = len(exercici["resposta"][0])
                        alumne = interpretar_sistema(resposta, n)
                        correcte = resposta_sistema_correcta(
                            alumne, exercici["resposta"]
                        )
                    elif tipus == "classificacio":
                        correcte = resposta_classificacio_correcta(
                            resposta, exercici["resposta"]
                        )
                    elif tipus == "parametre_rouche":
                        alumne = interpretar_resposta(resposta)
                        correcte = resposta_correcta(
                            alumne, exercici["resposta"]
                        )
                    elif tipus == "vector":
                        alumne = interpretar_vector(resposta)
                        correcte = resposta_vector_correcta(
                            alumne, exercici["resposta"]
                        )
                    elif tipus == "classificacio_vector":
                        correcte = resposta_classificacio_vector_correcta(
                            resposta, exercici["resposta"]
                        )
                    elif tipus == "interval":
                        alumne = interpretar_interval(resposta)
                        correcte = resposta_interval_correcta(
                            alumne, exercici["resposta"]
                        )
                    elif tipus == "text":
                        correcte = resposta_text_correcta(resposta, exercici["resposta"])
                    else:
                        alumne = interpretar_resposta(resposta)
                        if st.session_state.assignatura in ["⚛️ Física I", "⚛️ Física II", "⚗️ Química I", "⚗️ Química II"]:
                            correcte = resposta_ciencia_correcta(alumne, exercici["resposta"])
                        else:
                            if st.session_state.assignatura in ["📐 Matemàtiques I", "📐 Matemàtiques II"]:
                                correcte = resposta_mates_correcta_4sf(alumne, exercici["resposta"])
                            else:
                                correcte = resposta_correcta(
                                    alumne, exercici["resposta"]
                                )

                    if correcte:
                        st.success("🎉 Correcte!")
                    else:
                        st.error(
                            "❌ Incorrecte. Torna-ho a intentar."
                        )

                except Exception:
                    tipus = exercici.get("tipus_resposta", "escalar")
                    if tipus == "matriu":
                        msg = "⚠️ No he pogut interpretar la matriu. Escriu-la, per exemple, com `1 2; 3 4`."
                    elif tipus == "sistema":
                        msg = "⚠️ No he pogut interpretar el sistema. Escriu-lo, per exemple, com `x=2, y=-1, z=3`."
                    elif tipus == "classificacio":
                        msg = "⚠️ Escriu `SCD`, `SCI` o `SI`."
                    elif tipus == "vector":
                        msg = "⚠️ No he pogut interpretar el vector. Escriu-lo, per exemple, com `1, 2, 3`."
                    elif tipus == "classificacio_vector":
                        msg = "⚠️ Escriu `SI` o `NO`."
                    elif tipus == "interval":
                        msg = "⚠️ Escriu dos valors separats per una coma, per exemple `90, 110`."
                    else:
                        msg = "⚠️ No he pogut interpretar la resposta. Escriu-la amb la sintaxi indicada."
                    st.warning(msg)

        # BOTONS PRINCIPALS
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("👁️ Veure resposta"):
                st.session_state.mostrar_resposta = True
                st.rerun()

        with col2:
            if st.button("📖 Veure pas a pas"):
                st.session_state.mostrar_passos = True
                st.rerun()

        with col3:
            if st.button("➡️ Següent exercici"):
                nou_exercici()
                st.rerun()

        # RESPOSTA
        if st.session_state.mostrar_resposta:

            respostes = exercici["resposta"]

            tipus = exercici.get("tipus_resposta", "escalar")

            if tipus == "matriu":
                latex_respostes = [
                    sp.latex(r if isinstance(r, sp.MatrixBase) else sp.Matrix(r))
                    for r in respostes
                ]
                resposta_visual = " o ".join(f"${r}$" for r in latex_respostes)
            elif tipus == "sistema":
                resposta_visual = " o ".join(
                    "$" + _solution_text(r) + "$" for r in respostes
                )
            elif tipus == "classificacio":
                resposta_visual = " o ".join(f"`{r}`" for r in respostes)
            elif tipus == "vector":
                resposta_visual = " o ".join(
                    "$" + _vector_solution_text(r) + "$" for r in respostes
                )
            elif tipus == "classificacio_vector":
                resposta_visual = " o ".join(f"**{r}**" for r in respostes)
            elif tipus == "interval":
                resposta_visual = " o ".join(f"`{r[0]}, {r[1]}`" for r in respostes)
            elif tipus == "text":
                resposta_visual = " o ".join(f"**{r}**" for r in respostes)
            else:
                if st.session_state.assignatura in ["⚛️ Física I", "⚛️ Física II", "⚗️ Química I", "⚗️ Química II"]:
                    resposta_visual = " o ".join(
                        f"`{format_ciencia_4sf(r)}`" for r in respostes
                    )
                else:
                    if st.session_state.assignatura in ["📐 Matemàtiques I", "📐 Matemàtiques II"]:
                        resposta_visual = " o ".join(f"`{format_mates_4sf(r)}`" for r in respostes)
                    else:
                        latex_respostes = [
                            sp.latex(interpretar_resposta(str(r)))
                            for r in respostes
                        ]
                        resposta_visual = " o ".join(f"${r}$" for r in latex_respostes)

            st.info("Resposta: " + resposta_visual)

        # PASSOS
        if st.session_state.mostrar_passos:

            st.success("📖 Resolució pas a pas")
            st.markdown(exercici["passos"])

        st.divider()

        # NAVEGACIÓ
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("← Canviar dificultat"):
                tornar_dificultat()
                st.rerun()

        with col2:
            if st.button("📚 Canviar tema"):
                tornar_temes()
                st.rerun()

        with col3:
            if st.button("🏠 Inici"):
                tornar_inici()
                st.rerun()
