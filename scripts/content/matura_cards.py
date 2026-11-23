"""Uproszczone karty maturalne: polecenia CKE i puste komórki na kod."""
import copy
import re


def simplify_matura_card(notebook):
    number = notebook["metadata"]["course"]["number"]
    if number not in {8, 10, 12}:
        return notebook
    result = copy.deepcopy(notebook)
    official = [cell for cell in result["cells"]
                if cell["cell_type"] == "markdown"
                and cell.get("metadata", {}).get("presentation", {}).get("kind") == "matura"]
    if not official:
        raise ValueError(f"Karta {number}: brak treści zadania maturalnego.")
    source_block = "".join(official[0]["source"])
    source_line = next(line for line in source_block.splitlines() if line.startswith("**Źródło:**"))
    source_line = source_line.replace("**Źródło:**", "**Zadanie maturalne:**", 1).rstrip()
    pdf_link = re.search(r"\[arkusz-\d+\.pdf\]\([^)]+\)", source_block).group(0)
    cells = []
    task_numbers = []
    result_files = []
    for cell in official[1:]:
        raw = "".join(cell["source"]).strip()
        parts = raw.split("\n\n", 1)
        if len(parts) == 2 and parts[1].startswith("### "):
            raw = parts[1]
        raw = re.sub(r"^### ", "## ", raw)
        raw = raw.split("\n\nDo oceny oddajesz:", 1)[0].rstrip() + "\n"
        result_files.extend(re.findall(r"\bwyniki\d+(?:_\d+)?\.txt\b", raw))
        title = raw.splitlines()[0].removeprefix("## ")
        task = re.match(r"Zadanie (\d+\.\d+)\.\s", title)
        cell["source"] = raw.splitlines(keepends=True)
        cell["metadata"]["presentation"]["title"] = title
        cell["metadata"]["presentation"]["kind"] = "exercise" if task else "matura"
        cells.append(cell)
        if task:
            task_numbers.append(task[1])
            cells.append({
                "id": cell["id"].removesuffix("-md") + "-py",
                "cell_type": "code",
                "metadata": {"tags": ["exercise"],
                             "presentation": copy.deepcopy(cell["metadata"]["presentation"])},
                "source": [], "execution_count": None, "outputs": []
            })
    expected = {8: 4, 10: 4, 12: 2}[number]
    if len(task_numbers) != expected:
        raise ValueError(f"Karta {number}: oczekiwano {expected} podpunktów, odczytano {len(task_numbers)}.")
    names = result["metadata"]["course"]["inputs"]
    results = ", ".join(f"`{name}`" for name in dict.fromkeys(result_files))
    title = {8: "Liczby", 10: "Zapis symboliczny", 12: "Dron"}[number]
    intro = f"""# Karta pracy {number:02d}. {title} — sprawdzenie wiadomości

**Kurs:** Python — programowanie do matury rozszerzonej z informatyki  
**Prowadzący:** por. Jakub GRĄTKIEWICZ · jakub.gratkiewicz@wat.edu.pl

{source_line}  
**Oryginalny arkusz:** {pdf_link}

Samodzielnie rozwiąż zadania {task_numbers[0]}–{task_numbers[-1]} w języku Python. Wpisz rozwiązania w pustych komórkach bezpośrednio pod poleceniami. Samodzielnie napisz również kod wczytujący dane i zapisujący odpowiedzi.

Pliki wejściowe znajdują się obok notatnika: {", ".join(f"`{name}`" for name in names)}.

Do oceny oddaj uzupełniony `karta_pracy.ipynb` z własnym kodem oraz plik {results} z odpowiedziami dla pełnych danych, poprzedzonymi numerami zadań. Przed oddaniem uruchom własny kod od początku i zapisz notatnik.
"""
    first = result["cells"][0]
    first["source"] = intro.splitlines(keepends=True)
    first["metadata"]["presentation"].update(title="Sprawdzenie wiadomości", kind="intro")
    result["cells"] = [first] + cells
    result["metadata"]["course"].update(class_tasks=expected, homework_tasks=0)
    return result
