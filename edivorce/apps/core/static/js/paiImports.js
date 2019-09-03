(function(){
    let hidden = false
    let questionChangeText = {
        'en': 'Question changed',
        'pa': 'ਸਵਾਲ ਬਦਲਿਆ',
        'zh': '问题已更改变',
        'zh-tw': '问题已更改变',
        'fr': 'La question a été modifiée',
        'es': 'Pregunta modificada'
    }
    let inputInFocus = '';
    let questionChanging = false;
    let currentLang = localStorage.getItem('selectedLang') || 'en'
    $('div.question-well').on('click', (e) => {
        let upcomingInput = $(e.currentTarget).find('input').attr('name');
        if (upcomingInput !== inputInFocus) {
            window.paiSettings.messageMetadata.previousQuestion = inputInFocus;
            window.paiSettings.messageMetadata.nextQuestion = upcomingInput;
            inputInFocus = upcomingInput;
            questionChanging = true;
            $('#iframe-french').find('iframe')[0].contentWindow.postMessage({
                paiSettings: window.paiSettings,
                sendMessageToChat: {
                    message: questionChangeText[currentLang],
                    show: true
                }
            }, 'https://tars-stg.passage.ai')
        }
    })

    function highlightBox(identifier, eventTarget) {
        if (!identifier) {
            return
        }
        if(identifier !== 'next') {
            const questionNumber = identifier.charAt(identifier.length - 1) - 1
            $('.question-well').removeClass('hasFocus')
            let $questionWellToBeInFocus = $('.question-well').eq(questionNumber)
            $questionWellToBeInFocus.addClass('hasFocus')
            if (eventTarget) {
                $questionWellToBeInFocus.find(`input[name=${eventTarget}]`).trigger('focus')
            }
            inputInFocus = $questionWellToBeInFocus.find('input').attr('name')
            $('html,body').animate({
                scrollTop: $questionWellToBeInFocus.offset().top-200
            }, 100);
        } else {
            $('.question-well').removeClass('hasFocus')
        }
    }
    function selectPreviousAnswer(parent, answer, inputType) {
        if (parent && answer) {
            const questionNumber = parent.charAt(parent.length - 1) - 1
            if (inputType) {
                $('.question-well').eq(questionNumber).find(`input[type=${inputType}]`).val(`${answer}`)
                $('.question-well').eq(questionNumber).find(`input[type=${inputType}]`).trigger('change')
            } else {
                $('.question-well').eq(questionNumber).find(`input:radio[value='${answer}']`).trigger('click')
            }
        }
    }
    function receiveMessage(msg) {
        if (typeof msg.data == 'object') {
            const modifiedData = (msg.data);
            const { parent } = modifiedData;
            const { answer } = modifiedData;
            const { type } = modifiedData;
            const focus = modifiedData.ID || modifiedData.focus;
            if (!questionChanging) {
                selectPreviousAnswer(parent, answer, type || '');
            }
            highlightBox(modifiedData.question, focus);
            questionChanging = false;
        }
    };
    window.addEventListener('message', receiveMessage, false);

    var span = document.querySelector('#floating-side-menu'),
        div = document.querySelector('#paiChatIframeEmbedTarget h2'),
        win = $(window),
        sticky = div.getBoundingClientRect().bottom + window.scrollY;

    if (span.classList.contains('floating-chat')) {
        $(document).scroll(myFunction).scroll();
    }
    
    function myFunction() {
        if (window.pageYOffset+90 > sticky) {
            span.classList.add("sticky");
        } else {
            span.classList.remove("sticky");
        }
    }

    function compute() {
        var spanHeight = span.outerHeight(),
            divHeight = div.height(),
            spanOffset = span.offset().top + spanHeight,
            divOffset = div.offset().top + divHeight;
        //console.log(div.offset().top - $(document).scrollTop())
        //console.log(span.offset().top - $(document).scrollTop())
        if ((divOffset - $(document).scrollTop()+90) < window.innerHeight) {
            span.css("position", "relative")
            span.css("top", "unset")
            // console.log("Voila")
        }
        //} else if (div.offset().top + 45 > span.offset().top) {
        //  span.css("position", "absolute")
            //console.log("Voil 2 a")
        else {
            // console.log("What")
            span.css("position", "fixed")
        }
    }
})()
    