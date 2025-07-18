document.addEventListener('DOMContentLoaded', () => {
    // Referencias al DOM
    const searchInput = document.getElementById('search-input');
    const categoryFiltersContainer = document.getElementById('category-filters');
    const faqContainer = document.getElementById('faq-accordion-container');
    const rankingList = document.getElementById('faq-ranking-list');
    const paginationContainer = document.getElementById('pagination-container');
    const startTestBtn = document.getElementById('start-test-mode');
    const testModeContainer = document.getElementById('test-mode-container');
    const testQuestionArea = document.getElementById('test-question-area');
    const testQuestionEl = document.getElementById('test-question');
    const testAnswerEl = document.getElementById('test-answer');
    const showAnswerBtn = document.getElementById('show-answer-btn');
    const correctBtn = document.getElementById('correct-btn');
    const incorrectBtn = document.getElementById('incorrect-btn');
    const testResultsArea = document.getElementById('test-results-area');
    const testResultsList = document.getElementById('test-results-list');
    const restartTestBtn = document.getElementById('restart-test-btn');

    let allFaqs = [];
    let displayedFaqs = []; // FAQs después de aplicar filtros
    let currentPage = 1;
    const itemsPerPage = 10;

    let categories = [
        { id: 0, name: 'Institucional' },
        { id: 1, name: 'Programación' },
        { id: 2, name: 'Ciencia de Datos' },
        { id: 3, name: 'IA' },
        { id: 4, name: 'Estadística' },
        { id: 5, name: 'Inteligencia del Negocio' },
    ];
    let testState = { active: false, questions: [], currentIndex: 0, results: [] };

    // **Función para normalizar texto (ignorar acentos y puntuación)**
    const normalizeText = (text) => {
        if (!text) return '';
        return text
            .toLowerCase()
            .normalize('NFD') // Descompone acentos: 'á' -> 'a' + '´'
            .replace(/[\u0300-\u036f]/g, '') // Elimina los diacríticos
            .replace(/[¿¡.,;]/g, ''); // Elimina signos de puntuación comunes
    };
    
    function getCategoryNameById(id) {
        const category = categories.find(cat => cat.id === id);
    return category ? category.name : '';
    }

    const renderFaqs = () => {
        faqContainer.innerHTML = '';
        if (displayedFaqs.length === 0) {
            faqContainer.innerHTML = `<p class="text-gray-500">No se encontraron preguntas. Intenta con otra búsqueda.</p>`;
            renderPagination(); // Limpiar paginación si no hay resultados
            return;
        }

    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedItems = displayedFaqs.slice(startIndex, endIndex);
                
    paginatedItems.forEach(faq => {
        const faqElement = document.createElement('div');
        faqElement.className = 'border border-gray-200 dark:border-gray-700 rounded-lg';
        // **Contenido del acordeón movido a un div interno para un colapso limpio**
        faqElement.innerHTML = `
            <button class="accordion-header w-full text-left p-4 font-semibold flex justify-between items-center">
                <span>${faq.pregunta}</span>
                <i class="fas fa-chevron-down transition-transform"></i>
            </button>
            <div class="accordion-content-faq">
                <div class="p-4">
                    <p>${faq.respuesta}</p>
                    <div class="mt-2 text-xs text-gray-500">Categorías: ${getCategoryNameById(faq.categoria)}</div>
                </div>
            </div>
        `;
        faqContainer.appendChild(faqElement);
    });
    renderPagination();
};
            
const renderPagination = () => {
    paginationContainer.innerHTML = '';
    const totalPages = Math.ceil(displayedFaqs.length / itemsPerPage);

    if (totalPages <= 1) return; // No mostrar si hay 1 página o menos

    paginationContainer.innerHTML = `
        <button id="prev-page-btn" class="pagination-btn bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors">&laquo; Anterior</button>
        <span class="text-gray-700 dark:text-gray-300">Página ${currentPage} de ${totalPages}</span>
        <button id="next-page-btn" class="pagination-btn bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 transition-colors">Siguiente &raquo;</button>
    `;

    const prevBtn = document.getElementById('prev-page-btn');
    const nextBtn = document.getElementById('next-page-btn');

    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;

    prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderFaqs();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderFaqs();
        }
    });
};

const renderRanking = async (allFaqsData) => {
    try {
        const response = await fetch('/get_faq_ranking');
        const rankingData = await response.json();
        
        const sortedIds = Object.keys(rankingData).sort((a, b) => rankingData[b] - rankingData[a]).slice(0, 5);
        
        rankingList.innerHTML = '';
        sortedIds.forEach(id => {
            const faq = allFaqsData.find(f => f.id == id);
            if (faq) {
                const li = document.createElement('a');
                li.href = "#"; // Podría ser un enlace al ancla de la pregunta
                li.className = 'block p-2 rounded hover:bg-gray-50 ';
                li.textContent = faq.pregunta;
                rankingList.appendChild(li);
            }
        });
    } catch (error) {
        rankingList.innerHTML = `<p class="text-red-500 text-xs">No se pudo cargar el ranking.</p>`;
        console.error('Error fetching ranking:', error);
    }
};

const renderCategoryFilters = () => {
    categoryFiltersContainer.innerHTML = `<button class="category-tag py-1 px-3 rounded-full border bg-indigo-600 text-white" data-category="all">Todas</button>`;
    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'category-tag py-1 px-3 rounded-full border hover:bg-indigo-500 hover:text-white';
        btn.dataset.category = cat.id;
        btn.textContent = cat.name;
        categoryFiltersContainer.appendChild(btn);
    });
};

