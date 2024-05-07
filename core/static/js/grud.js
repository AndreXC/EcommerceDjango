

function createNotification(msg, type) {
    var alert = document.createElement('div');
    alert.classList.add('alert', 'hide');

    var iconClass = '';
    var bgColor = '';
    var borderColor = '';
    // Adapte o switch conforme necessário
    switch (type) {
        case 1: // Error
            iconClass = 'fa-times-circle';
            bgColor = '#e74c3c';
            break;
        case 2: // Warning
            iconClass = 'fa-exclamation-triangle';
            bgColor = '#f39c12';
            borderColor = '#d68910';
            break;
        case 3: // Pass
            iconClass = 'fa-check-circle';
            bgColor = '#2ecc71';
            borderColor = '#27ae60';
            break;
        default:
            iconClass = 'fa-info-circle';
            bgColor = '#3498db';
            borderColor = '#2980b9';
    }

    alert.innerHTML = `
        <img src="/static/img/seguranca.png" class="notify_icon"/>
        <i style ="position: relative; bottom: 10px; left: -3px;"class="fas ${iconClass}"></i>
        <span style ="position: relative; top: -9px; left: -3px;"class="msg">${msg}</span>
        <div class="close-btn">
            <i class="fas fa-times"></i>
        </div>
    `;  

    
    alert.style.top = "61px" 

    document.body.appendChild(alert);

    alert.classList.add("show");
    alert.classList.remove("hide");
    alert.classList.add("showAlert");
    window.addEventListener("scroll", function () {
        // Atualiza a posição vertical da notificação com uma transição suave
        alert.style.top = window.scrollY + "px";
    });

    setTimeout(function () {
        alert.classList.remove("show");
        alert.classList.add("hide");
        setTimeout(function () {
            document.body.removeChild(alert);   
        }, 1000); // Ajuste este tempo para combinar com a duração da animação hide_slide
    }, 5000);

    alert.querySelector('.close-btn').addEventListener('click', function () {
        alert.classList.remove("show");
        alert.classList.add("hide");    
        setTimeout(function () {
            document.body.removeChild(alert);
        }, 1000); // Ajuste este tempo para combinar com a duração da animação hide_slide
    });

}

function notifyProgram(msg, type) {
// Armazenar informações sobre a notificação
localStorage.setItem('notificationMsg', msg);
localStorage.setItem('notificationType', type);

// var element = document.getElementById('clientes-tables');
// var displayStyle = element.style.display;

// var element_download = document.getElementById('download-table');
// var displaydownload = element_download.style.display;

// // Armazenar o resultado da verificação no cache
// var shouldClickButton = (displayStyle !== 'none');
// var shouldClickdownload = (displaydownload !== 'none');

// caches.open('my-cache').then(function (cache) {
//     cache.put('shouldClickButton', new Response(shouldClickButton));
//     cache.put('shouldClickdownload', new Response(shouldClickdownload));
// });

var storedMsg = localStorage.getItem('notificationMsg');
var storedType = localStorage.getItem('notificationType');

if (storedMsg && storedType) {
    // Exibir a notificação após a reinicialização
    createNotification(storedMsg, parseInt(storedType));

    // Obter o valor da variável armazenada no cache
    caches.open('my-cache').then(function (cache) {
        cache.match('shouldClickButton').then(function (response) {
            if (response) {
                response.text().then(function (shouldClickButton) {
                    // Se a variável for `true`,
                    if (shouldClickButton === 'true') {
                        var buttonElement = document.getElementById('desh-user');
                        buttonElement.click();
                        setActive('desh-user');
                    }
                });
            }
        });

        cache.match('shouldClickdownload').then(function (response) {
            if (response) {
                response.text().then(function (shouldClickdownload) {
                    // Se a variável for `true`,
                    if (shouldClickdownload === 'true') {
                        var buttonElement_download = document.getElementById('desh-download');
                        buttonElement_download.click();
                        setActive('desh-download');
                    }
                });
            }
        });
    });

    // Limpar as informações armazenadas
    localStorage.removeItem('notificationMsg');
    localStorage.removeItem('notificationType');
}
}

// Verificar se há notificação armazenada após a reinicialização
// document.addEventListener('DOMContentLoaded', function () {

// });


function setActive(elementId) {
    const ulElement = document.querySelector('.side-menu');
    const activeLi = ulElement.querySelector('li.active');
    if (activeLi) activeLi.classList.remove('active');
    document.getElementById(elementId).classList.add('active');
    }


