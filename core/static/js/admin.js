// Função para definir um cookie
const setCookie = (name, value, days) => {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
};

// Função para obter o valor de um cookie
const getCookie = (name) => {
    const cookieName = `${name}=`;
    const cookieArray = document.cookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return null;
};

// Função para alternar o modo escuro
const toggleDarkMode = (darkModeOn) => {
    if (darkModeOn) {
        document.body.classList.add('dark');
        setCookie('darkMode', 'true', 365); // Definindo o cookie para durar 365 dias
    } else {
        document.body.classList.remove('dark');
        setCookie('darkMode', 'false', 365);
    }
};

// Verifica se o modo escuro está ativado no carregamento da página
window.addEventListener('DOMContentLoaded', () => {
    const isDarkMode = getCookie('darkMode') === 'true';
    if (isDarkMode) {
        toggleDarkMode(true);
        toggler.checked = true;
    }
});


const toggler = document.getElementById('theme-toggle');

if (toggler) {
    toggler.addEventListener('change', function () {
        toggleDarkMode(this.checked);
    });
} else {
    console.error("Elemento 'theme-toggle' não encontrado.");
}

// Função para verificar o tamanho da janela e realizar ações correspondentes
const checkWindowSize = () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
};

// Verifica o tamanho da janela ao carregar e redimensionar
window.addEventListener('DOMContentLoaded', checkWindowSize);
window.addEventListener('resize', checkWindowSize);

// Código existente para manipulação de links, barra de menu e botão de pesquisa permanece inalterado
const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});
