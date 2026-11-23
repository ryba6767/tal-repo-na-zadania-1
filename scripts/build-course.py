"""Generuje osobne katalogi lekcji i publikację bez rozwiązań ani kartkówek."""
import argparse
import hashlib
import io
import json
import re
import shutil
import textwrap
import zipfile
from pathlib import Path

from content.foundations import LESSONS as FOUNDATIONS
from content.numbers import LESSONS as NUMBERS
from content.symbols_geometry import LESSONS as SYMBOLS
from content.files import SOURCE_FILES, EXERCISE_FILES
from content.matura_cards import simplify_matura_card

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT.parent / "prezentacja-python"
TEACHER = ROOT / "materialy-prowadzacego"
LESSONS = FOUNDATIONS + NUMBERS + SYMBOLS
ORGANIZATION = "00_organizacja_i_zasady_zajec.md"


def clean(text):
    return textwrap.dedent(text).strip()


def source_lines(text):
    return [line + "\n" for line in clean(text).splitlines()]


def directory_name(lesson):
    return f"{lesson['number']:02d}_{lesson['slug']}"


def input_names(lesson):
    number = lesson["number"]
    return [name for _, name in SOURCE_FILES.get(number, [])] + list(EXERCISE_FILES.get(number, {}))


def make_notebook(lesson, teacher=False):
    cells = []
    section_number = 0

    def block(title, body="", code=None, kind="theory"):
        nonlocal section_number
        section_number += 1
        sid = f"s{section_number:03d}"
        meta = {"section": sid, "title": title, "kind": kind}
        cells.append({
            "id": f"{lesson['number']:02d}-{sid}-md", "cell_type": "markdown",
            "metadata": {"presentation": meta},
            "source": source_lines(f"## {title}\n\n{clean(body)}")
        })
        if code is not None:
            cells.append({
                "id": f"{lesson['number']:02d}-{sid}-py", "cell_type": "code",
                "metadata": {"tags": [kind if kind != "theory" else "example"], "presentation": meta},
                "source": source_lines(code), "execution_count": None, "outputs": []
            })

    number = lesson["number"]
    intro = f"""# Karta pracy {number:02d}. {lesson['title']}

**Kurs:** Python — programowanie do matury rozszerzonej z informatyki

**Prowadzący:** por. Jakub GRĄTKIEWICZ · jakub.gratkiewicz@wat.edu.pl

**Cel:** {lesson['destination']}

Znasz podstawy Pythona. Przypominamy potrzebne narzędzia i stosujemy je w coraz bardziej złożonych zadaniach.

Otwórz ten notatnik w folderze bieżącej lekcji. W zadaniu plikowym samodzielnie napisz otwarcie pliku, odczyt, konwersję, obliczenia i zapis odpowiedzi. Nie ma wspólnej komórki wczytującej dane ani gotowych list z plików zadaniowych.

Zadania 1–8 wykonujemy na lekcji, zadania 9–10 samodzielnie. Niedokończone zadania uzupełnij przed następnym spotkaniem.

W komórkach roboczych wpisz własny kod. Podane testy są początkowo komentarzami: odkomentuj je po napisaniu rozwiązania i dodaj własne przypadki. Samo wykonanie pustej komórki nie oznacza rozwiązania zadania.

Przed oddaniem zrestartuj jądro, uruchom własne komórki od początku i zapisz notatnik oraz wymagane pliki wynikowe."""
    cells.append({
        "id": f"{number:02d}-intro", "cell_type": "markdown",
        "metadata": {"presentation": {"section": "intro", "title": "Cel i sposób pracy", "kind": "intro"}},
        "source": source_lines(intro)
    })
    names = input_names(lesson)
    file_text = ("Pliki wejściowe w katalogu tej lekcji:\n\n" +
                 "\n".join("- " + name for name in names) +
                 "\n\nPrzeczytaj format w poleceniu. Pliki otwierasz we własnym kodzie; "
                 "nie przepisuj ich zawartości do programu. Nazwy wyników są podane w zadaniach. "
                 "Zapisuj wyniki obok notatnika i nie nadpisuj danych wejściowych."
                 if names else
                 "Ta karta jest powtórzeniem na niewielkich danych zapisanych w poleceniach. "
                 "Nie wymaga zewnętrznych plików wejściowych. Zachowaj własny kod w katalogu tej lekcji.")
    block("Katalog lekcji i dane", file_text, kind="organization")
    block("1. Przypomnienie",
          "\n".join(f"{i}. {q}" for i, q in enumerate(lesson["recall"], 1)) +
          "\n\nTo pytania do wspólnego powtórzenia, nie zestaw kartkówki.",
          "# Własne odpowiedzi:\n# 1.\n# 2.\n# 3.", "recall")
    block("2. Treść dydaktyczna i zadania na lekcji",
          "Przypomnij potrzebne narzędzia, przeczytaj kontrakt funkcji i sam napisz rozwiązanie. "
          "W zadaniach z plikiem pamiętaj również o odczycie danych i wymaganym zapisie wyniku.")

    if lesson["official"]:
        official = (ROOT / "tresci-maturalne" / lesson["official"]).read_text(encoding="utf-8")
        # Oryginalny PDF leży także w folderze tej lekcji; link działa w Jupyter i w paczce lekcji.
        official = official.replace("materialy-zrodlowe/", "")
        chunks = re.split(r"(?=^### )", official, flags=re.M)
        for index, chunk in enumerate(chunks):
            title = ("Zadanie maturalne · źródło i zakres" if index == 0
                     else chunk.splitlines()[0].removeprefix("### ").strip())
            block(title, chunk, kind="matura")

    for index, task in enumerate(lesson["tasks"], 1):
        for theory in lesson["theories"]:
            if theory["before"] == index:
                block(theory["title"], theory["text"], theory["example"])
        if index == 9:
            block("Podsumowanie",
                  "Wyjaśnij jedno własne rozwiązanie i wskaż ważny przypadek brzegowy. "
                  "W zadaniu plikowym pokaż kod od otwarcia pliku do zapisania odpowiedzi.")
            block("3. Zadania do samodzielnego wykonania",
                  "Wykonaj zadania 9–10 przed następnym spotkaniem. Zapisz również własne testy.",
                  kind="homework")
        title = f"Zadanie {index}: {task['title'].removeprefix('Samodzielnie: ')}"
        starter = (f"# Zadanie {index}. Napisz własne rozwiązanie.\n\n"
                   "# Testy — odkomentuj po napisaniu kodu:\n" +
                   "\n".join("# " + line for line in task["tests"].splitlines()))
        block(title, task["prompt"] + "\n\n**Wskazówka:** " + task["hint"],
              starter, "exercise" if index <= 8 else "homework")

    if teacher:
        block("Rozwiązania — tylko dla prowadzącego",
              "Ta wersja nie jest publikowana na stronie ani w paczkach ucznia. "
              "Przykłady i rozwiązania uruchamiaj od początku w folderze tej karty. "
              "Uczeń sam pisze kod, w tym wczytywanie plików.", kind="solution")
        for index, task in enumerate(lesson["tasks"], 1):
            block(f"Rozwiązanie {index}: {task['title'].removeprefix('Samodzielnie: ')}",
                  "Kod wzorcowy i aktywne testy kontrolne.",
                  task["solution"] + "\n\n# Sprawdzenie\n" + task["tests"] +
                  f'\nprint("Testy zadania {index}: OK")', "solution")

    notebook = {
        "nbformat": 4, "nbformat_minor": 5, "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
            "course": {"number": number, "title": lesson["title"],
                       "variant": "teacher" if teacher else "student",
                       "class_tasks": 8, "homework_tasks": 2, "inputs": names}
        }
    }
    return notebook if teacher else simplify_matura_card(notebook)


