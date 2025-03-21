function loadScores() {
    fetch('/get_scores')
        .then(response => response.json())
        .then(scores => {
            const scoreList = document.getElementById('score-list');
            scoreList.innerHTML = '';
            if (scores.length === 0) {
                scoreList.innerHTML = '<li>暂无分数记录</li>';
            } else {
                scores.forEach(s => {
                    const li = document.createElement('li');
                    li.textContent = `难度${s.level.toUpperCase()} ${s.time_mode === 'endless' ? '无尽' : s.time_mode + '秒'} ${s.score}分`;
                    scoreList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Error loading scores:', error);
            document.getElementById('score-list').innerHTML = '<li>加载失败</li>';
        });
}