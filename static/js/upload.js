function showUpload() {
    document.getElementById('upload').innerHTML = `
        <h2>添加单词库</h2>
        <textarea id="word-text" rows="5" cols="30" placeholder="book,书,L1\nschool,学校,L2\nteacher,老师,L3"></textarea><br>
        <input type="file" id="word-file" accept=".csv"><br>
        <button onclick="uploadWords()">上传</button>
        <button onclick="showMainMenu()">返回</button>
    `;
    document.getElementById('main-menu').style.display = 'none';
    document.getElementById('upload').style.display = 'block';
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
            if (!data.error) showMainMenu();
        });
}