function corAleatoria() {
    const rand = Math.random(); // número entre 0 e 1
    //cores = ["vermelho", "preto", "branco"]
    if (rand < 0.48) return 'preto';   // Preto 48%
    else if (rand < 0.96) return 'vermelho'; // Vermelho 48%
    else return 'branco';                // Branco 4%
}

module.exports = corAleatoria;