function corAleatoria() {
    const rand = Math.random(); // número entre 0 e 1

    if (rand < 0.48) return 'B';   // Preto 48%
    else if (rand < 0.96) return 'R'; // Vermelho 48%
    else return 'W';                // Branco 4%
}

module.exports = corAleatoria;