function atualizarTabela() {
    // Realiza uma requisição AJAX para a view Django que retorna os dados dos lanches
    $.ajax({
        url: '/updateTable',
        type: 'GET',
        success: function(data) {
            // Limpa a tabela
            $('table tbody').empty();
            
            // Preenche a tabela com os novos dados
            data.forEach(function(lanche) {
                var newRow = '<tr>' +
                    '<td><input style="display: none;" type="checkbox" class="cliente-checkbox" ' +
                    'data-id="' + lanche.id + '" ' +
                    'data-nome="' + lanche.nome + '" ' +
                    'data-preco="' + lanche.preco + '" ' +
                    'data-descricao="' + lanche.descricao + '" ' +
                    'data-quantidade="' + lanche.quantidade + '" ' +
                    'data-fotos="' + lanche.fotos + '"></td>' +
                    '<td><img src="/static/img/lanche1.png"></td>' +
                    '<td>' + lanche.id + '</td>' +
                    '<td>' + lanche.nome + '</td>' +
                    '<td>' + lanche.preco + '</td>' +
                    '<td>' + lanche.descricao + '</td>' +
                    '<td>' + lanche.quantidade + '</td>' +
                    '<td>' + lanche.fotos + '</td>' +
                    '</tr>';
                
                $('table tbody').append(newRow);
            });
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });

    
}




document.addEventListener('DOMContentLoaded', function () {
    var rows = document.querySelectorAll('tbody tr');

    rows.forEach(function (row) {
        row.addEventListener('click', function () {
            var checkbox = this.querySelector('.cliente-checkbox');
            checkbox.checked = !checkbox.checked; // Inverte o estado do checkbox
            toggleAnimation(checkbox, row); // Chama a função para adicionar/remover a classe na linha
            updateButtonVisibility(); // Atualiza a visibilidade dos botões
        });
    });

    function updateButtonVisibility() {
        var selectedClientes = document.querySelectorAll('.cliente-checkbox:checked');

        if (selectedClientes.length > 0) {
            var buttonContainer = document.querySelector('.icon-container');
            // Pelo menos um cliente selecionado, exibe os botões
            if (buttonContainer) {
                buttonContainer.style.display = 'flex';
            }

        } else {
            var buttonContainer = document.querySelector('.icon-container');
            // Nenhum cliente selecionado, oculta os botões
            if (buttonContainer) {
                buttonContainer.style.display = 'none';
            }
        }
    }

    function toggleAnimation(checkbox, row) {
        // Remove a classe de todas as linhas
        rows.forEach(function (otherRow) {
            otherRow.classList.remove('selected-row');
        });

        // Adiciona a classe à linha apenas se o checkbox estiver marcado
        if (checkbox.checked) {
            row.classList.add('selected-row');
        }
    }
    document.getElementById('delicon').addEventListener('click', function () {
        document.getElementById('loginModal').style.display = 'block';
    
        document.getElementById('loginForm').addEventListener('submit', function(event) {
            event.preventDefault();
    
            // Extrair dados de login e senha do formulário
            var login = document.getElementById('username_login').value;
            var senha = document.getElementById('password_login').value;
    
            // Fazer requisição AJAX para autenticação do usuário
            var authXhr = new XMLHttpRequest();
            authXhr.open('POST', '/ModalLogin');
            authXhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            authXhr.onload = function() {
                if (authXhr.status === 200) {
                    var response = JSON.parse(authXhr.responseText);
                    if (response.authenticated) {
                        document.getElementById('loginModal').style.display = 'none';
    
                        // Se as credenciais forem válidas, prosseguir com a lógica de exclusão dos clientes
                        var selectedClientes = getSelectedClientesData();
    
                        selectedClientes.forEach(function (user) {
                            // Fazer requisição AJAX para excluir o cliente
                            var deleteXhr = new XMLHttpRequest();
                            deleteXhr.open('POST', '/deleteAdmin');
                            deleteXhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                            deleteXhr.onload = function() {
                                if (deleteXhr.status === 200) {
                                    var deleteResponse = JSON.parse(deleteXhr.responseText);
                                    if (deleteResponse.success) {
                                        // Exclusão bem-sucedida
                                        console.log('Cliente excluído com sucesso!');
                                        window.location.href = '/succeedDelete';
                                        // notifyProgram('Cliente excluído com sucesso!', 2);
                                        // atualizarTabela();
                                    } else {
                                        // Erro ao excluir cliente
                                        notifyProgram('Erro ao excluir cliente:', 2);
                                        console.error('Erro ao excluir cliente:', deleteResponse.error);
                                    }
                                } else {
                                    // Erro de conexão
                                    console.error('Erro de conexão ao excluir cliente:', deleteXhr.status);
                                }
                            };
                            var params = 'cliente_id=' + encodeURIComponent(user.id); // Envia o ID do cliente
                            deleteXhr.send(params);
                        });
                    } else {
                        // Credenciais inválidas
                        createNotification("Usuário ou senha inválidos", 1);
                    }
                } else {
                    // Tratar erros de requisição, se necessário
                    createNotification("Erro de conexão", 1);
                }
            };
            var loginParams = 'username=' + encodeURIComponent(login) + '&password=' + encodeURIComponent(senha);
            authXhr.send(loginParams);
        });
    });
    
    
    
    
    
    // function excluirCliente(id_lanche) {
    //     var deleteXhr = new XMLHttpRequest();
    //     deleteXhr.open('POST', '/deleteAdmin'); // Defina a URL correta para a função no seu backend Django
    //     deleteXhr.setRequestHeader('Content-Type', 'application/json');
    //     deleteXhr.onload = function() {
    //         if (deleteXhr.status === 200) {
    //             // Lógica de exclusão concluída com sucesso
    //             notifyProgram('usuario exluido com id' + id_lanche + 'excluido com sucesso!', 2)
    //         } else {
    //             // Tratar erros de requisição, se necessário
    //             notifyProgram('erro', 1)

    //         }
    //     };
    //     deleteXhr.send(JSON.stringify({id_lanche: id_lanche}));
    // }
    

    function getSelectedClientesData() {
        var selectedClientes = document.querySelectorAll('.cliente-checkbox:checked');
        var selectedData = [];
    
        selectedClientes.forEach(function(checkbox) {
            selectedData.push({
                id: checkbox.getAttribute('data-id'),
                nome: checkbox.getAttribute('data-nome'),
                tipo: checkbox.getAttribute('data-tipo'),
                dataCriacao: checkbox.getAttribute('data-data-criacao'),
                endereco: checkbox.getAttribute('data-endereco'),
                cpf: checkbox.getAttribute('data-cpf'),
                telefone: checkbox.getAttribute('data-telefone'),
                email: checkbox.getAttribute('data-email')
            });
        });
                
        return selectedData;
    }
    
});

