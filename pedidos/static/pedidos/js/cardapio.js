document.addEventListener('DOMContentLoaded', function () {
    const mesaId = mesaIdGlobal;
    const botoesAdicionar = document.querySelectorAll('.adicionar-carrinho');
    const contador = document.getElementById('contador-carrinho');
    const toastEl = document.getElementById('toast-msg');
    const toastBody = toastEl.querySelector('.toast-body');
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastEl);
    const form = document.getElementById('formCliente');

    // Função utilitária para CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Mostrar modal se o cliente ainda não se identificou
    if (!localStorage.getItem('clienteRegistrado')) {
        const clienteModal = new bootstrap.Modal(document.getElementById('clienteModal'));
        clienteModal.show();
    }


        // Envio do formulário do modal via AJAX
        if (form && btnContinuar) {
            btnContinuar.addEventListener('click', function () {
                const formData = new FormData(form);
        
                fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: formData
                })
                .then(response => {
                    if (!response.ok) throw new Error('Erro no servidor');
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'ok') {
                        localStorage.setItem('clienteRegistrado', 'true');
        
                        // Fecha o modal
                        bootstrap.Modal.getInstance(document.getElementById('clienteModal')).hide();
        
                        // Redireciona após 1 segundo
                        setTimeout(() => {
                            window.location.href = `/pedidos/mesa/${mesaId}/produtos/`;
                        }, 1000);
                    } else {
                        console.error('Erro ao registrar cliente:', data);
                    }
                })
                .catch(error => console.error('Erro ao salvar cliente:', error));
            });
        }
    

    // Lógica de adicionar produto ao carrinho
    botoesAdicionar.forEach(btn => {
        btn.addEventListener('click', function () {
            const produtoId = this.dataset.produtoId;
            const nomeProduto = this.closest('.card-body').querySelector('.card-title').textContent;

            fetch('/pedidos/adicionar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `produto_id=${produtoId}&mesa_id=${mesaId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.total_itens !== undefined) {
                    contador.textContent = data.total_itens;

                    // Atualiza o toast
                    toastBody.textContent = `"${nomeProduto}" adicionado com sucesso!`;
                    toastBootstrap.show();

                    // Anima o contador
                    contador.classList.add('animate__animated', 'animate__bounceIn');
                    setTimeout(() => {
                        contador.classList.remove('animate__animated', 'animate__bounceIn');
                    }, 1000);
                }
            })
            .catch(error => {
                console.error('Erro ao adicionar ao carrinho:', error);
            });
        });
    });
});
