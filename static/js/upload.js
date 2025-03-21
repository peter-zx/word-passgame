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
    const text = document.getElementById('word-text').value.trim();
    const file = document.getElementById('word-file').files[0];
    const formData = new FormData();
    
    if (file) {
        formData.append('file', file);
    } else if (text) {
        formData.append('text', text);
    } else {
        alert('请提供文本或文件');
        return;
    }

    fetch('/upload_words', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if (!data.error) {
            localStorage.setItem('wordbankSelected', 'true'); // 标记词库已选择
            const newFile = data.message.match(/words\d+\.csv/)[0]; // 提取新文件名
            updateSelectedWordbank(newFile); // 更新指定词库
            showMainMenu();
        }
    })
    .catch(error => {
        console.error('Error uploading words:', error);
        alert('上传失败，请检查网络或输入格式');
    });
}

function updateSelectedWordbank(newFile) {
    fetch('/upload_words', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selected_files: [`data/${newFile}`] })
    })
    .then(response => response.json())
    .then(data => console.log(data.message || data.error))
    .catch(error => console.error('Error updating wordbank:', error));
}