const handleFilterAndSearch = () => {
    const searchTerm = normalizeText(searchInput.value);
    const activeBtnCategory = document.querySelector('.category-tag.active');
    const activeCategoryId = activeBtnCategory?.dataset.category || 'all';

    let filteredFaqs = allFaqs;
    if (activeCategoryId !== 'all') {
        filteredFaqs = filteredFaqs.filter(faq => (faq.categoria === parseInt(activeCategoryId, 10)));
    }

    if (searchTerm) {
        filteredFaqs = filteredFaqs.filter(faq => 
            normalizeText(faq.pregunta).includes(searchTerm) || 
            normalizeText(faq.respuesta).includes(searchTerm)
        );
    }
    
    displayedFaqs = filteredFaqs;
    currentPage = 1; // **Resetear a la primera página con cada nueva búsqueda**
    renderFaqs();
};

const startTest = () => {
    testState.active = true;
    
    // **Filtro para excluir preguntas con ID < 99**
    const testableFaqs = allFaqs.filter(faq => parseInt(faq.id, 10) >= 99);
    
    // Si no hay preguntas para el test, muestra un mensaje y detiene la función
    if (testableFaqs.length === 0) {
        testModeContainer.classList.remove('hidden');
        testQuestionArea.classList.add('hidden');
        testResultsArea.classList.remove('hidden');
        testResultsList.innerHTML = '<p>No hay preguntas disponibles para el modo test.</p>';
        return;
    }

    testState.questions = [...testableFaqs].sort(() => 0.5 - Math.random());
    testState.currentIndex = 0;
    testState.results = [];

    testModeContainer.classList.remove('hidden');
    testQuestionArea.classList.remove('hidden');
    testResultsArea.classList.add('hidden');

    displayNextTestQuestion();
};

const displayNextTestQuestion = () => {
    // will show max of 10 questions
    if (testState.currentIndex < 10) {
        const currentQuestion = testState.questions[testState.currentIndex];
        testQuestionEl.textContent = currentQuestion.pregunta;
        testAnswerEl.innerHTML = currentQuestion.respuesta;
        testAnswerEl.classList.add('hidden');
        showAnswerBtn.textContent = 'Ver Respuesta';
    } else {
        endTest();
    }
};

const endTest = () => {
    testState.active = false;
    testQuestionArea.classList.add('hidden');
    testResultsArea.classList.remove('hidden');
    testResultsList.innerHTML = '';

    // show the score
    const correctAnswers = testState.results.filter(r => r.correct).length;
    const totalQuestions = 10;
    const score = totalQuestions > 0 ? (correctAnswers / totalQuestions) * 100 : 0;

    const summary = document.createElement('div');
    summary.innerHTML = `
        <p class="font-bold text-lg">Test finalizado</p>
        <p>Tu puntaje: <span class="font-bold text-2xl ${score >= 60 ? 'text-green-500' : 'text-red-500'}">${score.toFixed(0)}%</span> (${correctAnswers} de ${totalQuestions} correctas)</p>
        <hr class="my-3">
    `;
    testResultsList.appendChild(summary);

    // Mostrar un resumen de las respuestas
    testState.results.forEach(result => {
        const resultEl = document.createElement('div');
        resultEl.className = 'p-2 rounded mb-2';
        resultEl.innerHTML = `
            <p class="font-semibold">${result.question}</p>
            <p class="${result.correct ? 'text-green-500' : 'text-red-500'}">${result.correct ? '✅ Respondiste bien' : '❌ No sabías'}</p>
        `;
        testResultsList.appendChild(resultEl);
    });
};
        
const handleTestAnswer = (isCorrect) => {
    const currentQuestion = testState.questions[testState.currentIndex];

    // Guardar el resultado
    testState.results.push({
        question: currentQuestion.pregunta,
        correct: isCorrect
    });

    testState.currentIndex++;
    displayNextTestQuestion();
};

const init = async () => {
    try {
        const response = await fetch('/get_faq');
        allFaqs = await response.json();
        displayedFaqs = [...allFaqs]; // Inicialmente mostrar todas
        renderFaqs();
        renderCategoryFilters();
        await renderRanking(allFaqs);
    } catch (error) {
        faqContainer.innerHTML = `<p class="text-red-500">Error al cargar las preguntas frecuentes.</p>`;
    }
};

searchInput.addEventListener('input', handleFilterAndSearch);
categoryFiltersContainer.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
        document.querySelectorAll('.category-tag').forEach(btn => {
            btn.classList.remove('active', 'bg-indigo-600', 'text-white');
            // Restaurar estilo por defecto
            if (!document.body.classList.contains('dark-mode')) {
                    btn.classList.add('hover:bg-indigo-500', 'hover:text-white');
            }
        });
        e.target.classList.add('active', 'bg-indigo-600', 'text-white');
        e.target.classList.remove('hover:bg-indigo-500', 'hover:text-white');
        handleFilterAndSearch();
    }
});

    faqContainer.addEventListener('click', (e) => {
        const header = e.target.closest('.accordion-header');
        if (header) {
            header.classList.toggle('active');
            header.querySelector('i').classList.toggle('rotate-180');
        }
    });
    startTestBtn.addEventListener('click', startTest);
    showAnswerBtn.addEventListener('click', () => {
        testAnswerEl.classList.toggle('hidden');

        if (testAnswerEl.classList.contains('hidden')) {
            showAnswerBtn.textContent = 'Ver Respuesta';
        } else {
            showAnswerBtn.textContent = 'Ocultar Respuesta';
        }
    });

    correctBtn.addEventListener('click', () => handleTestAnswer(true));
    incorrectBtn.addEventListener('click', () => handleTestAnswer(false));
    restartTestBtn.addEventListener('click', startTest);

    init();
});