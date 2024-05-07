function openModal() {
    document.getElementById('cadastroLancheModal').style.display = "block";
}

// Função para fechar o modal
function closeModal() {
    document.getElementById('cadastroLancheModal').style.display = "none";
}


function previewImages(event) {
    var preview = document.getElementById('imagePreview');
    preview.innerHTML = '';
    var files = event.target.files;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var reader = new FileReader();
        reader.onload = function (event) {
            var img = document.createElement('img');
            img.src = event.target.result;
            preview.appendChild(img);
        }
        reader.readAsDataURL(file);
    }
}


function formatPrice(input) {
    // Remove qualquer formatação existente
    let value = input.value.toString().replace(/\D/g, '');
    
    // Adiciona "R$" e formata o valor
    value = parseFloat(value / 100).toFixed(2);
    value = "R$" + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    
    // Atualiza o valor exibido no campo
    input.value = value;
}