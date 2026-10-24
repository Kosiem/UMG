# Qiskit + IBM Quantum Runtime — praktyczny poradnik od zera

To jest całkowicie najważniejszy plik w tym projekcie.

Tu masz wszystko w jednym miejscu:
- co robi ten kod,
- co oznaczają qubity i bramki,
- co to jest Bell, GHZ i splątanie,
- co oznaczają te dziwne napisy typu `IZ`, `ZZ`, `XX`,
- jak czytać ten skrypt linia po linii,
- i co jest ważne z teorii.

Jeśli coś w mechanice kwantowej jest dla Ciebie niejasne, to tutaj trzeba to wyjaśnić prostym językiem.

---

## 1. O co chodzi w tym skrypcie?

Ten skrypt pokazuje dwa klasyczne eksperymenty z mechaniki kwantowej:

1. stan Bell na 2 qubitach,
2. stan GHZ na wielu qubitach.

W praktyce robimy tak:
- tworzymy obwód kwantowy,
- dodajemy bramki,
- uruchamiamy go na backendzie IBM Quantum,
- mierzymy różne obserwable,
- rysujemy wyniki.

To jest prosty i dobry pierwszy przykład z Qiskit.

---

## 2. Najpierw: co to jest bit?

Normalny bit w komputerze może być tylko w jednym z dwóch stanów:
- 0
- 1

To jest bardzo proste i klasyczne.

### 2.1 Co to jest qubit?

Qubit jest jak bit, ale ma jedną bardzo ważną różnicę:
- nie musi być tylko w stanie 0 albo 1,
- może być w superpozycji.

Superpozycja znaczy mniej więcej:
- qubit jest „jednocześnie” w stanie 0 i 1,
- aż do momentu pomiaru.

Po pomiarze dostajesz konkretny wynik:
- 0 albo 1,
- z pewnym prawdopodobieństwem.

Czyli qubit jest bardziej „prawdopodobieństwowy” niż klasyczny bit.

---

## 3. Co to są bramki kwantowe?

Bramki kwantowe to operacje, które zmieniają stan qubitów.

W tym skrypcie są najważniejsze dwie:
- H (Hadamard)
- CX (CNOT)

### 3.1 Bramka H

Bramka H odpowiada za superpozycję.

Działa tak:

H|0> = (|0> + |1>) / sqrt(2)
H|1> = (|0> - |1>) / sqrt(2)

Czyli:
- z |0> robi coś w rodzaju „0 i 1 naraz”,
- a z |1> też robi superpozycję.

W praktyce:
- po H qubit nie ma jeszcze konkretnej wartości,
- dopiero przy pomiarze dostajesz 0 albo 1.

### 3.2 Bramka CNOT

CNOT działa na dwa qubity.

Jeden qubit jest kontrolny, drugi jest celem.

Jeśli kontrolny qubit jest równy 1, to cel jest odwracany:
- 0 -> 1
- 1 -> 0

Przykład:
- stan |10> zamienia się w |11>
- stan |00> pozostaje |00>

To jest bardzo ważne, bo CNOT tworzy splątanie.

---

## 4. Co to jest splątanie?

Splątanie jest najważniejszym pojęciem w mechanice kwantowej.

To sytuacja, gdzie dwa qubity są ze sobą tak powiązane, że nie da się opisać ich osobno.

Najprościej:
- jeśli zmierzysz jeden qubit, od razu wiesz coś o drugim,
- nawet jeśli są bardzo daleko od siebie.

To nie jest klasyczna zależność typu „to było ustalone wcześniej”.

To jest coś zupełnie innego.

### 4.1 Przykład intuicyjny

Wyobraź sobie dwa żetony, które są splątane.

Gdy mierzymy pierwszy, to drugi od razu przyjmuje odpowiedni stan.

To nie jest magia, tylko konsekwencja matematyki mechaniki kwantowej.

---

## 5. Co to jest stan Bell?

Stan Bell to najbardziej klasyczny stan splątany dla 2 qubitów.

Ma postać:

|Φ+> = (|00> + |11>) / sqrt(2)

To znaczy:
- albo oba qubity są w stanie 00,
- albo oba qubity są w stanie 11,
- ale nie wiadomo, który przypadek jest prawdziwy, dopóki nie mierzymy.

