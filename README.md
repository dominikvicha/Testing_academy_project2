
# Testing_academy_projekt2
# 2 - Upgrade of Task Manager
- Autor: Vícha Dominik 
- discord: Dominik V
- email: dominik.vicha@gmail.com

### Project description 
- upgraded version of the Task manager (project 1 - https://github.com/dominikvicha/Task-manager-.git ) 
- tasks are not saved in the memory but saved in the MySQL database
- things you can do with the tasks: 
    - add task
    - show task
    - update task
    - delete task
- second part is to create a tests via pytest
- the second table is created with same structure as the existing one
- there are two main files:
   - main.py - python code
   - test_main.py - testing in python 
  
### Requiremts ###
- You need to install the Testing framework - Pytest.
- The official documentation is here: https://docs.pytest.org/en/stable/
- MySQL Workbench 

### How to start the tests ###
- Start it by:
- test_main.py
- pytest              (you can see just the "." it means passed.) 
  
- If this doesnt work, make sure you have the right path for the main.py file, for example: pytest  python/python_learning/test_main.py
 
### Ouput data ###
- output data are in the terminal window

### If anything feel free to message me. :) ###

### Summary of project ###
### Pozitiva: ###
### Aplikace ### 
### Funkcionalita ###
- Pokrýváš všechny hlavní operace CRUD.
- Aplikace je interaktivní, vstupy jsou kontrolované a uživatelsky přívětivé.
- Přidání ENUM typu pro stav úkolu je vynikající volba, tím omezuješ možné hodnoty a zjednodušuješ logiku.
- Struktura a modularita
- Kód je rozdělený do jednotlivých funkcí s jasným účelem.
- Funkce jako aktualizovat_ukol a odstranit_ukol mají možnost předat vlastní připojení (conn), což zvyšuje opětovnou použitelnost.
- Používáš try-except-finally, což přispívá ke stabilitě.
- Technické drobnosti
- Používáš datetime.date.today() pro vložení dne vytvoření.
- Validace vstupů (isdigit, strip, lower) je systematická.
- Správně používáš parametrizované dotazy (%s), což chrání proti SQL injection.
- Jasná komunikace se uživatelem.
- Výpisy úkolů jsou přehledné a formátované.
- Potvrzení před mazáním je velmi dobrý prvek.


### Testy ###

- Testuješ všechny klíčové funkce: pridat_ukol, aktualizovat_ukol, odstranit_ukol, a to jak pozitivní, tak negativní scénáře.
- Simuluješ uživatelský vstup přes monkeypatch, což je nejlepší přístup u aplikací, které používají input(). Ale určitě by bylo lepší mít inputy oddělené
- Izolace testů
- Každý test si vkládá a maže vlastní testovací data, což je výborná praxe.
- Nepředpokládáš žádný předchozí stav databáze → to je správně.
- Úklid po sobě
- Používáš DELETE FROM po testu, takže databáze nezůstává zaplněná testovacími daty.
- V negativních testech ověřuješ, že nedošlo ke změně.
- Testy jsou pojmenovány výstižně (positive, negative).
- Používáš assert, a v některých případech přidáváš i hlášku - to je bonus při ladění.


### Co by šlo vylepšit: ### 
### Aplikace

- Chybí uzavření cursoru:
- Nezavíráš kurzor (cursor.close()), to může vést k vyčerpání prostředků při delším běhu programu.
- Doporučuji používat with conn.cursor() as cursor: ten se zavře automaticky.
- Drobné opakování kódu:
- Např. výpis seznamu úkolů je použit víckrát - šlo by vyčlenit do zvláštní funkce vypis_ukoly().
- vytvoreni_tabulky je fajn, ale do produkce by měl být oddělen - ideálně samostatný skript nebo podmínka CREATE TABLE IF NOT EXISTS.
- Hodnoty jako 'nezahájeno', 'probíhá', 'dokončeno' můžeš definovat jako konstanty na začátku kódu:


### Testy ### 

- Ačkoli ověřuješ data v DB, mohl bys ověřit i výstupy na stdout (capsys fixture v pytestu), např. že se vypíše "Úkol byl úspěšně přidán"
- V některých testech znovu připojuješ databázi zbytečně: Například v test_aktualizovat_ukol_negative znovu voláš connect_test_db() místo použití stávajícího připojení.

### Závěrem:### 
- Velmi dobře navržený konzolový nástroj, který lze snadno rozšířit a udržovat. Máš velký potenciál rozvíjet ho dál. Skvělé testy pro databázový projekt. Pokud bys doplnil fixture, přidal - pokrytí chybových stavů tak by to bylo skvělé.

- Celkove hodnotím projekt pozitivně. Jsou zde oblasti, které lze zlepšit, ale z testerského hlediska skvělá práce. Projekt schvaluji.




