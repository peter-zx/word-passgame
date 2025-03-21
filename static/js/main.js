console.log("main.js loaded");
let currentLevel = 'lv1';
let currentTimeMode = '65';

function showMainMenu() {
    console.log("Showing main menu");
    const hasWordbank = localStorage.getItem('wordbankSelected') === 'true';
    document.getElementById('main-menu').innerHTML = `
        <h1>知识消消乐</h1>
        ${!hasWordbank ? '<p style="color: red; font-weight: bold; background: #ffe6e6; padding: 10px;">新手提示：请先选择词库以开始游戏！</p>' : ''}
        <h3>选择模式</h3>
        <div class="mode-grid">
            <div class="card" onclick="showLevels('65')">65秒</div>
            <div class="card" onclick="showLevels('125')">125秒</div>
            <div class="card" onclick="showLevels('180')">180秒</div>
            <div class="card" onclick="showLevels('endless')">无尽模式</div>
        </div>
        <button onclick="showWordbank()">词库选择</button>
        <button onclick="showWrongWords()">错题本</button>
        <div id="scoreboard"><h3>排行榜</h3><ul id="score-list"></ul></div>
    `;
    document.getElementById('main-menu').style.display = 'block';
    document.getElementById('level-menu').style.display = 'none';
    document.getElementById('game').style.display = 'none';
    document.getElementById('upload').style.display = 'none';
    document.getElementById('end-modal').style.display = 'none';
    loadScores();
}

// 其他函数保持不变
function showLevels(timeMode) {
    currentTimeMode = timeMode;
    document.getElementById('level-menu').innerHTML = `
        <h2>选择难度</h2>
        <div class="level-grid">
            <div class="card" onclick="startGame('lv1')">Lv1</div>
            <div class="card" onclick="startGame('lv2')">Lv2</div>
            <div class="card" onclick="startGame('lv3')">Lv3</div>
            <div class="card" onclick="startGame('lv4')">Lv4</div>
            <div class="card" onclick="startGame('lv5')">Lv5</div>
            <div class="card" onclick="startGame('lv6')">Lv6</div>
        </div>
        <button onclick="showMainMenu()">返回</button>
    `;
    document.getElementById('main-menu').style.display = 'none';
    document.getElementById('level-menu').style.display = 'block';
}

function showWrongWords() {
    fetch('/wrong_words')
        .then(response => response.json())
        .then(wrongWords => {
            document.getElementById('end-modal').innerHTML = `
                <div class="modal-header">
                    <h2>错题本</h2>
                    <button class="modal-close" onclick="closeWrongWords()">X</button>
                </div>
                <div class="wrong-word-list">
                    ${wrongWords.length ? `
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: #f0f0f0;">
                                    <th style="border: 1px solid #333; padding: 8px;">中文</th>
                                    <th style="border: 1px solid #333; padding: 8px;">英文</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${wrongWords.map(w => `
                                    <tr>
                                        <td style="border: 1px solid #333; padding: 8px;">${w.chinese || '未知'}</td>
                                        <td style="border: 1px solid #333; padding: 8px;">${w.english || '未知'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    ` : '<p>暂无错选单词</p>'}
                </div>
            `;
            document.getElementById('end-modal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading wrong words:', error);
            alert('无法加载错题本');
        });
}

function closeWrongWords() {
    document.getElementById('end-modal').style.display = 'none';
}

showMainMenu();