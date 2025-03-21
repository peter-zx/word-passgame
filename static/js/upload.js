function showWordbank() {
    console.log("Entering showWordbank()");
    fetch('/get_wordbanks')
        .then(response => response.json())
        .then(data => {
            const uploadElement = document.getElementById('upload');
            uploadElement.innerHTML = `
                <h2>词库选择</h2>
                <div id="wordbank-list">
                    ${data.wordbanks.length ? data.wordbanks.map(w => `
                        <label><input type="checkbox" name="wordbank" value="${w}"> ${w}</label><br>
                    `).join('') : '<p>暂无词库文件</p>'}
                </div>
                <button onclick="selectWordbanks()">使用选中词库</button>
                <button onclick="showUploadForm()">添加单词库</button>
                <button onclick="showMainMenu()">返回</button>
            `;
            document.getElementById('main-menu').style.display = 'none';
            uploadElement.style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading wordbanks:', error);
            alert('无法加载词库列表');
        });
}

function showUploadForm() {
    const uploadElement = document.getElementById('upload');
    uploadElement.innerHTML = `
        <h2>添加单词库</h2>
        <textarea id="word-text" rows="5" cols="30" placeholder="book,书,L1\nschool,学校,L2\nteacher,老师,L3"></textarea><br>
        <input type="file" id="word-file" accept=".csv"><br>
        <button onclick="uploadWords()">上传</button>
        <button onclick="showWordbank()">返回</button>
    `;
}

function uploadWords() {
    console.log("Entering uploadWords()");
<<<<<<< HEAD
    let text = document.getElementById('word-text').value.trim();
=======
    const text = document.getElementById('word-text').value.trim();
>>>>>>> 4657e4082a86963a5d422b1da1d927fffb84aa20
    const file = document.getElementById('word-file').files[0];
    const formData = new FormData();
    
    if (file) {
        console.log("Uploading file:", file.name);
        formData.append('file', file);
    } else if (text) {
<<<<<<< HEAD
        text = text.replace(/，/g, ',');
=======
>>>>>>> 4657e4082a86963a5d422b1da1d927fffb84aa20
        console.log("Uploading text:", text);
        formData.append('text', text);
    } else {
        alert('请提供文本或文件');
        return;
    }

    fetch('/upload_words', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            return response.text().then(text => { throw new Error(`HTTP error! status: ${response.status}, response: ${text}`); });
        }
        return response.json();
    })
    .then(data => {
        console.log("Server response:", data);
        alert(data.message || data.error);
        if (!data.error) {
            localStorage.setItem('wordbankSelected', 'true');
            showWordbank();
        }
    })
    .catch(error => {
        console.error('Error uploading words:', error);
        alert('上传失败: ' + error.message);
    });
}

function selectWordbanks() {
    const selected = Array.from(document.querySelectorAll('input[name="wordbank"]:checked'))
        .map(cb => cb.value);
    if (selected.length === 0) {
        alert('请选择至少一个词库');
        return;
    }
    console.log("Selected wordbanks:", selected);
    fetch('/upload_words', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
<<<<<<< HEAD
        body: JSON.stringify({ selected_files: selected })  // 移除多余的 "data/" 前缀，后端处理路径
=======
        body: JSON.stringify({ selected_files: selected })
>>>>>>> 4657e4082a86963a5d422b1da1d927fffb84aa20
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message || data.error);
        alert(data.message || data.error);
        if (!data.error) {
            localStorage.setItem('wordbankSelected', 'true');
            showMainMenu();
        }
    })
    .catch(error => console.error('Error selecting wordbanks:', error));
}