Po pomiarze:
- jeśli pierwszy qubit daje 0, to drugi da 0,
- jeśli pierwszy qubit daje 1, to drugi da 1.

To jest właśnie splątanie.

### 5.1 Skąd ten stan się bierze w kodzie?

W skrypcie:

```python
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
```

To robi dokładnie:
1. tworzy 2 qubity,
2. wykonuje H na qubicie 0,
3. wykonuje CNOT z qubitu 0 na qubit 1,
4. dzięki temu otrzymujemy stan Bell.

---

## 6. Co to jest stan GHZ?

GHZ to uogólnienie Bell na więcej qubitów.

Dla 3 qubitów wygląda to tak:

|GHZ_3> = (|000> + |111>) / sqrt(2)

Dla n qubitów:

|GHZ_n> = (|0...0> + |1...1>) / sqrt(2)

Czyli:
- albo wszyscy qubity są 0,
- albo wszyscy qubity są 1,
- ale nie wiemy, który przypadek jest prawdziwy, dopóki nie zrobimy pomiaru.

To jest silne, globalne splątanie wielu qubitów.

---

## 7. Co to są obserwable?

Obserwable to operatory, które reprezentują wielkości mierzalne.

Przykłady wielkości mierzalnych:
- spin,
- energia,
- polaryzacja,
- magnetyzacja.

W Qiskit obserwable zapisujemy najczęściej jako napisy typu:
- `Z`
- `X`
- `Y`
- `I`

I łączymy je w operatory:
- `ZZ`
- `XX`
- `ZI`
- `IZ`
- `IX`
- `XI`

### 7.1 Co to oznacza `ZZ`?

`ZZ` oznacza: zmierz operator Z na pierwszym qubicie i Z na drugim qubicie.

Czyli w praktyce:
- mierzymy czy qubity są skorelowane w bazie Z.

### 7.2 Co to oznacza `IX`?

`IX` oznacza:
- I na pierwszym qubicie,
- X na drugim qubicie.

Czyli mierzymy X na drugim qubicie, a pierwszy pozostawia bez zmiany.

### 7.3 Dlaczego używa się tych napisów?

Bo Qiskit zapisuje obserwable jako operatory Pauliego w bardzo wygodny sposób.

Nie trzeba się przejmować tym, że to są duże macierze — Qiskit robi to za Ciebie.

---

## 8. Co to jest `SparsePauliOp`?

`SparsePauliOp` to klasa z Qiskit, która pozwala reprezentować operatory typu:
- `Z`
- `X`
- `Y`
- `ZZ`
- `XX`
- `IZ`

W kodzie jest to:

```python
observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
observables = [SparsePauliOp(label) for label in observables_labels]
```

Czyli:
- bierzemy napisy z operatorami,
- zamieniamy je na obiekty Qiskit,
- potem przekazujemy je do `Estimator`.

---

## 9. Co robi ten kod z Bell?

To jest dokładnie ten fragment:

```python
# Create a new circuit with two qubits
qc = QuantumCircuit(2)

# Add a Hadamard gate to qubit 0
qc.h(0)

# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)
```

Działa to tak:

1. tworzy 2 qubity,
2. robi H na qubicie 0,
3. robi CNOT z qubitu 0 do qubitu 1,
4. dzięki temu otrzymujemy stan Bell.

---

## 10. Co to jest `qc.draw("mpl")`?

To po prostu rysuje schemat obwodu.

Widzisz wtedy:
- H na pierwszym qubicie,
- CNOT między tymi qubitami.

To pomaga zobaczyć, co dokładnie budujesz.

---

## 11. Co robi `generate_preset_pass_manager`?

To jest bardzo ważna linia:

```python
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
```

Działa to tak:
- bierze twój obwód,
- przygotowuje go do konkretnego backendu IBM,
- mapuje qubity na fizyczne qubity,
- optymalizuje obwód,
- zamienia go do formatu, który da się uruchomić na realnym sprzęcie.

To nazywa się transpile.

### 11.1 Czym jest transpile?

Transpile to proces przekształcania obwodu kwantowego do wersji kompatybilnej z konkretnym backendem.

