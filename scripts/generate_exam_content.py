from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / 'data' / 'catalog.json').read_text(encoding='utf-8'))

YEARS = list(range(2018, 2027))
YEAR_POINTER = {'value': 0}

def next_year() -> int:
    year = YEARS[YEAR_POINTER['value'] % len(YEARS)]
    YEAR_POINTER['value'] += 1
    return year


def make_item(subject_id: str, subiect_id: str, chapter_id: str, prompt: str, options: list[str], correct_index: int,
              explanation: str, hint: str, difficulty: str = 'intermediate', source_label: str | None = None,
              source_type: str = 'adaptat după modele / simulări oficiale', worked_steps: list[str] | None = None,
              tags: list[str] | None = None) -> dict:
    year = next_year()
    return {
        'id': f'{subject_id}:{chapter_id}:{year}:{difficulty}:{YEAR_POINTER["value"]}',
        'subject_id': subject_id,
        'subiect_id': subiect_id,
        'chapter_id': chapter_id,
        'year': year,
        'source_type': source_type,
        'source_label': source_label or f'An de referință {year} · stil ministerial',
        'difficulty': difficulty,
        'prompt': prompt,
        'options': options,
        'correct_index': correct_index,
        'explanation': explanation,
        'hint': hint,
        'worked_steps': worked_steps or [],
        'tags': tags or [],
    }


def make_example(subject_id: str, subiect_id: str, chapter_id: str, micro_recap: str, attention_hook: str,
                 title: str, statement: str, steps: list[str], quick_checks: list[str],
                 memory_hook: str, sprint_plan: list[str]) -> dict:
    return {
        'subject_id': subject_id,
        'subiect_id': subiect_id,
        'chapter_id': chapter_id,
        'micro_recap': micro_recap,
        'attention_hook': attention_hook,
        'concrete_example': {
            'title': title,
            'statement': statement,
            'steps': steps,
        },
        'quick_checks': quick_checks,
        'memory_hook': memory_hook,
        'sprint_plan': sprint_plan,
    }


# --- Templates for mathematics ---

