import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def roll_dice(n_rolls, n_dice, probs):
    rolls = np.random.choice([1,2,3,4,5,6], size=(n_rolls, n_dice), p=probs)
    return np.sum(rolls, axis=1)

# Настройка страницы
st.set_page_config(
    page_title="Симулятор бросков костей", 
    page_icon="🎲",
    layout="wide"
)

# Заголовок
st.title("🎲 Статистика бросков игральных костей")
st.markdown("""
*Исследование распределения случайных величин*  
ФИЗ-1, Университет ИТМО
""")

# Панель управления
with st.sidebar:
    st.header("Параметры")
    n_rolls = st.slider(
        "Количество бросков", 
        10, 10**6, 1000, 100,
        help="Увеличьте для более точных результатов"
    )
    n_dice = st.selectbox(
        "Количество костей", 
        [1, 2, 3, 4, 5], 
        index=0
    )
    bias_level = st.slider(
        "Неидеальность костей", 
        -0.1, 0.1, 0.0, 0.01,
        help="Смещение центра масс (0 = идеальная кость)"
    )
    
# Основная логика
def run_simulation():
    # Расчет вероятностей с учетом смещения
    p = 1/6 + bias_level
    p = max(0.0, min(1.0, p))
    remaining_prob = (1 - p)/5.0
    probs = [remaining_prob]*5 + [p]
    
    # Генерация данных
    data = roll_dice(n_rolls, n_dice, probs)
    
    # Расчет теоретических параметров
    faces = np.array([1,2,3,4,5,6])
    mean_per_die = np.sum(faces * probs)
    var_per_die = np.sum((faces - mean_per_die)**2 * probs)
    
    # Построение графика
    fig, ax = plt.subplots(figsize=(10,6))
    ax.hist(data, 
           bins=range(n_dice, 6*n_dice + 2), 
           density=True, 
           alpha=0.7, 
           label="Эксперимент")
    
    # Теоретическая кривая
    if n_dice == 1:
        ax.stem(faces, probs, linefmt='r-', markerfmt='ro', 
               basefmt=' ', label="Теория")
    else:
        x = np.linspace(n_dice, 6*n_dice, 1000)
        theory_mean = n_dice * mean_per_die
        theory_std = np.sqrt(n_dice * var_per_die)
        pdf = norm.pdf(x, theory_mean, theory_std)
        ax.plot(x, pdf, 'r-', linewidth=2, label="Нормальное распределение")
    
    ax.set_xlabel("Сумма очков" if n_dice > 1 else "Значение")
    ax.set_ylabel("Плотность вероятности")
    ax.legend()
    st.pyplot(fig)
    
    # Статистика
    st.subheader("Анализ результатов")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Экспериментальные значения**")
        st.metric("Среднее", f"{np.mean(data):.2f}")
        st.metric("Стандартное отклонение", f"{np.std(data):.2f}")
    
    with col2:
        st.markdown("**Теоретические значения**")
        st.metric("Ожидаемое среднее", f"{n_dice*mean_per_die:.2f}")
        st.metric("Ожидаемое отклонение", f"{np.sqrt(n_dice*var_per_die):.2f}")

# Запуск при нажатии кнопки
if st.sidebar.button("Запустить моделирование", type="primary"):
    with st.spinner("Выполняется симуляция..."):
        run_simulation()
    st.success("Готово!")

# Методические материалы
with st.expander("📚 Теоретическая справка"):
    st.markdown("""
    ### Статистические закономерности
    - **Одна кость**: Равномерное распределение
    - **Несколько костей**: Нормальное распределение (ЦПТ)
    - **Неидеальность**: Смещение вероятностей
    """)