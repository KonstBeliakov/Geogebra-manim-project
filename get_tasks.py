import zipfile, io, fitz  # fitz = PyMuPDF
import re, json, requests

# Скачиваем архив
URL = "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_7.zip"
with zipfile.ZipFile(io.BytesIO(requests.get(URL).content)) as zf:
    tasks = []
    for name in zf.namelist():
        if name.endswith(".pdf"):
            pdf_data = zf.read(name)
            doc = fitz.open(stream=pdf_data, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            # Очищаем текст
            text = re.sub(r"\n{2,}", "\n", text.strip())

            # Пытаемся вытащить задачи (например, по ключевым словам "Task", "Problem", "Exercise" и пр.)
            if any(word in text for word in ["Task", "Problem", "Exercise"]):
                tasks.append({"title": name, "text": text})

# Сохраняем задачи
with open("tasks_from_pdf.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, ensure_ascii=False, indent=2)

print(f"Извлечено {len(tasks)} задач")