Dlaczego to potrzebne?
- bo każdy komputer kwantowy ma inną topologię qubitów,
- inne połączenia pomiędzy nimi,
- różne ograniczenia sprzętowe.

Czyli to jest jak „przerobienie programu na wersję pod konkretny komputer”.

---

## 12. Co robi `Estimator`?

To jest kluczowa linia:

```python
estimator = Estimator(mode=backend)
job = estimator.run([(isa_circuit, mapped_observables)])
```

`Estimator` liczy wartości oczekiwane operatorów dla danego obwodu.

Czyli:
- pyta: „jaki jest wynik pomiaru dla tych obserwabli?”
- a odpowiedź jest w postaci wartości oczekiwanych.

### 12.1 Co to są `evs` i `stds`?

Po `job.result()` dostajesz wyniki:

```python
values = pub_result["evs"]
errors = pub_result["stds"]
```

`evs` = expected values = wartości oczekiwane,
`stds` = standard deviations = błędy standardowe / rozrzut.

Najprościej:
- `evs` = średni wynik pomiaru,
- `stds` = jak bardzo wyniki były rozproszone.

---

## 13. Co robi `job.result()[0]`?

To po prostu pobiera wynik z zadania.

W skrypcie mamy:

```python
job_result = job.result()
pub_result = job.result()[0]
```

Czyli:
- `job_result` to wynik całego zadania,
- `pub_result` to wynik pierwszego zestawu danych,
- w naszej sytuacji są to wartości dla obserwabli.

---

## 14. Co to są te napisy `IZ`, `IX`, `ZI`, `XI`, `ZZ`, `XX`?

To są obserwable,
czyli operatory pomiarowe.

Zapiszmy je po ludzku:

- `IZ` = Z na pierwszym qubicie, I na drugim,
- `IX` = I na pierwszym, X na drugim,
- `ZI` = Z na pierwszym, I na drugim,
- `XI` = X na pierwszym, I na drugim,
- `ZZ` = Z na obu qubitach,
- `XX` = X na obu qubitach.

To są różne „sposoby patrzenia” na ten sam stan.

Dzięki temu widzimy, jak stan Bell zachowuje się w różnych bazach.

---

## 15. Co oznacza `X`, `Y`, `Z`?

To są operatory Pauliego, czyli podstawowe operatory w mechanice kwantowej.

Najprościej:
- `Z` mierzy „wartość” qubitu w bazie Z,
- `X` mierzy w bazie X,
- `Y` mierzy w bazie Y,
- `I` to identyczność, czyli „nie robimy nic” na danym qubicie.

W praktyce:
- te operatory są używane do pomiarów i do budowania obserwabli.

---

## 16. Co robi ten kod dla GHZ?

To jest ten fragment:

```python
def create_ghz_state_circuit(n: int) -> QuantumCircuit:
  if isinstance(n, int) and n >= 2:
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n - 1):
      qc.cx(i, i + 1)
  else:
    raise Exception("n is not a valid input")
  return qc
```

Co robi?
- tworzy `n` qubitów,
- wykonuje H na pierwszym qubicie,
- wykonuje serię CNOT: 0->1, 1->2, 2->3, ...
- w ten sposób powstaje stan GHZ.

To jest po prostu rozszerzenie Bell na więcej qubitów.

---

## 17. Co robią te stringi typu `"Z" + "I" * i + "Z" + "I" * (n - 2 - i)`?

To generuje operatory korelacji dla stanu GHZ.

Dla n = 5 może to dawać na przykład:
- `ZZIII`
- `IZZII`
- `IIZZI`
- `IIIZZ`

czyli patrzymy na pary qubitów i mierzymy, czy są skorelowane.

To pozwala sprawdzić, jak bardzo qubity są powiązane w zależności od odległości.

---

## 18. Dlaczego normalizujemy wyniki?

W tym fragmencie:

```python
values = [
    v / values[0] for v in values
]
```

Dzielimy wszystkie wyniki przez pierwszy wynik.

Dlaczego?
- żeby łatwiej porównywać kształt zależności,
- nie patrzeć tylko na wartość absolutną,
- zobaczyć, jak korelacja maleje wraz z odległością.

