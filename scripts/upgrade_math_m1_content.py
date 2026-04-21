from __future__ import annotations

import json
from fractions import Fraction
from itertools import cycle
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / 'data' / 'catalog.json'
CHAPTER_EXAMPLES_PATH = ROOT / 'data' / 'chapter_examples.json'
EXAM_BANK_PATH = ROOT / 'data' / 'exam_bank.json'
FEED_PATH = ROOT / 'data' / 'knowledge_feed.jsonl'

YEARS = cycle(range(2018, 2027))
RAW_COUNTER = {'value': 0}

MATH_SUBIECT_MAP = {
    'subiectul-1': [
        'multimi-intervale-si-logica-matematica',
        'functii-si-reprezentari-grafice',
        'functia-de-gradul-i-si-functia-de-gradul-al-ii-lea',
        'siruri-aritmetice-si-geometrice',
        'puteri-radicali-si-logaritmi',
        'numere-complexe',
        'functia-exponentiala-si-functia-logaritmica',
        'ecuatii-si-inecuatii-exponentiale-logaritmice-si-trigonometrice',
        'metode-de-numarare-si-combinatorica',
        'probabilitati-statistica-si-matematici-financiare',
        'vectori-in-plan-si-coliniaritate',
        'geometrie-analitica-in-plan',
        'trigonometrie-elementara',
        'aplicatii-de-trigonometrie-si-produs-scalar',
    ],
    'subiectul-2': [
        'matrice-determinanti-si-sisteme-liniare',
        'grupuri-si-legi-de-compozitie',
        'inele-corpuri-si-polinoame',
    ],
    'subiectul-3': [
        'limite-de-functii',
        'continuitate',
        'derivabilitate',
        'studiul-functiilor-cu-ajutorul-derivatelor',
        'primitive',
        'integrala-definita',
        'aplicatii-ale-integralei',
    ],
}

BAC_SLOT = {
    'multimi-intervale-si-logica-matematica': 'Subiectul I · item 1',
    'siruri-aritmetice-si-geometrice': 'Subiectul I · item 1',
    'numere-complexe': 'Subiectul I · item 1',
    'functii-si-reprezentari-grafice': 'Subiectul I · item 2',
    'functia-de-gradul-i-si-functia-de-gradul-al-ii-lea': 'Subiectul I · item 2',
    'puteri-radicali-si-logaritmi': 'Subiectul I · item 3',
    'functia-exponentiala-si-functia-logaritmica': 'Subiectul I · item 3',
    'ecuatii-si-inecuatii-exponentiale-logaritmice-si-trigonometrice': 'Subiectul I · item 3',
    'metode-de-numarare-si-combinatorica': 'Subiectul I · item 4',
    'probabilitati-statistica-si-matematici-financiare': 'Subiectul I · item 4',
    'vectori-in-plan-si-coliniaritate': 'Subiectul I · item 5',
    'geometrie-analitica-in-plan': 'Subiectul I · item 5',
    'trigonometrie-elementara': 'Subiectul I · item 6',
    'aplicatii-de-trigonometrie-si-produs-scalar': 'Subiectul I · item 6',
    'matrice-determinanti-si-sisteme-liniare': 'Subiectul II · exercițiul 1',
    'grupuri-si-legi-de-compozitie': 'Subiectul II · exercițiul 2',
    'inele-corpuri-si-polinoame': 'Subiectul II · exercițiul 2',
    'limite-de-functii': 'Subiectul III · exercițiul 1',
    'continuitate': 'Subiectul III · exercițiul 1',
    'derivabilitate': 'Subiectul III · exercițiul 1',
    'studiul-functiilor-cu-ajutorul-derivatelor': 'Subiectul III · exercițiul 1',
    'primitive': 'Subiectul III · exercițiul 2',
    'integrala-definita': 'Subiectul III · exercițiul 2',
    'aplicatii-ale-integralei': 'Subiectul III · exercițiul 2',
}

SUBIECT_SUMMARY = {
    'subiectul-1': '6 itemi scurți de tip M_mate-info: numere și calcule rapide, funcții, ecuații de bază, combinatorică/probabilități, geometrie analitică și trigonometrie.',
    'subiectul-2': 'Exercițiul 1 pune accent pe matrice, determinanți, sisteme și tipurile clasice de subpunct c; exercițiul 2 merge pe legi de compoziție sau polinoame.',
    'subiectul-3': 'Analiză matematică: limite, continuitate și asimptote, derivate și studiu de funcție, apoi primitive, integrale și aplicațiile lor.',
}


def fmt_fraction(value: Fraction | int | float | str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, float):
        value = Fraction(value).limit_denominator()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def fmt_interval(a: int | Fraction, b: int | Fraction, left_closed: bool, right_closed: bool) -> str:
    left = '[' if left_closed else '('
    right = ']' if right_closed else ')'
    return f"{left}{fmt_fraction(a)}, {fmt_fraction(b)}{right}"


def fmt_set(items: list[str] | tuple[str, ...] | list[int] | tuple[int, ...]) -> str:
    return '{' + ', '.join(str(item) for item in items) + '}'


def optionize(correct: str, wrongs: list[str], seed: int) -> tuple[list[str], int]:
    correct = str(correct)
    uniq = []
    seen = {correct}
    for wrong in wrongs:
        wrong = str(wrong)
        if wrong not in seen:
            uniq.append(wrong)
            seen.add(wrong)
        if len(uniq) == 3:
            break
    while len(uniq) < 3:
        filler = f"variantă {seed}-{len(uniq)}"
        if filler not in seen:
            uniq.append(filler)
            seen.add(filler)
    pos = seed % 4
    if pos == 0:
        options = [correct] + uniq
        index = 0
    elif pos == 1:
        options = [uniq[0], correct, uniq[1], uniq[2]]
        index = 1
    elif pos == 2:
        options = [uniq[0], uniq[1], correct, uniq[2]]
        index = 2
    else:
        options = [uniq[0], uniq[1], uniq[2], correct]
        index = 3
    return options, index


def make_raw(prompt: str, correct: str, wrongs: list[str], explanation: str, hint: str,
             worked_steps: list[str] | None = None, tags: list[str] | None = None) -> dict:
    RAW_COUNTER['value'] += 1
    return {
        'prompt': prompt,
        'correct': str(correct),
        'wrongs': [str(item) for item in wrongs],
        'explanation': explanation,
        'hint': hint,
        'worked_steps': worked_steps or [],
        'tags': tags or [],
        'seed': RAW_COUNTER['value'],
    }


def finalize_chapter(chapter_id: str, subiect_id: str, raws: list[dict]) -> list[dict]:
    subject_id = 'matematica_m1'
    slot = BAC_SLOT[chapter_id]
    items = []
    for index, raw in enumerate(raws, start=1):
        if index <= 8:
            difficulty = 'beginner'
        elif index <= 16:
            difficulty = 'intermediate'
        else:
            difficulty = 'advanced'
        options, correct_index = optionize(raw['correct'], raw['wrongs'], raw['seed'])
        year = next(YEARS)
        items.append({
            'id': f'{subject_id}:{chapter_id}:{index:02d}',
            'subject_id': subject_id,
            'subiect_id': subiect_id,
            'chapter_id': chapter_id,
            'year': year,
            'source_type': 'adaptat după modele și bareme oficiale 2018-2026',
            'source_label': 'adaptat după modele / bareme M1',
            'difficulty': difficulty,
            'prompt': raw['prompt'],
            'options': options,
            'correct_index': correct_index,
            'explanation': raw['explanation'],
            'hint': raw['hint'],
            'worked_steps': raw['worked_steps'],
            'tags': raw['tags'],
            'bac_slot': slot,
        })
    if len(items) != 20:
        raise ValueError(f'{chapter_id} generated {len(items)} items instead of 20')
    return items


def gen_sets() -> list[dict]:
    raws = []
    intervals = [
        (-3, 4, False, True, 0, 6, True, False),
        (-5, 2, True, False, -1, 7, True, True),
        (1, 8, False, False, 3, 5, True, True),
        (-2, 5, True, True, -4, 1, False, True),
        (0, 9, True, False, 2, 12, False, True),
    ]
    for a, b, lc1, rc1, c, d, lc2, rc2 in intervals:
        left = max(a, c)
        right = min(b, d)
        left_closed = lc1 if a >= c else lc2
        right_closed = rc1 if b <= d else rc2
        correct = fmt_interval(left, right, left_closed, right_closed)
        wrongs = [
            fmt_interval(min(a, c), max(b, d), lc1, rc2),
            fmt_interval(left, right, False, False),
            fmt_interval(left, right, True, True),
        ]
        raws.append(make_raw(
            f'Fie A = {fmt_interval(a, b, lc1, rc1)} și B = {fmt_interval(c, d, lc2, rc2)}. Care este intersecția A ∩ B?',
            correct,
            wrongs,
            f'Intersecția păstrează doar valorile comune celor două intervale, deci obții {correct}.',
            'Desenează cele două intervale pe aceeași axă și păstrează doar zona comună.',
            ['marchezi capetele', 'alegi porțiunea comună', 'verifici dacă fiecare capăt este inclus'],
            ['intervale', 'intersecție']
        ))
    abs_params = [(3, 2), (-1, 4), (5, 3), (0, 2), (2, 5)]
    for center, radius in abs_params:
        correct = fmt_interval(center - radius, center + radius, True, True)
        wrongs = [
            fmt_interval(center - radius, center + radius, False, False),
            fmt_interval(center + radius, center - radius, True, True) if center + radius < center - radius else fmt_interval(center - radius, center + radius, True, False),
            fmt_interval(-(center + radius), center + radius, True, True),
        ]
        raws.append(make_raw(
            f'Mulțimea soluțiilor inecuației |x - ({center})| ≤ {radius} este:',
            correct,
            wrongs,
            f'Pentru |x-a| ≤ r, soluțiile sunt toate valorile din intervalul [{center - radius}, {center + radius}].',
            'Scrie regula generală |x-a| ≤ r ⇒ a-r ≤ x ≤ a+r.',
            ['identifici centrul a', 'scazi și aduni raza r', 'scrii intervalul cu capete incluse'],
            ['modul', 'inecuație']
        ))
    floor_params = [(2, 15), (3, 7), (5, 24), (7, 30), (1, 5)]
    for whole, rem in floor_params:
        value = whole + Fraction(rem, 10)
        correct = str(int(value))
        wrongs = [str(int(value) + 1), str(int(value) - 1 if int(value) > 0 else 0), fmt_fraction(Fraction(rem, 10))]
        raws.append(make_raw(
            f'Partea întreagă a numărului x = {fmt_fraction(value)} este:',
            correct,
            wrongs,
            f'Partea întreagă este cel mai mare număr întreg mai mic sau egal cu {fmt_fraction(value)}, deci {correct}.',
            'Partea întreagă nu rotunjește; caută cel mai mare întreg care nu depășește numărul.',
            ['localizezi numărul între doi întregi consecutivi', 'alegi întregul mai mic'],
            ['parte întreagă']
        ))
    subset_params = [3, 4, 5, 6, 7]
    for n in subset_params:
        correct = str(2 ** n)
        wrongs = [str(2 ** n - 1), str(n ** 2), str(n * 2)]
        raws.append(make_raw(
            f'O mulțime cu {n} elemente are exact câte submulțimi?',
            correct,
            wrongs,
            f'Numărul total de submulțimi ale unei mulțimi cu n elemente este 2^n, deci obții {correct}.',
            'Formula-cheie este 2^n, nu n^2 și nici 2n.',
            ['scrii formula 2^n', 'înlocuiești n', 'calculezi'],
            ['submulțimi']
        ))
    return raws


def gen_functions() -> list[dict]:
    raws = []
    for a, b, x in [(2, 3, 1), (-1, 5, 2), (3, -4, -1), (4, 0, 3), (-2, -1, 4)]:
        y = a * x + b
        correct = f'({x}, {y})'
        wrongs = [f'({y}, {x})', f'({x}, {y + 1})', f'({x + 1}, {y})']
        raws.append(make_raw(
            f'Pentru funcția f(x) = {a}x {b:+d}, care punct aparține graficului ei?',
            correct,
            wrongs,
            f'Un punct aparține graficului dacă are forma (x, f(x)). Pentru x={x}, obții f(x)={y}.',
            'Înlocuiește x în formulă și compară doar perechile de tip (x, f(x)).',
            ['alegi valoarea lui x', 'calculezi f(x)', 'citești punctul (x, f(x))'],
            ['grafic', 'punct pe grafic']
        ))
    for a, b in [(2, -6), (3, 9), (-4, 8), (5, -10), (-2, -4)]:
        x0 = Fraction(-b, a)
        correct = fmt_fraction(x0)
        wrongs = [fmt_fraction(-x0), fmt_fraction(x0 + 1), '0']
        raws.append(make_raw(
            f'Graficul funcției f(x) = {a}x {b:+d} intersectează axa Ox pentru x =',
            correct,
            wrongs,
            f'Pe axa Ox avem f(x)=0. Din {a}x {b:+d}=0 rezultă x={correct}.',
            'Intersecția cu Ox înseamnă y=0.',
            ['egalezi f(x) cu 0', 'izolezi necunoscuta x'],
            ['intersecție cu Ox']
        ))
    for a, b, c, d, x in [(2, 1, 3, -2, 1), (1, -3, 2, 4, 0), (-1, 5, 4, 1, 2), (3, 0, -2, 6, -1), (2, -1, 5, 0, 3)]:
        gx = c * x + d
        val = a * gx + b
        correct = str(val)
        wrongs = [str(a * x + b), str(c * x + d), str(val + 1)]
        raws.append(make_raw(
            f'Dacă f(x) = {a}x {b:+d} și g(x) = {c}x {d:+d}, atunci (f∘g)({x}) este:',
            correct,
            wrongs,
            f'Întâi calculezi g({x})={gx}, apoi aplici f pe rezultatul obținut: f({gx})={val}.',
            'Compunerea se face în ordinea indicată: mai întâi g, apoi f.',
            ['calculezi g(x)', 'înlocuiești rezultatul în f'],
            ['compunere de funcții']
        ))
    for func, truth, wrongs in [
        ('f(x)=x^2+1', 'funcție pară', ['funcție impară', 'strict descrescătoare pe R', 'fără minim']),
        ('f(x)=x^3', 'funcție impară', ['funcție pară', 'mărginită', 'strict pozitivă pe R']),
        ('f(x)=2x+1', 'strict crescătoare pe R', ['strict descrescătoare pe R', 'funcție pară', 'funcție impară']),
        ('f(x)=-3x+4', 'strict descrescătoare pe R', ['strict crescătoare pe R', 'funcție impară', 'funcție constantă']),
        ('f(x)=x^2', 'are minim egal cu 0', ['are maxim egal cu 0', 'este impară', 'este strict descrescătoare pe R']),
    ]:
        raws.append(make_raw(
            f'Care afirmație este corectă pentru {func}?',
            truth,
            wrongs,
            f'Proprietatea corectă se citește direct din forma funcției: pentru {func}, afirmația adevărată este „{truth}”.',
            'Verifică întâi forma funcției: coeficientul lui x, paritatea sau valorile evidente.',
            ['identifici tipul funcției', 'testezi proprietatea relevantă'],
            ['proprietăți funcții']
        ))
    return raws


