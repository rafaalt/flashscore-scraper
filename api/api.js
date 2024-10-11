const express = require('express');
const app = express();
const port = 3000;
const xlsx = require('xlsx');
const path = require('path');
const fs = require('fs');

const tourneys = [
    "serieA",
    "serieB",
    "copaDoBrasil",
    "libertadores",
    "sulamericana"
]

const years = [
    2021, 2922, 2023
]

app.use(express.json());

// GET ALL GAMES

app.get('/', (req, res) => {
    const data = getGamesThisYear()
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;

    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;

    const paginatedData = data.slice(startIndex, endIndex);

    res.json({
        currentPage: page, 
        totalPages: Math.ceil(data.length / limit),
        totalItems: data.length,
        itemsPerPage: limit,
        results: paginatedData
    });
});

// GET GAMES BY TOURNEY 

app.get('/jogos/:campeonato', (req, res) => {
    try {
        const league = req.params.campeonato
        const year = parseInt(req.query.year) || 2023
        const filePath = path.join(__dirname, `data/${league}/${year}.xlsx`);
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
        const limit = parseInt(req.query.limit) || 20;

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

// SAVE GAME

app.post('/save', (req, res) => {
    try {
        const {
            id,
            homeTeam,
            homeTeamUrl,
            awayTeam,
            awayTeamUrl,
            scoreHome,
            scoreAway,
            pointsHome, 
            pointsAway,
            referee,
            stadium,
            capacity,
            public,
            date,
            time,
            country,
            round
        } = req.body;

        if (!id || 
            !homeTeam || 
            !homeTeamUrl || 
            !awayTeam || 
            !awayTeamUrl || 
            scoreHome === undefined || 
            scoreAway === undefined ||
            pointsHome === undefined ||
            pointsAway === undefined ||
            !date || 
            !time || 
            !country || 
            !round) {
            console.log(`ERRO: Todos os campos obrigatórios devem ser preenchidos`)
            return res.status(400).json({ error: 'Todos os campos obrigatórios devem ser preenchidos' });
        }

        const jogo = {
            id,
            homeTeam,
            homeTeamUrl,
            awayTeam,
            awayTeamUrl,
            scoreHome,
            scoreAway,
            pointsHome, 
            pointsAway,
            referee,
            stadium,
            capacity,
            public,
            date,
            time,
            country,
            round
        };

        saveGameToXLSX(jogo);
        console.log(`Jogo ${id} salvo com sucesso.`)
        res.status(200).json({ message: 'Jogo salvo com sucesso na planilha!' });
    } catch (error) {
        res.status(500).json({ error: 'Erro ao salvar o jogo' });
    }
});

// DELETE GAME

app.delete('/remove/:id', (req, res) => {
    try {
        const { id } = req.params;

        deleteGameFromXLSX(id);

        res.status(200).json({ message: 'Jogo deletado com sucesso!' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});

// MARK: - FUNCTIONS

function normalizeString(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function getGamesThisYear() {
    var response = []
    tourneys.forEach((tourney) => {
        try {
            const filePath = path.join(__dirname, `data/${tourney}/2023.xlsx`);
            const workbook = xlsx.readFile(filePath);
    
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
    
            const data = xlsx.utils.sheet_to_json(sheet);
            response = response.concat(data)
        } catch (error) {
            console.error('Erro ao ler o arquivo XLSX:', error);
        }
    })

    // Ordena o vetor pela data mais recente
    response.sort((a, b) => {
        const dateA = parseDate(a.date);
        const dateB = parseDate(b.date);
        return dateB - dateA; // Ordena de forma decrescente (mais recente primeiro)
    });

    return response
}

function parseDate(dateString) {
    const [day, month, year] = dateString.split('/');
    return new Date(`${year}-${month}-${day}`);
}

const saveGameToXLSX = (jogo) => {
    const filePath = './games.xlsx';
    let workbook;
    const sheetName = 'Jogos';

    if (fs.existsSync(filePath)) {
        workbook = xlsx.readFile(filePath);
    } else {
        workbook = xlsx.utils.book_new();
    }

    let worksheet = workbook.Sheets[sheetName];
    if (!worksheet) {
        worksheet = xlsx.utils.json_to_sheet([]);
        xlsx.utils.book_append_sheet(workbook, worksheet, sheetName);
    }

    let data = xlsx.utils.sheet_to_json(worksheet);

    const game = data.find(gameData => gameData.id === jogo.id);

    if(game) {
        console.log("ERRO: Jogo já presente no banco de dados.")
        throw new Error('Jogo já presente no banco de dados.')
    }

    data.push({
        'id': jogo.id,
        'homeTeam': jogo.homeTeam,
        'homeTeamImage': jogo.homeTeamUrl,
        'awayTeam': jogo.awayTeam,
        'awayTeamImage': jogo.awayTeamUrl,
        'scoreHome': jogo.scoreHome,
        'scoreAway': jogo.scoreAway,
        'pointsHome': jogo.pointsHome,
        'pointsAway': jogo.pointsAway,
        'referee': jogo.referee || '',
        'stadium': jogo.stadium || '',
        'capacity': jogo.capacity || '',
        'public': jogo.public || '',
        'date': jogo.date,
        'time': jogo.time,
        'country': jogo.country,
        'round': jogo.round
    });

    const newWorksheet = xlsx.utils.json_to_sheet(data);
    workbook.Sheets[sheetName] = newWorksheet;

    xlsx.writeFile(workbook, filePath);
};

const deleteGameFromXLSX = (id) => {
    const filePath = './games.xlsx';
    const sheetName = 'Jogos';

    if (!fs.existsSync(filePath)) {
        console.log("Arquivo não encontrado.")
        throw new Error('Arquivo não encontrado.');
    }

    const workbook = xlsx.readFile(filePath);
    let worksheet = workbook.Sheets[sheetName];

    if (!worksheet) {
        console.log("ERRO: Planilha não encontrada.")
        throw new Error('Planilha não encontrada.');
    }

    let data = xlsx.utils.sheet_to_json(worksheet);

    const newData = data.filter(jogo => jogo.id !== id);

    if (newData.length === data.length) {
        console.log("ERRO: Jogo com esse ID não encontrado.")
        throw new Error('Jogo com esse ID não encontrado.');
    }

    const newWorksheet = xlsx.utils.json_to_sheet(newData);
    workbook.Sheets[sheetName] = newWorksheet;

    xlsx.writeFile(workbook, filePath);
};