def slide_sections(notebook):
    sections = []
    for cell in notebook["cells"]:
        p = cell["metadata"]["presentation"]
        if p["kind"] == "solution":
            continue
        raw = "".join(cell["source"]).strip()
        if cell["cell_type"] == "code":
            fence = chr(96) * 3
            raw = f"{fence}python\n{raw}\n{fence}"
        if sections and sections[-1]["id"] == p["section"]:
            sections[-1]["markdown"] += "\n\n" + raw
        else:
            sections.append(dict(id=p["section"], title=p["title"], kind=p["kind"],
                                 context="", markdown=raw))
    return sections


def organization_lesson():
    source = (ROOT / ORGANIZATION).read_text(encoding="utf-8")
    chunks = re.split(r"(?=^## )", source, flags=re.M)
    sections = []
    for i, chunk in enumerate(chunks):
        title = "Organizacja i zasady zajęć" if i == 0 else chunk.splitlines()[0][3:]
        sections.append(dict(id=f"org-{i}", title=title, kind="organization",
                             context="", markdown=chunk.strip()))
    return dict(number=0, kind="organization", title="Organizacja i zasady zajęć",
                sourceFile=ORGANIZATION, download=ORGANIZATION, assetBase="",
                sections=sections)


def write_notebook(path, notebook):
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
    path.write_text(encoded, encoding="utf-8")
    return hashlib.sha256(encoded.encode()).hexdigest()