def math_example_and_items(chapter_id: str, title: str, subiect_id: str) -> tuple[dict, list[dict]]:
    sid = 'matematica_m1'
    if chapter_id == 'multimi-intervale-si-logica-matematica':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Transformi rapid informația din enunț în intervale și apoi lucrezi doar cu intersecții, reuniuni și condiții de apartenență.',
            'Primul reflex: notezi mulțimile explicit și verifici capetele intervalelor.',
            'Exemplu lucrat · intersecție de intervale',
            'Dacă A = (-2, 5] și B = [1, 7), determină A ∩ B și verifică dacă 5 aparține intersecției.',
            [
                'Intersecția păstrează doar valorile comune celor două intervale.',
                'Capătul din stânga devine 1, deoarece de acolo încep valorile comune.',
                'Capătul din dreapta rămâne 5 și este inclus, deci A ∩ B = [1, 5].',
                'Numărul 5 aparține intersecției pentru că 5 este admis în ambele intervale.',
            ],
            ['Poți scrie intersecția fără să desenezi axa?', 'Știi să verifici separat capetele?'],
            'A∩B = „ce rămâne în ambele”.',
            ['scrie mulțimile', 'desenează axa', 'verifică capetele'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Fie A = (-3, 4] și B = [0, 6). Care este intersecția A ∩ B?',
                      ['(-3, 6)', '[0, 4]', '(0, 4]', '[0, 6)'], 1,
                      'Valorile comune încep de la 0, inclus, și se opresc la 4, inclus. Rezultă [0, 4].',
                      'Desenează cele două intervale pe aceeași axă și păstrează doar porțiunea comună.',
                      'beginner', worked_steps=['marchezi A', 'marchezi B', 'iei zona comună']),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă x ∈ (-∞, 2] ∩ [−1, 5), care afirmație este sigur adevărată?',
                      ['x < -1', '-1 ≤ x ≤ 2', '2 < x < 5', 'x ≥ 5'], 1,
                      'Intersecția celor două intervale este [-1, 2], deci x este între -1 și 2, cu capetele incluse.',
                      'Calculează întâi intersecția, apoi interpretează enunțul.',
                      'intermediate'),
        ]
        return example, items
    if chapter_id == 'functii-si-reprezentari-grafice':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La bac se verifică frecvent dacă știi să citești domeniul, imaginea și monotonia direct dintr-un tabel sau grafic.',
            'Nu porni cu formule: citește mai întâi datele vizuale sau tabelare.',
            'Exemplu lucrat · citirea unei funcții din tabel',
            'Pentru x ∈ {−1, 0, 1, 2}, valorile sunt f(x) = {3, 1, 1, 3}. Ce observi despre minim și simetrie?',
            [
                'Valoarea minimă este 1 și apare pentru x = 0 și x = 1.',
                'Valorile 3 și 3 la capete sugerează o distribuție simetrică în jurul mijlocului intervalului discret.',
                'La astfel de itemi, întrebarea nu cere neapărat formula, ci proprietățile citite corect.',
            ],
            ['Poți identifica rapid punctele de minim?', 'Știi să compari valori fără a căuta formula?'],
            'Graficul se citește înainte să se calculeze.',
            ['citești domeniul', 'compari valorile', 'formulezi proprietatea'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Funcția f are valorile: f(−2)=4, f(−1)=1, f(0)=0, f(1)=1. Care afirmație este adevărată?',
                      ['Valoarea minimă este 1', '0 nu aparține imaginii funcției', 'f(0) este minimul valorilor date', 'Funcția are doar valori negative'], 2,
                      'Din tabel, cea mai mică valoare este 0, obținută pentru x = 0.',
                      'Compară direct valorile din tabel.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă graficul unei funcții taie axa Oy în punctul (0, −3), ce concluzie este corectă?',
                      ['f(−3)=0', 'f(0)=−3', 'f(3)=0', 'graficul nu are intersecție cu Oy'], 1,
                      'Intersecția cu Oy are întotdeauna abscisa 0, deci ordinata punctului este f(0).',
                      'Axa Oy înseamnă x = 0.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'functia-de-gradul-i-si-functia-de-gradul-al-ii-lea':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La funcțiile de gradul I și II apare des legătura dintre ecuație, semn și reprezentarea grafică.',
            'Pentru inecuații de gradul II, rădăcinile și semnul lui a îți spun tot traseul.',
            'Exemplu lucrat · inecuație de gradul al II-lea',
            'Rezolvă x² − 5x + 6 ≤ 0.',
            [
                'Factorizezi: x² − 5x + 6 = (x−2)(x−3).',
                'Rădăcinile sunt 2 și 3.',
                'Coeficientul lui x² este pozitiv, deci parabola este sub sau pe axă între rădăcini.',
                'Soluția este [2, 3].',
            ],
            ['Știi unde este soluția când a > 0?', 'Poți lega semnul de poziția parabolei?'],
            'Parabola „pozitivă” este negativă doar între rădăcini.',
            ['factorizezi', 'marchezi rădăcinile', 'alegi intervalul de semn'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Mulțimea soluțiilor inecuației x² − 4x + 3 ≤ 0 este:',
                      ['(−∞, 1] ∪ [3, ∞)', '[1, 3]', '(1, 3)', '[−1, 3]'], 1,
                      'x² − 4x + 3 = (x−1)(x−3), iar pentru a>0 soluțiile sunt între rădăcini, inclusiv capetele.',
                      'Factorizează și fă semnul pe intervale.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru funcția f(x)=2x−6, intersecția cu axa Ox se obține pentru x =',
                      ['−3', '0', '3', '6'], 2,
                      'Pe axa Ox avem f(x)=0. Rezolvând 2x−6=0 obținem x=3.',
                      'Intersecția cu Ox înseamnă y=0.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'siruri-aritmetice-si-geometrice':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Pentru șiruri identifici întâi regula: diferență constantă sau raport constant.',
            'La bac, primul pas este să verifici dacă ai progresie aritmetică sau geometrică.',
            'Exemplu lucrat · termen general',
            'Într-un șir aritmetic cu a1 = 4 și rația r = 3, calculează a5.',
            [
                'Formula este an = a1 + (n−1)·r.',
                'a5 = 4 + 4·3 = 16.',
                'La verificare, poți genera rapid termenii: 4, 7, 10, 13, 16.',
            ],
            ['Știi formula pentru an?', 'Poți diferenția între rație și raport?'],
            'Aritmetic = aduni; geometric = înmulțești.',
            ['identifici tipul', 'scrii formula', 'verifici pe 2 termeni'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Într-un șir aritmetic cu a1 = 2 și r = 5, termenul a4 este:',
                      ['12', '15', '17', '22'], 2,
                      'a4 = 2 + 3·5 = 17.',
                      'Folosește an = a1 + (n−1)r.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Într-un șir geometric cu a1 = 3 și q = 2, termenul a5 este:',
                      ['24', '36', '48', '96'], 2,
                      'a5 = 3·2^4 = 48.',
                      'Pentru șir geometric folosești an = a1·q^(n−1).', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'vectori-in-plan-si-coliniaritate':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Verifici coliniaritatea comparând coordonatele sau scriind un vector ca multiplu al altuia.',
            'Dacă un vector este multiplu scalar al celuilalt, punctele sau vectorii sunt coliniari.',
            'Exemplu lucrat · coliniaritate',
            'Sunt coliniari vectorii u(2,4) și v(1,2)?',
            [
                'Observi că u = 2·v.',
                'Fiind multipli scalar, au aceeași direcție.',
                'Rezultă că vectorii sunt coliniari.',
            ],
            ['Poți găsi același raport pe coordonate?', 'Știi diferența dintre coliniari și perpendiculari?'],
            'Coliniar = unul este k ori celălalt.',
            ['scrii coordonatele', 'compari rapoartele', 'formulezi concluzia'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Vectorii u(3,6) și v(1,2) sunt:',
                      ['perpendiculari', 'coliniari', 'egali', 'opuşi obligatoriu'], 1,
                      'u = 3·v, deci sunt coliniari.',
                      'Verifică dacă există un k cu u = k·v.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă A(1,1), B(3,3), C(5,5), atunci punctele A, B, C sunt:',
                      ['coliniare', 'vârfurile unui triunghi echilateral', 'necoliniare', 'simetrice față de Oy'], 0,
                      'Toate au coordonate de forma (t,t), deci aparțin aceleiași drepte y=x.',
                      'Compară pantele sau recunoaște dreapta comună.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'trigonometrie-elementara':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La trigonometrie, valorile speciale și identitatea fundamentală apar foarte des în subiectele scurte.',
            'Dacă unghiul este „special”, încearcă imediat să-l legi de tabelul standard.',
            'Exemplu lucrat · valori speciale',
            'Calculează sin(π/6) și cos(π/3).',
            [
                'Din tabelul standard, sin(π/6)=1/2.',
                'Tot din tabel, cos(π/3)=1/2.',
                'La itemii rapizi, viteza vine din memorarea valorilor standard.',
            ],
            ['Știi perechea π/6 ↔ 1/2?', 'Știi că sin și cos se citesc diferit pe cerc?'],
            'π/6, π/4, π/3 sunt unghiurile-cheie.',
            ['recunoști unghiul', 'citești valoarea', 'verifici intervalul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Valoarea lui sin(π/6) este:',
                      ['0', '1/2', '√2/2', '√3/2'], 1,
                      'Din valorile trigonometrice speciale, sin(π/6)=1/2.',
                      'Gândește-te la triunghiul 30°-60°-90°.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă sin x = √3/2 și x este unghi ascuțit, atunci x poate fi:',
                      ['π/6', 'π/4', 'π/3', 'π/2'], 2,
                      'Pentru unghi ascuțit, sin x = √3/2 corespunde lui π/3.',
                      'Asociază valorile speciale cu unghiurile.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'aplicatii-de-trigonometrie-si-produs-scalar':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Produsul scalar leagă imediat unghiul dintre vectori de coordonate.',
            'Când produsul scalar este 0, suspectezi perpendicularitate.',
            'Exemplu lucrat · perpendicularitate',
            'Pentru u(1,2) și v(2,−1), decide dacă sunt perpendiculari.',
            [
                'Calculezi u·v = 1·2 + 2·(−1) = 0.',
                'Produsul scalar nul înseamnă vectori perpendiculari.',
                'Așadar, vectorii formează un unghi de 90°.',
            ],
            ['Știi formula u·v?', 'Poți recunoaște imediat cazul 0?'],
            'u·v = 0 înseamnă unghi drept.',
            ['calculezi produsul scalar', 'interpretezi rezultatul', 'formulezi concluzia'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Pentru u(1,2) și v(2,−1), produsul scalar este:',
                      ['−1', '0', '1', '2'], 1,
                      '1·2 + 2·(−1)=0.',
                      'Aplică direct formula coordonată cu coordonată.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă u·v = 0 pentru doi vectori nenuli, atunci vectorii sunt:',
                      ['coliniari', 'perpendiculari', 'egali', 'paraleli obligatoriu'], 1,
                      'Produsul scalar nul caracterizează perpendicularitatea vectorilor nenuli.',
                      'Leagă definiția de unghiul dintre vectori.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'puteri-radicali-si-logaritmi':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La puteri, radicali și logaritmi, simplificarea corectă și condițiile de existență fac diferența.',
            'Nu sari peste factorul comun din radical: rescrierea bună scurtează tot exercițiul.',
            'Exemplu lucrat · radicali',
            'Simplifică √50 − √8.',
            [
                '√50 = √(25·2) = 5√2.',
                '√8 = √(4·2) = 2√2.',
                'Diferența devine 5√2 − 2√2 = 3√2.',
            ],
            ['Scoți factorul pătrat perfect din radical?', 'Verifici semnul înainte de a combina termenii?'],
            'Caută întâi pătratul perfect ascuns.',
            ['descompui numerele', 'scoți radicalii', 'reduci termenii asemenea'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Valoarea expresiei √18 / √2 este:',
                      ['3', '6', '9', '√9/2'], 0,
                      '√18/√2 = √9 = 3.',
                      'Folosește regula √a/√b = √(a/b), când a și b sunt pozitive.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă log2(x) = 3, atunci x este:',
                      ['6', '8', '9', '16'], 1,
                      'Din definiție, x = 2^3 = 8.',
                      'Transformă imediat logaritmul în formă exponențială.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'numere-complexe':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La numere complexe, operațiile pe forma a+bi trebuie făcute ordonat, cu i² = −1.',
            'După înmulțire, caută automat termenul i² pentru a-l înlocui cu −1.',
            'Exemplu lucrat · înmulțire',
            'Calculează (1+i)(2−i).',
            [
                'Dezvolți: 2 − i + 2i − i².',
                'Înlocuiești i² cu −1, deci −i² = +1.',
                'Rezultatul este 3 + i.',
            ],
            ['Păstrezi separat partea reală și cea imaginară?', 'Înlocuiești corect i²?'],
            'i² = −1 este comutatorul exercițiului.',
            ['dezvolți', 'înlocuiești i²', 'grupezi termenii'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Rezultatul expresiei (2+i)+(1−3i) este:',
                      ['3−2i', '3+2i', '1−2i', '2−3i'], 0,
                      'Aduni separat părțile reale și imaginare: 2+1=3, iar 1i−3i=−2i.',
                      'Grupează real cu real și imaginar cu imaginar.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru z = 3−4i, modulul |z| este:',
                      ['1', '5', '7', '25'], 1,
                      '|z| = √(3²+4²)=5.',
                      'Aplică teorema lui Pitagora pe coordonatele (a,b).', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'functia-exponentiala-si-functia-logaritmica':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La funcțiile exponențiale și logaritmice, sensul de variație depinde de bază.',
            'Dacă baza este >1, funcția exponențială crește; dacă este între 0 și 1, descrește.',
            'Exemplu lucrat · citirea monotonicității',
            'Pentru f(x)=2^x, decide dacă funcția este crescătoare sau descrescătoare.',
            [
                'Baza 2 este mai mare decât 1.',
                'O funcție exponențială cu baza a>1 este crescătoare pe R.',
                'Așadar, f este crescătoare.',
            ],
            ['Știi regula pentru baza >1?', 'Poți aplica aceeași idee și la logaritm?'],
            'Baza dictează monotonia.',
            ['verifici baza', 'alegi regula', 'formulezi proprietatea'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Funcția f(x)=3^x este pe R:',
                      ['constantă', 'crescătoare', 'descrescătoare', 'periodică'], 1,
                      'Pentru baza 3>1, funcția exponențială este crescătoare.',
                      'Identifică baza și compar-o cu 1.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Domeniul funcției g(x)=log2(x) este:',
                      ['R', 'R\\{0\\}', '(0,∞)', '[0,∞)'], 2,
                      'Logaritmul este definit doar pentru argument strict pozitiv.',
                      'În logaritm, argumentul trebuie să fie > 0.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'ecuatii-si-inecuatii-exponentiale-logaritmice-si-trigonometrice':
        example = make_example(
            sid, subiect_id, chapter_id,
            'În ecuații și inecuații, transformarea la aceeași bază și verificarea condițiilor de existență sunt obligatorii.',
            'Pentru inecuații logaritmice, nu uita: argumentul trebuie mai întâi să existe.',
            'Exemplu lucrat · inecuație exponențială',
            'Rezolvă 2^x > 8.',
            [
                'Scrii 8 = 2^3.',
                'Obții 2^x > 2^3.',
                'Cum baza 2>1, compari exponenții: x > 3.',
            ],
            ['Ai adus termenii la aceeași bază?', 'Ai verificat dacă sensul inecuației se păstrează?'],
            'Aceeași bază, apoi compari exponenții.',
            ['aduci la aceeași bază', 'compari exponenții', 'scrii soluția'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Soluția ecuației 3^x = 27 este:',
                      ['2', '3', '4', '9'], 1,
                      '27 = 3^3, deci x = 3.',
                      'Rescrie membrul drept ca putere cu aceeași bază.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Soluția inecuației 2^x > 16 este:',
                      ['x > 2', 'x > 3', 'x > 4', 'x ≥ 4'], 2,
                      '16 = 2^4, iar pentru baza 2>1 rezultă x > 4.',
                      'Atenție la diferența dintre > și ≥.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'metode-de-numarare-si-combinatorica':
        example = make_example(
            sid, subiect_id, chapter_id,
            'În combinatorică alegi între permutări, aranjamente și combinații după ce observi dacă ordinea contează.',
            'Întrebarea-cheie: schimbarea ordinii produce alt rezultat?',
            'Exemplu lucrat · combinații',
            'Din 5 elevi alegem 2 reprezentanți. Câte alegeri sunt?',
            [
                'Ordinea nu contează, deci folosim combinații.',
                'C(5,2)=10.',
                'Dacă ar conta cine este președinte și cine vicepreședinte, problema s-ar schimba.',
            ],
            ['Te-ai întrebat dacă ordinea contează?', 'Poți deosebi combinația de aranjament?'],
            'Alegere fără ordine = combinație.',
            ['decizi dacă ordinea contează', 'alegi formula', 'calculezi'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Numărul de moduri în care alegi 2 elevi din 4 este:',
                      ['4', '6', '8', '12'], 1,
                      'C(4,2)=6.',
                      'Nu contează ordinea, deci este combinație.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Numărul permutărilor mulțimii {1,2,3} este:',
                      ['3', '6', '9', '27'], 1,
                      'P3 = 3! = 6.',
                      'Pentru toate așezările distincte ale n elemente folosești n!.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'probabilitati-statistica-si-matematici-financiare':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La probabilități și statistică, pornești de la definiția clasică și de la media aritmetică.',
            'Numără întâi cazurile favorabile și totale, abia apoi simplifică fracția.',
            'Exemplu lucrat · probabilitate clasică',
            'Se aruncă un zar. Probabilitatea de a obține un număr par este?',
            [
                'Cazuri totale: 6.',
                'Cazuri favorabile: 2, 4, 6, deci 3.',
                'Probabilitatea este 3/6 = 1/2.',
            ],
            ['Ai numărat corect spațiul de rezultate?', 'Ai simplificat fracția?'],
            'Probabilitatea = favorabile / totale.',
            ['identifici cazurile', 'scrii raportul', 'simplifici'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Media aritmetică a numerelor 2, 4, 6 este:',
                      ['3', '4', '5', '6'], 1,
                      '(2+4+6)/3 = 4.',
                      'Aduni toate valorile și împarți la numărul lor.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'La aruncarea unui zar echilibrat, probabilitatea de a obține un număr mai mare decât 4 este:',
                      ['1/6', '1/3', '1/2', '2/3'], 1,
                      'Numerele mai mari decât 4 sunt 5 și 6, deci 2 cazuri din 6: 2/6 = 1/3.',
                      'Scrie explicit cazurile favorabile.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'geometrie-analitica-in-plan':
        example = make_example(
            sid, subiect_id, chapter_id,
            'În geometria analitică, ecuația dreptei și coordonatele punctelor se citesc prin formule fixe.',
            'Dacă ai două puncte, poți obține imediat panta și apoi ecuația dreptei.',
            'Exemplu lucrat · mijlocul segmentului',
            'Pentru A(1,3) și B(5,7), găsește coordonatele mijlocului M.',
            [
                'Formula este M((x1+x2)/2, (y1+y2)/2).',
                'M((1+5)/2, (3+7)/2) = (3,5).',
                'La verificare, vezi dacă M este „la jumătatea distanței” pe ambele coordonate.',
            ],
            ['Știi formula mijlocului?', 'Poți interpreta grafic rezultatul?'],
            'Mijloc = media coordonatelor.',
            ['scrii formula', 'înlocuiești coordonatele', 'verifici'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Mijlocul segmentului cu capetele A(0,2) și B(4,6) este:',
                      ['(2,4)', '(4,2)', '(1,2)', '(0,4)'], 0,
                      'Media coordonatelor dă M((0+4)/2,(2+6)/2)=(2,4).',
                      'Fă media separat pe x și pe y.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Ecuația unei drepte paralele cu Ox are forma:',
                      ['x = c', 'y = c', 'x + y = c', 'xy = c'], 1,
                      'O dreaptă paralelă cu Ox are ordinata constantă, deci y=c.',
                      'Leagă direcția dreptei de coordonata care rămâne constantă.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'matrice-determinanti-si-sisteme-liniare':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La matrice și determinanți, ordinea calculelor și semnul sunt esențiale.',
            'Pentru determinantul de ordin 2, regula este simplă: produsul diagonalelor principale minus produsul diagonalelor secundare.',
            'Exemplu lucrat · determinant de ordin 2',
            'Calculează determinantul matricei [[1,2],[3,4]].',
            [
                'det = 1·4 − 2·3.',
                'Rezultă 4 − 6 = −2.',
                'Un determinant nenul indică, de obicei, sistem compatibil determinat pentru matricea coeficienților.',
            ],
            ['Ai păstrat ordinea produselor?', 'Ai verificat semnul final?'],
            'La 2x2: ad − bc.',
            ['scrii formula', 'înlocuiești', 'calculezi corect semnul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Determinantul matricei [[2,1],[5,3]] este:',
                      ['1', '−1', '6', '11'], 0,
                      '2·3 − 1·5 = 1.',
                      'Aplică formula ad−bc.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Sistemul x+y=3, x−y=1 are soluția:',
                      ['(1,2)', '(2,1)', '(3,0)', '(0,3)'], 1,
                      'Adunând ecuațiile obții 2x=4, deci x=2 și apoi y=1.',
                      'Elimină o necunoscută prin adunare sau scădere.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'limite-de-functii':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La limite, simplificarea algebrică înainte de înlocuire evită formele nedeterminate.',
            'Dacă obții 0/0, nu te bloca: factorizezi sau raționalizezi.',
            'Exemplu lucrat · formă nedeterminată',
            'Calculează lim x→2 (x²−4)/(x−2).',
            [
                'Factorizezi numărătorul: x²−4=(x−2)(x+2).',
                'Simplifici factorul comun x−2.',
                'Rămâne lim x→2 (x+2)=4.',
            ],
            ['Recunoști tipul 0/0?', 'Știi ce metodă de simplificare se potrivește?'],
            '0/0 înseamnă „mai lucrează puțin”, nu „nu există”.',
            ['înlocuiești', 'identifici forma', 'simplifici și recalculezi'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Valoarea limitei lim x→1 (x²−1)/(x−1) este:',
                      ['0', '1', '2', 'nu există'], 2,
                      'x²−1=(x−1)(x+1), iar după simplificare rămâne x+1, deci limita este 2.',
                      'Factorizează diferența de pătrate.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă lim x→a f(x)=L, atunci expresia descrie:',
                      ['valoarea exactă a lui f(a) obligatoriu', 'comportamentul lui f(x) lângă a', 'doar semnul lui f', 'derivata lui f în a'], 1,
                      'Limita descrie comportamentul funcției în apropierea lui a, nu neapărat valoarea exactă în punct.',
                      'Separă ideea de limită de valoarea funcției în punct.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'continuitate':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Continuitatea într-un punct cere trei condiții: existența lui f(a), existența limitei și egalitatea dintre ele.',
            'Ține minte triada: funcția există, limita există, sunt egale.',
            'Exemplu lucrat · condiție de continuitate',
            'Pentru f(x)=x+1 dacă x<2 și f(2)=3, verifică continuitatea în x=2.',
            [
                'Limita când x→2 din expresia x+1 este 3.',
                'Valoarea funcției este f(2)=3.',
                'Cum limita și valoarea coincid, funcția este continuă în 2.',
            ],
            ['Ai verificat și valoarea funcției, nu doar limita?', 'Ai analizat din ambele părți dacă e nevoie?'],
            'Continuitate = „lipit” fără săritură.',
            ['calculezi limita', 'găsești f(a)', 'compari'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'O funcție este continuă în a dacă:',
                      ['limita există și este 0', 'f(a)=0', 'lim x→a f(x)=f(a)', 'are derivată în a'], 2,
                      'Definiția standard este egalitatea dintre limită și valoarea funcției în punct.',
                      'Reține formula-cheie a continuității.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru f(x)=x², funcția este pe R:',
                      ['discontinuă', 'continuă', 'continuă doar în 0', 'nedefinită'], 1,
                      'Polinoamele sunt continue pe tot domeniul lor, deci pe R.',
                      'Folosește proprietatea generală a polinoamelor.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'derivabilitate':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Derivata măsoară viteza de variație a funcției; la bac apar frecvent reguli de derivare de bază.',
            'Dacă vezi puteri simple, derivarea se face rapid cu regula lui x^n.',
            'Exemplu lucrat · derivată',
            'Derivează funcția f(x)=x³.',
            [
                'Aplici regula: (x^n)′ = n·x^(n−1).',
                'Rezultă f′(x)=3x².',
                'La final, verifică dacă nu ai uitat coeficienții constanți.',
            ],
            ['Știi regula pentru x^n?', 'Derivezi și constantele corect?'],
            'Scazi exponentul cu 1 și îl cobori în față.',
            ['alegi regula', 'derivezi', 'verifici exponentul final'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Derivata funcției f(x)=x² este:',
                      ['x', '2x', 'x²', '2'], 1,
                      'Aplicând regula puterii obții 2x.',
                      'Folosește (x^n)′ = n·x^(n−1).', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Derivata funcției g(x)=3x² este:',
                      ['3x', '6x', '6x²', '9x'], 1,
                      'Constanta 3 rămâne în față, iar derivata lui x² este 2x, deci 6x.',
                      'Nu uita coeficientul din față.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'studiul-functiilor-cu-ajutorul-derivatelor':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Semnul derivatei îți spune monotonia; punctele unde derivata se anulează sunt candidați la extreme.',
            'La studiul funcției, schema fixă te salvează: domeniu, derivată, puncte critice, semn, tabel de variație.',
            'Exemplu lucrat · monotonie',
            'Pentru f′(x)=2x−4, unde poate avea f un punct critic?',
            [
                'Punctele critice apar unde derivata este 0 sau nu există.',
                'Rezolvi 2x−4=0 și obții x=2.',
                'Apoi studiezi semnul derivatei în jurul lui 2 pentru monotonie.',
            ],
            ['Știi ce este un punct critic?', 'Ai făcut legătura între semnul derivatei și variație?'],
            'Derivata pozitivă urcă, derivata negativă coboară.',
            ['calculezi derivata', 'afli punctele critice', 'faci tabelul de semn'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Dacă f′(x)>0 pe un interval, atunci f este pe acel interval:',
                      ['constantă', 'crescătoare', 'descrescătoare', 'periodică'], 1,
                      'Derivata pozitivă indică creștere.',
                      'Leagă semnul derivatei de variația funcției.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru f′(x)=x−1, punctul critic este la x =',
                      ['−1', '0', '1', '2'], 2,
                      'Punctul critic apare când derivata este 0, deci x−1=0 ⇒ x=1.',
                      'Rezolvă ecuația f′(x)=0.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'primitive':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La primitive, cauți o funcție care, derivată, dă expresia inițială.',
            'Gândește „inversul derivării”.',
            'Exemplu lucrat · primitivă elementară',
            'Găsește o primitivă pentru f(x)=2x.',
            [
                'Știi că derivata lui x² este 2x.',
                'Deci o primitivă este F(x)=x²+C.',
                'Constanta C trebuie mereu menționată.',
            ],
            ['Ai adăugat constanta de integrare?', 'Ai verificat prin derivare?'],
            'Primitiva este derivarea „în sens invers”.',
            ['recunoști modelul', 'scrii primitiva', 'adaugi +C'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'O primitivă a funcției f(x)=3 este:',
                      ['3x + C', 'x³ + C', '0', '3 + C'], 0,
                      'Derivata lui 3x este 3.',
                      'Pentru o constantă k, o primitivă este kx + C.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'O primitivă a funcției f(x)=x este:',
                      ['x² + C', 'x²/2 + C', '1/x + C', 'ln x + C'], 1,
                      'Derivata lui x²/2 este x.',
                      'Verifică prin derivare răspunsul ales.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'integrala-definita':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La integrala definită, după ce găsești o primitivă aplici formula Newton-Leibniz.',
            'Ordinea este fixă: primitivă, capăt superior minus capăt inferior.',
            'Exemplu lucrat · calcul de integrală',
            'Calculează ∫(de la 0 la 1) 2x dx.',
            [
                'O primitivă pentru 2x este x².',
                'Aplici formula: x²|₀¹ = 1² − 0².',
                'Rezultatul este 1.',
            ],
            ['Ai găsit corect primitiva?', 'Ai evaluat în ordinea corectă?'],
            'Sus minus jos, niciodată invers.',
            ['găsești primitiva', 'evaluezi la capete', 'scazi corect'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Valoarea integralei ∫(de la 0 la 2) 1 dx este:',
                      ['1', '2', '3', '4'], 1,
                      'Integrala funcției constante 1 pe [0,2] este 2.',
                      'Poți interpreta și ca aria unui dreptunghi de bază 2 și înălțime 1.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă F este o primitivă a lui f, atunci ∫(de la a la b) f(x)dx este:',
                      ['F(a)+F(b)', 'F(a)−F(b)', 'F(b)−F(a)', 'f(b)−f(a)'], 2,
                      'Formula Newton-Leibniz dă F(b)−F(a).',
                      'Memorează ordinea corectă a capetelor.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'aplicatii-ale-integralei':
        example = make_example(
            sid, subiect_id, chapter_id,
            'Aplicația clasică la bac este aria domeniului delimitat de grafic și axă.',
            'Înainte de integrală, verifică dacă funcția este deasupra sau sub axa Ox.',
            'Exemplu lucrat · aria sub grafic',
            'Determină aria de sub graficul lui f(x)=x pe intervalul [0,1].',
            [
                'Pe [0,1], funcția este pozitivă.',
                'Aria este ∫(de la 0 la 1) x dx = x²/2|₀¹ = 1/2.',
                'Cum funcția este deasupra axei, aria coincide cu valoarea integralei.',
            ],
            ['Ai verificat semnul funcției pe interval?', 'Știi când trebuie modul?'],
            'Arie = integrală doar dacă funcția nu schimbă semnul.',
            ['verifici semnul', 'calculezi integrala', 'interpretezi aria'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Aria de sub graficul lui f(x)=1 pe [0,3] este:',
                      ['1', '2', '3', '4'], 2,
                      'Este aria unui dreptunghi cu baza 3 și înălțimea 1, deci 3.',
                      'La funcția constantă, gândește geometric.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru o funcție pozitivă pe [a,b], aria sub grafic este:',
                      ['−∫a^b f(x)dx', '∫a^b f(x)dx', 'doar f(b)−f(a)', 'nu se poate calcula'], 1,
                      'Dacă funcția rămâne pozitivă, aria coincide cu valoarea integralei definite.',
                      'Leagă semnul funcției de interpretarea geometrică.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'grupuri-si-legi-de-compozitie':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La legi de compoziție verifici operația, elementul neutru și inversele.',
            'În multe exerciții, elementul neutru se găsește rezolvând a∘e=a.',
            'Exemplu lucrat · element neutru',
            'Pe R, fie a∘b = a + b + 1. Găsește elementul neutru e.',
            [
                'Impunem a∘e = a.',
                'Rezultă a + e + 1 = a.',
                'Deci e = −1.',
            ],
            ['Ai scris condiția de neutru la stânga și la dreapta?', 'Poți verifica rezultatul?'],
            'Neutrul păstrează elementul „neschimbat”.',
            ['scrii condiția', 'rezolvi ecuația', 'verifici'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Pentru legea a∘b = a+b pe R, elementul neutru este:',
                      ['−1', '0', '1', 'nu există'], 1,
                      'La adunarea obișnuită, 0 păstrează orice număr neschimbat.',
                      'Caută e astfel încât a∘e=a.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă operația este a∘b=a+b+1, elementul neutru este:',
                      ['−1', '0', '1', '2'], 0,
                      'Din a+e+1=a obții e=−1.',
                      'Impunerea condiției de neutru rezolvă exercițiul.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'inele-corpuri-si-polinoame':
        example = make_example(
            sid, subiect_id, chapter_id,
            'La polinoame apar des teorema împărțirii cu rest și schema lui Horner.',
            'Dacă ți se cere restul la împărțirea lui P(x) la x−a, gândește instant P(a).',
            'Exemplu lucrat · restul împărțirii',
            'Pentru P(x)=x²−1, află restul împărțirii la x−1.',
            [
                'Prin teorema restului, restul este P(1).',
                'P(1)=1−1=0.',
                'Deci x−1 divide polinomul.',
            ],
            ['Ai recunoscut forma x−a?', 'Știi să calculezi P(a) rapid?'],
            'Rest la x−a → calculezi P(a).',
            ['identifici a', 'calculezi P(a)', 'interpretezi rezultatul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Restul împărțirii polinomului P(x)=x²+2x+3 la x−1 este:',
                      ['3', '4', '6', '0'], 2,
                      'Restul este P(1)=1+2+3=6.',
                      'Aplică teorema restului.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă P(2)=0, atunci x−2 este pentru P(x):',
                      ['factor', 'coeficient', 'grad', 'rădăcină dublă obligatoriu'], 0,
                      'Prin teorema factorului, dacă P(2)=0 atunci x−2 este factor al polinomului.',
                      'Leagă valoarea nulă de existența factorului.', 'intermediate'),
        ]
        return example, items
    raise KeyError(f'No math template for {chapter_id}')


# --- Templates for informatics ---

def info_example_and_items(chapter_id: str, title: str, subiect_id: str) -> tuple[dict, list[dict]]:
    sid = 'informatica_mate_info'
    if chapter_id == 'algoritmi-si-reprezentare-in-pseudocod':
        example = make_example(sid, subiect_id, chapter_id,
            'Primul pas la info este să înțelegi clar inputul, outputul și pașii dintre ele.',
            'Nu sări direct în cod: în 2026 viteza vine din schemă clară, nu din improvizație.',
            'Exemplu lucrat · pseudocod minim',
            'Construiește pașii pentru afișarea sumei a două numere citite de la tastatură.',
            ['citești a și b', 'calculezi s ← a+b', 'afișezi s'],
            ['Știi diferența dintre citire, procesare și afișare?', 'Poți rescrie aceiași pași în pseudocod?'],
            'Input → procesare → output.',
            ['notezi datele de intrare', 'descrii calculul', 'verifici rezultatul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Un algoritm corect pentru suma a două numere trebuie să facă, în ordine:',
                      ['afișare → citire → calcul', 'calcul → citire → afișare', 'citire → calcul → afișare', 'calcul → afișare → citire'], 2,
                      'Fluxul firesc este: citești datele, procesezi, apoi afișezi rezultatul.',
                      'Gândește orice problemă ca pe un traseu input-output.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'În pseudocod, instrucțiunea „citește n” aparține etapei de:',
                      ['procesare', 'ieșire', 'intrare', 'comentariu'], 2,
                      'Citirea unei valori reprezintă etapa de intrare.',
                      'Asociază fiecare instrucțiune cu rolul ei.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'date-variabile-expresii-si-operatori':
        example = make_example(sid, subiect_id, chapter_id,
            'La exercițiile scurte urmărești actualizarea valorilor din variabile pas cu pas.',
            'După fiecare atribuire, „oprești filmul” și notezi noua valoare.',
            'Exemplu lucrat · atribuire',
            'Inițial x=2. După instrucțiunea x←x+3, care este noua valoare?',
            ['Vechea valoare este 2.', 'Calculezi 2+3=5.', 'Noua valoare a lui x devine 5.'],
            ['Știi că partea dreaptă se calculează cu valoarea veche?', 'Poți urmări mai multe atribuiri la rând?'],
            'Atribuirea rescrie variabila cu noua valoare.',
            ['iei valoarea veche', 'calculezi expresia', 'rescrii variabila'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Dacă x=4 și executăm x←x*2−1, valoarea finală a lui x este:',
                      ['5', '7', '8', '9'], 1,
                      '4*2−1 = 7.',
                      'Evaluează expresia folosind valoarea curentă a lui x.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Operatorul „mod” este folosit pentru a afla:',
                      ['câtul împărțirii', 'restul împărțirii', 'partea întreagă a radicalului', 'numărul de cifre'], 1,
                      'Operatorul modulo returnează restul împărțirii.',
                      'Leagă operatorii de rolul lor concret în probleme.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'structuri-de-control-secventa-alternativa-repetitivitate':
        example = make_example(sid, subiect_id, chapter_id,
            'Aici alegi între secvență, if și buclă, în funcție de tipul cerinței.',
            'Când vezi „pentru fiecare”, „până când”, „de n ori”, gândește automat repetitivitate.',
            'Exemplu lucrat · buclă simplă',
            'Descrie pe scurt cum ai afișa numerele de la 1 la 5.',
            ['inițializezi i cu 1', 'cât timp i≤5 afișezi i', 'crești i cu 1'],
            ['Recunoști momentul în care ai nevoie de repetiție?', 'Știi unde se actualizează contorul?'],
            'Repetitivitate = inițializare + condiție + actualizare.',
            ['alegi structura', 'scrii condiția', 'actualizezi contorul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Pentru a executa aceiași pași de 10 ori, structura potrivită este:',
                      ['alternativă', 'repetitivă', 'declarație', 'comentariu'], 1,
                      'Când o secvență trebuie reluată, folosești o structură repetitivă.',
                      'Caută în enunț indiciul „de câte ori”.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Instrucțiunea if ... then ... else este folosită când:',
                      ['vrei să repeți aceeași acțiune', 'vrei să alegi între două ramuri', 'vrei să citești un fișier', 'vrei să sortezi un vector'], 1,
                      'Structura alternativă alege între două ramuri, în funcție de condiție.',
                      'Asociază structura cu scopul ei.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'subprograme-predefinite-si-functii-standard':
        example = make_example(sid, subiect_id, chapter_id,
            'Funcțiile standard te ajută să nu rescrii calcule deja existente în limbaj.',
            'La bac se verifică des dacă știi ce produce o funcție precum abs, sqrt sau strlen.',
            'Exemplu lucrat · funcție standard',
            'Determină rezultatul expresiei abs(−7).',
            ['Funcția abs dă valoarea absolută.', 'Valoarea absolută a lui −7 este 7.', 'Rezultatul final este 7.'],
            ['Recunoști ce intră și ce iese din funcția standard?', 'Știi dacă tipul datelor rămâne numeric?'],
            'Funcțiile standard economisesc cod și timp.',
            ['identifici funcția', 'aplici definiția', 'verifici tipul rezultatului'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Rezultatul expresiei abs(−3)+abs(2) este:',
                      ['−1', '1', '5', '−5'], 2,
                      'abs(−3)=3 și abs(2)=2, deci suma este 5.',
                      'Calculează separat fiecare apel de funcție.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Funcția sqrt(49) întoarce:',
                      ['7', '14', '2401', '0'], 0,
                      'sqrt calculează rădăcina pătrată principală, deci 7.',
                      'Leagă funcția de operația matematică asociată.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'complexitate-si-urmarirea-executiei':
        example = make_example(sid, subiect_id, chapter_id,
            'La urmărirea execuției notezi valorile după fiecare pas; la complexitate cauți numărul dominant de operații.',
            'Nu încerca să memorezi tot: fă un tabel de urmărie pentru variabile.',
            'Exemplu lucrat · număr de pași',
            'O buclă for de la 1 la n execută o instrucțiune simplă. Ce complexitate are?',
            ['Instrucțiunea se repetă n ori.', 'Numărul de pași crește liniar cu n.', 'Complexitatea este O(n).'],
            ['Știi să ignori constantele?', 'Poți face diferența între O(n) și O(n²)?'],
            'Liniar = o singură buclă simplă.',
            ['numeri buclele', 'vezi cum depind de n', 'păstrezi termenul dominant'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'O singură parcurgere a unui vector cu n elemente are, de regulă, complexitate:',
                      ['O(1)', 'O(log n)', 'O(n)', 'O(n²)'], 2,
                      'Fiecare element este vizitat o dată, deci numărul de pași crește liniar.',
                      'Întreabă-te de câte ori se repetă operația dominantă.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Două bucle for imbricate, fiecare de la 1 la n, duc de obicei la complexitate:',
                      ['O(n)', 'O(n log n)', 'O(n²)', 'O(2n)'], 2,
                      'Fiecare valoare a primei bucle produce n pași în a doua, deci aproximativ n·n.',
                      'Buclele imbricate multiplică numărul de pași.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'tablouri-unidimensionale':
        example = make_example(sid, subiect_id, chapter_id,
            'La vectori, problema standard este parcurgerea și actualizarea unei statistici: sumă, maxim, frecvență.',
            'La orice tablou, decide ce „informație acumulată” păstrezi.',
            'Exemplu lucrat · maxim într-un vector',
            'Pentru vectorul [2, 7, 4], determină valoarea maximă.',
            ['Pornești cu maxim=2.', 'Compari cu 7 și actualizezi maxim=7.', 'Compari cu 4 și păstrezi 7.'],
            ['Știi de unde pornești inițializarea?', 'Poți face aceeași schemă pentru minim sau sumă?'],
            'Parcurgere + comparație + actualizare.',
            ['inițializezi', 'parcurgi', 'actualizezi când găsești mai bun'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'În vectorul [5, 1, 9, 3], valoarea maximă este:',
                      ['1', '3', '5', '9'], 3,
                      'Parcurgând toate valorile, cea mai mare este 9.',
                      'Comparația se face cu fiecare element.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru a afla suma elementelor unui vector, la fiecare pas:',
                      ['rescrii tot vectorul', 'aduni elementul curent la sumă', 'sortezi vectorul', 'ștergi valorile pare'], 1,
                      'Schema standard este sum ← sum + v[i].',
                      'Ține minte variabila-acumulator.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'matrice-si-tablouri-bidimensionale':
        example = make_example(sid, subiect_id, chapter_id,
            'La matrice, indiciile vin din poziție: linii, coloane, diagonală principală sau secundară.',
            'Dacă cerința menționează diagonala, uită-te imediat la relația dintre indici.',
            'Exemplu lucrat · diagonala principală',
            'În matricea [[1,2],[3,4]], determină suma elementelor de pe diagonala principală.',
            ['Pe diagonala principală ai pozițiile (1,1) și (2,2).', 'Valorile sunt 1 și 4.', 'Suma este 5.'],
            ['Știi cum identifici diagonala principală?', 'Poți trece de la indici la valori?'],
            'Diagonala principală: i = j.',
            ['identifici pozițiile', 'citești valorile', 'calculezi suma'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Suma diagonalei principale a matricei [[2,0],[1,5]] este:',
                      ['2', '5', '6', '7'], 3,
                      'Elementele de pe diagonala principală sunt 2 și 5, deci suma este 7.',
                      'Folosește regula i=j.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Într-o matrice n×n, elementele de pe diagonala principală verifică:',
                      ['i+j=n+1', 'i=j', 'i<j', 'i>j'], 1,
                      'Pe diagonala principală, indicele de linie este egal cu cel de coloană.',
                      'Asociază noțiunea de diagonală cu relația dintre indici.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'siruri-de-caractere':
        example = make_example(sid, subiect_id, chapter_id,
            'La șiruri, numără, cauți, extragi sau înlocuiești; totul pornește de la poziția caracterelor.',
            'Nu încerca să vizualizezi tot deodată: mergi caracter cu caracter sau pe funcții standard.',
            'Exemplu lucrat · lungime de șir',
            'Determină lungimea șirului "BAC".',
            ['Șirul conține caracterele B, A, C.', 'Numărul lor este 3.', 'Deci lungimea este 3.'],
            ['Știi diferența dintre caracter și șir?', 'Poți număra fără spații și semne suplimentare?'],
            'Șir = secvență ordonată de caractere.',
            ['identifici șirul', 'numeri caracterele', 'scrii rezultatul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Lungimea șirului "INFO" este:',
                      ['3', '4', '5', '6'], 1,
                      'Șirul conține 4 caractere.',
                      'Numără toate caracterele o singură dată.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Funcția care verifică poziția unui caracter într-un șir este utilă pentru:',
                      ['sortare numerică', 'căutare în șir', 'scriere în fișier binar', 'desenarea graficului'], 1,
                      'Operațiile pe șiruri includ frecvent căutarea unui caracter sau subșir.',
                      'Leagă funcția de problema practică pe care o rezolvă.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'inregistrari-si-structuri-de-date-simple':
        example = make_example(sid, subiect_id, chapter_id,
            'Înregistrarea grupează date diferite despre aceeași entitate.',
            'Când vezi „nume + notă + clasă”, gândește structura de tip înregistrare.',
            'Exemplu lucrat · model de înregistrare',
            'Vrei să memorezi pentru un elev: nume, media și absențele. Ce tip de structură alegi?',
            ['Datele sunt de tipuri diferite.', 'Toate descriu aceeași entitate: elevul.', 'O înregistrare este alegerea naturală.'],
            ['Știi când nu este suficient un tablou simplu?', 'Poți enumera câmpurile unei înregistrări?'],
            'Înregistrarea = „fișa” unui obiect.',
            ['identifici entitatea', 'listezi câmpurile', 'alegi tipurile potrivite'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Pentru a memora nume și medie pentru un elev, structura potrivită este:',
                      ['un singur int', 'o înregistrare', 'doar un șir de caractere', 'o matrice 2×2 obligatoriu'], 1,
                      'O înregistrare permite câmpuri diferite pentru aceeași entitate.',
                      'Întreabă-te dacă datele descriu același obiect.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Câmpurile unei înregistrări trebuie să fie:',
                      ['toate de același tip', 'neapărat numere întregi', 'adaptate tipului de informație stocat', 'ordonate alfabetic'], 2,
                      'Fiecare câmp primește tipul potrivit informației pe care o memorează.',
                      'Leagă tipul de natura datelor.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'fisiere-text':
        example = make_example(sid, subiect_id, chapter_id,
            'La fișiere text, schema standard este: deschizi, citești până la sfârșit, prelucrezi, închizi.',
            'Multe probleme sunt aceleași ca la vectori, doar că datele vin din fișier.',
            'Exemplu lucrat · numărare valori',
            'Dintr-un fișier care conține numerele 2 5 8, vrei să afli câte numere sunt.',
            ['citești primul număr', 'mărești contorul la fiecare citire reușită', 'la final, contorul este 3'],
            ['Poți distinge între citire și prelucrare?', 'Știi când se oprește bucla de citire?'],
            'Fișier text = intrare secvențială.',
            ['deschizi', 'citești până la EOF', 'închizi și afișezi'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Într-un fișier text, datele sunt citite de regulă:',
                      ['secvențial', 'doar aleator', 'doar în ordine descrescătoare', 'în paralel'], 0,
                      'Fișierele text sunt tratate uzual secvențial, de la început la sfârșit.',
                      'Gândește fluxul natural de citire.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Pentru a număra valorile dintr-un fișier text, folosești util:',
                      ['un contor crescut la fiecare citire', 'doar un sort', 'o matrice fixă', 'o funcție trigonomterică'], 0,
                      'Schema standard este un contor incrementat la fiecare element citit.',
                      'Asociază problema cu o variabilă-acumulator.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'subprograme-definite-de-utilizator':
        example = make_example(sid, subiect_id, chapter_id,
            'Subprogramele separă logica în piese reutilizabile și ușor de testat.',
            'Dacă aceeași operație apare de mai multe ori, merită extrasă într-o funcție sau procedură.',
            'Exemplu lucrat · funcție simplă',
            'Definim funcția patrat(x) care întoarce x*x. Ce întoarce patrat(4)?',
            ['Înlocuiești x cu 4.', 'Calculezi 4*4.', 'Rezultatul este 16.'],
            ['Știi diferența dintre procedură și funcție?', 'Poți urmări parametrii trimiși?'],
            'Funcția întoarce o valoare, procedura execută pași.',
            ['identifici parametrii', 'urmărești corpul funcției', 'scrii rezultatul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'O funcție definită de utilizator are rolul principal de a:',
                      ['întoarce o valoare sau a grupa logică reutilizabilă', 'desena grafice', 'înlocui compilatorul', 'șterge automat erorile'], 0,
                      'Funcțiile și procedurile organizează logica și permit reutilizarea codului.',
                      'Gândește-te la „o bucată de cod cu nume”.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă funcția f(x)=x+1, atunci apelul f(5) produce:',
                      ['4', '5', '6', '7'], 2,
                      'Înlocuind x cu 5 obții 6.',
                      'Urmărește parametrul efectiv în corpul funcției.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'recursivitate':
        example = make_example(sid, subiect_id, chapter_id,
            'În recursivitate contează două lucruri: cazul de bază și apelul care reduce problema.',
            'Dacă nu vezi clar cazul de oprire, algoritmul recursiv nu este încă sigur.',
            'Exemplu lucrat · factorial recursiv',
            'Pentru n! definit prin n!=n·(n−1)! și 0!=1, calculează 3!.',
            ['3! = 3·2!', '2! = 2·1!', '1! = 1·0! = 1, deci 3! = 6.'],
            ['Ai identificat cazul de bază?', 'Problema se reduce la una mai mică?'],
            'Recursivitate = definiție în funcție de un caz mai mic.',
            ['găsești cazul de bază', 'urmărești apelurile', 'revii cu rezultatele'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Într-o funcție recursivă este obligatoriu să existe:',
                      ['o matrice', 'un caz de bază', 'sortare', 'un fișier text'], 1,
                      'Cazul de bază oprește recursia și face algoritmul corect.',
                      'Fără caz de bază, apelurile nu se opresc.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă fact(0)=1 și fact(n)=n·fact(n−1), atunci fact(3) este:',
                      ['3', '4', '6', '9'], 2,
                      'fact(3)=3·2·1=6.',
                      'Desfășoară apelurile până la cazul de bază.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'tehnici-elementare-de-algoritmica':
        example = make_example(sid, subiect_id, chapter_id,
            'Aici intră frecvent cifrele unui număr, divizibilitatea, Euclid, Fibonacci sau sume simple.',
            'Când vezi „cifrele unui număr”, gândește imediat la operațiile /10 și %10.',
            'Exemplu lucrat · sumă a cifrelor',
            'Determină suma cifrelor numărului 125.',
            ['Ultima cifră este 5, apoi 2, apoi 1.', 'Le aduni: 5+2+1.', 'Rezultatul este 8.'],
            ['Știi cum extragi ultima cifră?', 'Știi cum elimini ultima cifră?'],
            'cifră = n%10, eliminare = n/10.',
            ['iei ultima cifră', 'o aduni', 'elimini cifra și repeți'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Ultima cifră a numărului n se obține cu:',
                      ['n/10', 'n%10', 'n*n', 'sqrt(n)'], 1,
                      'Operatorul modulo 10 extrage ultima cifră.',
                      'Leagă tiparul „cifre” de operațiile / și %.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Algoritmul lui Euclid este folosit pentru:',
                      ['sortare', 'cmmdc', 'parcurgere în graf', 'citire fișier'], 1,
                      'Algoritmul lui Euclid calculează cel mai mare divizor comun.',
                      'Asociază numele algoritmului cu scopul lui.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'cautare-si-sortare':
        example = make_example(sid, subiect_id, chapter_id,
            'La căutare și sortare contează când este justificat un algoritm și ce cost are.',
            'Dacă vectorul este deja ordonat, căutarea binară devine o armă foarte bună.',
            'Exemplu lucrat · căutare binară',
            'În vectorul ordonat [1,3,5,7,9], cauți valoarea 7. Cu ce metodă eficientă începi?',
            ['Vectorul este ordonat.', 'Se poate tăia repetat în jumătăți.', 'Alegerea naturală este căutarea binară.'],
            ['Ai verificat dacă datele sunt ordonate?', 'Poți explica de ce binara este mai rapidă?'],
            'Ordonat → căutare binară.',
            ['vezi dacă e ordonat', 'alegi algoritmul', 'justifici eficiența'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Căutarea binară se aplică direct pe un vector:',
                      ['neordonat', 'ordonat', 'cu numere negative doar', 'de lungime pară doar'], 1,
                      'Condiția esențială este ordonarea datelor.',
                      'Fără ordine, nu poți elimina jumătăți de interval.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Bubble sort este o metodă de:',
                      ['căutare', 'sortare', 'compresie', 'criptare'], 1,
                      'Bubble sort este un algoritm clasic de sortare.',
                      'Asociază numele metodei cu familia ei.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'interclasare-frecvente-si-prelucrari-eficiente':
        example = make_example(sid, subiect_id, chapter_id,
            'Interclasarea combină eficient două șiruri ordonate; frecvențele rezumă rapid aparițiile.',
            'Dacă ai multe valori mici sau repetate, vectorul de frecvență economisește timp.',
            'Exemplu lucrat · frecvență',
            'Pentru valorile 2,2,5, de câte ori apare 2?',
            ['Parcurgi valorile și incrementezi frecvența corespunzătoare.', 'Pentru 2, contorul ajunge la 2.', 'Așadar, frecvența lui 2 este 2.'],
            ['Poți ține un contor pentru fiecare valoare?', 'Știi când interclasarea cere două șiruri ordonate?'],
            'Frecvența = „de câte ori apare”.',
            ['numeri aparițiile', 'actualizezi contorul', 'citești rezultatul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Interclasarea standard presupune că cele două șiruri inițiale sunt:',
                      ['ordonate', 'goale', 'de aceeași lungime', 'neapărat distincte'], 0,
                      'Interclasarea eficientă funcționează pe două șiruri deja ordonate.',
                      'Verifică precondiția algoritmului.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Un vector de frecvență este util pentru a afla rapid:',
                      ['numărul de linii dintr-un fișier', 'de câte ori apare o valoare', 'adresa unei funcții', 'graful asociat'], 1,
                      'Frecvențele memorează numărul de apariții pentru fiecare valoare.',
                      'Leagă structura de întrebarea „de câte ori?”.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'backtracking':
        example = make_example(sid, subiect_id, chapter_id,
            'Backtracking generează soluții pas cu pas și revine când un drum devine imposibil.',
            'În minte, imaginează-ți un arbore de decizie pe care îl explorezi cu revenire.',
            'Exemplu lucrat · alegere controlată',
            'Vrei toate numerele de 2 cifre formate doar din 1 și 2. Cum procedezi?',
            ['Alegi prima cifră dintre 1 și 2.', 'Pentru fiecare alegi a doua cifră tot dintre 1 și 2.', 'Obții 11, 12, 21, 22.'],
            ['Poți formula regula de validare?', 'Înțelegi momentul în care „te întorci” la pasul anterior?'],
            'Alegi, verifici, mergi mai departe; dacă nu merge, revii.',
            ['definești pașii', 'testezi validarea', 'revii când nu mai poți continua'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Backtracking este folosit în special pentru:',
                      ['citirea unui fișier', 'generarea tuturor soluțiilor valide', 'înmulțirea matricelor', 'afișarea unui singur număr'], 1,
                      'Backtracking explorează sistematic spațiul tuturor soluțiilor posibile.',
                      'Gândește în termeni de arbore de posibilități.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'În backtracking, revenirea are loc când:',
                      ['s-a găsit o soluție sau o ramură devine invalidă', 'programul se închide', 'vectorul este sortat', 'fișierul e gol'], 0,
                      'Algoritmul revine când a completat o soluție sau când nu mai poate continua valid.',
                      'Asociază revenirea cu tăierea unei ramuri.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'generare-combinatorica':
        example = make_example(sid, subiect_id, chapter_id,
            'Generarea combinatorică produce aranjări, combinații sau submulțimi în ordine sistematică.',
            'Întrebarea de bază: ordinea contează sau nu?',
            'Exemplu lucrat · submulțimi',
            'Pentru mulțimea {1,2}, care sunt submulțimile?',
            ['Ai ∅, {1}, {2}, {1,2}.', 'Le obții alegând pentru fiecare element: îl iei sau nu.', 'În total sunt 4 submulțimi.'],
            ['Poți lega numărul submulțimilor de 2^n?', 'Poți deosebi combinațiile de permutări?'],
            'Fiecare element are două stări: inclus sau nu.',
            ['stabilești regula', 'generezi sistematic', 'verifici dacă ai toate cazurile'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Numărul submulțimilor unei mulțimi cu 3 elemente este:',
                      ['3', '6', '8', '9'], 2,
                      'O mulțime cu n elemente are 2^n submulțimi, deci 2^3=8.',
                      'Amintește-ți regula 2^n.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Dacă ordinea contează, problema este mai apropiată de:',
                      ['combinații', 'permutări / aranjamente', 'vector de frecvență', 'fișier text'], 1,
                      'Când ordinea contează, generezi aranjări sau permutări.',
                      'Pornește mereu de la întrebarea despre ordine.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'grafuri-neorientate':
        example = make_example(sid, subiect_id, chapter_id,
            'În grafurile neorientate, muchiile nu au sens, iar gradul unui vârf este numărul de muchii incidente.',
            'Desenează rapid graful sau lista de adiacență ca să nu pierzi relațiile.',
            'Exemplu lucrat · gradul unui vârf',
            'Într-un graf cu muchiile {1-2, 1-3}, care este gradul vârfului 1?',
            ['Vârful 1 este incident cu două muchii.', 'Deci gradul său este 2.', 'Direcția nu contează în graf neorientat.'],
            ['Știi să numeri muchiile incidente?', 'Poți deosebi gradul de numărul total de vârfuri?'],
            'Grad = câte legături are vârful.',
            ['listezi muchiile', 'numeri incidențele', 'scrii gradul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Într-un graf neorientat, muchia 2-5 este aceeași cu:',
                      ['5-2', '2→5', '5→2 dar doar uneori', 'nu are echivalent'], 0,
                      'În graf neorientat nu există direcție, deci 2-5 și 5-2 descriu aceeași muchie.',
                      'Neorientat = fără sens.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Gradul unui vârf într-un graf neorientat este:',
                      ['numărul de vârfuri din graf', 'numărul muchiilor incidente', 'numărul de componente conexe', 'valoarea maximă din matrice'], 1,
                      'Gradul se definește ca numărul muchiilor incidente acelui vârf.',
                      'Fă legătura dintre vârf și muchiile care „intră” în el.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'grafuri-orientate':
        example = make_example(sid, subiect_id, chapter_id,
            'În grafurile orientate contează sensul arcelor, deci separi gradul intern de cel extern.',
            'Orice săgeată care pleacă mărește gradul extern; orice săgeată care intră mărește gradul intern.',
            'Exemplu lucrat · grade într-un digraf',
            'În digraful cu arcele 1→2 și 3→2, care este gradul intern al vârfului 2?',
            ['În 2 intră două arce: 1→2 și 3→2.', 'Gradul intern este 2.', 'Gradul extern al lui 2 este 0 aici.'],
            ['Poți separa clar „intră” de „iese”?', 'Știi că direcția schimbă răspunsul?'],
            'Intern = intră, extern = iese.',
            ['marchezi săgețile', 'numeri ce intră', 'numeri ce iese'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Într-un graf orientat, arcul 1→3 este diferit de:',
                      ['1-3', '3→1', 'ambele', 'niciuna'], 2,
                      'Direcția contează, deci 1→3 și 3→1 sunt distincte, iar 1-3 descrie alt tip de graf.',
                      'Atenție la sensul săgeții.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Gradul extern al unui vârf într-un graf orientat numără:',
                      ['arcele care intră', 'arcele care ies', 'numărul total de vârfuri', 'muchiile neorientate'], 1,
                      'Gradul extern este numărul arcelor care pleacă din vârf.',
                      'Extern = iese din vârf.', 'intermediate'),
        ]
        return example, items
    if chapter_id == 'arbori':
        example = make_example(sid, subiect_id, chapter_id,
            'Arborele este un graf conex, fără cicluri; frunzele au grad 1 în arbore neorientat.',
            'Când vezi „arbore”, verifici automat conexitatea și absența ciclurilor.',
            'Exemplu lucrat · frunză',
            'În arborele cu muchiile {1-2, 2-3}, care vârfuri sunt frunze?',
            ['Vârful 1 are grad 1 și vârful 3 are grad 1.', 'Vârful 2 are grad 2.', 'Frunzele sunt 1 și 3.'],
            ['Știi definiția frunzei?', 'Poți număra gradele rapid?'],
            'Frunză = grad 1.',
            ['calculezi gradele', 'identifici gradul 1', 'verifici structura de arbore'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Un arbore cu n vârfuri are exact:',
                      ['n muchii', 'n−1 muchii', 'n+1 muchii', '2n muchii'], 1,
                      'Proprietatea fundamentală a arborilor este că au n−1 muchii.',
                      'Leagă noțiunea de arbore de formula standard.', 'beginner'),
            make_item(sid, subiect_id, chapter_id,
                      'Într-un arbore neorientat, o frunză este un vârf cu grad:',
                      ['0', '1', '2', 'n−1'], 1,
                      'Frunza are exact o muchie incidentă, deci grad 1.',
                      'Caută vârfurile „de capăt”.', 'intermediate'),
        ]
        return example, items
    raise KeyError(f'No info template for {chapter_id}')


# --- Templates for Romanian ---
ROMANA_WORKS = {
    'mihai-eminescu-poezie-si-romantism': ('Luceafărul', 'condiția geniului și opoziția dintre absolut și terestru'),
    'ion-creanga-basm-si-proza-memorialistica': ('Povestea lui Harap-Alb', 'drumul inițiatic și maturizarea eroului'),
    'i-l-caragiale-comedie-si-schita': ('O scrisoare pierdută', 'satira moravurilor politice și comicul de limbaj'),
    'titu-maiorescu-critica-si-junimism': ('„În contra direcției de astăzi în cultura română”', 'spiritul critic și teoria formelor fără fond'),
    'ioan-slavici-nuvela-realista-si-morala': ('Moara cu noroc', 'conflictul moral al personajului și degradarea prin patimă'),
    'george-bacovia-simbolism': ('Plumb', 'criza interioară și universul claustrant'),
    'lucian-blaga-poezie-modernista': ('Eu nu strivesc corola de minuni a lumii', 'cunoașterea luciferică și protejarea misterului'),
    'tudor-arghezi-modernism-si-estetica-uratului': ('Testament', 'poetica transformării urâtului în valoare estetică'),
    'ion-barbu-ermetism-si-joc-secund': ('Riga Crypto și lapona Enigel / Joc secund', 'poezia intelectualizată și limbajul ermetic'),
    'mihail-sadoveanu-roman-traditional-si-istoric': ('Baltagul', 'restabilirea ordinii și itinerariul inițiatic'),
    'liviu-rebreanu-roman-realist-obiectiv': ('Ion', 'tema pământului și conflictul dintre glasul pământului și glasul iubirii'),
    'camil-petrescu-roman-subiectiv-si-autenticitate': ('Ultima noapte de dragoste, întâia noapte de război', 'autenticitatea și perspectiva subiectivă'),
    'g-calinescu-roman-balzacian-si-critica': ('Enigma Otiliei', 'viziunea balzaciană și tema moștenirii'),
    'e-lovinescu-modernism-critic': ('sincronismul', 'modernizarea literaturii prin sincronizare cu Occidentul'),
    'marin-preda-roman-postbelic': ('Moromeții', 'destrămarea lumii tradiționale și criza familiei'),
    'nichita-stanescu-neomodernism': ('Leoaică tânără, iubirea / Emoție de toamnă', 'metafora revelatorie și reinventarea limbajului poetic'),
    'marin-sorescu-poezie-si-dramaturgie-postbelica': ('Iona', 'singurătatea modernă și meditația asupra libertății'),
}

def rom_example_and_item(chapter_id: str, title: str, subiect_id: str) -> tuple[dict, list[dict]]:
    sid = 'romana_mate_info'
    if chapter_id == 'text-la-prima-vedere':
        example = make_example(sid, subiect_id, chapter_id,
            'La Subiectul I punctele vin din răspunsuri precise, scurte și ancorate în fragment.',
            'Nu răspunde din impresie: subliniază în text locul din care scoți ideea.',
            'Exemplu lucrat · răspuns pe text suport',
            'Fragment: „În dimineața aceea, orașul părea mai liniștit decât de obicei.” Cum justifici ideea de atmosferă calmă?',
            ['Identifici cuvântul-cheie: „mai liniștit”.', 'Îl transformi într-o formulare proprie: atmosfera este calmă.', 'Răspunsul trebuie să trimită explicit la fragment.'],
            ['Ai citat sau parafrazat exact zona relevantă?', 'Răspunsul tău are maximum 1-2 enunțuri clare?'],
            'Textul suport îți oferă deja dovada; tu doar o formulezi corect.',
            ['citești cerința', 'marchezi dovada', 'scrii răspunsul scurt'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'În răspunsurile pe text suport, varianta cea mai sigură este să:',
                      ['inventezi o interpretare fără exemplu', 'te raportezi direct la fragment și formulezi precis', 'scrii cât mai mult, fără structură', 'eviți citarea indiciilor din text'], 1,
                      'La Subiectul I contează răspunsul exact și ancorat în text.',
                      'Caută în fragment dovada, apoi formulează scurt.', 'beginner', tags=['text-suport']),
        ]
        return example, items
    if chapter_id == 'sens-denotativ-conotativ-si-expresivitate':
        example = make_example(sid, subiect_id, chapter_id,
            'Cuvântul are sens denotativ când numește direct și sens conotativ când sugerează sau încarcă afectiv.',
            'La bac, nu defini lung; arată cum funcționează cuvântul în context.',
            'Exemplu lucrat · sens conotativ',
            'În sintagma „inimă de piatră”, de ce avem sens conotativ?',
            ['Nu este vorba despre o piatră reală.', 'Expresia sugerează lipsa de empatie.', 'Apare o valoare figurată, deci conotativă.'],
            ['Poți separa sensul literal de cel figurat?', 'Ai legat răspunsul de efectul expresiv?'],
            'Denotativ = literal; conotativ = figurat / sugerat.',
            ['citești expresia', 'verifici sensul literal', 'formulezi efectul figurat'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'În expresia „glas cald”, adjectivul „cald” are sens predominant:',
                      ['denotativ strict fizic', 'conotativ, sugerând apropiere și afecțiune', 'matematic', 'tehnic'], 1,
                      '„Cald” nu descrie temperatura propriu-zisă a vocii, ci un efect afectiv și expresiv.',
                      'Întreabă-te dacă sensul este literal sau figurat.', 'intermediate', tags=['expresivitate']),
        ]
        return example, items
    if chapter_id == 'text-argumentativ':
        example = make_example(sid, subiect_id, chapter_id,
            'Un text argumentativ bun are teză clară, doi pași de argumentare și o concluzie coerentă.',
            'La început, formulează poziția ta fără ezitare: asta este teza.',
            'Exemplu lucrat · schemă',
            'Tema: „Lectura dezvoltă imaginația”. Cum începi?',
            ['Formulezi teza: „Consider că lectura dezvoltă imaginația”.', 'Adaugi un argument personal sau cultural.', 'Închei reluând ideea într-o concluzie.'],
            ['Ai o teză explicită?', 'Fiecare argument susține exact teza?'],
            'Teză → argumente → concluzie.',
            ['scrii poziția', 'alegi 2 argumente', 'închizi logic textul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Care formulare funcționează cel mai bine ca teză pentru un text argumentativ?',
                      ['Poate că uneori, într-un fel, lectura...', 'Consider că lectura dezvoltă imaginația și spiritul critic.', 'Și eu citesc, dar depinde.', 'Lectura este o activitate și atât.'], 1,
                      'Teza trebuie să fie clară, fermă și ușor de susținut cu argumente.',
                      'Caută propoziția care ia o poziție explicită.', 'beginner', tags=['argumentare']),
        ]
        return example, items
    if chapter_id == 'norme-de-redactare-ortografie-punctuatie-morfosintaxa':
        example = make_example(sid, subiect_id, chapter_id,
            'Punctele ușoare se pierd la redactare când elevul scrie în grabă și nu recitește.',
            'La finalul oricărui răspuns, fă o verificare de 20 de secunde pe ortografie și punctuație.',
            'Exemplu lucrat · verificare rapidă',
            'Compară: „Sau dus acasă.” vs „S-au dus acasă.” Care este forma corectă?',
            ['Forma corectă este „S-au dus acasă.”', 'Apare verbul auxiliar + pronumele clitic.', 'Greșeala vine din confuzia dintre omofone.'],
            ['Recunoști repede formele omofone?', 'Ai timp de o recitire finală?'],
            'Multe greșeli se repară prin recitire lentă.',
            ['citești propoziția', 'verifici forma corectă', 'corectezi înainte de predare'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Varianta corectă este:',
                      ['Sau întâlnit în fața școlii.', 'S-au întâlnit în fața școlii.', 'S au întâlnit în fața școlii.', 'Sau-ntâlnit în fața școlii.'], 1,
                      'Forma corectă include cratimă: „S-au întâlnit”.',
                      'Verifică structura auxiliarului și pronumelui.', 'beginner', tags=['redactare']),
        ]
        return example, items
    if chapter_id == 'perspectiva-narativa-si-punct-de-vedere':
        example = make_example(sid, subiect_id, chapter_id,
            'Perspectiva narativă se identifică prin persoană, tipul naratorului și accesul la conștiința personajelor.',
            'La analiză, caută pronumele și verbele: ele îți spun imediat cine povestește.',
            'Exemplu lucrat · narator',
            'Fragment: „Am intrat în cameră și am înțeles că totul se schimbase.” Ce indică persoana I?',
            ['Verbele la persoana I sugerează un narator implicat.', 'Punctul de vedere este interiorizat.', 'Perspectiva este subiectivă.'],
            ['Ai observat marcile persoanei?', 'Poți formula și efectul lor?'],
            'Persoana I apropie cititorul de conștiința personajului-narator.',
            ['identifici persoana', 'numești naratorul', 'spui efectul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Un narator la persoana I sugerează, de regulă, o perspectivă:',
                      ['obiectivă și omniscientă', 'subiectivă, interiorizată', 'dramatică', 'strict descriptivă fără implicare'], 1,
                      'Persoana I implică adesea un narator participant sau martor, deci o perspectivă subiectivă.',
                      'Caută marcile persoanei gramaticale.', 'intermediate', tags=['perspectiva-narativa']),
        ]
        return example, items
    if chapter_id == 'rolul-didascaliilor-si-particularitatile-textului-dramatic':
        example = make_example(sid, subiect_id, chapter_id,
            'În textul dramatic, didascaliile dau informații de joc scenic, spațiu, gestică și ton.',
            'Nu le trata ca pe un detaliu marginal: ele construiesc sens și atmosferă.',
            'Exemplu lucrat · funcția didascaliilor',
            'Didascalia „vorbește apăsat, apropiindu-se de fereastră” ce transmite?',
            ['Indică modul de rostire.', 'Sugerează tensiunea și mișcarea scenică.', 'Ajută cititorul și actorul să înțeleagă situația.'],
            ['Ai numit funcția scenică și efectul?', 'Poți face diferența între replică și didascalie?'],
            'Didascaliile „montează scena” în mintea cititorului.',
            ['identifici didascalia', 'spui ce indică', 'explici efectul'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Didascaliile într-un text dramatic au rolul principal de a:',
                      ['înlocui personajele', 'oferi indicații scenice și de interpretare', 'explica formule matematice', 'prezenta bibliografia'], 1,
                      'Ele fixează cadrul scenic, gesturile, tonul și alte repere de interpretare.',
                      'Gândește textul dramatic ca pe un spectacol în potență.', 'beginner', tags=['dramatic']),
        ]
        return example, items
    if chapter_id == 'caracterizare-de-personaj':
        example = make_example(sid, subiect_id, chapter_id,
            'Caracterizarea bună pornește de la trăsătură și o dovedește prin faptă, limbaj sau relații.',
            'Nu enumera trăsături fără probă: fiecare idee are nevoie de un exemplu.',
            'Exemplu lucrat · schemă',
            'Vrei să arăți că un personaj este ambițios. Ce faci?',
            ['Formulezi trăsătura.', 'O susții printr-o faptă sau o replică relevantă.', 'Închei explicând ce efect are asupra evoluției personajului.'],
            ['Ai dovada textuală?', 'Ai legat trăsătura de rolul personajului în operă?'],
            'Trăsătură + dovadă + interpretare.',
            ['alegi trăsătura', 'găsești exemplul', 'explici semnificația'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'În caracterizarea unui personaj, exemplul concret are rolul de a:',
                      ['umple spațiul', 'dovedi trăsătura enunțată', 'evita analiza', 'înlocui concluzia'], 1,
                      'Fără dovadă, trăsătura rămâne o afirmație gratuită.',
                      'Caută varianta care susține analiza, nu ornamentul.', 'beginner', tags=['personaj']),
        ]
        return example, items
    if chapter_id == 'elemente-de-compozitie-si-limbaj':
        example = make_example(sid, subiect_id, chapter_id,
            'Compoziția și limbajul devin puncte de analiză atunci când arăți ce rol au în sensul textului.',
            'Nu spune doar „există metafore”; explică efectul lor.',
            'Exemplu lucrat · rolul titlului',
            'Cum poți comenta un titlu sugestiv?',
            ['Pornești de la sensul literal sau simbolic.', 'Îl legi de tema textului.', 'Arăți cum pregătește lectura operei.'],
            ['Ai comentat rolul, nu doar ai numit procedeele?', 'Ai făcut legătura cu tema?'],
            'Procedeu + efect + sens în ansamblu.',
            ['identifici elementul', 'spui efectul', 'legi de semnificația operei'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Când comentezi un procedeu de limbaj, pasul esențial este să:',
                      ['îl numeri', 'spui ce efect produce și ce susține în text', 'îl copiezi integral', 'îl eviți'], 1,
                      'La bac, procedeele trebuie interpretate, nu doar enumerate.',
                      'Caută funcția elementului de limbaj.', 'intermediate', tags=['compozitie']),
        ]
        return example, items
    # Subiectul III - essay chapters
    if chapter_id == 'curente-literare-si-repere-istorico-literare':
        example = make_example(sid, subiect_id, chapter_id,
            'Reperele istorico-literare funcționează ca o hartă: epocă, curent, trăsături, autori-reper.',
            'Când blochezi la eseu, începe cu curentul și două trăsături clare.',
            'Exemplu lucrat · schemă de încadrare',
            'Cum încadrezi rapid o operă în realism?',
            ['Numești curentul și perioada.', 'Precizezi două trăsături: obiectivitate, tipicitate, atenție la social.', 'Le demonstrezi prin operă.'],
            ['Ai două trăsături verificabile?', 'Poți lega trăsăturile de exemple din text?'],
            'Curentul nu se memorează singur; se leagă de autor și operă.',
            ['stabilești curentul', 'alegi 2 trăsături', 'le dovedești prin operă'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      'Pentru încadrarea unei opere într-un curent literar, varianta potrivită este să:',
                      ['spui doar anul apariției', 'numești curentul și dovedești 1-2 trăsături prin text', 'redai biografia completă a autorului', 'eviți exemplele din operă'], 1,
                      'Încadrarea cere numirea curentului și demonstrarea lui prin trăsături recognoscibile în text.',
                      'Gândește eseul ca pe o demonstrație, nu ca pe o listă.', 'beginner', tags=['curente-literare']),
        ]
        return example, items
    if chapter_id in ROMANA_WORKS:
        work, thesis = ROMANA_WORKS[chapter_id]
        example = make_example(sid, subiect_id, chapter_id,
            f'Pentru {work}, ai nevoie de un rezumat ultra-scurt, de o teză clară și de 2 repere relevante.',
            'Nu învăța eseul ca bloc de text: învață-l pe „noduri” de idei și exemple.',
            f'Mini-plan de eseu · {work}',
            f'Construiește un răspuns de plecare pentru opera {work}.',
            [
                f'Teză de pornire: opera valorifică {thesis}.',
                'Alegi două repere: temă/conflict/personaj/compoziție/limbaj, după cerință.',
                'Închei legând exemplele de specificul operei și de viziunea autorului.',
            ],
            [f'Poți formula teza fără să intri încă în detalii?', 'Ai pregătit două exemple concrete, nu doar etichete?'],
            f'Cheia de memorie: {work} = {thesis}.',
            ['rostești teza', 'alegi 2 repere', 'închei coerent'],
        )
        items = [
            make_item(sid, subiect_id, chapter_id,
                      f'Care teză de început funcționează cel mai bine pentru un eseu despre {work}?',
                      [
                          'Opera este interesantă și frumoasă, fără alte precizări.',
                          f'Opera evidențiază {thesis}, susținută prin construcția personajelor și prin momentele-cheie ale acțiunii.',
                          'Autorul s-a născut într-o anumită perioadă, iar asta este suficient.',
                          'Eseul poate începe direct cu o concluzie generală fără teză.',
                      ], 1,
                      'O teză bună anunță ideea centrală și deschide direcțiile de demonstrație ale eseului.',
                      'Alege formularea care are poziție clară și deschide analiza.', 'intermediate', tags=['eseu', work]),
        ]
        return example, items
    raise KeyError(f'No Romanian template for {chapter_id}')


EXAMPLE_BUILDERS = {
    'matematica_m1': math_example_and_items,
    'informatica_mate_info': info_example_and_items,
    'romana_mate_info': rom_example_and_item,
}


items = []
examples = []
errors = []
for subject in CATALOG['subjects']:
    builder = EXAMPLE_BUILDERS.get(subject['id'])
    if not builder:
        continue
    for subiect in subject.get('subiecte', []):
        for chapter in subiect.get('chapters', []):
            try:
                example, chapter_items = builder(chapter['id'], chapter['title'], subiect['id'])
            except Exception as exc:
                errors.append((subject['id'], chapter['id'], str(exc)))
                continue
            examples.append(example)
            items.extend(chapter_items)

payload_examples = {'meta': {'generated': True, 'count': len(examples)}, 'items': examples}
payload_items = {'meta': {'generated': True, 'count': len(items), 'note': 'Itemi adaptați în stilul modelelor ministeriale și etichetați pe capitole pentru antrenament aplicativ.'}, 'items': items}

(ROOT / 'data' / 'chapter_examples.json').write_text(json.dumps(payload_examples, ensure_ascii=False, indent=2), encoding='utf-8')
(ROOT / 'data' / 'exam_bank.json').write_text(json.dumps(payload_items, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'Generated {len(examples)} examples and {len(items)} quiz items.')
if errors:
    print('Errors:')
    for err in errors:
        print(err)
