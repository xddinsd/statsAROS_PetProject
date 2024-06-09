# Оценка результатов призеров ВСОШ в следующем году

## Введение

Соревновательный дух и стремление к интеллектуальному развитию являются ключевыми аспектами Всероссийских школьных олимпиад. Эти мероприятия предоставляют уникальную возможность школьникам продемонстрировать свои знания и способности в различных научных областях. В данной работе я сосредоточился на изучении долгосрочных результатов дипломантов ВСОШ в течение двух лет: 2022-2023 и 2023-2024 годов. Моя цель - исследовать, оказывает ли статус призера либо победителя олимпиады влияние на академические достижения учащихся в следующем году.

## Методология

### Гипотезы
   
Призеры и победители прошлого года на олимпиаде, в сравнении с остальными участниками,
* **Первая гипотеза:** | будут показывать более высокие баллы.
   
* **Вторая гипотеза:**  | будут занимать более высокие места.

### Сбор данных

Для исследования были выбраны предметы: Экономика, Физика, Математика   
По годам: 21-22, 22-23. 23-24.   
Имеющиеся в открытых источниках данные были в формате pdf без возможности редактирования, поэтому были применен метод OCR([сайт](https://tools.pdf24.org/ru/ocr-pdf)) и написаны скрипты для парсинга и форматирования полученных txt-файлов.

### Выборка

Для анализа была выбрана когорта учащихся, ставших призерами либо победителями в прошлом учебном году, что сократило охватываемые в исследовании годы: 22-23, 23-24. Как контрольная группа были выбраны все остальные участники соревнования.     
   
* В рамках первой гипотезы я получил много разных выборок, которые нельзя объединять из-за разной разбалловки и количества участников в разных олимпиадах и классах.
* В рамках второй гипотезы данные проблемы были решены за счет метрики - перцениль участника. Данные были аггрегированы по результату участника в прошлом году.

### Инструменты анализа

Для тестирования гипотезы использовались следующие статистические тесты:

1. **Тест Шапиро-Уилка**: для проверки нормальности распределения полученных баллов.
2. **Тест Левена**: для проверки гомогенности дисперсий двух групп.
3. **T-тест Стьюдента и Z-тест**: для поиска статистически значимых различий между средними значениями двух групп при условии нормальности распределения и гомогенности дисперсий.
4. **Тест Колмогорова-Смирнова**: для сравнения функций распределения двух выборок.
5. **Для визуализации использовались графики:** scatterPlot, histPlot, QQPlot, Boxplot и график доверительных интервалов для средних, если проведен Т-Тест.
6. **Графики -> дашборд:** [Streamlit](https://statsarospetproject.streamlit.app/)

### Выводы

1) Для первой гипотезы анализ показал наличие статистически значимых различий для следующих выборок:
* Математика 22-23 в 10м и 11м классе
* Математика 23-24 в 10м и 11м классе
* Физика 22-23 в 11м классе
* Физика 23-24 в 10м и 11м классе
* Экономика 22-23 в 10м классе
* Экономика 23-24 в 10м и 11м классе   
2) Для второй гипотезы анализ показал p-уровень значимости для нулевой гипотезы менее 0.0001

## Результаты

1) **Первая гипотеза** демонстрирует статистическую достоверность для десяти из одиннадцати выборок при уровне значимости _alpha_=0,05.

	**Было установлено следующее:**
* Для групп математиков и экономистов все анализируемые выборки продемонстрировали статистическую значимость при проверке гипотезы.  
* __В группе физиков одна выборка из четырёх не статистическую значимость результатов.__ 
* Не была найдена какая-либо явная зависимость от года, в котором проводилась олимпиада, и класса участников.

2) **Вторая гипотеза статистически подтверждена**

## Обсуждение и заключение
В данном исследовании были проанализированы результаты ВСОШ призеров прошлых лет по математике, физике и экономике за 22-23 и 23-24 год.   
1) **Призеры в среднем действительно занимают более высокие места.** Это может быть связано с множеством факторов, которые было бы интересно дополнительно рассмотреть в последующих исследованиях.
2) **Гипотеза о более высоком среднем балле не была подтверждена.** Это может быть связано с маленьким объемом выборок, методами исследования и множеством дополнительных факторов, таких как влияние сложности в выбранном году регионального этапа и изменениям эффективности олимпиадных школ.


* Результаты наводят на мысль о возможном влиянии дополнительных факторов на успех участников в различные годы и по различным предметам. Эти наблюдения подчеркивают важность проведения более глубоких исследований, учитывающих разнообразные факторы, чтобы более точно определить причины различий в результатах участников.


---
