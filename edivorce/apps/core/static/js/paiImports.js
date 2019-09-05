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
    function selectCheckboxesOnPage(listOfOptions) {
        let allCheckboxes = $('.checkbox-group input[type=checkbox]');
        for (i = 0; i < allCheckboxes.length; i++) {
            let toMarkAs = false;
            let currentValue = allCheckboxes[i]
            if (listOfOptions.includes(currentValue.value)) {
                toMarkAs = true;
            }
            if (
                (!$(allCheckboxes[i]).prop("checked") && toMarkAs ) ||
                ($(allCheckboxes[i]).prop("checked") && !toMarkAs )
            ) {
                $(allCheckboxes[i]).trigger('click')
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
            const { multi_select } = modifiedData;
            if (!questionChanging) {
                selectPreviousAnswer(parent, answer, type || '');
            }
            if (multi_select) {
                selectCheckboxesOnPage(multi_select);
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
        $(document).scroll(sidebarScrollHandler).scroll();
    }
    
    function sidebarScrollHandler() {
        if (window.pageYOffset+90 > sticky) {
            span.classList.add("sticky");
        } else {
            span.classList.remove("sticky");
        }
    }
})()
    