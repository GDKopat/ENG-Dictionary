import json,os,random,sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')



def is_file():
    if os.path.exists("dictionary.json"):   #Проверка на наличие файла словаря
        return True
    else:
        print("Файл словаря не найден. Выберите действие '1, для создания файла ")
        return False

def check_file():
    dat = {
    "some test word": "some test text",
    "bed": "кровать"

}

    if os.path.exists("dictionary.json"):   #Проверка на наличие файла словаря
        print("Файл словаря найден")
        with open("dictionary.json", "r") as f:
            file_data = f.read()
            print(file_data)

    else:
        print("Файл словаря не найден, создаём...")
        with open("dictionary.json", "w") as f:   #Создание файла словаря
            print("Файл успешно создан")
            json.dump(dat, f, ensure_ascii=False, indent=4)



def add_data_to_json():
    while True:
        key = str(input("Введите слово/словосочетание которое хотите добавить в словарь(если такой уже существует, он заменится на то что вы введете), \nЛибо 0 для отмены:  "))
        if key == "0":
            print("Выход из добавления слова/словосочетания")
            break

        value_to_key = str(input(f"Введите значения для '{key}': "))


        if is_file():
            #Открываем словарь для чтения
            
            with open("dictionary.json", "r") as f:
                data = json.load(f)

                #Добавляем новую пару
            data[key] = value_to_key

                #Сохраняем пару в словарь
            with open("dictionary.json", "w") as f:
                json.dump(data,f,ensure_ascii=False, indent=4)

            print(f"Ключ '{key}' со значением '{value_to_key}' добавлен!")
            print("Текущий словарь:", data)



def search_words_fisrt_bookva():
    if is_file():
        while True:
            words = []
            #Получаем первую букву на которую будем искать слова
            bookva = str(input("Введите букву, чтобы увидеть все слова на эту букву и их значения либо 0 для выхода: "))
            if not bookva:
                print("Введите букву!")

            elif bookva == "0":
                print("Выход из посика по букве.")
                break
            elif len(bookva) != 1:
                print("Длинна буквы не должна превышать 1 символ")
                pass

            with open("dictionary.json", "r") as f:
                data = json.load(f)
                key_list = list(data.keys()) #получаем список ключей
                
            for i in key_list: #проходимся по всему списку ключей
                if i[0].lower() == bookva.lower():
                    words.append(i)

            for word in words:#вывод всех ключей на букву и их значений
                print(f"{word} - {data[word]}")

            return words


def victorina_words():
    if is_file():
        statistika = []
        popitka = 1
        print("Это викторина слов...")

        while True:
            with open("dictionary.json", "r") as f:
                data = json.load(f)

            if len(data) < 4:
                print("В словаре слишком мало слов для викторины (нужно минимум 4)")
                break
            
            choise = str(input("\nВведите 0 для выхода или любую клавишу для игры: "))
            if choise == "0":
                print("Выход из викторины слов.")
                break


            keys = list(data.keys())
            rand_words = []

            #Выбираем 3 случайных разных слова
            while len(rand_words) < 3:
                random_word_temp = random.choice(keys)
                if random_word_temp not in rand_words:
                    rand_words.append(random_word_temp)

            #Правильное слово (загаданное)
            correct_word = random.choice(rand_words)
            correct_meaning = data[correct_word]

            #Получаем значения для вариантов ответов
            other_keys = [k for k in keys if k != correct_word]
            other_meanings = [data[k] for k in other_keys]

            #Выбираем 3 неправильных варианта
            wrong_meanings = random.sample(other_meanings, min(3, len(other_meanings)))

            #Создаем варианты ответов (1 правильный + 3 неправильных)
            variants = {
                "1": wrong_meanings[0] if len(wrong_meanings) > 0 else "Нет варианта",
                "2": wrong_meanings[1] if len(wrong_meanings) > 1 else "Нет варианта",
                "3": wrong_meanings[2] if len(wrong_meanings) > 2 else "Нет варианта",
                "4": correct_meaning
            }

            # Перемешиваем варианты
            variant_items = list(variants.items())
            random.shuffle(variant_items)
            variants = dict(variant_items)

            #Находим правильный номер варианта
            correct_number = None
            for num, meaning in variants.items():
                if meaning == correct_meaning:
                    correct_number = num
                    break

            #Выводим вопрос
            print("\n" + "=" * 50)
            print(f"{popitka} попытка. Вопрос: Что означает слово/словосочетание '{correct_word}'?")
            print("=" * 50)
            popitka += 1

            #Выводим варианты
            for num, meaning in variants.items():
                print(f"{num}. {meaning}")

            print("-" * 50)

            #Получаем ответ
            while True:
                answer = input("Ваш ответ (номер варианта): ")
                if answer in variants:
                    break
                print("Введите номер от 1 до 4!")

            #Проверяем
            if answer == correct_number:
                print(f"\nПРАВИЛЬНО! {correct_word} - {correct_meaning}")
                statistika.append(1)
            else:
                print(f"\nНЕПРАВИЛЬНО! Правильный ответ: {correct_number}. {correct_meaning}")
                statistika.append(0)

            print()

    sredn = 0
    all_attepts = len(statistika)
    for chis in statistika:
        sredn += chis

    if all_attepts > 0:
        naib_obsh_del = sredn / all_attepts
        print(f"Процент правильных попыток(от 0 до 1) = {naib_obsh_del}/1")
    else:
        print("Нет попыток для статистики.")



def delete_word_from_data():
    if is_file():
        words_list = search_words_fisrt_bookva()  #Сохраняем список слов

        if not words_list:  #Если нет слов на последнюю введенную букву
            print("Сначала найдите слова через поиск по букве")
            return

        choise = str(input("Введите слово/словосочетание которое хотите удалить: "))

        #Альтернатива: можно просто удалять по введенному слову без проверки
        chiose_two = str(input(f"Вы точно хотите удалить '{choise}' ? y or n: "))
        
        if chiose_two == "y":
            with open("dictionary.json", "r") as f:
                data = json.load(f)

            if choise in data:  #Проверяем, существует ли слово
                del data[choise]
                
                with open("dictionary.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"Слово '{choise}' удалено!")
            else:
                print(f"Слово '{choise}' не найдено в словаре!")

        elif chiose_two == "n":
            print("Отменено!")
        else:
            print("Неправильно введено y or n!")




def main():
    choises = {
        "1": lambda:check_file(),
        "2": lambda:add_data_to_json(),
        "3": lambda:search_words_fisrt_bookva(),
        "4": lambda:victorina_words(),
        "5": lambda:delete_word_from_data(),
    }
    while True:
        print("""
Привет! это словарь английских слов!
1 - Показать словарь
2 - Добавить/изменить   слово/словосочетание
3 - Найти слова/словосочетания по первой букве
4 - Викторина
5 - Удалить слово/словосочетание
0 - Выход""")
        choise = str(input("Введите действие: "))
        if choise in choises:
            choises[choise]()
        elif choise == "0":
            print("Пока!")
            break
        else:
            print("Нет такого варианта.")

main()
