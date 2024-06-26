window.addEventListener('DOMContentLoaded', () => {
    // var latexCodeTextarea = document.getElementById('latex-container');
   
    try {
        renderMathInElement(document.getElementById('latex-container'), {
            delimiters: [
                
                {left: "$$", right: "$$", display: true},
                {left: "$", right: "$", display: false},
                {left: "\\(", right: "\\)", display: false},
                {left: "\\begin{equation}", right: "\\end{equation}", display: true},
                {left: "\\begin{align}", right: "\\end{align}", display: true},
                {left: "\\begin{alignat}", right: "\\end{alignat}", display: true},
                {left: "\\begin{gather}", right: "\\end{gather}", display: true},
                {left: "\\begin{CD}", right: "\\end{CD}", display: true},
                {left: "\\[", right: "\\]", display: true}
            ],
            throwOnError: false
        });
    }
    catch (error) {
    }
});

