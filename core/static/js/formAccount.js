function validateForm() {
    var name = document.getElementById("name_create").value;
    var razaoSocial = document.getElementById("razãoSocial_create").value;
    var email = document.getElementById("email_create").value;
    var password = document.getElementById("password_create").value;
    var endereco = document.getElementById("endereco_create").value;
    var cep = document.getElementById("cep_create").value;
    var telefone = document.getElementById("telefone_create").value;

    // Verifica se todos os campos estão preenchidos, exceto Razão Social
    if (name === "" || email === "" || password === "" || endereco === "" || cep === "" || telefone === "") {
        alert("Por favor, preencha todos os campos obrigatórios, exceto Razão Social.");
        return false;
    }

    // Verifica se o email possui o formato correto
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById("error_email").style.display ="block";
        document.getElementById("error_email").textContent = "Formato do email incorreto (seuemail@provedor.com)";        
        return false;
    }

    // Formata o CPF (assumindo que seja o campo "cep_create")
    // O código para formatar o CPF seria inserido aqui

    // Submete o formulário se todos os campos estiverem preenchidos e o email estiver em um formato válido
    document.getElementById("b-form").submit();
}

function formatarCEP() {
    var cepInput = document.getElementById("cep_create");
    var cepValue = cepInput.value.replace(/\D/g, ''); // Remove caracteres não numéricos
    var formattedCep = '';

    if (cepValue.length > 5) {
        formattedCep = cepValue.substr(0, 5) + '-' + cepValue.substr(5);
    } else {
        formattedCep = cepValue;
    }

    cepInput.value = formattedCep;
}

// Função para formatar o número de telefone
function formatarTelefone(input) {
    // Remover todos os caracteres não numéricos
    var telefone = document.getElementById("telefone_create");
    var numero = input.value.replace(/\D/g, '');
    
    // Verificar o tamanho do número para aplicar a formatação adequada
    if (numero.length === 11) {
      // Se o número tiver 11 dígitos, formatar como (XX) XXXXX-XXXX
      telefone.value = '(' + numero.substring(0, 2) + ') ' + numero.substring(2, 7) + '-' + numero.substring(7);
    } else if (numero.length === 10) {
      // Se o número tiver 10 dígitos, formatar como (XX) XXXX-XXXX
      telefone.value = '(' + numero.substring(0, 2) + ') ' + numero.substring(2, 6) + '-' + numero.substring(6);
    } else {
      // Caso contrário, manter o número original
      telefone.value = numero;
    }
  }




