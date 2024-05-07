
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector('#searchModal input[type="search"]');
    const allLanches = document.querySelectorAll('.fruite-item');
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim().toLowerCase();
        allLanches.forEach(lanche => {
            const lancheNome = lanche.querySelector('.text-white').textContent.trim().toLowerCase();
            if (lancheNome.includes(searchTerm)) {
                lanche.style.display = 'block';
            } else {
                lanche.style.display = 'none';
            }
        });
    });
});