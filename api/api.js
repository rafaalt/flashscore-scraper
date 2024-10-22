const express = require('express');
const app = express();
const port = 3000;
const xlsx = require('xlsx');
const path = require('path');
const fs = require('fs');

const gamesSavePath = './data/myGames.xlsx'

const tourneys = [
    "serieA",
    "serieB",
    "copaDoBrasil",
    "libertadores",
    "sulamericana"
]

const years = [
    2021, 2022, 2023, 2024
]

app.use(express.json());

// GET MY GAMES

app.get('/myGames', (req, res) => {
    try {
        const workbook = xlsx.readFile(gamesSavePath);

        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
    
        const data = xlsx.utils.sheet_to_json(sheet);

        data.sort((a, b) => {
            const dateA = parseDate(a.date);
            const dateB = parseDate(b.date);
            return dateB - dateA;
        });
    
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
    } catch (error) {
        console.error('Erro ao ler o arquivo XLSX:', error);
        res.status(400).json({ error: 'Erro ao ler o arquivo XLSX' });
    }
});

app.get('/team/:team/:side', (req, res) => {
    const data = getAllGames()
    console.log(data.length)
    const team = req.params.team
    const side = req.params.side

    const teamName = normalizeString(team)
    var newData = data

    if (side == "home") {
        newData = newData.filter(game => normalizeString(game.homeTeam).includes(teamName))
    } else if (side == "away") {
        newData = newData.filter(game => normalizeString(game.awayTeam).includes(teamName))
    } else {
        newData = newData.filter(game => normalizeString(game.homeTeam).includes(teamName) || normalizeString(game.awayTeam).includes(teamName))
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
});

// SEARCH GAME

app.post('/search', (req, res) => {
    const {
        homeTeam,
        awayTeam,
        scoreHome,
        scoreAway,
        year,
        tourney
    } = req.body;
    var data
    if (year && tourney) {
        data = getTourneyYearGames(tourney, year)
    } else if (year) {
        data = getYearGames(year)
    } else if (tourney) {
        data = getTourneyGames(tourney)
    } else {
        data = getAllGames()
    }
    var newData = data
    if (awayTeam) {
        newData = newData.filter(game => normalizeString(game.awayTeam).includes(normalizeString(awayTeam)))
        newData = newData.filter(game => normalizeString(game.homeTeam).includes(normalizeString(homeTeam)))
    } else {
    newData = newData.filter(game => normalizeString(game.homeTeam).includes(normalizeString(homeTeam))
     || normalizeString(game.awayTeam).includes(normalizeString(homeTeam)))
    }
    if (scoreHome) {
        newData = newData.filter(game => game.scoreHome == scoreHome)
    }
    if (scoreAway) {
        newData = newData.filter(game => game.scoreAway == scoreAway)
    }

    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;

    const startIndex = (page - 1) * limit;
    const endIndex = page * limit;

    const paginatedData = newData.slice(startIndex, endIndex);

    res.json({
        currentPage: page, 
        totalPages: Math.ceil(data.length / limit),
        totalItems: newData.length,
        itemsPerPage: limit,
        results: paginatedData
    });
});

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
        const year = parseInt(req.query.year) || 2024
        const filePath = path.join(__dirname, `data/${league}/${year}.xlsx`);
        const workbook = xlsx.readFile(filePath);

        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];

        const data = xlsx.utils.sheet_to_json(sheet);
        var newData = data
        
        const team = req.query.team
        if (team) {
            teamName = normalizeString(team)
            newData = newData.filter(game => normalizeString(game.homeTeam).includes(teamName) || normalizeString(game.awayTeam).includes(teamName))
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
        res.status(400).json({ error: 'Erro ao ler o arquivo XLSX' });
    }
});

// SAVE GAME