def gen_linear_quadratic() -> list[dict]:
    raws = []
    linear_data = [(2, -8), (3, 6), (-4, 12), (5, -15), (-2, -6)]
    for a, b in linear_data:
        x0 = Fraction(-b, a)
        correct = fmt_fraction(x0)
        wrongs = [fmt_fraction(-x0), fmt_fraction(x0 + 2), '0']
        raws.append(make_raw(
            f'Rădăcina funcției f(x) = {a}x {b:+d} este:',
            correct,
            wrongs,
            f'Rădăcina se obține din ecuația {a}x {b:+d}=0, de unde x={correct}.',
            'Pentru funcție de gradul I, rădăcina vine din ax+b=0.',
            ['egalezi ax+b cu 0', 'izolezi x'],
            ['funcție liniară']
        ))
    quad_roots = [(-5, 6), (-7, 10), (1, -6), (-1, -6), (-9, 20)]
    for s, p in quad_roots:
        # x^2 + s x + p = 0, roots are chosen to be integer by construction
        import math
        delta = s * s - 4 * p
        r1 = Fraction(-s - int(math.isqrt(delta)), 2)
        r2 = Fraction(-s + int(math.isqrt(delta)), 2)
        correct = fmt_set([fmt_fraction(r1), fmt_fraction(r2)])
        wrongs = [fmt_set([fmt_fraction(r1 + 1), fmt_fraction(r2)]), fmt_set([fmt_fraction(r1), fmt_fraction(-r2)]), fmt_set([fmt_fraction(r1 + r2)])]
        raws.append(make_raw(
            f'Mulțimea soluțiilor ecuației x^2 {s:+d}x {p:+d} = 0 este:',
            correct,
            wrongs,
            f'Factorizezi sau folosești formula. Rădăcinile sunt {fmt_fraction(r1)} și {fmt_fraction(r2)}.',
            'Verifică mai întâi dacă produsul și suma rădăcinilor sunt ușor de recunoscut.',
            ['determină rădăcinile', 'scrie mulțimea soluțiilor'],
            ['ecuație de gradul II']
        ))
    vertex_data = [(1, -4, 3), (1, -6, 8), (2, -8, 5), (-1, 4, -3), (1, 2, -3)]
    for a, b, c in vertex_data:
        xv = Fraction(-b, 2 * a)
        yv = a * xv * xv + b * xv + c
        correct = fmt_fraction(yv)
        wrongs = [fmt_fraction(yv + 1), fmt_fraction(xv), fmt_fraction(-yv)]
        raws.append(make_raw(
            f'Valoarea extremă a funcției f(x) = {a}x^2 {b:+d}x {c:+d} este:',
            correct,
            wrongs,
            f'Extremul se află în vârful parabolei. Pentru xV={fmt_fraction(xv)}, obții f(xV)={correct}.',
            'Calculează mai întâi abscisa vârfului: -b/(2a).',
            ['calculezi xV', 'înlocuiești în f', 'citești valoarea extremă'],
            ['parabolă', 'vârf']
        ))
    discr_data = [(1, -4, 4), (1, 2, 1), (2, -8, 8), (1, -6, 9), (3, 6, 3)]
    for a, b, c in discr_data:
        correct = 'are o singură rădăcină reală dublă'
        wrongs = ['are două rădăcini reale distincte', 'nu are rădăcini reale', 'are infinit de multe rădăcini']
        raws.append(make_raw(
            f'Ecuația {a}x^2 {b:+d}x {c:+d} = 0:',
            correct,
            wrongs,
            'Discriminantul este zero, deci ecuația are o singură rădăcină reală dublă.',
            'Calculează Δ = b^2 - 4ac.',
            ['calculezi discriminantul', 'interpretezi valoarea lui Δ'],
            ['discriminant']
        ))
    return raws


