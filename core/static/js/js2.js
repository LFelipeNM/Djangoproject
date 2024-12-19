// Função para redirecionar após 3 segundos
function redirecionarApos3Segundos(url) {
    setTimeout(() => {
        window.location.href = url;  // Usa o argumento 'url'
    }, 1000);  // 3000 milissegundos = 3 segundos
}

// Chame a função passando a URL desejada
document.addEventListener('DOMContentLoaded', () => {
    redirecionarApos3Segundos('/cadastro/123');  // Certifique-se de usar a barra inicial
});
