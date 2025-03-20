function showWordbank() {
    fetch('/words') // 临时用 /words 获取所有词库文件，实际应新增路由
        .then(response => response.json())
        .then(() => {
            const wordFiles = ['default_words.csv', 'words1.csv', 'wrong_words.csv']; // 模拟文件列表，需后端支持
            document.getElementById('upload').innerHTML = `
                <h2>词库选择</h2>
                <div class="wordbank-grid" id="wordbank-grid">
                    ${wordFiles.map(file => `<div class="wordbank-item" data-file="${file}" onclick="toggleWordbankItem(this)">${file}</div>`).join('')}
                </div>
                <button onclick="updateSelectedWordbank()">确认选择</button>
                <button onclick="showUpload()">添加单词库</button>
                <button onclick="showMainMenu()">返回</button>
            `;
            document.getElementById('main-menu').style.display = 'none';
            document.getElementById('upload').style.display = 'block';
        });
}

function toggleWordbankItem(element) {
    element.classList.toggle('selected');
}

function updateSelectedWordbank() {
    const selectedItems = document.querySelectorAll('.wordbank-item.selected');
    const selectedFiles = Array.from(selectedItems).map(item => `data/${item.dataset.file}`);
    fetch('/upload_words', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selected_files: selectedFiles })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if (!data.error) {
            localStorage.setItem('wordbankSelected', 'true'); // 标记已选择词库
            showMainMenu();
        }
    });
}

function showUpload() {
    document.getElementById('upload').innerHTML = `
        <h2>添加单词库</h2>
        <textarea id="word-text" rows="5" cols="30" placeholder="book,书,L1\nschool,学校,L2\nteacher,老师,L3"></textarea><br>
        <input type="file" id="word-file" accept=".csv"><br>
        <button onclick="uploadWords()">上传</button>
        <button onclick="showWordbank()">返回</button>
    `;
}

function uploadWords() {
    const text = document.getElementById('word-text').value;
    const file = document.getElementById('word-file').files[0];
    const formData = new FormData();
    if (file) formData.append('file', file);
    else if (text) formData.append('text', text);
    else {
        alert('请提供文本或文件');
        return;
    }
    fetch('/upload_words', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            if (!data.error) showWordbank();
        });
}