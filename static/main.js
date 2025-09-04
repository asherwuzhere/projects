window.addEventListener('DOMContentLoaded', () => {
    const resume = document.getElementById('resume');
    if (resume) {
        fetch('static/resume.txt')
            .then(res => res.text())
            .then(text => {
                resume.textContent = text;
            });
    }
});