def gen_sequences() -> list[dict]:
    raws = []
    for a1, r, n in [(2, 3, 5), (1, 4, 6), (-3, 2, 7), (5, -1, 8), (4, 5, 4)]:
        an = a1 + (n - 1) * r
        raws.append(make_raw(
            f'Într-o progresie aritmetică cu a1 = {a1} și r = {r}, termenul a{n} este:',
            str(an),
            [str(an + r), str(an - r), str(a1 + n * r)],
            f'Pentru progresie aritmetică, an = a1 + (n-1)r = {an}.',
            'Folosește formula an = a1 + (n-1)r.',
            ['scrii formula', 'înlocuiești valorile'],
            ['progresie aritmetică']
        ))
    for a1, q, n in [(3, 2, 5), (1, 3, 4), (2, -2, 5), (5, 2, 3), (-1, 3, 4)]:
        an = a1 * (q ** (n - 1))
        raws.append(make_raw(
            f'Într-o progresie geometrică cu b1 = {a1} și q = {q}, termenul b{n} este:',
            str(an),
            [str(an * q), str(an // q if q not in (0, 1, -1) else an + 1), str(a1 * (q ** n))],
            f'Pentru progresie geometrică, bn = b1·q^(n-1) = {an}.',
            'Atenție: la geometrică înmulțești cu q, nu aduni.',
            ['scrii bn = b1·q^(n-1)', 'calculezi puterea'],
            ['progresie geometrică']
        ))
    for a1, r, n in [(1, 2, 5), (3, 3, 4), (2, 5, 6), (4, -1, 7), (-2, 4, 5)]:
        s = n * (2 * a1 + (n - 1) * r) // 2
        raws.append(make_raw(
            f'Suma primilor {n} termeni ai progresiei aritmetice cu a1 = {a1} și r = {r} este:',
            str(s),
            [str(s + n), str(a1 + (n - 1) * r), str(s - r)],
            f'Sn = n(a1 + an)/2 = {s}.',
            'Calculează întâi an sau folosește direct formula Sn = n[2a1+(n-1)r]/2.',
            ['aplici formula sumei', 'efectuezi calculele'],
            ['sumă progresie']
        ))
    progression_triples = [
        (2, 5, 8, 'aritmetică'),
        (3, 6, 12, 'geometrică'),
        (4, 7, 10, 'aritmetică'),
        (2, 4, 8, 'geometrică'),
        (1, 4, 7, 'aritmetică'),
    ]
    for x, y, z, kind in progression_triples:
        correct = f'sunt în progresie {kind}'
        wrongs = ['nu formează nicio progresie', 'sunt în progresie aritmetică' if kind == 'geometrică' else 'sunt în progresie geometrică', 'sunt termeni consecutivi doar după reordonare']
        explanation = 'Pentru progresie aritmetică verifici media: 2·termenul din mijloc = suma extremelor. Pentru geometrică verifici pătratul termenului din mijloc.'
        raws.append(make_raw(
            f'Numerele {x}, {y}, {z}:',
            correct,
            wrongs,
            explanation,
            'Verifică relația 2y=x+z sau y^2=xz.',
            ['testezi condiția de progresie aritmetică sau geometrică'],
            ['condiție progresie']
        ))
    return raws


def gen_powers_radicals_logs() -> list[dict]:
    raws = []
    power_cases = [
        ('2^3 · 2^5', '2^8', ['2^15', '2^2', '4^8']),
        ('3^7 : 3^4', '3^3', ['3^11', '3^4', '9^3']),
        ('(2^3)^4', '2^12', ['2^7', '8^4', '2^64']),
        ('5^-2', '1/25', ['-1/25', '25', '1/10']),
        ('4^(3/2)', '8', ['6', '16', '2']),
    ]
    for expr, correct, wrongs in power_cases:
        raws.append(make_raw(
            f'Simplifică expresia {expr}.',
            correct,
            wrongs,
            f'Aplici regulile puterilor și obții {correct}.',
            'La aceeași bază, la înmulțire aduni exponenții, la împărțire îi scazi.',
            ['aplici regula potrivită puterilor'],
            ['puteri']
        ))
    radical_cases = [
        ('√50', '5√2', ['25√2', '10√5', '√25']),
        ('√72', '6√2', ['4√2', '3√8', '12√2']),
        ('³√(8x^3)', '2x', ['8x', '2x^3', 'x'],),
        ('√(1/9)', '1/3', ['3', '1/9', '-1/3']),
        ('√48 / √3', '4', ['16', '4√3', '2']),
    ]
    for expr, correct, wrongs in radical_cases:
        raws.append(make_raw(
            f'Calculul corect pentru {expr} este:',
            correct,
            wrongs,
            f'Scoți factorii pătrați sau folosești proprietățile radicalilor și obții {correct}.',
            'Caută întâi factorul perfect pătrat sau simplificarea directă.',
            ['descompui numărul sub radical', 'scoți factorii potriviți'],
            ['radicali']
        ))
    log_cases = [
        ('log_2 8', '3', ['2', '4', '8']),
        ('log_3 1/9', '-2', ['-3', '2', '1/9']),
        ('log_5 125', '3', ['25', '2', '5']),
        ('log_2 32', '5', ['16', '4', '6']),
        ('log_10 0.01', '-2', ['-1', '2', '0.1']),
    ]
    for expr, correct, wrongs in log_cases:
        raws.append(make_raw(
            f'Valoarea expresiei {expr} este:',
            correct,
            wrongs,
            f'Prin definiție, log_a b = c dacă a^c=b. Aici obții {correct}.',
            'Transformă logaritmul în ecuație exponențială.',
            ['scrii forma exponențială', 'identifici exponentul'],
            ['logaritmi']
        ))
    exist_cases = [
        ('log_2 (x-1)', 'x > 1', ['x ≥ 1', 'x < 1', 'x ≠ 1']),
        ('log_5 (3x+6)', 'x > -2', ['x ≥ -2', 'x < -2', 'x ≠ -2']),
        ('log_3 (2-x)', 'x < 2', ['x ≤ 2', 'x > 2', 'x ≠ 2']),
        ('log_7 (x+4)', 'x > -4', ['x ≥ -4', 'x < -4', 'x ≠ -4']),
        ('log_4 (5-2x)', 'x < 5/2', ['x ≤ 5/2', 'x > 5/2', 'x ≠ 5/2']),
    ]
    for expr, correct, wrongs in exist_cases:
        raws.append(make_raw(
            f'Condiția de existență pentru expresia {expr} este:',
            correct,
            wrongs,
            f'Argumentul logaritmului trebuie să fie strict pozitiv, deci condiția este {correct}.',
            'La logaritm, argumentul este strict pozitiv.',
            ['impui argumentul > 0', 'rezolvi inecuația'],
            ['condiție de existență']
        ))
    return raws


def gen_complex_numbers() -> list[dict]:
    raws = []
    i_cases = [(3, '-i'), (4, '1'), (5, 'i'), (6, '-1'), (7, '-i')]
    for power, correct in i_cases:
        wrongs = ['1', '-1', 'i']
        raws.append(make_raw(
            f'Valoarea lui i^{power} este:',
            correct,
            wrongs,
            'Puterile lui i se repetă din 4 în 4: i, -1, -i, 1.',
            'Redu exponentul modulo 4.',
            ['împarți exponentul la 4', 'citești restul'],
            ['puteri ale lui i']
        ))
    for z1, z2 in [((2, 3), (1, -1)), ((-1, 4), (3, 2)), ((5, -2), (-3, 1)), ((1, 1), (2, 5)), ((4, -3), (-2, -1))]:
        (a, b), (c, d) = z1, z2
        correct = f'{a + c} {b + d:+d}i'
        wrongs = [f'{a - c} {b - d:+d}i', f'{a + d} {b + c:+d}i', f'{a + c} {-(b + d):+d}i']
        raws.append(make_raw(
            f'Dacă z1 = {a} {b:+d}i și z2 = {c} {d:+d}i, atunci z1 + z2 este:',
            correct,
            wrongs,
            f'Aduni separat părțile reale și imaginare: ({a}+{c}) + ({b}+{d})i = {correct}.',
            'La adunare, nu amesteci partea reală cu partea imaginară.',
            ['adaugi părțile reale', 'adaugi coeficienții lui i'],
            ['numere complexe']
        ))
    for a, b in [(3, 4), (5, 12), (1, -1), (-4, 3), (2, -5)]:
        modulus = int((a * a + b * b) ** 0.5)
        correct = str(modulus) if modulus * modulus == a * a + b * b else f'√{a * a + b * b}'
        wrongs = [str(abs(a) + abs(b)), str(a * a + b * b), str(abs(a - b))]
        raws.append(make_raw(
            f'Modulul numărului complex z = {a} {b:+d}i este:',
            correct,
            wrongs,
            f'|z| = √(a^2+b^2) = {correct}.',
            'Aplică formula |a+bi| = √(a^2+b^2).',
            ['calculezi a^2+b^2', 'extragi radicalul'],
            ['modul']
        ))
    for a, b in [(2, 5), (-3, 4), (1, -7), (6, -1), (-2, -3)]:
        correct = f'{a} {-b:+d}i'
        wrongs = [f'{-a} {b:+d}i', f'{a} {b:+d}i', f'{-a} {-b:+d}i']
        raws.append(make_raw(
            f'Conjugatul numărului z = {a} {b:+d}i este:',
            correct,
            wrongs,
            f'Conjugatul schimbă semnul părții imaginare, deci obții {correct}.',
            'Păstrezi partea reală și schimbi doar semnul lui bi.',
            ['identifici partea reală', 'inversezi semnul părții imaginare'],
            ['conjugat']
        ))
    return raws


def gen_exp_log_functions() -> list[dict]:
    raws = []
    eval_cases = [('2^x', 3, '8'), ('3^x', 2, '9'), ('log_2 x', 16, '4'), ('log_3 x', 27, '3'), ('5^x', 0, '1')]
    for expr, value, correct in eval_cases:
        wrongs = ['2', '5', '0']
        question = f'Pentru funcția f(x) = {expr}, valoarea lui f({value}) este:' if '^x' in expr else f'Pentru funcția f(x) = {expr}, valoarea lui f({value}) este:'
        raws.append(make_raw(
            question,
            correct,
            wrongs,
            f'Înlocuiești direct în funcție și obții {correct}.',
            'La logaritm, întreabă-te „la ce putere ridic baza pentru a obține argumentul?”',
            ['înlocuiești argumentul în funcție'],
            ['funcții exponențiale', 'funcții logaritmice']
        ))
    prop_cases = [
        ('f(x)=2^x', 'este strict crescătoare pe R', ['este strict descrescătoare pe R', 'are domeniul (0,∞)', 'are valori doar întregi']),
        ('f(x)=(1/3)^x', 'este strict descrescătoare pe R', ['este strict crescătoare pe R', 'are domeniul (0,∞)', 'este periodică']),
        ('f(x)=log_2 x', 'are domeniul (0,∞)', ['are domeniul R', 'are imaginea (0,∞)', 'este pară']),
        ('f(x)=log_{1/2} x', 'este strict descrescătoare pe (0,∞)', ['este strict crescătoare pe (0,∞)', 'are domeniul R', 'nu are inversă']),
        ('f(x)=10^x', 'are imaginea (0,∞)', ['are imaginea R', 'are minim egal cu 0 atins', 'este descrescătoare']),
    ]
    for func, correct, wrongs in prop_cases:
        raws.append(make_raw(
            f'Care afirmație este adevărată pentru {func}?',
            correct,
            wrongs,
            f'Proprietatea corectă pentru {func} este „{correct}”.',
            'Ține minte: baza > 1 dă funcție exponențială crescătoare, baza din (0,1) o face descrescătoare.',
            ['recunoști tipul funcției', 'aplici proprietatea de monotonicitate / domeniu'],
            ['proprietăți funcții']
        ))
    inverse_cases = [
        ('f(x)=2^x', 'f^{-1}(x)=log_2 x', ['f^{-1}(x)=2x', 'f^{-1}(x)=1/2^x', 'f^{-1}(x)=log_x 2']),
        ('f(x)=3^x', 'f^{-1}(x)=log_3 x', ['f^{-1}(x)=3x', 'f^{-1}(x)=1/3^x', 'f^{-1}(x)=log_x 3']),
        ('f(x)=log_2 x', 'funcția inversă este 2^x', ['funcția inversă este x^2', 'funcția inversă este log_x 2', 'nu are inversă']),
        ('f(x)=log_5 x', 'funcția inversă este 5^x', ['funcția inversă este x^5', 'funcția inversă este 1/5^x', 'nu are inversă']),
        ('f(x)=e^x', 'funcția inversă este ln x', ['funcția inversă este x·e', 'funcția inversă este e^{-x}', 'funcția inversă este log_e e']),
    ]
    for func, correct, wrongs in inverse_cases:
        raws.append(make_raw(
            f'Pentru {func}, care afirmație despre inversă este corectă?',
            correct,
            wrongs,
            f'Funcțiile exponențiale și logaritmice de aceeași bază sunt inverse una alteia.',
            'Perechea de bază este a^x ↔ log_a x.',
            ['identifici baza', 'scrii funcția inversă'],
            ['funcție inversă']
        ))
    graph_cases = [
        ('graficul lui y=2^x', '(0,1)', ['(1,0)', '(0,0)', '(1,2^0)']),
        ('graficul lui y=log_2 x', '(1,0)', ['(0,1)', '(2,0)', '(0,2)']),
        ('graficul lui y=3^x', '(0,1)', ['(1,3)', '(0,3)', '(1,1)']),
        ('graficul lui y=ln x', '(1,0)', ['(0,1)', '(e,0)', '(0,e)']),
        ('graficul lui y=(1/2)^x', '(0,1)', ['(1,0)', '(0,1/2)', '(2,1)']),
    ]
    for graph, correct, wrongs in graph_cases:
        raws.append(make_raw(
            f'Punctul sigur comun pentru {graph} este:',
            correct,
            wrongs,
            f'Funcțiile exponențiale trec prin (0,1), iar funcțiile logaritmice prin (1,0).',
            'Recunoaște tipul funcției: exponențială sau logaritmică.',
            ['identifici tipul graficului', 'alegi punctul standard'],
            ['reprezentare grafică']
        ))
    return raws


def gen_exp_log_trig_equations() -> list[dict]:
    raws = []
    exp_eq_cases = [
        ('2^(x+1)=16', '3', ['4', '2', '5']),
        ('3^(2x-1)=27', '2', ['1', '3', '4']),
        ('5^(x-2)=1/25', '0', ['-2', '2', '4']),
        ('4^(x+1)=64', '2', ['3', '1', '0']),
        ('2^(2x)=32', '5/2', ['5', '3/2', '2']),
    ]
    for expr, correct, wrongs in exp_eq_cases:
        raws.append(make_raw(
            f'Rezolvați în R ecuația {expr}.',
            f'x = {correct}',
            [f'x = {w}' for w in wrongs],
            f'Aduci cele două părți la aceeași bază și egalezi exponenții. Rezultă x = {correct}.',
            'Primul reflex: rescrie ambele membre cu aceeași bază.',
            ['rescrii la aceeași bază', 'egalezi exponenții'],
            ['ecuație exponențială']
        ))
    log_eq_cases = [
        ('log_2(x-1)=3', '4', ['3', '5', '8']),
        ('log_3(2x+1)=2', '4', ['3', '5', '8']),
        ('log_5(x+2)=1', '3', ['5', '1', '2']),
        ('log_10(x)=2', '100', ['10', '20', '2']),
        ('log_2(x+3)=4', '13', ['16', '11', '8']),
    ]
    for expr, correct, wrongs in log_eq_cases:
        raws.append(make_raw(
            f'Rezolvați în R ecuația {expr}.',
            f'x = {correct}',
            [f'x = {w}' for w in wrongs],
            f'Transformi logaritmul în formă exponențială și verifici condiția de existență. Rezultă x = {correct}.',
            'Nu uita condiția de existență a argumentului logaritmului.',
            ['scrii forma exponențială', 'rezolvi ecuația', 'verifici condiția de existență'],
            ['ecuație logaritmică']
        ))
    radical_cases = [
        ('√(x+1)=3', '8', ['7', '9', '10']),
        ('√(2x-1)=5', '13', ['12', '11', '26']),
        ('√(x+4)=x', '4', ['2', '5', '6']),
        ('√(x+9)=x+1', '3', ['2', '4', '8']),
        ('³√(x+1)=2', '7', ['8', '6', '9']),
    ]
    for expr, correct, wrongs in radical_cases:
        raws.append(make_raw(
            f'Rezolvați în R ecuația {expr}.',
            f'x = {correct}',
            [f'x = {w}' for w in wrongs],
            f'Ridici la puterea potrivită, rezolvi ecuația și verifici soluția. Rezultă x = {correct}.',
            'La radical de ordin par verifici soluția obținută în ecuația inițială.',
            ['impui condiția de existență', 'ridici la putere', 'verifici soluția'],
            ['ecuație cu radical']
        ))
    trig_cases = [
        ('sin x = 0, x ∈ [0, 2π)', fmt_set(['0', 'π']), [fmt_set(['π/2', '3π/2']), fmt_set(['0', '2π']), fmt_set(['π'])]),
        ('cos x = 1/2, x ∈ [0, 2π)', fmt_set(['π/3', '5π/3']), [fmt_set(['2π/3', '4π/3']), fmt_set(['π/6', '11π/6']), fmt_set(['π/3'])]),
        ('sin x = 1, x ∈ [0, 2π)', fmt_set(['π/2']), [fmt_set(['3π/2']), fmt_set(['0', 'π']), fmt_set(['π/2', '3π/2'])]),
        ('cos x = -1, x ∈ [0, 2π)', fmt_set(['π']), [fmt_set(['0']), fmt_set(['2π/3', '4π/3']), fmt_set(['π/2'])]),
        ('tan x = 1, x ∈ [0, 2π)', fmt_set(['π/4', '5π/4']), [fmt_set(['3π/4', '7π/4']), fmt_set(['π/2']), fmt_set(['π/4'])]),
    ]
    for expr, correct, wrongs in trig_cases:
        raws.append(make_raw(
            f'Rezolvați ecuația {expr}.',
            correct,
            wrongs,
            f'Folosești valorile trigonometrice standard și obții mulțimea soluțiilor {correct}.',
            'Gândește pe cercul trigonometric și ține cont de intervalul dat.',
            ['identifici valoarea standard', 'scrii toate soluțiile din interval'],
            ['ecuație trigonometrică']
        ))
    return raws


def gen_combinatorics() -> list[dict]:
    raws = []
    product_cases = [
        (4, 3, 12), (5, 2, 10), (6, 4, 24), (3, 7, 21), (8, 2, 16)
    ]
    for m, n, total in product_cases:
        raws.append(make_raw(
            f'Dacă o alegere se face în {m} moduri și apoi alta în {n} moduri, numărul total de posibilități este:',
            str(total),
            [str(m + n), str(m * n - 1), str(max(m, n))],
            f'Aplici regula produsului: {m}·{n} = {total}.',
            'Pentru etape succesive, totalul se obține prin înmulțire.',
            ['identifici cele două etape', 'înmulțești numărul de posibilități'],
            ['regula produsului']
        ))
    comb_cases = [(5, 2, 10), (6, 3, 20), (7, 2, 21), (8, 1, 8), (9, 2, 36)]
    for n, k, val in comb_cases:
        raws.append(make_raw(
            f'Numărul combinațiilor de {k} elemente din {n} elemente este:',
            str(val),
            [str(val - 1), str(n * k), str(n + k)],
            f'C({n},{k}) = {val}.',
            'Pentru combinații ordinea nu contează.',
            ['recunoști tipul de alegere', 'aplici formula combinațiilor'],
            ['combinații']
        ))
    arrange_cases = [(5, 2, 20), (6, 3, 120), (4, 2, 12), (7, 1, 7), (8, 2, 56)]
    for n, k, val in arrange_cases:
        raws.append(make_raw(
            f'Numărul aranjamentelor de {k} elemente din {n} elemente este:',
            str(val),
            [str(val // 2 if val > 1 else 1), str(n ** k), str(val + k)],
            f'A({n},{k}) = {val}.',
            'La aranjamente ordinea contează.',
            ['aplici formula aranjamentelor'],
            ['aranjamente']
        ))
    subset_cases = [(5, 32), (6, 64), (7, 128), (4, 16), (3, 8)]
    for n, total in subset_cases:
        raws.append(make_raw(
            f'O mulțime cu {n} elemente are exact câte submulțimi?',
            str(total),
            [str(total - 1), str(n * 2), str(n ** 2)],
            f'Numărul total de submulțimi este 2^{n} = {total}.',
            'Nu confunda submulțimile cu combinațiile de câte k elemente.',
            ['aplici formula 2^n'],
            ['submulțimi']
        ))
    return raws


def gen_probability_stats_finance() -> list[dict]:
    raws = []
    prob_cases = [
        ('mulțimea numerelor naturale de două cifre', 'numărul să fie multiplu de 9 și impar', '1/18', ['1/9', '1/15', '5/18']),
        ('mulțimea numerelor naturale de două cifre', 'numărul să aibă ambele cifre pare', '5/18', ['1/2', '2/9', '1/18']),
        ('mulțimea {1,2,3,4,5}', 'numărul extras să fie par', '2/5', ['1/5', '3/5', '1/2']),
        ('mulțimea {1,2,3,4,5,6}', 'numărul extras să fie divizibil cu 3', '1/3', ['1/2', '2/3', '1/6']),
        ('mulțimea {0,1,2,3,4,5,6,7,8,9}', 'cifra extrasă să fie mai mare decât 6', '3/10', ['2/10', '4/10', '7/10']),
    ]
    for universe, event, correct, wrongs in prob_cases:
        raws.append(make_raw(
            f'Calculați probabilitatea ca, alegând un element din {universe}, {event}.',
            correct,
            wrongs,
            f'Probabilitatea se calculează ca raport între cazurile favorabile și cele posibile. Rezultă {correct}.',
            'Numără separat cazurile posibile și cele favorabile.',
            ['determină toate cazurile posibile', 'numără cazurile favorabile', 'formează raportul'],
            ['probabilități']
        ))
    mean_cases = [
        ([6, 8, 10], '8'),
        ([4, 6, 8, 10], '7'),
        ([3, 3, 9], '5'),
        ([2, 5, 8, 11], '13/2'),
        ([7, 9, 14], '10'),
    ]
    for values, correct in mean_cases:
        wrongs = [str(sum(values)), str(max(values)), str(min(values))]
        raws.append(make_raw(
            f'Media aritmetică a numerelor {values} este:',
            correct,
            wrongs,
            f'Suma numerelor împărțită la numărul lor dă media aritmetică, deci obții {correct}.',
            'Aduni toate valorile și împarți la câte sunt.',
            ['calculezi suma', 'împarți la numărul valorilor'],
            ['medie aritmetică']
        ))
    weighted_cases = [
        ([10, 8, 9], [2, 1, 3], '28/3'),
        ([7, 9], [1, 2], '25/3'),
        ([5, 6, 10], [1, 1, 2], '31/4'),
        ([4, 8, 9], [3, 2, 1], '37/6'),
        ([6, 10], [4, 1], '34/5'),
    ]
    for vals, weights, correct in weighted_cases:
        raws.append(make_raw(
            f'Media ponderată a valorilor {vals} cu ponderile {weights} este:',
            correct,
            [str(sum(vals)), str(sum(weights)), '1'],
            f'Media ponderată este suma produselor împărțită la suma ponderilor, deci obții {correct}.',
            'Înmulțește fiecare valoare cu ponderea ei și apoi împarte la suma ponderilor.',
            ['calculezi suma ponderată', 'împarți la totalul ponderilor'],
            ['medie ponderată']
        ))
    finance_cases = [
        (1000, 10, 1, '1100'), (1200, 5, 2, '1320'), (800, 25, 1, '1000'), (1500, 8, 1, '1620'), (2000, 12, 1, '2240')
    ]
    for capital, rate, years, correct in finance_cases:
        raws.append(make_raw(
            f'La dobândă simplă, capitalul final obținut din {capital} lei, la rata de {rate}% pe an, după {years} an(i), este:',
            correct,
            [str(capital), str(int(capital * (1 + rate / 100))), str(int(capital * rate / 100))],
            f'Cu dobândă simplă, capitalul final este C(1+rt), deci obții {correct} lei.',
            'Ai grijă dacă problema spune „dobândă simplă”, nu compusă.',
            ['aplici formula capitalului final'],
            ['matematici financiare']
        ))
    return raws


def gen_vectors() -> list[dict]:
    raws = []
    point_pairs = [((1, 2), (4, 6)), ((-1, 3), (2, 7)), ((0, 0), (5, -2)), ((2, -1), (6, 4)), ((-3, -2), (1, 1))]
    for A, B in point_pairs:
        correct = f'({B[0]-A[0]}, {B[1]-A[1]})'
        wrongs = [f'({A[0]-B[0]}, {A[1]-B[1]})', f'({A[0]+B[0]}, {A[1]+B[1]})', f'({B[1]-A[1]}, {B[0]-A[0]})']
        raws.append(make_raw(
            f'Dacă A{A} și B{B}, atunci vectorul AB are coordonatele:',
            correct,
            wrongs,
            f'Vectorul AB = (xB-xA, yB-yA) = {correct}.',
            'Scazi coordonatele punctului de plecare din cele ale punctului de sosire.',
            ['aplici formula coordonatelor vectorului'],
            ['vectori']
        ))
    col_data = [((2, 4), (1, 2)), ((3, 6), (2, 5)), ((-2, 1), (4, -2)), ((5, 10), (-1, -2)), ((4, 0), (1, 1))]
    for u, v in col_data:
        correct = 'sunt coliniari' if u[0] * v[1] == u[1] * v[0] else 'nu sunt coliniari'
        wrongs = ['nu sunt coliniari', 'sunt egali', 'sunt perpendiculari'] if correct == 'sunt coliniari' else ['sunt coliniari', 'sunt opuși', 'au același modul']
        raws.append(make_raw(
            f'Vectorii u{u} și v{v}:',
            correct,
            wrongs,
            'Doi vectori sunt coliniari dacă unul este multiplu scalar al celuilalt sau dacă produsul în cruce este zero.',
            'Compară rapoartele coordonatelor sau calculează determinantul 2x2.',
            ['verifici proporționalitatea coordonatelor'],
            ['coliniaritate']
        ))
    oa_bc = [((1, 2), (3, 4), '(4, 6)'), ((2, -1), (5, 3), '(7, 2)'), ((0, 3), (1, 1), '(1, 4)'), ((-2, 4), (3, 0), '(1, 4)'), ((4, 1), (0, -2), '(4, -1)')]
    for A, B, correct in oa_bc:
        wrongs = ['(0, 0)', f'({A[0]}, {A[1]})', f'({B[0]}, {B[1]})']
        raws.append(make_raw(
            f'În reperul xOy, punctele A{A} și B{B} sunt date. Dacă OA = BC ca vectori, coordonatele lui C sunt:',
            correct,
            wrongs,
            f'Dacă OA = BC, atunci C = B + OA. Rezultă C = {correct}.',
            'Aduni coordonatele vectorului OA la coordonatele punctului B.',
            ['calculezi OA', 'adaugi vectorul la B'],
            ['translație vectorială']
        ))
    scalar_cases = [((2, 4), 2, '(4, 8)'), ((-1, 3), -2, '(2, -6)'), ((5, -2), 3, '(15, -6)'), ((0, 4), -1, '(0, -4)'), ((3, 3), 1, '(3, 3)')]
    for vec, k, correct in scalar_cases:
        wrongs = [f'({vec[0]+k}, {vec[1]+k})', f'({vec[0]*k}, {vec[1]+k})', f'({vec[1]*k}, {vec[0]*k})']
        raws.append(make_raw(
            f'Produsul scalarului {k} cu vectorul u{vec} este:',
            correct,
            wrongs,
            f'Înmulțești fiecare coordonată cu {k}, obținând {correct}.',
            'La înmulțirea cu scalar nu aduni nimic, doar multiplici fiecare coordonată.',
            ['înmulțești fiecare coordonată cu scalarul'],
            ['scalar', 'vector']
        ))
    return raws


def gen_analytic_geometry() -> list[dict]:
    raws = []
    slope_cases = [((1, 2), (3, 6), '2'), ((-1, 1), (1, 5), '2'), ((0, 0), (2, -4), '-2'), ((2, 5), (5, 5), '0'), ((-2, -1), (2, 3), '1')]
    for A, B, correct in slope_cases:
        wrongs = ['-1', '1', '3'] if correct not in ('-1', '1', '3') else ['0', '2', '-2']
        raws.append(make_raw(
            f'Panta dreptei care trece prin punctele A{A} și B{B} este:',
            correct,
            wrongs,
            f'Panta este (yB-yA)/(xB-xA), deci obții {correct}.',
            'Scazi coordonatele în ordinea corectă: sus y, jos x.',
            ['aplici formula pantei'],
            ['pantă']
        ))
    line_cases = [((1, 2), (3, 6), 'y = 2x'), ((0, 1), (2, 5), 'y = 2x + 1'), ((-1, 0), (1, 4), 'y = 2x + 2'), ((2, 3), (4, 3), 'y = 3'), ((1, -1), (3, -5), 'y = -2x + 1')]
    for A, B, correct in line_cases:
        wrongs = ['y = x', 'x = 0', 'y = 0'] if correct not in ('y = x', 'x = 0', 'y = 0') else ['y = 2x', 'y = x + 1', 'x = 1']
        raws.append(make_raw(
            f'Ecuația dreptei determinate de punctele A{A} și B{B} este:',
            correct,
            wrongs,
            f'Calculezi panta și apoi scrii ecuația dreptei. Obții {correct}.',
            'După pantă, folosește forma punct-pantă sau substituția în y=mx+n.',
            ['calculezi panta', 'determină termenul liber'],
            ['ecuația dreptei']
        ))
    parallel_cases = [
        ('d1: y = 2x + 1 și d2: y = 2x - 3', 'sunt paralele', ['sunt perpendiculare', 'coincid', 'nu au nicio relație clară']),
        ('d1: y = -x + 4 și d2: y = x + 2', 'sunt perpendiculare', ['sunt paralele', 'coincid', 'au aceeași ordonată la origine']),
        ('d1: y = 3x și d2: y = 3x + 5', 'sunt paralele', ['sunt perpendiculare', 'se intersectează sub un unghi de 45°', 'coincid']),
        ('d1: y = 1/2 x și d2: y = -2x + 1', 'sunt perpendiculare', ['sunt paralele', 'coincid', 'nu pot fi comparate']),
        ('d1: y = -3x + 1 și d2: y = -3x - 2', 'sunt paralele', ['sunt perpendiculare', 'coincid', 'se intersectează în origine']),
    ]
    for statement, correct, wrongs in parallel_cases:
        raws.append(make_raw(
            f'Pentru dreptele {statement}, afirmația corectă este:',
            correct,
            wrongs,
            'Compari pantele: pante egale înseamnă paralele, produs -1 înseamnă perpendiculare.',
            'Uit-te mai întâi la coeficienții lui x.',
            ['compari pantele'],
            ['paralelism', 'perpendicularitate']
        ))
    midpoint_cases = [((1, 2), (5, 6), '(3, 4)'), ((-1, 0), (3, 4), '(1, 2)'), ((2, -2), (4, 2), '(3, 0)'), ((0, 0), (2, 8), '(1, 4)'), ((-3, 1), (1, 5), '(-1, 3)')]
    for A, B, correct in midpoint_cases:
        wrongs = [f'({A[0]+B[0]}, {A[1]+B[1]})', f'({(A[0]+B[0])//2}, {(A[1]+B[1])})', f'({A[0]}, {B[1]})']
        raws.append(make_raw(
            f'Mijlocul segmentului AB, unde A{A} și B{B}, este:',
            correct,
            wrongs,
            f'Mijlocul are coordonatele medii ale capetelor, deci {correct}.',
            'Aduni coordonatele și împarți fiecare rezultat la 2.',
            ['calculezi media absciselor și a ordonatelor'],
            ['mijloc de segment']
        ))
    return raws


def gen_trig_elementary() -> list[dict]:
    raws = []
    special_values = [
        ('sin(π/6)', '1/2', ['0', '√2/2', '√3/2']),
        ('cos(π/3)', '1/2', ['0', '√2/2', '√3/2']),
        ('sin(π/4)', '√2/2', ['1/2', '√3/2', '1']),
        ('cos(π/6)', '√3/2', ['1/2', '√2/2', '0']),
        ('tan(π/4)', '1', ['0', '√3', '1/2']),
    ]
    for expr, correct, wrongs in special_values:
        raws.append(make_raw(
            f'Valoarea lui {expr} este:',
            correct,
            wrongs,
            f'Din tabelul valorilor trigonometrice speciale, obții {correct}.',
            'Apelează la triunghiurile speciale 30°-60°-90° și 45°-45°-90°.',
            ['citești valoarea din tabelul special'],
            ['trigonometrie']
        ))
    identity_cases = [
        ('sin^2 x + cos^2 x', '1', ['0', 'sin x + cos x', '2']),
        ('1 + tan^2 x', '1/cos^2 x', ['1/sin^2 x', 'cos^2 x', 'tan x']),
        ('1 + cot^2 x', '1/sin^2 x', ['1/cos^2 x', 'cot x', 'sin^2 x']),
        ('sin(2x)', '2 sin x cos x', ['sin^2 x + cos^2 x', '2 sin^2 x', '2 cos^2 x']),
        ('cos(2x)', 'cos^2 x - sin^2 x', ['1', 'sin^2 x - cos^2 x', '2 sin x cos x']),
    ]
    for expr, correct, wrongs in identity_cases:
        raws.append(make_raw(
            f'Formula corectă pentru {expr} este:',
            correct,
            wrongs,
            f'Identitatea trigonomterică standard dă exact relația {correct}.',
            'Separă formulele fundamentale de cele pentru unghi dublu.',
            ['recunoști identitatea cerută'],
            ['identități trigonometrice']
        ))
    double_angle = [
        ('sin x = 1/2 și x este ascuțit, valoarea lui sin 2x este', '√3/2', ['1/2', '1', '√2/2']),
        ('cos x = √3/2 și x este ascuțit, valoarea lui cos 2x este', '1/2', ['√3/2', '0', '-1/2']),
        ('sin x = √2/2 și x este ascuțit, valoarea lui sin 2x este', '1', ['√2/2', '1/2', '0']),
        ('cos x = 1/2 și x este ascuțit, valoarea lui sin 2x este', '√3/2', ['1/2', '1', '√2/2']),
        ('sin x = √3/2 și x este ascuțit, valoarea lui cos 2x este', '-1/2', ['1/2', '0', '√3/2']),
    ]
    for prompt, correct, wrongs in double_angle:
        raws.append(make_raw(
            prompt + ':',
            correct,
            wrongs,
            f'Folosești formulele pentru unghi dublu și relația fundamentală. Rezultă {correct}.',
            'Dacă ai doar sin x sau doar cos x, găsește și cealaltă valoare din sin^2x+cos^2x=1.',
            ['calculezi valoarea lipsă dacă este necesar', 'aplici formula de unghi dublu'],
            ['unghi dublu']
        ))
    sign_cases = [
        ('sin x > 0 pentru x în cadranul', 'I sau II', ['II sau III', 'III sau IV', 'doar I']),
        ('cos x > 0 pentru x în cadranul', 'I sau IV', ['I sau II', 'II sau III', 'doar IV']),
        ('tan x > 0 pentru x în cadranele', 'I și III', ['II și IV', 'I și II', 'III și IV']),
        ('sin x < 0 pentru x în cadranele', 'III și IV', ['I și II', 'II și III', 'I și IV']),
        ('cos x < 0 pentru x în cadranele', 'II și III', ['I și IV', 'III și IV', 'I și II']),
    ]
    for prompt, correct, wrongs in sign_cases:
        raws.append(make_raw(
            prompt + ':',
            correct,
            wrongs,
            f'Pe cercul trigonometric, semnul funcției se citește pe cadrane. Varianta corectă este {correct}.',
            'Gândește-te la semnul coordonatelor pe cerc: cos este abscisa, sin este ordonata.',
            ['citești semnele pe cadrane'],
            ['cercul trigonometric']
        ))
    return raws


def gen_trig_applications() -> list[dict]:
    raws = []
    area_cases = [
        (6, 4, '1/2', '6'),
        (8, 5, '√3/2', '10√3'),
        (10, 3, '1', '15'),
        (4, 7, '1/2', '7'),
        (12, 6, '√3/2', '18√3'),
    ]
    for a, b, sin_c, correct in area_cases:
        wrongs = [str(a * b), str((a + b) // 2), 'ab/2']
        raws.append(make_raw(
            f'Într-un triunghi, dacă două laturi au lungimile {a} și {b}, iar sinusul unghiului cuprins este {sin_c}, aria este:',
            correct,
            wrongs,
            f'Formula ariei este A = ab·sin(C)/2. Aplicând-o, obții {correct}.',
            'La arie contează sinusul unghiului cuprins dintre cele două laturi.',
            ['aplici formula A = ab·sin(C)/2'],
            ['aria triunghiului']
        ))
    cos_cases = [
        (3, 4, 5, 'π/2'),
        (5, 5, 5, 'π/3'),
        (6, 8, 10, 'π/2'),
        (2, 2, 2, 'π/3'),
        (5, 12, 13, 'π/2'),
    ]
    for a, b, c, correct in cos_cases:
        wrongs = ['π/6', '2π/3', '0']
        raws.append(make_raw(
            f'Într-un triunghi cu laturile {a}, {b}, {c}, unghiul opus laturii {c} poate fi:',
            correct,
            wrongs,
            f'Aplici teorema cosinusului și recunoști unghiul. Rezultă {correct}.',
            'Când a^2+b^2=c^2, unghiul opus lui c este drept.',
            ['aplici teorema cosinusului', 'recunoști valoarea lui cos'],
            ['teorema cosinusului']
        ))
    dot_cases = [
        ((1, 2), (3, 4), '11'), ((2, 0), (0, 5), '0'), ((-1, 3), (2, 1), '1'), ((4, -2), (1, 3), '-2'), ((2, 2), (3, -3), '0')
    ]
    for u, v, correct in dot_cases:
        wrongs = [str(u[0] + v[0] + u[1] + v[1]), str(u[0] * v[0]), str(u[1] * v[1])]
        raws.append(make_raw(
            f'Produsul scalar al vectorilor u{u} și v{v} este:',
            correct,
            wrongs,
            f'Produsul scalar este u1·v1 + u2·v2 = {correct}.',
            'Înmulțești coordonatele de același rang și apoi aduni.',
            ['calculezi u1v1', 'calculezi u2v2', 'aduni rezultatele'],
            ['produs scalar']
        ))
    angle_cases = [
        ((1, 0), (0, 1), 'sunt perpendiculari', ['sunt paraleli', 'formează un unghi de 45°', 'au același sens']),
        ((2, 2), (1, 1), 'sunt paraleli', ['sunt perpendiculari', 'formează 60°', 'au produsul scalar 1']),
        ((3, 0), (-1, 0), 'sunt coliniari de sens opus', ['sunt perpendiculari', 'sunt paraleli de același sens', 'nu pot fi comparați']),
        ((1, 2), (2, -1), 'formează un unghi ascuțit? nu', ['sunt paraleli', 'sunt perpendiculari', 'formează un unghi nul']),
        ((1, 1), (1, -1), 'sunt perpendiculari', ['sunt paraleli', 'au același modul și aceeași direcție', 'sunt identici']),
    ]
    for u, v, correct, wrongs in angle_cases:
        raws.append(make_raw(
            f'Pentru vectorii u{u} și v{v}, afirmația corectă este:',
            correct,
            wrongs,
            'Poți decide din produsul scalar și din proporționalitatea coordonatelor dacă vectorii sunt perpendiculari sau paraleli.',
            'Produs scalar zero ⇒ perpendiculari. Proporționalitate ⇒ coliniari/paraleli.',
            ['verifici produsul scalar sau proporționalitatea'],
            ['unghi între vectori']
        ))
    return raws

# Additional chapters will be appended below.

def gen_matrices() -> list[dict]:
    raws = []
    add_cases = [
        (((1, 2), (3, 4)), ((2, 1), (0, -1)), '((3, 3), (3, 3))'),
        (((2, 0), (1, 5)), ((-1, 4), (3, 2)), '((1, 4), (4, 7))'),
        (((3, 1), (0, 2)), ((1, -1), (4, 3)), '((4, 0), (4, 5))'),
        (((0, 2), (2, 0)), ((5, 1), (1, 5)), '((5, 3), (3, 5))'),
        (((-1, 3), (2, 4)), ((2, 2), (1, -3)), '((1, 5), (3, 1))'),
    ]
    for A, B, correct in add_cases:
        wrongs = ['((0, 0), (0, 0))', '((1, 1), (1, 1))', '((2, 2), (2, 2))']
        raws.append(make_raw(
            f'Suma matricelor A={A} și B={B} este:',
            correct,
            wrongs,
            'Aduni elementele aflate pe aceeași poziție.',
            'Scrie matricea rezultat element cu element.',
            ['adaugi elementele de pe aceeași poziție'],
            ['matrice', 'adunare']
        ))
    det_cases = [(((2, 1), (3, 4)), '5'), (((1, 2), (5, 1)), '-9'), (((3, 0), (2, -1)), '-3'), (((4, 2), (1, 3)), '10'), (((-1, 2), (3, 5)), '-11')]
    for A, correct in det_cases:
        wrongs = ['0', '1', '2'] if correct not in ('0', '1', '2') else ['-1', '3', '4']
        raws.append(make_raw(
            f'Determinantul matricei A={A} este:',
            correct,
            wrongs,
            'Pentru matrice 2x2, det(A)=ad-bc.',
            'Înmulțești diagonala principală și scazi produsul diagonalei secundare.',
            ['aplici formula ad-bc'],
            ['determinant']
        ))
    inv_cases = [(((1, 2), (3, 5)), 'A^-1 = ((-5, 2), (3, -1))', ['A^-1 = ((5, -2), (-3, 1))', 'A^-1 = A^t', 'A^-1 = ((1, 0), (0, 1))']),
                 (((2, 1), (1, 1)), 'A^-1 = ((1, -1), (-1, 2))', ['A^-1 = ((2, -1), (-1, 1))', 'A^-1 = A', 'A^-1 = ((1, 1), (1, 2))']),
                 (((3, 1), (2, 1)), 'A^-1 = ((1, -1), (-2, 3))', ['A^-1 = ((3, -1), (-2, 1))', 'A^-1 = A^t', 'A^-1 = ((1, 0), (0, 1))']),
                 (((1, -1), (1, 2)), 'A^-1 = ((2/3, 1/3), (-1/3, 1/3))', ['A^-1 = ((2, 1), (-1, 1))', 'A^-1 = ((1, 1), (-1, 2))', 'A^-1 nu există']),
                 (((4, 1), (3, 1)), 'A^-1 = ((1, -1), (-3, 4))', ['A^-1 = ((4, -1), (-3, 1))', 'A^-1 = A', 'A^-1 = A^t'])]
    for A, correct, wrongs in inv_cases:
        raws.append(make_raw(
            f'Pentru matricea A={A}, varianta corectă pentru inversă este:',
            correct,
            wrongs,
            'Calculezi determinantul, transpusa cofactorilor și apoi împarți la determinant.',
            'Verifică mai întâi dacă determinantul este nenul.',
            ['calculezi det(A)', 'scrii adjuncta', 'împarți la determinant'],
            ['inversă de matrice']
        ))
    system_cases = [
        ('{x+y=5, x-y=1}', '(x,y)=(3,2)'),
        ('{2x+y=7, x-y=2}', '(x,y)=(3,1)'),
        ('{x+2y=8, x-y=2}', '(x,y)=(4,2)'),
        ('{3x+y=10, x-y=2}', '(x,y)=(3,1)'),
        ('{2x-y=1, x+y=5}', '(x,y)=(2,3)'),
    ]
    for system, correct in system_cases:
        wrongs = ['(x,y)=(1,1)', '(x,y)=(0,0)', '(x,y)=(2,2)']
        raws.append(make_raw(
            f'Soluția sistemului {system} este:',
            correct,
            wrongs,
            'Poți rezolva prin substituție, reducere sau cu regula lui Cramer.',
            'Verifică rapid soluția obținută prin înlocuire în ambele ecuații.',
            ['rezolvi sistemul', 'verifici perechea obținută'],
            ['sisteme liniare']
        ))
    return raws


def gen_composition_laws() -> list[dict]:
    raws = []
    calc_cases = [
        ('x*y = x + y + 2', 1, 3, '6'),
        ('x*y = xy + 1', 2, 4, '9'),
        ('x*y = x + 2y', 3, 5, '13'),
        ('x*y = x - y + 4', 7, 2, '9'),
        ('x*y = 2xy - x', 2, 3, '10'),
    ]
    for law, x, y, correct in calc_cases:
        wrongs = [str(x + y), str(x * y), str(int(correct) + 1)]
        raws.append(make_raw(
            f'Pe R se definește legea {law}. Atunci {x}*{y} este:',
            correct,
            wrongs,
            f'Înlocuiești x={x} și y={y} în legea dată și obții {correct}.',
            'La legi de compoziție nu inventezi o regulă nouă: aplici exact expresia din definiție.',
            ['înlocuiești valorile în lege'],
            ['lege de compoziție']
        ))
    comm_cases = [
        ('x*y = x + y + 1', 'este comutativă', ['nu este comutativă', 'nu are element neutru', 'este doar asociativă']),
        ('x*y = x + 2y', 'nu este comutativă', ['este comutativă', 'este doar pe Z', 'este distributivă față de sine']),
        ('x*y = xy', 'este comutativă', ['nu este comutativă', 'nu are element neutru', 'nu este asociativă']),
        ('x*y = x - y', 'nu este comutativă', ['este comutativă', 'are neutru 0', 'este asociativă']),
        ('x*y = x + y - 3', 'este comutativă', ['nu este comutativă', 'nu admite calcule', 'este doar pe N']),
    ]
    for law, correct, wrongs in comm_cases:
        raws.append(make_raw(
            f'Pentru legea {law}, afirmația corectă este:',
            correct,
            wrongs,
            'Verifici dacă schimbarea lui x cu y păstrează aceeași expresie.',
            'Comutativitatea se testează comparând x*y și y*x.',
            ['scrii x*y și y*x', 'compari cele două expresii'],
            ['comutativitate']
        ))
    neutral_cases = [
        ('x*y = x + y - 4', 'e = 4', ['e = 0', 'e = -4', 'nu există element neutru']),
        ('x*y = xy', 'e = 1', ['e = 0', 'e = -1', 'nu există element neutru']),
        ('x*y = x + y + 2', 'e = -2', ['e = 2', 'e = 0', 'nu există element neutru']),
        ('x*y = x - y', 'nu există element neutru', ['e = 0', 'e = 1', 'e = -1']),
        ('x*y = x + 2y', 'nu există element neutru', ['e = 0', 'e = 1', 'e = -1']),
    ]
    for law, correct, wrongs in neutral_cases:
        raws.append(make_raw(
            f'Pentru legea {law}, elementul neutru este:',
            correct,
            wrongs,
            'Cauți e astfel încât x*e=e*x=x pentru orice x din mulțime.',
            'Scrie simultan condițiile x*e=x și e*x=x.',
            ['impui condițiile pentru elementul neutru'],
            ['element neutru']
        ))
    inverse_cases = [
        ('x*y = x + y - 2, cu neutru 2', 'simetricul lui 5 este -1', ['simetricul lui 5 este 1', 'simetricul lui 5 este 2', 'simetricul lui 5 nu există']),
        ('x*y = x + y + 4, cu neutru -4', 'simetricul lui 3 este -11', ['simetricul lui 3 este 11', 'simetricul lui 3 este -3', 'simetricul lui 3 nu există']),
        ('x*y = xy, pe R* cu neutru 1', 'simetricul lui 4 este 1/4', ['simetricul lui 4 este -4', 'simetricul lui 4 este 4', 'simetricul lui 4 nu există']),
        ('x*y = x + y - 6, cu neutru 6', 'simetricul lui 8 este 4', ['simetricul lui 8 este -4', 'simetricul lui 8 este 6', 'simetricul lui 8 nu există']),
        ('x*y = x - y, pe R', 'nu toți au simetric', ['toți au simetric 0', 'toți au simetric 1', 'simetricul coincide cu opusul']),
    ]
    for law, correct, wrongs in inverse_cases:
        raws.append(make_raw(
            f'Pentru legea {law}, afirmația corectă este:',
            correct,
            wrongs,
            'Elementul simetrizabil se găsește din x*x\' = e, unde e este elementul neutru.',
            'După ce găsești neutrul, rezolvi ecuația x*x\'=e.',
            ['scrii condiția pentru simetric'],
            ['element simetric']
        ))
    return raws


def gen_polynomials() -> list[dict]:
    raws = []
    rem_cases = [
        ('P(x)=x^2-5x+6', 'P(2)=0', ['P(2)=2', 'P(2)=6', 'P(2)=-2']),
        ('P(x)=x^2-1', 'P(1)=0', ['P(1)=1', 'P(1)=2', 'P(1)=-1']),
        ('P(x)=x^3-8', 'P(2)=0', ['P(2)=4', 'P(2)=8', 'P(2)=-8']),
        ('P(x)=x^2+x-6', 'P(2)=0', ['P(2)=2', 'P(2)=4', 'P(2)=-2']),
        ('P(x)=x^2-9', 'P(3)=0', ['P(3)=3', 'P(3)=9', 'P(3)=-3']),
    ]
    for poly, correct, wrongs in rem_cases:
        raws.append(make_raw(
            f'Pentru {poly}, afirmația corectă este:',
            correct,
            wrongs,
            'Înlocuiești valoarea cerută în polinom. Dacă rezultatul este 0, atunci x-a este factor.',
            'Teorema restului: restul împărțirii la x-a este P(a).',
            ['calculezi P(a)'],
            ['teorema restului']
        ))
    root_cases = [
        ('x^2-5x+6=0', fmt_set(['2', '3']), [fmt_set(['-2', '-3']), fmt_set(['1', '6']), fmt_set(['3'])]),
        ('x^2-7x+10=0', fmt_set(['2', '5']), [fmt_set(['-2', '-5']), fmt_set(['1', '10']), fmt_set(['5'])]),
        ('x^2+x-6=0', fmt_set(['-3', '2']), [fmt_set(['3', '-2']), fmt_set(['1', '-6']), fmt_set(['2'])]),
        ('x^2-9=0', fmt_set(['-3', '3']), [fmt_set(['3']), fmt_set(['-9', '1']), fmt_set(['0', '3'])]),
        ('x^2-4x+3=0', fmt_set(['1', '3']), [fmt_set(['-1', '-3']), fmt_set(['0', '3']), fmt_set(['4', '-1'])]),
    ]
    for equation, correct, wrongs in root_cases:
        raws.append(make_raw(
            f'Mulțimea rădăcinilor ecuației {equation} este:',
            correct,
            wrongs,
            'Factorizezi sau aplici formula și obții rădăcinile corecte.',
            'Verifică suma și produsul rădăcinilor prin relațiile lui Viète.',
            ['determini rădăcinile', 'scrii mulțimea soluțiilor'],
            ['rădăcini', 'Viète']
        ))
    factor_cases = [
        ('x^2-5x+6', '(x-2)(x-3)', ['(x+2)(x+3)', '(x-1)(x-6)', '(x+1)(x-6)']),
        ('x^2-9', '(x-3)(x+3)', ['(x-9)(x+1)', '(x-3)^2', '(x+9)(x-1)']),
        ('x^2+x-6', '(x+3)(x-2)', ['(x-3)(x+2)', '(x+1)(x-6)', '(x-1)(x+6)']),
        ('x^2-4x+4', '(x-2)^2', ['(x+2)^2', '(x-4)x', '(x-1)(x-3)']),
        ('x^2+5x+6', '(x+2)(x+3)', ['(x-2)(x-3)', '(x+1)(x+6)', '(x-1)(x+6)']),
    ]
    for poly, correct, wrongs in factor_cases:
        raws.append(make_raw(
            f'Descompunerea corectă în factori a polinomului {poly} este:',
            correct,
            wrongs,
            'Cauți două numere cu suma și produsul potrivite.',
            'Verifică simultan suma și produsul termenilor constanți.',
            ['cauți rădăcinile sau perechea potrivită', 'scrii produsul factorilor'],
            ['factorizare']
        ))
    degree_cases = [
        ('P(x)=3x^4-2x+1', '4', ['3', '2', '1']),
        ('P(x)=x^5+x^2', '5', ['2', '7', '1']),
        ('P(x)=7x-3', '1', ['7', '0', '2']),
        ('P(x)=2', '0', ['1', '2', '-1']),
        ('P(x)=x^3-4x^2+x', '3', ['2', '4', '1']),
    ]
    for poly, correct, wrongs in degree_cases:
        raws.append(make_raw(
            f'Gradul polinomului {poly} este:',
            correct,
            wrongs,
            'Gradul este cel mai mare exponent al lui x cu coeficient nenul.',
            'Nu te uita la coeficienți, ci la exponentul maxim.',
            ['identifici termenul de grad maxim'],
            ['grad de polinom']
        ))
    return raws


def gen_limits() -> list[dict]:
    raws = []
    inf_cases = [
        ('lim x→∞ (3x+1)/(x+2)', '3', ['1', '0', '∞']),
        ('lim x→∞ (2x^2-1)/(x^2+3)', '2', ['1', '0', '∞']),
        ('lim x→∞ (5x^3+2)/(x^3-1)', '5', ['1', '0', '∞']),
        ('lim x→∞ (x+4)/(2x-3)', '1/2', ['2', '0', '1']),
        ('lim x→∞ (7x^2)/(x^2+1)', '7', ['1', '0', '∞']),
    ]
    for expr, correct, wrongs in inf_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'La infinit pentru raport de polinoame de același grad, limita este raportul coeficienților termenilor dominanți.',
            'Împarte sus și jos la puterea cea mai mare a lui x.',
            ['identifici termenii dominanți', 'formezi raportul coeficienților'],
            ['limită la infinit']
        ))
    finite_cases = [
        ('lim x→2 (x^2-4)/(x-2)', '4', ['2', '0', '∞']),
        ('lim x→3 (x^2-9)/(x-3)', '6', ['3', '0', '∞']),
        ('lim x→1 (x^2-1)/(x-1)', '2', ['1', '0', '∞']),
        ('lim x→-1 (x^2-1)/(x+1)', '-2', ['2', '0', '∞']),
        ('lim x→4 (x^2-16)/(x-4)', '8', ['4', '0', '∞']),
    ]
    for expr, correct, wrongs in finite_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'Factorizezi numărătorul și simplifici factorul comun, apoi înlocuiești.',
            'Dacă obții forma 0/0, caută factor comun sau folosește regulile de limită.',
            ['factorizezi', 'simplifici', 'înlocuiești'],
            ['limită', '0/0']
        ))
    radical_cases = [
        ('lim x→0 (√(x+1)-1)/x', '1/2', ['1', '0', '∞']),
        ('lim x→0 (√(1+2x)-1)/x', '1', ['1/2', '2', '0']),
        ('lim x→∞ (√(x^2+1)-x)', '0', ['1', '∞', '-1']),
        ('lim x→∞ (√(x^2+4x)-x)', '2', ['4', '0', '∞']),
        ('lim x→∞ (√(x^2+6x)-x)', '3', ['6', '0', '∞']),
    ]
    for expr, correct, wrongs in radical_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'Amplifici cu conjugata sau scoți factorul dominant și obții limita corectă.',
            'La diferențe cu radicali, conjugata este de obicei reflexul bun.',
            ['amplifici cu conjugata sau scoți factorul dominant'],
            ['limită cu radical']
        ))
    remarkable_cases = [
        ('lim x→0 sin x / x', '1', ['0', '∞', '-1']),
        ('lim x→0 (e^x-1)/x', '1', ['0', 'e', '-1']),
        ('lim n→∞ (1+1/n)^n', 'e', ['1', '0', '∞']),
        ('lim x→0 ln(1+x)/x', '1', ['0', '∞', '-1']),
        ('lim x→0 (1-cos x)/x^2', '1/2', ['1', '0', '2']),
    ]
    for expr, correct, wrongs in remarkable_cases:
        raws.append(make_raw(
            f'Valoarea limitei remarcabile {expr} este:',
            correct,
            wrongs,
            'Aceasta este una dintre limitele remarcabile standard din programa M1.',
            'Merită memorate exact în forma lor canonică.',
            ['recunoști limita remarcabilă'],
            ['limită remarcabilă']
        ))
    return raws


