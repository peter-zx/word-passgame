let selectedWords = [];
let matchedPairs = new Set();
let wrongWords = [];
let groups = [];
let currentGroup = 0;
let score = 0;
let timerId = null;
let timeLeft = 0;
let rows = 4;

function startGame(level) {
    currentLevel = level;
    score = 0;
    currentGroup = 0;
    wrongWords = [];
    fetch(`/game/${level}`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to load game');
            return response.json();
        })
        .then(data => {
            groups = data.groups;
            rows = data.rows;
            document.getElementById('main-menu').style.display = 'none';
            document.getElementById('level-menu').style.display = 'none';
            document.getElementById('game').style.display = 'block';
            loadGroup();
            startTimer();
        })
        .catch(error => {
            console.error('Error loading game:', error);
            alert('Failed to load game.');
        });
}

function loadGroup() {
    if (currentTimeMode !== 'endless' && currentGroup >= 6) {
        endGame();
        return;
    }
    if (currentGroup >= groups.length && currentTimeMode === 'endless') {
        fetchNextGroup();
        return;
    }
    const { grid, word_ids } = groups[currentGroup];
    document.getElementById('game').innerHTML = `
        <div id="timer">时间: --</div>
        <div id="score">分数: ${score}</div>
        <div id="group-info">第 ${currentGroup + 1}${currentTimeMode === 'endless' ? '' : '/6'} 组</div>
        <div id="game-grid" class="game-grid"></div>
        <button onclick="endGame()">结束游戏</button>
        <button onclick="showLevels(currentTimeMode)">返回</button>
        <button onclick="showMainMenu()">回到主页</button>
    `;
    const gameGrid = document.getElementById('game-grid');
    selectedWords = [];
    matchedPairs.clear();
    grid.forEach(cell => {
        const cellElement = document.createElement('div');
        cellElement.classList.add('cell');
        if (matchedPairs.has(cell.id)) cellElement.classList.add('matched');
        cellElement.textContent = cell.value;
        cellElement.dataset.id = cell.id;
        cellElement.addEventListener('click', () => handleCellClick(cell.id, word_ids, cellElement));
        gameGrid.appendChild(cellElement);
    });
    window.wordIds = word_ids;
}

function handleCellClick(cellId, word_ids, cellElement) {
    if (matchedPairs.has(cellId) || selectedWords.includes(cellId)) return;
    selectedWords.push(cellId);
    cellElement.classList.add('selected');

    if (selectedWords.length === 2) {
        fetch('/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                word1_id: selectedWords[0],
                word2_id: selectedWords[1],
                word_ids: word_ids
            })
        })
        .then(response => response.json())
        .then(data => {
            const cells = document.querySelectorAll('.cell.selected');
            if (data.result) {
                score += 1;
                document.getElementById('score').textContent = `分数: ${score}`;
                cells.forEach(cell => {
                    cell.classList.remove('selected');
                    cell.classList.add('matched');
                    matchedPairs.add(parseInt(cell.dataset.id));
                });
            } else {
                cells.forEach(cell => {
                    cell.classList.remove('selected');
                    cell.classList.add('wrong');
                    const word = word_ids[cell.dataset.id];
                    wrongWords.push({ english: word.value, chinese: word.pair, difficulty: 'L1' }); // 默认 L1
                    setTimeout(() => cell.classList.remove('wrong'), 500);
                });
            }
            selectedWords = [];
            if (matchedPairs.size === rows * 2) {
                currentGroup += 1;
                setTimeout(loadGroup, 500);
            }
        });
    }
}

function fetchNextGroup() {
    fetch(`/next_group/${currentLevel}`)
        .then(response => response.json())
        .then(data => {
            groups.push({ grid: data.grid, word_ids: data.word_ids });
            loadGroup();
        });
}

function startTimer() {
    stopTimer();
    if (currentTimeMode === 'endless') {
        timeLeft = 0;
        document.getElementById('timer').textContent = `时间: ${timeLeft}秒`;
        timerId = setInterval(() => {
            timeLeft += 1;
            document.getElementById('timer').textContent = `时间: ${timeLeft}秒`;
        }, 1000);
    } else {
        timeLeft = parseInt(currentTimeMode);
        document.getElementById('timer').textContent = `剩余时间: ${timeLeft}秒`;
        timerId = setInterval(() => {
            timeLeft -= 1;
            document.getElementById('timer').textContent = `剩余时间: ${timeLeft}秒`;
            if (timeLeft <= 0) endGame();
        }, 1000);
    }
}

function stopTimer() {
    if (timerId) clearInterval(timerId);
    timerId = null;
}

function endGame() {
    stopTimer();
    Promise.all([
        fetch('/save_score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ time_mode: currentTimeMode, level: currentLevel, score: score })
        }),
        fetch('/wrong_words', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wrong_words: wrongWords })
        })
    ]).then(() => {
        document.getElementById('end-modal').innerHTML = `
            <div class="modal-header">
                <h2>游戏结束</h2>
                <button class="modal-close" onclick="closeModal()">X</button>
            </div>
            <p id="final-score">你的分数: ${score}</p>
            <p>错选 ${wrongWords.length} 个单词，详情请查看错题本</p>
            <div class="modal-buttons">
                <button onclick="showMainMenu()">回到主页</button>
                <button onclick="nextLevel()">下一关</button>
            </div>
        `;
        document.getElementById('end-modal').style.display = 'block';
    });
}

function closeModal() {
    document.getElementById('end-modal').style.display = 'none';
}

function nextLevel() {
    const levels = ['lv1', 'lv2', 'lv3', 'lv4', 'lv5', 'lv6'];
    const nextIdx = levels.indexOf(currentLevel) + 1;
    if (nextIdx < levels.length) {
        startGame(levels[nextIdx]);
        document.getElementById('end-modal').style.display = 'none';
    } else {
        alert('已经是最后一关！');
        showMainMenu();
    }
}