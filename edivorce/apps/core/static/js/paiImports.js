(function(){

    let questionSteps = {};
    function loadPassageChat(lang) {
        if (!lang) {
            lang = 'en';
        }
        if (lang == 'default') {
            return;
        } 
        let preparedMeta = {
            parent: url,
            pageData: questionSteps
        };
        window.paiSettings = {
            botId: '1028834855', // Your bot id. Required.
            iframeEmbedTarget: 'iframe-french', // Enable the embedded iframe mode by passing the ID of the parent element for the iframe.
            iframeEmbedUrlParameters: `&resetHistory&verticalQuickReplies&enableSpeechRecognition=en-US&enableconsolelogs&language=${lang}&messagemetadata=${JSON.stringify(preparedMeta)}`, // Append these to the src URL of the iframe.
            enableSpeechRecognition: 'en-US',
            userMessageColor: '#2b5580', // Change the background color of the user message bubble.
            brandColor: '#2b5580', // Change text and highlight color. Any valid CSS color. Also changes shadow of cta button! Default 'rgb(17, 151, 255)'.
            messageMetadata: preparedMeta,
        };
        (function(){var w=window;var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.PassageAI=i;function l(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://tars-stg.passage.ai/loader.min.js?language=fr&botId='+window.paiSettings.botId;var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);}l()
        })();
    }
    var language = localStorage.getItem('selectedLang');

    $(window).on('load', function() {
        $("div[class^='question-well']").each((index, li) => {
            if ($(li).attr('id')) {
                let isVisible = $(li).css('display') === 'block' ? true : false;
                questionSteps[$(li).attr('id')] = isVisible
            }
        })
        loadPassageChat(language)
    });

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
    let dontTriggerClickFunction = false;
    let currentLang = localStorage.getItem('selectedLang') || 'en'
    $('div.question-well').on('click', (e) => {
        if (dontTriggerClickFunction) {
            return
        }
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

    function highlightBox(identifier, eventTarget, questionToHighlight) {
        if (!identifier) {
            return
        }
        if(identifier !== 'next') {
            const questionNumber = identifier.charAt(identifier.length - 1) - 1 
            $('.question-well').removeClass('hasFocus')
            let $questionWellToBeInFocus = $('.question-well').eq(questionNumber)
            let scrollValue = $questionWellToBeInFocus.offset().top - 400
            $questionWellToBeInFocus.addClass('hasFocus')
            if (eventTarget) {
                $questionWellToBeInFocus.find(`input[name=${eventTarget}]`).trigger('focus')
                scrollValue = $questionWellToBeInFocus.find(`input[name=${eventTarget}]`).offset().top - 400;
            }
            inputInFocus = $questionWellToBeInFocus.find('input').attr('name')
            $questionWellToBeInFocus.find('.question-focus').removeClass('question-focus');
            if (questionToHighlight) {
                $questionWellToBeInFocus.find(`input[name=${questionToHighlight}]`).closest('tr').find('.fact-sheet-question').addClass('question-focus');
            }
            if (questionToHighlight) {
                scrollValue = $('.question-focus').offset().top - 400;
            }
            $('html,body').animate({
                scrollTop: scrollValue
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
                dontTriggerClickFunction = true;
                $('.question-well').eq(questionNumber).find(`input:radio[value='${answer}']`).trigger('click');
                dontTriggerClickFunction = false;
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

    function clickOnThis(onThisSelector) {
        dontTriggerClickFunction = true;
        if ($(onThisSelector).is(':visible')) {
            $(onThisSelector).trigger('click');
        } else {
            console.log(`Click triggered on a hidden element. Selector is ${onThisSelector}`)
        }
        dontTriggerClickFunction = false;
    }

    function receiveMessage(msg) {
        if (typeof msg.data == 'object') {
            const modifiedData = (msg.data);
            const { parent } = modifiedData;
            const { answer } = modifiedData;
            const { type } = modifiedData;
            const focus = modifiedData.ID || modifiedData.focus;
            const { multi_select } = modifiedData;
            const { click_selector } = modifiedData;
            const { highlight_the_question } = modifiedData;

            console.log(modifiedData)
            if (click_selector) {
                clickOnThis(click_selector);
            }
            if (!questionChanging) {
                selectPreviousAnswer(parent, answer, type || '');
            }
            if (multi_select) {
                selectCheckboxesOnPage(multi_select);
            }
            if (modifiedData.question) {
                highlightBox(modifiedData.question, focus, highlight_the_question);
            }
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
})();
