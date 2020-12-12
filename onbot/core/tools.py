

def get_var(var: str, text: str):
    var = f"{var.lower()}."
    raws = text.splitlines()
    for raw in raws:
        if raw.lower().startswith(var):
            return raw[2:].strip()


def get_question(text: str):
    t_ru = "Выберите один ответ:"
    t_en = "Select one:"
    if t_ru in text:
        indx = text.index(t_ru)
    elif t_en in text:
        indx = text.index(t_en)
    else:
        return False
    return text[:indx].strip()