def gen_continuity() -> list[dict]:
    raws = []
    cont_cases = [
        ('f(x)={x+1, x<2; ax-1, x≥2}', 'a = 2', ['a = 1', 'a = 0', 'a = 3']),
        ('f(x)={2x+3, x<1; ax+1, x≥1}', 'a = 4', ['a = 2', 'a = 0', 'a = -4']),
        ('f(x)={x^2, x<1; ax, x≥1}', 'a = 1', ['a = 2', 'a = 0', 'a = -1']),
        ('f(x)={x+2, x<0; ax+2, x≥0}', 'a poate fi orice număr real', ['a = 1', 'a = 0', 'a = -1']),
        ('f(x)={3x-1, x<2; ax+1, x≥2}', 'a = 2', ['a = 1', 'a = 3', 'a = 5']),
    ]
    for prompt, correct, wrongs in cont_cases:
        raws.append(make_raw(
            f'Pentru ca funcția {prompt} să fie continuă în punctul de racord, trebuie să avem:',
            correct,
            wrongs,
            'Egalăm limita din stânga cu limita din dreapta și cu valoarea funcției în punctul respectiv.',
            'La continuitate în punctul de lipire, cele două expresii trebuie să dea aceeași valoare.',
            ['calculezi limita stângă', 'calculezi limita dreaptă', 'egalezi valorile'],
            ['continuitate']
        ))
    asym_h_cases = [
        ('f(x)=(x+1)/(x+2)', 'y = 1', ['y = 0', 'x = -2', 'y = x']),
        ('f(x)=(2x^2+1)/(x^2+3)', 'y = 2', ['y = 0', 'x = 0', 'y = 1']),
        ('f(x)=1/(x+1)', 'y = 0', ['y = 1', 'x = -1', 'y = x+1']),
        ('f(x)=(3x-2)/(x+5)', 'y = 3', ['y = 0', 'x = -5', 'y = 1/3']),
        ('f(x)=(4x^2)/(2x^2+1)', 'y = 2', ['y = 4', 'y = 0', 'x = 0']),
    ]
    for func, correct, wrongs in asym_h_cases:
        raws.append(make_raw(
            f'Asimptota orizontală la +∞ pentru {func} este:',
            correct,
            wrongs,
            f'Limita funcției la infinit este {correct.split("=")[1].strip()}, deci asimptota orizontală este {correct}.',
            'Pentru rapoarte de polinoame de același grad, asimptota orizontală vine din raportul coeficienților dominanți.',
            ['calculezi limita la infinit', 'scrii ecuația y=l'],
            ['asimptotă orizontală']
        ))
    asym_v_cases = [
        ('f(x)=1/(x-2)', 'x = 2', ['y = 2', 'x = -2', 'nu are asimptotă verticală']),
        ('f(x)=3/(x+1)', 'x = -1', ['y = -1', 'x = 1', 'nu are asimptotă verticală']),
        ('f(x)=x/(x-5)', 'x = 5', ['y = 1', 'x = -5', 'nu are asimptotă verticală']),
        ('f(x)=2/(x+4)', 'x = -4', ['y = -4', 'x = 4', 'nu are asimptotă verticală']),
        ('f(x)=(x+1)/(x-3)', 'x = 3', ['y = 1', 'x = -3', 'nu are asimptotă verticală']),
    ]
    for func, correct, wrongs in asym_v_cases:
        raws.append(make_raw(
            f'Asimptota verticală a funcției {func} este:',
            correct,
            wrongs,
            'Asimptota verticală apare acolo unde numitorul se anulează și funcția tinde la ±∞.',
            'Găsește valorile interzise ale variabilei din numitor.',
            ['rezolvi ecuația numitorului = 0'],
            ['asimptotă verticală']
        ))
    classify_cases = [
        ('f(x)=x^2', 'este continuă pe R', ['nu este continuă în 0', 'nu este continuă pentru x<0', 'este continuă doar pe (0,∞)']),
        ('f(x)=1/(x-2)', 'este continuă pe R\\{2}', ['este continuă pe R', 'nu este continuă nicăieri', 'este continuă doar în 2']),
        ('f(x)=√(x+1)', 'este continuă pe [-1,∞)', ['este continuă pe R', 'este continuă pe (0,∞)', 'nu este continuă nicăieri']),
        ('f(x)=ln x', 'este continuă pe (0,∞)', ['este continuă pe R', 'este continuă pe [0,∞)', 'este discontinuă peste tot']),
        ('f(x)=|x|', 'este continuă pe R', ['nu este continuă în 0', 'este continuă doar pentru x≥0', 'este continuă doar pentru x≤0']),
    ]
    for func, correct, wrongs in classify_cases:
        raws.append(make_raw(
            f'Funcția {func}:',
            correct,
            wrongs,
            'Folosești proprietățile de continuitate ale funcțiilor elementare și domeniul lor natural.',
            'Mai întâi stabilește domeniul funcției.',
            ['identifici domeniul', 'apelezi la continuitatea funcțiilor elementare'],
            ['continuitatea funcțiilor elementare']
        ))
    return raws


