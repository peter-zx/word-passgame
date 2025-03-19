function loadScores() {
    fetch('/get_scores')
        .then(response => response.json())
        .then(scores => {
            const scoreList = document.getElementById('score-list');
            scoreList.innerHTML = '';
            scores.forEach(s => {
                const li = document.createElement('li');
                li.textContent = `难度${s.level.toUpperCase()} ${s.time_mode === 'endless' ? '无尽' : s.time_mode + '秒'} ${s.score}分`;
                scoreList.appendChild(li);
            });
        });
}