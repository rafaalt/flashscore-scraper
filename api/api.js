const express = require('express');
const app = express();
const port = 3000;
const xlsx = require('xlsx');
const path = require('path');

app.use(express.json());

app.get('/', (req, res) => {
    res.send('Bem-vindo à API!');
});

// GET GAMES 

app.get('/jogos/:campeonato', (req, res) => {
    try {
        const league = req.params.campeonato
        const year = parseInt(req.query.year) || 2023
        const filePath = path.join(__dirname, `data/${league}_${year}.xlsx`);
        const workbook = xlsx.readFile(filePath);

        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];

        const data = xlsx.utils.sheet_to_json(sheet);
        var newData = data
        
        const team = req.query.team
        if (team) {
            teamName = normalizeString(team)
            newData = newData.filter(game => normalizeString(game.homeTeam) === teamName || normalizeString(game.awayTeam) === teamName)
        }

        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;

        const startIndex = (page - 1) * limit;
        const endIndex = page * limit;

        const paginatedData = newData.slice(startIndex, endIndex);

        res.json({
            currentPage: page, 
            totalPages: Math.ceil(newData.length / limit),
            totalItems: newData.length,
            itemsPerPage: limit,
            results: paginatedData
        });

    } catch (error) {
        console.error('Erro ao ler o arquivo XLSX:', error);
        res.status(500).json({ error: 'Erro ao ler o arquivo XLSX' });
    }
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});

// MARK: - FUNCTIONS

function normalizeString(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}