def gen_derivatives() -> list[dict]:
    raws = []
    poly_cases = [
        ('f(x)=x^3-2x', 'f\'(x)=3x^2-2', ['f\'(x)=x^2-2', 'f\'(x)=3x-2', 'f\'(x)=3x^2']),
        ('f(x)=2x^4+x', 'f\'(x)=8x^3+1', ['f\'(x)=8x^4+1', 'f\'(x)=4x^3+1', 'f\'(x)=8x^3']),
        ('f(x)=5x^2-3', 'f\'(x)=10x', ['f\'(x)=5x', 'f\'(x)=10', 'f\'(x)=10x-3']),
        ('f(x)=x^5', 'f\'(x)=5x^4', ['f\'(x)=x^4', 'f\'(x)=4x^5', 'f\'(x)=5x']),
        ('f(x)=7x-1', 'f\'(x)=7', ['f\'(x)=1', 'f\'(x)=7x', 'f\'(x)=0']),
    ]
    for func, correct, wrongs in poly_cases:
        raws.append(make_raw(
            f'Pentru {func}, derivata este:',
            correct,
            wrongs,
            'Aplici formula (x^n)\'=n x^(n-1) și derivata constantei este 0.',
            'Derivata unui număr este 0.',
            ['derivi termen cu termen'],
            ['derivată polinomială']
        ))
    prod_cases = [
        ('f(x)=x·e^x', 'f\'(x)=e^x+x e^x', ['f\'(x)=e^x', 'f\'(x)=x e^x', 'f\'(x)=x']),
        ('f(x)=x·ln x', 'f\'(x)=ln x + 1', ['f\'(x)=1/x', 'f\'(x)=ln x', 'f\'(x)=x/x']),
        ('f(x)=(x+1)(x-2)', 'f\'(x)=2x-1', ['f\'(x)=x-1', 'f\'(x)=2x+1', 'f\'(x)=x^2-1']),
        ('f(x)=x sin x', 'f\'(x)=sin x + x cos x', ['f\'(x)=cos x', 'f\'(x)=x cos x', 'f\'(x)=sin x']),
        ('f(x)=x cos x', 'f\'(x)=cos x - x sin x', ['f\'(x)=-sin x', 'f\'(x)=x sin x', 'f\'(x)=cos x + x sin x']),
    ]
    for func, correct, wrongs in prod_cases:
        raws.append(make_raw(
            f'Pentru {func}, derivata corectă este:',
            correct,
            wrongs,
            'Aplici regula produsului: (fg)\'=f\'g+fg\'.',
            'Nu uita să derivezi ambii factori.',
            ['aplici regula produsului', 'simplifici dacă este nevoie'],
            ['regula produsului']
        ))
    chain_cases = [
        ('f(x)=ln(2x+1)', 'f\'(x)=2/(2x+1)', ['f\'(x)=1/(2x+1)', 'f\'(x)=2x/(2x+1)', 'f\'(x)=ln 2']),
        ('f(x)=e^(3x)', 'f\'(x)=3e^(3x)', ['f\'(x)=e^(3x)', 'f\'(x)=3x e^(3x)', 'f\'(x)=e^x']),
        ('f(x)=sin(4x)', 'f\'(x)=4 cos(4x)', ['f\'(x)=cos(4x)', 'f\'(x)=4 sin(4x)', 'f\'(x)=-4 sin(4x)']),
        ('f(x)=cos(2x)', 'f\'(x)=-2 sin(2x)', ['f\'(x)=2 cos(2x)', 'f\'(x)=sin(2x)', 'f\'(x)=-sin x']),
        ('f(x)=√(x+3)', 'f\'(x)=1/(2√(x+3))', ['f\'(x)=1/√(x+3)', 'f\'(x)=√(x+3)', 'f\'(x)=1/2']),
    ]
    for func, correct, wrongs in chain_cases:
        raws.append(make_raw(
            f'Pentru {func}, derivata corectă este:',
            correct,
            wrongs,
            'Aplici regula lanțului: derivata funcției exterioare înmulțită cu derivata expresiei interioare.',
            'La funcțiile compuse apare în plus derivata lui u(x).',
            ['identifici funcția compusă', 'aplici regula lanțului'],
            ['regula lanțului']
        ))
    tangent_cases = [
        ('f(x)=x^2, x0=1', 'm_t = 2', ['m_t = 1', 'm_t = 0', 'm_t = 4']),
        ('f(x)=x^2+1, x0=2', 'm_t = 4', ['m_t = 2', 'm_t = 3', 'm_t = 5']),
        ('f(x)=x^3, x0=1', 'm_t = 3', ['m_t = 1', 'm_t = 2', 'm_t = 0']),
        ('f(x)=2x+5, x0=0', 'm_t = 2', ['m_t = 5', 'm_t = 0', 'm_t = 1']),
        ('f(x)=ln x, x0=1', 'm_t = 1', ['m_t = 0', 'm_t = e', 'm_t = -1']),
    ]
    for prompt, correct, wrongs in tangent_cases:
        raws.append(make_raw(
            f'Pentru {prompt}, panta tangentei în punctul x0 este:',
            correct,
            wrongs,
            'Panta tangentei este derivata funcției în punctul respectiv.',
            'Mai întâi derivezi, apoi înlocuiești x0.',
            ['calculezi f\'(x)', 'înlocuiești x0'],
            ['tangentă']
        ))
    return raws