def prepare_lesson_folder(lesson, folder):
    folder.mkdir(parents=True, exist_ok=True)
    assets = []
    for year, filename in SOURCE_FILES.get(lesson["number"], []):
        shutil.copy2(ROOT / "dane" / str(year) / filename, folder / filename)
        assets.append(folder / filename)
    for filename, contents in EXERCISE_FILES.get(lesson["number"], {}).items():
        (folder / filename).write_text(contents, encoding="utf-8")
        assets.append(folder / filename)
    if lesson["official"]:
        year = lesson["official"][:4]
        filename = f"arkusz-{year}.pdf"
        shutil.copy2(ROOT / "materialy-zrodlowe" / filename, folder / filename)
        assets.append(folder / filename)
    return assets


def write_archive(path, entries):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, relative in sorted(entries, key=lambda pair: pair[1]):
            entry = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, source.read_bytes())


def refresh_organization():
    """Odświeża tylko zasady, lekcję 0 i jej kopię w ZIP, nie zmieniając kart ani danych."""
    slides = SITE / "slides-data.js"
    archive_path = SITE / "kurs-python.zip"
    prefix = "window.PYTHON_COURSE = "
    source = slides.read_text(encoding="utf-8").strip()
    assert source.startswith(prefix)
    course = json.loads(source.removeprefix(prefix).removesuffix(";"))
    assert course["lessons"][0]["number"] == 0
    course["lessons"][0] = organization_lesson()
    course["meta"]["sectionCount"] = sum(len(l["sections"]) for l in course["lessons"])

    document = (ROOT / ORGANIZATION).read_bytes()
    target = "kurs-python/" + ORGANIZATION
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.namelist().count(target) == 1
        entries = [(info, archive.read(info)) for info in archive.infolist()]
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for info, contents in entries:
            archive.writestr(info, document if info.filename == target else contents)

    (SITE / ORGANIZATION).write_bytes(document)
    slides.write_text(prefix + json.dumps(course, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    archive_path.write_bytes(buffer.getvalue())
    print("Zaktualizowano zasady, lekcję 0 i kurs-python.zip. Karty i dane pozostały bez zmian.")


def main():
    SITE.mkdir(exist_ok=True)
    (SITE / "pobierz").mkdir(exist_ok=True)
    TEACHER.mkdir(exist_ok=True)
    shutil.copy2(ROOT / ORGANIZATION, SITE / ORGANIZATION)
    lessons = [organization_lesson()]
    public_entries = [(ROOT / "README.md", "kurs-python/README.md"),
                      (ROOT / ORGANIZATION, "kurs-python/" + ORGANIZATION)]
    for lesson in LESSONS:
        dirname = directory_name(lesson)
        folder = ROOT / dirname
        assets = prepare_lesson_folder(lesson, folder)
        notebook = make_notebook(lesson)
        card = folder / "karta_pracy.ipynb"
        checksum = write_notebook(card, notebook)
        guide = folder / "README.md"
        guide.write_text(
            f"# Lekcja {lesson['number']}. {lesson['title']}\n\n"
            "Otwórz karta_pracy.ipynb w Jupyter w tym katalogu. "
            "Nie korzystaj z kodu ani zmiennych uruchomionych w innej karcie.\n\n"
            + ("Pliki wejściowe:\n\n" + "\n".join("- " + n for n in input_names(lesson)) +
               "\n\nSam napisz otwarcie, odczyt i konwersję danych. Wyniki zapisuj obok notatnika "
               "pod nazwami z poleceń. Nie zmieniaj plików wejściowych.\n"
               if input_names(lesson) else "Ta lekcja nie wymaga zewnętrznych danych wejściowych.\n")
            + "\nPrzed oddaniem zrestartuj jądro i uruchom własny kod od początku.\n",
            encoding="utf-8")
        files = [card, guide, *assets]
        publish_folder = SITE / "lekcje" / dirname
        publish_folder.mkdir(parents=True, exist_ok=True)
        for file in files:
            shutil.copy2(file, publish_folder / file.name)
            public_entries.append((file, "kurs-python/" + dirname + "/" + file.name))
        write_archive(SITE / "pobierz" / f"{dirname}.zip",
                      [(file, dirname + "/" + file.name) for file in files])
        teacher_folder = TEACHER / dirname
        prepare_lesson_folder(lesson, teacher_folder)
        write_notebook(teacher_folder / "rozwiazania.ipynb", make_notebook(lesson, teacher=True))
        lessons.append({
            "number": lesson["number"], "kind": "lesson", "title": lesson["title"],
            "sourceFile": f"{dirname}/karta_pracy.ipynb",
            "notebook": f"lekcje/{dirname}/karta_pracy.ipynb",
            "download": f"pobierz/{dirname}.zip", "assetBase": f"lekcje/{dirname}/",
            "checksum": checksum, "sections": slide_sections(notebook)
        })
    course = {
        "meta": {
            "title": "Python — programowanie do matury rozszerzonej",
            "shortTitle": "Python · matura rozszerzona",
            "standard": "Powtórzenie i zadania maturalne · 12 lekcji",
            "teacher": "por. Jakub GRĄTKIEWICZ", "email": "jakub.gratkiewicz@wat.edu.pl",
            "lessonCount": 12, "sectionCount": sum(len(x["sections"]) for x in lessons),
            "taskCount": sum(len(x["tasks"]) for x in LESSONS)
        }, "lessons": lessons
    }
    (SITE / "slides-data.js").write_text(
        "window.PYTHON_COURSE = " + json.dumps(course, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8")
    # Jawna lista: nigdy nie publikujemy teacher/, źródła generatora ani dawnych kodów C++.
    write_archive(SITE / "kurs-python.zip", public_entries)
    print(f"Karty ucznia: 12, katalogi lekcji: 12, zadania: {course['meta']['taskCount']}.")
    print("Lekcja 0: zasady. Rozwiązania i kartkówki: wyłącznie materialy-prowadzacego.")
    print(f"Prezentacja: {SITE / 'index.html'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--organization-only", action="store_true",
                        help="aktualizuj tylko zasady, lekcję 0 i zasady w paczce ZIP")
    args = parser.parse_args()
    if args.organization_only:
        refresh_organization()
    else:
        main()
