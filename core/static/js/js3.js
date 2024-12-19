// Função para redirecionar após 3 segundos
function redirecionarApos3Segundos(url) {
    setTimeout(() => {
        window.location.href = url;  
    }, 1000);  
}


document.addEventListener('DOMContentLoaded', () => {
    redirecionarApos3Segundos('/consultas/teste');  
});