def gen_study_by_derivative() -> list[dict]:
    raws = []
    mono_cases = [
        ('f\'(x)=2x', 'f este crescătoare pe (0,∞)', ['f este descrescătoare pe (0,∞)', 'f este constantă pe R', 'f este crescătoare pe (-∞,0)']),
        ('f\'(x)=-3', 'f este strict descrescătoare pe R', ['f este strict crescătoare pe R', 'f este constantă pe R', 'f este crescătoare pe (0,∞)']),
        ('f\'(x)=x-1', 'f este crescătoare pe (1,∞)', ['f este crescătoare pe (-∞,1)', 'f este descrescătoare pe (1,∞)', 'f este constantă în 1']),
        ('f\'(x)=-(x+2)^2', 'f este descrescătoare pe R', ['f este crescătoare pe R', 'f este constantă pe R', 'f este crescătoare pe (-∞,-2)']),
        ('f\'(x)=(x-3)^2', 'f este crescătoare pe R', ['f este descrescătoare pe R', 'f este crescătoare doar pe (3,∞)', 'f este constantă în 3']),
    ]
    for prompt, correct, wrongs in mono_cases:
        raws.append(make_raw(
            f'Dacă {prompt}, atunci afirmația corectă este:',
            correct,
            wrongs,
            'Semnul derivatei dictează monotonia funcției pe intervalele respective.',
            'f\'(x) > 0 înseamnă crescătoare, iar f\'(x) < 0 înseamnă descrescătoare.',
            ['studiezi semnul derivatei'],
            ['monotonie']
        ))
    extremum_cases = [
        ('f\'(x)=x(x-2)', 'f are puncte critice în x=0 și x=2', ['f nu are puncte critice', 'f are un singur punct critic în x=1', 'f are maxim în orice punct']),
        ('f\'(x)=x^2-1', 'f are puncte critice în x=-1 și x=1', ['f are un singur punct critic în x=0', 'f nu are puncte critice', 'f are puncte critice în x=1 și x=2']),
        ('f\'(x)=3x^2', 'f are punct critic în x=0', ['f nu are puncte critice', 'f are puncte critice în x=±1', 'f are infinit de multe puncte critice']),
        ('f\'(x)=(x-4)^2', 'f are punct critic în x=4', ['f nu are puncte critice', 'f are puncte critice în x=±4', 'f are punct critic în x=2']),
        ('f\'(x)=x+5', 'f are punct critic în x=-5', ['f are punct critic în x=5', 'f nu are puncte critice', 'f are punct critic în x=0']),
    ]
    for prompt, correct, wrongs in extremum_cases:
        raws.append(make_raw(
            f'Dacă {prompt}, atunci afirmația corectă este:',
            correct,
            wrongs,
            'Punctele critice apar unde derivata se anulează sau nu există.',
            'Rezolvă ecuația f\'(x)=0.',
            ['egalezi derivata cu 0'],
            ['puncte critice']
        ))
    tangent_cases = [
        ('f(x)=x^2+1, în x0=1', 'y = 2x', ['y = x+1', 'y = 2x+1', 'y = x']),
        ('f(x)=x^2, în x0=2', 'y = 4x-4', ['y = 2x', 'y = 4x', 'y = x+2']),
        ('f(x)=x^3, în x0=1', 'y = 3x-2', ['y = x+1', 'y = 3x+2', 'y = x-2']),
        ('f(x)=2x+5, în x0=0', 'y = 2x+5', ['y = 5', 'y = 2x', 'y = x+5']),
        ('f(x)=ln x, în x0=1', 'y = x-1', ['y = x', 'y = 1', 'y = x+1']),
    ]
    for prompt, correct, wrongs in tangent_cases:
        raws.append(make_raw(
            f'Ecuația tangentei la graficul funcției {prompt} este:',
            correct,
            wrongs,
            'Folosești formula y-y0=f\'(x0)(x-x0).',
            'Calculează separat panta și punctul de tangență.',
            ['calculezi f\'(x0)', 'calculezi y0', 'scrii ecuația tangentei'],
            ['ecuația tangentei']
        ))
    rolle_cases = [
        ('f(x)=x^2-1 pe [-1,1]', 'există c=0 cu f\'(c)=0', ['nu există niciun astfel de c', 'c=1', 'c=-1']),
        ('f(x)=x^3-x pe [-1,1]', 'există c în (-1,1) cu f\'(c)=0', ['nu există niciun astfel de c', 'c trebuie să fie unul dintre capete', 'teorema nu se aplică']),
        ('f(x)=sin x pe [0,π]', 'există c=π/2 cu f\'(c)=0', ['nu există niciun astfel de c', 'c=0', 'c=π']),
        ('f(x)=x^2 pe [-1,1]', 'teorema lui Rolle nu se aplică', ['există c=0 cu f\'(c)=0', 'c=1', 'c=-1']),
        ('f(x)=x^3-3x pe [-√3,√3]', 'există c=0 cu f\'(c)=0', ['nu există niciun astfel de c', 'c=√3', 'c=-√3']),
    ]
    for prompt, correct, wrongs in rolle_cases:
        raws.append(make_raw(
            f'Pentru {prompt}, afirmația corectă este:',
            correct,
            wrongs,
            'Verifici mai întâi ipotezele teoremei lui Rolle și apoi rezolvi f\'(x)=0.',
            'Nu sari direct la f\'(x)=0; verifică și condiția f(a)=f(b).',
            ['verifici ipotezele teoremei', 'rezolvi f\'(x)=0'],
            ['Rolle']
        ))
    return raws