app.post('/save', (req, res) => {
    try {
        const {
            id,
            homeTeam,
            homeTeamImage,
            awayTeam,
            awayTeamImage,
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
            !homeTeamImage || 
            !awayTeam || 
            !awayTeamImage || 
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
            homeTeamImage,
            awayTeam,
            awayTeamImage,
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
        res.status(400).json({ error: 'Erro ao salvar o jogo' });
    }
})

// DELETE GAME

app.delete('/delete/:id', (req, res) => {
    try {
        const { id } = req.params;

        deleteGameFromXLSX(id);
        console.log(`Jogo ${id} deletado com sucesso`)
        res.status(200).json({ message: 'Jogo deletado com sucesso!' });
    } catch (error) {
        res.status(400).json({ error: error.message });
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
            const filePath = path.join(__dirname, `data/${tourney}/2024.xlsx`);
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

function getYearGames(year) {
    var response = []
    tourneys.forEach((tourney) => {
        try {
            const filePath = path.join(__dirname, `data/${tourney}/${year}.xlsx`);
            const workbook = xlsx.readFile(filePath);
    
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
    
            const data = xlsx.utils.sheet_to_json(sheet);
            response = response.concat(data)
        } catch (error) {
            console.error('Erro ao ler o arquivo XLSX:', error);
        }
    })
    return response
}

function getTourneyGames(tourney) {
    var response = []
    years.forEach((year) => {
        try {
            const filePath = path.join(__dirname, `data/${tourney}/${year}.xlsx`);
            const workbook = xlsx.readFile(filePath);
    
            const sheetName = workbook.SheetNames[0];
            const sheet = workbook.Sheets[sheetName];
    
            const data = xlsx.utils.sheet_to_json(sheet);
            response = response.concat(data)
        } catch (error) {
            console.error('Erro ao ler o arquivo XLSX:', error);
        }
    })
    return response
}

function getTourneyYearGames(tourney, year) {
    var response = []
    try {
        const filePath = path.join(__dirname, `data/${tourney}/${year}.xlsx`);
        const workbook = xlsx.readFile(filePath);
    
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
    
        const data = xlsx.utils.sheet_to_json(sheet);
        response = response.concat(data)
    } catch (error) {
        console.error('Erro ao ler o arquivo XLSX:', error);
    }
    return response
}

function getAllGames() {
    var response = []
    years.forEach((year) => {
        tourneys.forEach((tourney) => {
            try {
                const filePath = path.join(__dirname, `data/${tourney}/${year}.xlsx`);
                const workbook = xlsx.readFile(filePath);
        
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
        
                const data = xlsx.utils.sheet_to_json(sheet);
                response = response.concat(data)
            } catch (error) {
                console.error('Erro ao ler o arquivo XLSX:', error);
            }
        })    
    })

    // Ordena o vetor pela data mais recente
    response.sort((a, b) => {
        const dateA = parseDate(a.date, a.id);
        const dateB = parseDate(b.date, b.id);
        return dateB - dateA; // Ordena de forma decrescente (mais recente primeiro)
    });

    return response
}

function parseDate(dateString, id) {
    const [day, month, year] = dateString.split('/');
    return new Date(`${year}-${month}-${day}`);
}

const saveGameToXLSX = (jogo) => {
    let workbook;
    const sheetName = 'Jogos';

    if (fs.existsSync(gamesSavePath)) {
        workbook = xlsx.readFile(gamesSavePath);
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
        'homeTeamImage': jogo.homeTeamImage,
        'awayTeam': jogo.awayTeam,
        'awayTeamImage': jogo.awayTeamImage,
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

    xlsx.writeFile(workbook, gamesSavePath);
};

const deleteGameFromXLSX = (id) => {
    const sheetName = 'Jogos';

    if (!fs.existsSync(gamesSavePath)) {
        console.log("Arquivo não encontrado.")
        throw new Error('Arquivo não encontrado.');
    }

    const workbook = xlsx.readFile(gamesSavePath);
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

    xlsx.writeFile(workbook, gamesSavePath);
};