To jest po prostu normalizacja.

---

## 19. Co to znaczy „korelacja maleje z odległością”?

W stanie GHZ korelacja między qubitami jest silna.

Ale gdy qubity są dalej od siebie, to ich korelacja zwykle słabnie.

W praktyce narysowany wykres pokazuje, jak szybko to zachodzi.

To jest ważne, bo w prawdziwych układach kwantowych:
- błąd i dekoherencja mają wielki wpływ,
- więc korelacje nie zawsze są idealne.

---

## 20. Czym jest dekoherencja?

Dekoherencja to utrata spójności przez interakcję z otoczeniem.

Najprościej:
- qubit nie jest całkowicie odizolowany,
- ma kontakt z otoczeniem,
- przez to traci swoje kwantowe właściwości,
- i wyniki stają się mniej „idealne”.

W kodzie jest to:

```python
options.dynamical_decoupling.enable = True
options.dynamical_decoupling.sequence_type = "XY4"
```

To techniki redukujące wpływ dekoherencji.

---

## 21. Co robi `QiskitRuntimeService`?

To jest połączenie z IBM Quantum Runtime.

```python
QiskitRuntimeService.save_account(...)
service = QiskitRuntimeService()
```

Czyli:
- zapisuję dane logowania,
- potem łączę się z usługą IBM,
- wybieram backend dla eksperymentu.

### 21.1 Co robi `least_busy`?

```python
backend = service.least_busy(simulator=False, operational=True)
```

To wybiera najmniej obciążony działający backend.

Czyli:
- nie bierze symulatora,
- bierze urządzenie działające,
- wybiera to, które jest wolne.

---

## 22. Co to jest `QuantumCircuit`?

To jest główny obiekt Qiskit do budowania obwodów kwantowych.

Przykład:

```python
qc = QuantumCircuit(2)
```

Czyli: „stwórz obwód z 2 qubitami”.

Potem do niego dodajesz bramki:
- `qc.h(0)`
- `qc.cx(0, 1)`

To są operacje na qubitach.

---

## 23. Co to jest `plt.show()`?

To po prostu pokazuje wykres.

```python
plt.plot(...)
plt.show()
```

Bez tego wynik nie pojawi się na ekranie.

---

## 24. Co jest najważniejsze do zrozumienia?

Jeśli zapamiętasz tylko kilka rzeczy, to niech to będzie:

1. qubit jest jak bit, ale może być w superpozycji,
2. H robi superpozycję,
3. CNOT robi splątanie,
4. Bell to stan splątany dla 2 qubitów,
5. GHZ to Bell dla wielu qubitów,
6. obserwable to różne sposoby mierzenia tego stanu,
7. `Estimator` liczy wartości oczekiwane,
8. wykresy pokazują, jak te korelacje się zachowują.

---

## 25. Najprostsze wyjaśnienie całego skryptu w 5 zdaniach

1. Tworzymy 2 qubity i robimy na nich H oraz CNOT, żeby uzyskać stan Bell.
2. Potem mierzymy różne obserwable (`IZ`, `XX`, `ZZ` itd.), żeby zobaczyć, jak qubity są skorelowane.
3. Następnie tworzymy stan GHZ dla 100 qubitów, używając H i wielu CNOT-ów.
4. Mierzymy korelacje typu `Z_i Z_0` dla różnych odległości.
5. Wyniki pokazują, jak silnie splątanie działa i jak zmienia się ono w praktyce.

---

## 26. Podsumowanie

Ten skrypt jest bardzo dobrym pierwszym przykładem z Qiskit, bo pokazuje najważniejsze rzeczy od razu:
- qubit,
- bramki,
- splątanie,
- Bell,
- GHZ,
- pomiar obserwabli,
- transpile,
- backend IBM Quantum,
- wynik w postaci wykresu.

To jest dokładnie ten poziom, od którego zaczyna się zrozumienie kwantowych obwodów.

Jeśli chcesz, to mogę teraz zrobić jeszcze jedną wersję tego pliku:
- bardzo krótką, „na 1 stronę”,
- albo bardzo dokładną, „po linijce z komentarzem do każdego fragmentu kodu”.

To będzie już gotowe do nauki i bez stresu.