def gen_primitives() -> list[dict]:
    raws = []
    basic_cases = [
        ('∫ x^2 dx', 'x^3/3 + C', ['x^2/2 + C', '3x^2 + C', 'x^3 + C']),
        ('∫ 2x dx', 'x^2 + C', ['2x^2 + C', 'x + C', 'ln x + C']),
        ('∫ 1/x dx', 'ln|x| + C', ['1/(x^2) + C', 'x + C', 'e^x + C']),
        ('∫ e^x dx', 'e^x + C', ['xe^x + C', 'ln x + C', '1/e^x + C']),
        ('∫ cos x dx', 'sin x + C', ['-sin x + C', 'cos x + C', '-cos x + C']),
    ]
    for expr, correct, wrongs in basic_cases:
        raws.append(make_raw(
            f'O primitivă pentru {expr} este:',
            correct,
            wrongs,
            f'Derivând {correct}, revii la integrand.',
            'Verifică prin derivare rezultatul ales.',
            ['alegi formula de integrare', 'verifici prin derivare'],
            ['primitivă']
        ))
    poly_cases = [
        ('∫ (3x^2-4) dx', 'x^3-4x + C', ['3x^3-4x + C', 'x^3-4 + C', 'x^2-4x + C']),
        ('∫ (4x^3+2x) dx', 'x^4+x^2 + C', ['4x^4+x^2 + C', 'x^4+2x + C', 'x^3+x^2 + C']),
        ('∫ (5x^4-x) dx', 'x^5-x^2/2 + C', ['5x^5-x^2/2 + C', 'x^5-x^2 + C', 'x^4-x/2 + C']),
        ('∫ (2x+3) dx', 'x^2+3x + C', ['2x^2+3x + C', 'x^2+3 + C', 'ln x + 3x + C']),
        ('∫ (x^5+1) dx', 'x^6/6 + x + C', ['x^5/5 + x + C', 'x^6 + x + C', 'x^6/5 + C']),
    ]
    for expr, correct, wrongs in poly_cases:
        raws.append(make_raw(
            f'Rezultatul corect pentru {expr} este:',
            correct,
            wrongs,
            'Integrezi termen cu termen folosind regula ∫x^n dx = x^(n+1)/(n+1)+C.',
            'Crești exponentul cu 1 și împarți la noul exponent.',
            ['integrezi fiecare termen separat'],
            ['integrare polinomială']
        ))
    trig_exp_cases = [
        ('∫ sin x dx', '-cos x + C', ['cos x + C', 'sin x + C', 'x sin x + C']),
        ('∫ 2e^x dx', '2e^x + C', ['e^x + C', '2xe^x + C', 'ln x + C']),
        ('∫ 3/x dx', '3ln|x| + C', ['ln|x| + C', '3/x^2 + C', '3x + C']),
        ('∫ -sin x dx', 'cos x + C', ['-cos x + C', 'sin x + C', '-x cos x + C']),
        ('∫ 4cos x dx', '4sin x + C', ['sin x + C', '-4sin x + C', '4cos x + C']),
    ]
    for expr, correct, wrongs in trig_exp_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'Aplici formula standard corespunzătoare funcției elementare din integrand.',
            'Ține minte perechea: (sin x)\' = cos x și (cos x)\' = -sin x.',
            ['alegi formula standard de primitivare'],
            ['primitivă standard']
        ))
    selection_cases = [
        ('F(x)=x^2+1', 'poate fi o primitivă a lui f(x)=2x', ['poate fi o primitivă a lui f(x)=x^2+1', 'nu poate fi primitivată', 'este derivata lui 2x']),
        ('F(x)=e^x', 'poate fi o primitivă a lui f(x)=e^x', ['poate fi o primitivă a lui f(x)=x e^x', 'nu este nicio primitivă', 'poate fi o primitivă a lui f(x)=ln x']),
        ('F(x)=ln|x|', 'poate fi o primitivă a lui f(x)=1/x', ['poate fi o primitivă a lui f(x)=x', 'nu poate fi derivată', 'este primitivă pentru e^x']),
        ('F(x)=sin x', 'poate fi o primitivă a lui f(x)=cos x', ['poate fi o primitivă a lui f(x)=sin x', 'nu poate fi primitivă', 'este primitivă pentru -cos x']),
        ('F(x)=x^3/3', 'poate fi o primitivă a lui f(x)=x^2', ['poate fi o primitivă a lui f(x)=x^3', 'nu poate fi primitivă', 'este primitivă pentru 3x^2']),
    ]
    for F, correct, wrongs in selection_cases:
        raws.append(make_raw(
            f'Afirmația corectă despre {F} este:',
            correct,
            wrongs,
            'Verifici prin derivare: dacă F\'=f, atunci F este o primitivă pentru f.',
            'La primitive, verificarea rapidă se face prin derivare.',
            ['derivezi funcția propusă', 'compari cu integrandul'],
            ['verificare prin derivare']
        ))
    return raws


def gen_definite_integrals() -> list[dict]:
    raws = []
    poly_cases = [
        ('∫_0^1 x dx', '1/2', ['1', '0', '2']),
        ('∫_0^2 2x dx', '4', ['2', '8', '1']),
        ('∫_1^3 x^2 dx', '26/3', ['9', '8', '13/3']),
        ('∫_0^1 (x^2+1) dx', '4/3', ['1', '2', '5/3']),
        ('∫_0^2 (3x^2) dx', '8', ['4', '6', '12']),
    ]
    for expr, correct, wrongs in poly_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'Determină o primitivă și aplică formula lui Newton-Leibniz.',
            'Întâi găsești o primitivă, apoi calculezi F(b)-F(a).',
            ['găsești o primitivă', 'aplici F(b)-F(a)'],
            ['integrală definită']
        ))
    exp_cases = [
        ('∫_0^1 e^x dx', 'e-1', ['e', '1', '1/e']),
        ('∫_1^e 1/x dx', '1', ['ln e', 'e-1', '0']),
        ('∫_0^π sin x dx', '2', ['0', '1', 'π']),
        ('∫_0^(π/2) cos x dx', '1', ['0', '2', 'π/2']),
        ('∫_0^1 3e^x dx', '3e-3', ['e-1', '3e', '3']),
    ]
    for expr, correct, wrongs in exp_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'Folosești o primitivă elementară și apoi aplici capetele intervalului.',
            'Nu uita să păstrezi exact capetele intervalului de integrare.',
            ['găsești o primitivă standard', 'înlocuiești capetele'],
            ['integrală definită', 'Newton-Leibniz']
        ))
    symmetry_cases = [
        ('∫_-1^1 x^3 dx', '0', ['2', '-2', '1']),
        ('∫_-2^2 x dx', '0', ['4', '-4', '2']),
        ('∫_-a^a x^5 dx, pentru a>0', '0', ['2a^5', 'a^6', 'nu se poate decide']),
        ('∫_-1^1 x^2 dx', '2/3', ['0', '1/3', '1']),
        ('∫_-2^2 (x^3+x) dx', '0', ['4', '-4', '8']),
    ]
    for expr, correct, wrongs in symmetry_cases:
        raws.append(make_raw(
            f'Valoarea integralei {expr} este:',
            correct,
            wrongs,
            'Funcțiile impare integrate pe intervale simetrice dau 0.',
            'Verifică mai întâi paritatea integrandului.',
            ['verifici dacă funcția este pară sau impară', 'folosești proprietatea de simetrie'],
            ['simetrie la integrale']
        ))
    substitution_cases = [
        ('∫_0^1 2x(x^2+1) dx', '3', ['2', '1', '4']),
        ('∫_0^1 3(x+1)^2 dx', '7', ['6', '8', '9']),
        ('∫_0^1 (2x)/(x^2+1) dx', 'ln 2', ['1', '2ln 2', '0']),
        ('∫_0^2 (x+1) dx', '4', ['3', '5', '2']),
        ('∫_0^1 4x^3 dx', '1', ['4', '0', '2']),
    ]
    for expr, correct, wrongs in substitution_cases:
        raws.append(make_raw(
            f'Calculați {expr}.',
            correct,
            wrongs,
            'Poți folosi schimbarea de variabilă sau recunoașterea rapidă a unei primitive compuse.',
            'Caută expresia interioară u și derivata ei u\'.',
            ['identifici variabila interioară', 'scrii primitiva sau faci substituția'],
            ['schimbare de variabilă']
        ))
    return raws


