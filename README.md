# Оценка результатов призеров ВСОШ в следующем году




## TL;DR
Собрал данные и проанализировал гипотезу, используя Pandas, Scipy, Matplotlib \
Дашборд на Streamlit: https://statsarospetproject.streamlit.app/




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
