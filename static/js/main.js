let currentLevel = 'lv1';
let currentTimeMode = '65';

function showMainMenu() {
    document.getElementById('main-menu').innerHTML = `
        <h1>知识消消乐</h1>
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
    loadScores(); // 依赖 scores.js 中的函数
}

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

// 初始化主菜单
showMainMenu();