def gen_integral_applications() -> list[dict]:
    raws = []
    area_ox_cases = [
        ('f(x)=x pe [0,2]', '2', ['1', '4', '0']),
        ('f(x)=2x pe [0,1]', '1', ['2', '1/2', '0']),
        ('f(x)=x^2 pe [0,1]', '1/3', ['1/2', '1', '2/3']),
        ('f(x)=3x pe [0,2]', '6', ['3', '12', '0']),
        ('f(x)=1-x pe [0,1]', '1/2', ['1', '0', '2']),
    ]
    for prompt, correct, wrongs in area_ox_cases:
        raws.append(make_raw(
            f'Aria regiunii mărginită de graficul funcției {prompt}, axa Ox și verticale capetelor intervalului este:',
            correct,
            wrongs,
            'Aria se obține prin integrală definită, deoarece funcția este nenegativă pe interval.',
            'Verifică mai întâi dacă funcția este deasupra axei Ox pe interval.',
            ['scrii integrala ariei', 'calculezi integrală definită'],
            ['arie sub grafic']
        ))
    between_curves = [
        ('f(x)=x și g(x)=0 pe [0,2]', '2', ['1', '4', '0']),
        ('f(x)=x+1 și g(x)=1 pe [0,1]', '1/2', ['1', '0', '2']),
        ('f(x)=2x și g(x)=x pe [0,1]', '1/2', ['1', '0', '3/2']),
        ('f(x)=x^2+1 și g(x)=1 pe [0,1]', '1/3', ['1', '2/3', '0']),
        ('f(x)=3x+2 și g(x)=2 pe [0,2]', '6', ['3', '12', '0']),
    ]
    for prompt, correct, wrongs in between_curves:
        raws.append(make_raw(
            f'Aria dintre graficele funcțiilor {prompt} este:',
            correct,
            wrongs,
            'Integrezi funcția de sus minus funcția de jos pe intervalul dat.',
            'Stabilește clar care grafic este deasupra celuilalt.',
            ['scrii diferența f-g', 'calculezi integrală definită'],
            ['aria dintre două grafice']
        ))
    avg_cases = [
        ('f(x)=x pe [0,2]', '1', ['2', '1/2', '0']),
        ('f(x)=x^2 pe [0,1]', '1/3', ['1/2', '1', '2/3']),
        ('f(x)=2x+1 pe [0,1]', '2', ['3', '1', '4']),
        ('f(x)=3 pe [2,5]', '3', ['1', '5', '9']),
        ('f(x)=1-x pe [0,1]', '1/2', ['0', '1', '2']),
    ]
    for prompt, correct, wrongs in avg_cases:
        raws.append(make_raw(
            f'Valoarea medie a funcției {prompt} este:',
            correct,
            wrongs,
            'Valoarea medie se calculează cu formula 1/(b-a) ∫_a^b f(x)dx.',
            'Nu uita factorul 1/(b-a).',
            ['calculezi integrala definită', 'împarți la lungimea intervalului'],
            ['valoare medie']
        ))
    sign_cases = [
        ('f(x)=-x pe [0,1]', 'aria geometrică este 1/2', ['aria geometrică este -1/2', 'aria geometrică este 0', 'aria geometrică este 1']),
        ('f(x)=x-1 pe [0,1]', 'aria geometrică este 1/2', ['aria geometrică este -1/2', 'aria geometrică este 0', 'aria geometrică este 1']),
        ('f(x)=-2x pe [0,1]', 'aria geometrică este 1', ['aria geometrică este -1', 'aria geometrică este 2', 'aria geometrică este 0']),
        ('f(x)=1-2x pe [0,1/2]', 'aria geometrică este 1/4', ['aria geometrică este -1/4', 'aria geometrică este 1/2', 'aria geometrică este 0']),
        ('f(x)=-3 pe [0,2]', 'aria geometrică este 6', ['aria geometrică este -6', 'aria geometrică este 3', 'aria geometrică este 0']),
    ]
    for prompt, correct, wrongs in sign_cases:
        raws.append(make_raw(
            f'Pentru {prompt}, afirmația corectă este:',
            correct,
            wrongs,
            'Aria geometrică este întotdeauna pozitivă, chiar dacă integrala definită ar ieși negativă.',
            'Separă clar noțiunea de arie geometrică de valoarea unei integrale semnate.',
            ['verifici semnul funcției', 'iei valoarea absolută dacă este nevoie'],
            ['aria geometrică']
        ))
    return raws

GENERATORS: dict[str, Callable[[], list[dict]]] = {
    'multimi-intervale-si-logica-matematica': gen_sets,
    'functii-si-reprezentari-grafice': gen_functions,
    'functia-de-gradul-i-si-functia-de-gradul-al-ii-lea': gen_linear_quadratic,
    'siruri-aritmetice-si-geometrice': gen_sequences,
    'puteri-radicali-si-logaritmi': gen_powers_radicals_logs,
    'numere-complexe': gen_complex_numbers,
    'functia-exponentiala-si-functia-logaritmica': gen_exp_log_functions,
    'ecuatii-si-inecuatii-exponentiale-logaritmice-si-trigonometrice': gen_exp_log_trig_equations,
    'metode-de-numarare-si-combinatorica': gen_combinatorics,
    'probabilitati-statistica-si-matematici-financiare': gen_probability_stats_finance,
    'vectori-in-plan-si-coliniaritate': gen_vectors,
    'geometrie-analitica-in-plan': gen_analytic_geometry,
    'trigonometrie-elementara': gen_trig_elementary,
    'aplicatii-de-trigonometrie-si-produs-scalar': gen_trig_applications,
    'matrice-determinanti-si-sisteme-liniare': gen_matrices,
    'grupuri-si-legi-de-compozitie': gen_composition_laws,
    'inele-corpuri-si-polinoame': gen_polynomials,
    'limite-de-functii': gen_limits,
    'continuitate': gen_continuity,
    'derivabilitate': gen_derivatives,
    'studiul-functiilor-cu-ajutorul-derivatelor': gen_study_by_derivative,
    'primitive': gen_primitives,
    'integrala-definita': gen_definite_integrals,
    'aplicatii-ale-integralei': gen_integral_applications,
}


def invert_subiect_map() -> dict[str, str]:
    inverse = {}
    for subiect_id, chapters in MATH_SUBIECT_MAP.items():
        for chapter_id in chapters:
            inverse[chapter_id] = subiect_id
    return inverse


def patch_catalog() -> dict[str, str]:
    payload = json.loads(CATALOG_PATH.read_text(encoding='utf-8'))
    inverse = invert_subiect_map()
    for subject in payload['subjects']:
        if subject['id'] != 'matematica_m1':
            continue
        chapter_lookup = {}
        for subiect in subject['subiecte']:
            for chapter in subiect['chapters']:
                chapter_lookup[chapter['id']] = chapter
        rebuilt = []
        for subiect in subject['subiecte']:
            subiect_id = subiect['id']
            subiect['summary'] = SUBIECT_SUMMARY[subiect_id]
            new_chapters = []
            for chapter_id in MATH_SUBIECT_MAP[subiect_id]:
                chapter = chapter_lookup[chapter_id]
                new_chapters.append(chapter)
            subiect['chapters'] = new_chapters
            rebuilt.append(subiect)
        subject['subiecte'] = rebuilt
    CATALOG_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return inverse


def patch_examples_and_feed(inverse: dict[str, str]) -> None:
    examples = json.loads(CHAPTER_EXAMPLES_PATH.read_text(encoding='utf-8'))
    for entry in examples['items']:
        if entry.get('subject_id') == 'matematica_m1':
            entry['subiect_id'] = inverse.get(entry['chapter_id'], entry.get('subiect_id', ''))
    CHAPTER_EXAMPLES_PATH.write_text(json.dumps(examples, ensure_ascii=False, indent=2), encoding='utf-8')

    lines = []
    existing_titles = set()
    if FEED_PATH.exists():
        for raw in FEED_PATH.read_text(encoding='utf-8').splitlines():
            if not raw.strip():
                continue
            obj = json.loads(raw)
            if obj.get('subject_id') == 'matematica_m1':
                obj['subiect_id'] = inverse.get(obj.get('chapter_id', ''), obj.get('subiect_id', ''))
            existing_titles.add(obj.get('title', ''))
            lines.append(obj)

    notebook_entries = [
        {
            'id': 'math-uploaded-subiect-1',
            'timestamp': '2026-04-20T10:55:00+00:00',
            'source_type': 'uploaded_summary',
            'source_name': 'Subiectul 1 M1.pdf',
            'subject_id': 'matematica_m1',
            'subiect_id': 'subiectul-1',
            'chapter_id': '',
            'title': 'Fișa M1 · Subiectul I · hartă de capitole',
            'text': 'Notițele tale pentru Subiectul I grupează explicit calcule, mulțimi și submulțimi, parte întreagă și fracționară, progresii, numere complexe, ecuații raționale, logaritmice și exponențiale, inecuații, funcții, combinări, probabilități, binom, matematici financiare, vectori, geometrie analitică și trigonometrie. În aplicație, aceste capitole au fost mutate sub Subiectul I pentru a reflecta structura reală M1.',
            'keywords': ['subiectul 1', 'm1', 'mulțimi', 'progresii', 'numere complexe', 'funcții', 'ecuații', 'probabilități', 'vectori', 'trigonometrie'],
        },
        {
            'id': 'math-uploaded-subiect-2',
            'timestamp': '2026-04-20T10:56:00+00:00',
            'source_type': 'uploaded_summary',
            'source_name': 'Subiectul 2 M1.pdf',
            'subject_id': 'matematica_m1',
            'subiect_id': 'subiectul-2',
            'chapter_id': '',
            'title': 'Fișa M1 · Subiectul II · hartă de capitole',
            'text': 'Notițele tale pentru Subiectul II pun accent pe noțiuni generale de matrice, transpusa, adunarea și scăderea, înmulțirea cu scalar, urma, produsul a două matrice, determinanți, aplicații în geometrie, inversa, sisteme, Hamilton-Cayley, rang și tipuri de sisteme. Pentru exercițiul 2 apar legi de compoziție, comutativitate, asociativitate, polinoame, împărțire, divizibilitate, relațiile lui Viète, element neutru, element simetrizabil, monoid și grup.',
            'keywords': ['subiectul 2', 'm1', 'matrice', 'determinanți', 'inversă', 'sisteme', 'rang', 'hamilton-cayley', 'legi de compoziție', 'polinoame'],
        },
        {
            'id': 'math-uploaded-subiect-3',
            'timestamp': '2026-04-20T10:57:00+00:00',
            'source_type': 'uploaded_summary',
            'source_name': 'Subiectul 3 M1.pdf',
            'subject_id': 'matematica_m1',
            'subiect_id': 'subiectul-3',
            'chapter_id': '',
            'title': 'Fișa M1 · Subiectul III · hartă de capitole',
            'text': 'Notițele tale pentru Subiectul III merg pe limite de funcții, limite remarcabile, cazuri de nedeterminare, limite laterale, continuitate, asimptote, derivate, regula lui l’Hospital, monotonie, puncte de extrem, șirul lui Rolle, ecuația tangentei, derivate de ordin superior, puncte de inflexiune, primitive, integrale definite, integrări prin părți și schimbare de variabilă, plus calcul de arii și volume.',
            'keywords': ['subiectul 3', 'm1', 'limite', 'continuitate', 'asimptote', 'derivate', 'Rolle', 'tangentă', 'primitive', 'integrale'],
        },
    ]
    for entry in notebook_entries:
        if entry['title'] not in existing_titles:
            lines.append(entry)
    with FEED_PATH.open('w', encoding='utf-8') as fh:
        for obj in lines:
            fh.write(json.dumps(obj, ensure_ascii=False) + '\n')


def rebuild_exam_bank(inverse: dict[str, str]) -> None:
    payload = json.loads(EXAM_BANK_PATH.read_text(encoding='utf-8'))
    non_math = [item for item in payload['items'] if item.get('subject_id') != 'matematica_m1']
    math_items = []
    for chapter_id, generator in GENERATORS.items():
        raws = generator()
        math_items.extend(finalize_chapter(chapter_id, inverse[chapter_id], raws))
    payload['items'] = non_math + math_items
    EXAM_BANK_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Generated math items:', len(math_items))


def main() -> None:
    inverse = patch_catalog()
    patch_examples_and_feed(inverse)
    rebuild_exam_bank(inverse)
    print('Catalog, examples, feed and exam bank updated.')


if __name__ == '__main__':
    main()
